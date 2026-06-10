# open-personality — 概要设计

> 阶段二产出：技术设计文档
> 状态：✅ 设计已确认，后续阶段以此为蓝本

---

## 1. 架构总览

```
┌─────────────────────────────────────────────────────┐
│                     Browser                          │
│  ┌───────────┐ ┌──────────┐ ┌──────────┐            │
│  │  Home      │ │Question- │ │  Report  │            │
│  │  (入口)    │ │ naire    │ │  (结果)  │            │
│  └───────────┘ └──────────┘ └──────────┘            │
│         │              │              │              │
│         ▼              ▼              ▼              │
│  ┌─────────────────────────────────────────┐         │
│  │           Vue 3 + Vite + ECharts         │         │
│  │  • RadarChart    • ResultCard            │         │
│  │  • LanguageSwitch • EasterEggBanner      │         │
│  └───────────────────┬─────────────────────┘         │
│                      │ HTTP/REST                     │
└──────────────────────┼──────────────────────────────┘
                       │
              ┌────────┴────────┐
              │   FastAPI       │
              │  (Python)       │
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────────┐
        ▼              ▼                  ▼
┌──────────────┐ ┌──────────┐ ┌──────────────────┐
│ Questionnaire│ │ Scoring  │ │ MBTI Inference    │
│ Module       │ │ Engine   │ │ (概率映射)        │
└──────────────┘ └──────────┘ └──────────────────┘
        │              │                  │
        └──────────────┼──────────────────┘
                       ▼
              ┌──────────────────┐
              │  Report Generator │
              │  + Easter Egg     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  SQLite          │
              │  (SQLAlchemy)    │
              └──────────────────┘
```

---

## 2. 模块划分

| 模块 ID | 模块名 | 职责 | 单独可测 |
|---------|--------|------|---------|
| M01 | **问卷管理** (Questionnaire) | 提供题目列表、管理答题状态、验证提交数据 | ✅ |
| M02 | **计分引擎** (Scoring Engine) | 计算大五 5 域 + 30 子维度得分 | ✅ |
| M03 | **MBTI 推断** (MBTI Inference) | McCrae & Costa (1989) 概率化映射 | ✅ |
| M04 | **报告生成** (Report Generator) | 组装所有结果 + 文字解读（zh/en） | ✅ |
| M05 | **彩蛋引擎** (Easter Egg) | 概率判定 + 随机选取彩蛋 | ✅ |
| M06 | **持久化层** (Persistence) | SQLAlchemy CRUD 操作 | ✅ |
| M07 | **API 层** (API Layer) | 路由分发、请求/响应序列化 | ✅ |
| M08 | **前端视图** (Frontend UI) | 用户交互、可视化渲染、图片导出 | ✅ |

### 模块依赖关系

```
M01(问卷) → M07(API) → M02(计分) → M03(MBTI)
                                   → M05(彩蛋)
                                   → M04(报告) → M06(持久化)
M08(前端) ↔ M07(API)
```

---

## 3. 核心数据流

### 3.1 主流程（答题 → 报告）

```
用户答题完成 → POST /api/questionnaires/submit
1. API 层验证请求参数（模式、语言、答案格式）
2. 调用 M02 计分引擎
   ├─ 读取 IPIP-120/300 维度映射配置
   ├─ 计算 5 域原始分 → 标准化分 (T-score)
   └─ 计算 30 子维度原始分 → 标准化分
3. 调用 M03 MBTI 推断
   ├─ 读取 MBTI 映射权重文件
   ├─ 4 对维度分别计算概率 (Sigmoid 校准)
   └─ 输出 E/I, S/N, T/F, J/P 概率分布
4. 调用 M05 彩蛋引擎
   ├─ 10% 概率判定
   └─ 命中则随机选取 1 条彩蛋文案
5. 调用 M04 报告生成
   ├─ 根据语言读解读模板
   ├─ 组装得分 + MBTI + 彩蛋
   └─ 返回完整 Report 对象
6. 调用 M06 持久化层保存全部数据
   ├─ 开启数据库事务
   ├─ 写入 session 记录
   ├─ 批量写入 answers
   ├─ 写入 report 记录
   └─ 提交事务（全部落盘，或全部回滚）
7. 返回 → 前端渲染雷达图 + 卡片 + 解读文字
```

### 3.2 历史记录回顾流程

提供两条找回路径，互补覆盖：

**路径 A：首页输入分享码**（主动查询，必做）
```
用户输入 8 位码 → 点击查询
1. 前端校验格式（8 位 base62）
2. GET /api/report/{share_token}
3. 命中 → 跳转 ReportPage 渲染
4. 未命中 → 提示"分享码无效"
```

**路径 B：首页最近记录**（被动展示，同设备）
```
1. 用户完成答题后，前端将 { share_token, created_at } 写入 localStorage
2. 首页加载时读取 localStorage，展示最近 5 条记录
3. 用户点击任一条 → 跳转 ReportPage
```

两条路径共享同一个后端接口（`GET /api/report/{share_token}`），无需新增后端代码。

### 3.3 数据实体流转

```
AnswerItem (单题作答)
├─ item_id: str     (题目编号, 如 "ipip_01")
├─ value: int       (1~5 李克特)
└─ reversed: bool   (是否反向计分)

→ ScoringResult
├─ domains: { O: 48, C: 52, E: 39, A: 61, N: 44 }
├─ facets: { O_imagination: 52, O_artistic: 48, ... }
└─ t_scores: { O: 55, C: 48, ... }

→ MBTIResult
├─ ei: { E: 0.73, I: 0.27 }
├─ sn: { S: 0.32, N: 0.68 }
├─ tf: { T: 0.55, F: 0.45 }
├─ jp: { J: 0.41, P: 0.59 }
└─ confidence: 0.72   (最高概率对的不确定度)

→ Report
├─ session_id: UUID
├─ scores: ScoringResult
├─ mbti: MBTIResult
├─ interpretations: { domain_texts, facet_texts }
├─ easter_egg: str | null
├─ lang: "zh" | "en"
├─ share_token: str
├─ created_at: datetime
└─ mode: "standard" | "advanced"
```

---

## 4. 接口契约

### 4.1 API 端点

| 方法 | 路径 | 请求 | 响应 | 说明 |
|------|------|------|------|------|
| `GET` | `/api/questionnaires/items` | `?mode=standard&lang=zh` | `{ items: Item[] }` | 获取题目列表 |
| `POST` | `/api/questionnaires/submit` | `SubmitRequest` | `Report` | 提交作答，返回完整报告 |
| `GET` | `/api/report/{share_token}` | — | `Report` | 通过分享链接获取报告 |
| `GET` | `/api/i18n/{lang}` | `lang=zh` | `{ [key]: string }` | 获取语言包 |

### 4.2 请求/响应数据结构

```python
# --- 问卷题目 ---
class QuestionnaireItem:
    item_id: str        # "ipip_01"
    dimension: str      # "O" (所属域)
    facet: str          # "O_imagination" (所属子维度)
    text: str           # 当前语言的题目文本（API 按 lang 参数加载对应文件后填充）
    reversed: bool      # 是否反向计分

# --- 提交请求 ---
class SubmitRequest:
    mode: str           # "standard" | "advanced"
    lang: str           # "zh" | "en"
    answers: list[AnswerItem]

class AnswerItem:
    item_id: str        # 题目编号
    value: int          # 1~5

# --- 计分结果 ---
class ScoringResult:
    raw_scores: dict[str, float]    # {"O": 48, ...}
    t_scores: dict[str, float]      # {"O": 55, ...}
    facet_scores: dict[str, float]  # {"O_imagination": 52, ...}

# --- MBTI 结果 ---
class MBTIDimension:
    label_a: str        # "E"
    label_b: str        # "I"
    prob_a: float       # 0.73
    prob_b: float       # 0.27

class MBTIResult:
    dimensions: list[MBTIDimension]  # 4 对
    confidence: float                # 0~1
    type_code: str                   # "ENFP" (硬分类, 仅展示用)

# --- 解读片段 ---
class Interpretation:
    dimension: str          # "O"
    title_zh: str
    title_en: str
    body_zh: str
    body_en: str

# --- 报告 ---
class Report:
    session_id: str
    share_token: str
    mode: str
    lang: str
    scoring: ScoringResult
    mbti: MBTIResult
    interpretations: list[Interpretation]
    easter_egg: str | None
    created_at: str
```

---

## 5. 数据库设计

### 5.1 ER 概览

```
sessions ──1:N── answers
    │
    1:1
    │
reports
```

### 5.2 表结构

```sql
-- 作答会话
CREATE TABLE sessions (
    id          TEXT PRIMARY KEY,           -- UUID
    mode        TEXT NOT NULL,              -- 'standard' | 'advanced'
    lang        TEXT NOT NULL DEFAULT 'zh', -- 'zh' | 'en'
    share_token TEXT NOT NULL UNIQUE,       -- 短唯一标识 (8 位 base62)
    created_at  TEXT NOT NULL               -- ISO 8601
);
CREATE INDEX idx_sessions_share_token ON sessions(share_token);

-- 单题答案
CREATE TABLE answers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL REFERENCES sessions(id),
    item_id     TEXT NOT NULL,              -- 'ipip_01'
    value       INTEGER NOT NULL CHECK(value BETWEEN 1 AND 5)
);
CREATE INDEX idx_answers_session ON answers(session_id);

-- 报告
CREATE TABLE reports (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT NOT NULL UNIQUE REFERENCES sessions(id),
    big_five_scores TEXT NOT NULL,           -- JSON
    mbti_result     TEXT NOT NULL,           -- JSON
    interpretations TEXT NOT NULL,           -- JSON
    easter_egg      TEXT,                    -- NULL 表示未触发
    created_at      TEXT NOT NULL
);
CREATE INDEX idx_reports_session ON reports(session_id);
```

### 5.3 分享机制

- 每次提交成功后，后端生成 8 位 base62 token（大小写字母 + 数字）
- 前端显示 URL：`https://domain/report/{share_token}`
- 用户可复制/分享此链接，无需任何身份认证
- token 碰撞概率极低（62^8 ≈ 2.18 × 10^14 空间），不做去重检查

---

## 6. 模块接口签名

### 6.1 计分引擎 (M02)

```python
class ScoringEngine:
    def __init__(self, items_config: dict): ...

    def calculate(
        self,
        answers: list[AnswerItem],
        mode: str       # "standard" | "advanced"
    ) -> ScoringResult:
        """计算大五 5 域 + 30 子维度得分"""
        pass

    def _compute_raw_scores(
        self,
        answers: list[AnswerItem],
        dimension_map: dict[str, list[str]]
    ) -> dict[str, float]:
        """按域/子维度计算原始分（含反向计分）"""
        pass

    def _normalize(
        self,
        raw_scores: dict[str, float],
        norms: dict[str, NormConfig]
    ) -> dict[str, float]:
        """原始分 → T-score 标准化"""
        pass
```

### 6.2 MBTI 推断 (M03)

```python
class MBTIInference:
    def __init__(self, mapping_config: dict): ...

    def infer(
        self,
        big_five_scores: ScoringResult
    ) -> MBTIResult:
        """大五分数 → MBTI 概率映射"""
        pass

    def _compute_dimension(
        self,
        scores: ScoringResult,
        weights: list[WeightConfig]
    ) -> tuple[float, float]:
        """单对维度概率计算（Sigmoid 校准）"""
        pass

    def _confidence(
        self,
        prob_a: float,
        prob_b: float
    ) -> float:
        """基于概率分布的置信度"""
        pass
```

### 6.3 彩蛋引擎 (M05)

```python
class EasterEggEngine:
    def __init__(self, eggs_config: dict): ...

    def trigger(self, seed: str | None = None) -> str | None:
        """10% 概率触发，返回随机彩蛋文案或 None"""
        pass

    def _roll(self) -> bool:
        """概率判定"""
        pass

    def _pick(self, lang: str) -> str:
        """按语言随机选一条彩蛋"""
        pass
```

### 6.4 报告生成 (M04)

```python
class ReportGenerator:
    def __init__(self, interpretations_config: dict): ...

    def generate(
        self,
        scoring: ScoringResult,
        mbti: MBTIResult,
        easter_egg: str | None,
        lang: str,
        session_id: str,
        mode: str
    ) -> Report:
        """组装完整报告"""
        pass

    def _build_interpretations(
        self,
        scoring: ScoringResult,
        lang: str
    ) -> list[Interpretation]:
        """根据得分和语言生成文字解读"""
        pass
```

### 6.5 持久化层 (M06)

> **事务规则**：数据库写入只有一个入口——`save_complete_session`。计算成功前绝不碰数据库，计算成功后一次事务写入全部数据。
> 无单独的 `save_session`/`save_answers`/`save_report` 方法，杜绝部分写入导致的孤儿数据。

```python
class ReportRepository:
    def save_complete_session(
        self,
        session: Session,
        answers: list[AnswerItem],
        report: Report
    ) -> str:
        """写入完整作答数据。
        
        开启事务 → 写入 session → 批量写入 answers → 写入 report → 提交。
        任一步骤失败则全回滚，不留孤儿数据。
        返回 session_id。
        """
        pass

    def get_report_by_token(self, share_token: str) -> Report | None:
        """通过分享 token 查询报告（只读，无事务）"""
        pass
```

---

## 7. 项目目录结构

```
open-personality/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI 入口
│   │   ├── config.py              # 配置（数据库路径、环境）
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── questionnaire.py   # M07: 问卷 + 提交端点
│   │   │   └── report.py          # M07: 报告查询端点
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── scoring.py         # M02: 大五计分引擎
│   │   │   ├── mbti.py            # M03: MBTI 推断
│   │   │   ├── report_gen.py      # M04: 报告生成
│   │   │   └── easter_egg.py      # M05: 彩蛋引擎
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py        # M06: 引擎初始化
│   │   │   ├── models.py          # M06: SQLAlchemy ORM 模型
│   │   │   └── repository.py      # M06: 仓库层
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── models.py          # Pydantic 数据模型
│   ├── data/
│   │   ├── items/
│   │   │   ├── ipip120_zh.json
│   │   │   ├── ipip120_en.json
│   │   │   ├── ipip300_zh.json
│   │   │   └── ipip300_en.json
│   │   ├── mbti_mapping.json       # MBTI 映射权重（McCrae & Costa 1989）
│   │   ├── norms.json              # 常模数据（用于 T-score 标准化）
│   │   ├── interpretations_zh.json # 中文解读模板
│   │   ├── interpretations_en.json # 英文解读模板
│   │   └── easter_eggs.json        # 彩蛋文案
│   ├── requirements.txt
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_scoring.py         # M02 单元测试
│       ├── test_mbti.py            # M03 单元测试
│       ├── test_easter_egg.py      # M05 单元测试
│       ├── test_report_gen.py      # M04 单元测试
│       └── test_api.py             # M07 集成测试
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── views/
│   │   │   ├── HomePage.vue        # 首页（选择模式、语言、查询分享码、最近记录）
│   │   │   ├── QuestionnairePage.vue
│   │   │   └── ReportPage.vue      # 报告结果（含分享链接）
│   │   ├── components/
│   │   │   ├── RadarChart.vue
│   │   │   ├── ResultCard.vue
│   │   │   ├── LanguageSwitch.vue
│   │   │   ├── EasterEggBanner.vue
│   │   │   ├── ShareLink.vue
│   │   │   └── ShareCodeInput.vue  # 分享码查询输入框
│   │   ├── composables/
│   │   │   ├── useApi.js
│   │   │   ├── useI18n.js
│   │   │   └── useRecentReports.js # localStorage 最近记录
│   │   ├── i18n/
│   │   │   ├── zh.json
│   │   │   └── en.json
│   │   └── utils/
│   │       ├── api.js              # axios 实例
│   │       └── exportImage.js      # 结果卡片导出图片
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── docs/
│   ├── brief.md
│   ├── design.md                   # 本文件
│   └── proposal.md
├── AGENTS.md
├── status.md
├── requirements.txt
└── README.md
```

---

## 8. 关键设计决策

| 决策 | 选择 | 理由 |
|------|------|------|
| ORM 框架 | SQLAlchemy 2.0 | 迁移 PostgreSQL 零成本，Async 支持好 |
| 会话识别 | share_token (8 位 base62) | 无需注册登录，URL 可分享跨设备访问 |
| 权重存储 | JSON 配置文件 | 可独立修改，无需改代码即可回测校准 |
| 语言包架构 | 后端 + 前端各持一份 | 后端驱动解读文本 + 前端驱动 UI 界面，分离干净 |
| 标准化方法 | T-score (M=50, SD=10) | 心理学领域标准实践，结果易读 |
| 前端路由 | Vue Router (hash mode) | 无需服务端配置，share URL 可带 hash 直接访问 |

---

## 9. 数据文件格式

### 9.1 题目结构 (items/ipip120_zh.json)

```json
{
  "metadata": {
    "mode": "standard",
    "total_items": 120,
    "source": "IPIP-120",
    "lang": "zh"
  },
  "items": [
    {
      "item_id": "ipip_001",
      "dimension": "O",
      "facet": "O_imagination",
      "text": "我经常做白日梦。",
      "reversed": false
    }
  ]
}
```

### 9.2 MBTI 映射权重 (mbti_mapping.json)

```json
{
  "E_I": {
    "formula": "sigmoid(w1*E + w2*A + ... + bias)",
    "weights": {
      "E": 0.35,
      "A": -0.20
    },
    "bias": 0.0
  }
}
```

### 9.3 彩蛋 (easter_eggs.json)

```json
{
  "eggs": [
    {
      "id": "egg_001",
      "zh": "你的创造力指数堪比文艺复兴大师——建议今天请半天假去美术馆。",
      "en": "Your creativity rivals the Renaissance masters — take a half day for the museum."
    }
  ],
  "medium": [
    {
      "id": "medium_001",
      "zh": "（中等彩蛋文案）",
      "en": "..."
    }
  ],
  "trigger_rate": 0.1
}
```

---

## 10. 模块间调用关系矩阵

| 调用方 \\ 被调用方 | M01 问卷 | M02 计分 | M03 MBTI | M04 报告 | M05 彩蛋 | M06 持久化 | M07 API |
|------------------|---------|---------|---------|---------|---------|-----------|---------|
| **M01 问卷**     | —       | —       | —       | —       | —       | —         | 提供数据 |
| **M02 计分**     | —       | —       | —       | —       | —       | —         | —       |
| **M03 MBTI**     | —       | 读分数  | —       | —       | —       | —         | —       |
| **M04 报告**     | —       | 读分数  | 读结果  | —       | 读彩蛋  | —         | —       |
| **M05 彩蛋**     | —       | —       | —       | —       | —       | —         | —       |
| **M06 持久化**   | —       | —       | —       | —       | —       | —         | —       |
| **M07 API**      | 加载题目 | 调用    | 调用    | 调用    | 调用    | 调用      | —       |
| **M08 前端**     | —       | —       | —       | —       | —       | —         | HTTP    |

> 箭头方向：调用方 → 被调用方。例如 M07 API 调用了 M02/M03/M04/M05/M06。

---

## 11. 测试策略

### 11.1 分层测试

| 层 | 工具 | 覆盖范围 | 优先级 |
|----|------|---------|--------|
| 后端单元测试 | pytest | Scoring Engine, MBTI Inference, Easter Egg, Report Generator | P0 |
| 后端集成测试 | pytest + httpx | API 端点、数据库 CRUD | P0 |
| 前端单元测试 | Vitest | 组件渲染、composables、工具函数 | P1 |
| 前端 E2E | Playwright | 完整答题→报告流程、语言切换、图片导出 | P1 |

### 11.2 关键测试场景

**后端 P0**：
- 已知答案 → 验证大五分数是否与预期一致
- 已知大五分数 → 验证 MBTI 概率分布是否合理（E 高分 → E/I 中 E 概率 > 0.5）
- 全部选 3（中立）→ 验证所有域得分在中间范围
- 彩蛋 1000 次调用 → 实际触发率 ≈ 10%（±3%）
- API 提交 → 返回完整 Report 结构，字段非空
- share_token 查询 → 返回正确报告，不存在返回 404
- 反向计分题目 → 分数正确反转

**前端 P1**：
- 雷达图渲染 → 5 个域 + 30 子维度全部显示
- 语言切换 → 所有 UI 文本切换为目标语言
- 结果卡片导出 → 生成图片文件

### 11.3 测试数据策略

- 固定种子答案：用于计分测试，确保 CI 可重复
- 边界值：全部选 1、全部选 5、交替 1-5
- Mock 外部依赖（DB、文件读取）在单元测试中，集成测试用真实 SQLite

---

## 12. 错误处理策略

| 错误场景 | HTTP 状态码 | 响应格式 |
|---------|-----------|---------|
| 提交答案数量不符 (120/300) | 422 | `{ error: "item_count_mismatch", detail: "..." }` |
| 答案值超出 1-5 范围 | 422 | `{ error: "invalid_value", detail: "..." }` |
| share_token 不存在 | 404 | `{ error: "report_not_found" }` |
| 内部计分错误 | 500 | `{ error: "scoring_failed" }` |

---

## 13. 后续可扩展点

- **PostgreSQL 升级**：改 SQLAlchemy 连接字符串即可，零代码变更
- **微信小程序**：前端按分层架构迁移（见下方说明），API 层完全复用
- **多语言扩展**：新增 `data/items/ipip120_ja.json` + 解读模板 + 前端字典
- **部署配置**：阶段四决定，设计上已预留环境变量配置接口

### 13.1 小程序迁移策略（uni-app）

详见 `docs/frontend.md` §9 小程序迁移策略。

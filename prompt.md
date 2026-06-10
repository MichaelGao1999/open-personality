# open-personality — 主控 Prompt

> 阶段四产出：Agent Coding 用主控 Prompt
> 新会话只需读取本文件即可开始阶段五执行。

---

## 1. 项目架构

**open-personality**：大五人格（Big Five）Web 测评工具。标准模式 IPIP-120，高级模式 IPIP-300。附加 McCrae & Costa (1989) 概率化映射推断 MBTI，输出置信度而非硬分类。10% 概率彩蛋。

### 技术栈

| 层 | 选型 | 说明 |
|----|------|------|
| 后端 | Python 3.10+ / FastAPI | 轻量高性能，计分/概率计算天然适合 |
| 前端 | Vue 3 (Composition API) + Vite | SPA，hash mode 路由 |
| 图表 | ECharts + vue-echarts | 雷达图渲染 |
| 数据库 | SQLite (SQLAlchemy 2.0 ORM) | 按需可升级 PostgreSQL |
| 测试 | pytest / httpx / Vitest / Playwright | 分层测试策略 |
| 图片导出 | html2canvas | 结果卡片截图下载 |

### 模块列表与依赖顺序

```
Module 依赖图（自底向上）:

DATA (数据文件) ───────────────────────────┐
INFRA (基础设施) ───→ M06 (持久化) ──────┐   │
                                           │   │
M01 (问卷管理) ──→ M02 (计分引擎) ──→ M03 (MBTI推断) ──┐
                └─→ M05 (彩蛋引擎) ─────────────────┤
                                                     ▼
                                          M04 (报告生成) ──→ M07 (API层) ──→ M08 (前端)
                                          ↑
                                     M06 (持久化层保存 Report)
```

### 开发阶段建议

| Phase | 模块 | 并行度 | 说明 |
|-------|------|--------|------|
| A | INFRA + DATA | 可完全并行 | 骨架 + 数据文件，无代码依赖 |
| B | M02 / M03 / M05 / M04 | M02/M03/M05 并行，M04 后置 | 后端核心业务逻辑 |
| C | M01 / M06 / M07 | M01/M06 并行 → M07 最后 | 集成层 |
| D | M08 | 单独 | 前端（API 稳定后，或先 Mock） |
| E | E2E + 验证 | 单独 | 端到端测试 + 验收 |

---

## 2. 现有代码评估

当前工作区：**无任何已实现代码**。全部仅为设计文档。

- **保留**：无
- **重构**：无
- **新建**：全部 94 个子任务均为新建（详见 `docs/tasks/task-progress.md`）

---

## 3. 主 Agent（Orchestrator）职责

### 调度逻辑

1. 按 Phase A → B → C → D → E 顺序推进
2. 每个 Phase 内标记为可并行的模块，使用独立 SubAgent 并发执行
3. 每模块完成后运行验收检查，通过后再进入下一模块

### 派发模板

每次派发 SubAgent 时，Orchestrator 提供以下上下文：

```
## SubAgent 任务: {模块名} ({模块 ID})

### 设计文档引用
- docs/design.md §{相关章节号} — 接口签名/数据结构
- docs/tasks/task-{module_id}.md — 子任务清单

### 开发约束
- 代码路径：{backend/app/... 或 frontend/src/...}
- 测试路径：{backend/tests/... 或 frontend/src/...}
- 数据契约：design.md §4 为准，不可偏离
- 已知决策：如与 docs/brief.md 矛盾，以 brief.md 为准不复议

### 验收标准
1. 全部子任务完成（P1 优先）
2. 对应测试全部通过
3. 接口签名与 design.md 一致
4. 检查模块间数据契约检查点（task-progress.md §模块间接口契约检查点）
```

### 全局验收检查

Orchestrator 在每模块完成后必须执行：
1. `pytest backend/tests/`（后端）或 `vitest run`（前端）全部通过
2. 接口签名与 `docs/design.md` §4 逐字段比对
3. 数据契约检查点（`docs/tasks/task-progress.md` 中的 CP-01 ~ CP-07）

---

## 4. SubAgent 职责

### 开发流程

1. 读取对应 `docs/tasks/task-{module_id}.md` 全部子任务
2. 按 P1 → P2 优先级顺序实现
3. 遵循 TDD：测试先行（红）→ 实现（绿）→ 重构
4. 实现完成后运行测试确保通过

### 代码规范

**Python（后端）**：
- PEP 8 风格
- 完整类型注解（`def foo(x: int) -> str:`）
- Pydantic v2 model 定义
- SQLAlchemy 2.0 ORM（async session 或 sync session 均可）
- 不使用 `print` / `logging.debug` 等调试输出

**Vue 3（前端）**：
- Composition API + `<script setup>`
- 无全局状态管理（Pinia/Vuex） — 全部用 composable + 组件内 reactive state
- 路由 hash mode
- API 调用统一通过 `src/utils/api.js`

**异常处理**：
- 业务层抛出 `ValueError`（含描述信息）
- API 层统一由错误处理中间件捕获，转换为标准 JSON 错误响应
- 不要在各模块内部捕获后静默处理

### 测试要求

- 后端单元测试：mock 文件 I/O 和 DB 依赖
- 后端集成测试：使用真实 SQLite `:memory:` 数据库
- 前端单元测试：Vitest，测试 composables 和组件渲染
- 测试数据：固定种子答案（可重现）；边界值（全1/全5/全3/交替）

---

## 5. 测试规范

### 分层测试策略

| 层 | 工具 | 覆盖范围 | 优先级 |
|----|------|---------|--------|
| 后端单元测试 | pytest | Scoring Engine, MBTI Inference, Easter Egg, Report Generator | P0 |
| 后端集成测试 | pytest + httpx | API 端点、数据库 CRUD | P0 |
| 前端单元测试 | Vitest | 组件渲染、composables、工具函数 | P1 |
| 前端 E2E | Playwright | 完整答题→报告流程、语言切换、图片导出 | P2 |

### 覆盖率要求

- 后端 P0 模块（M02/M03/M04/M05/M07）：行覆盖率 ≥ 85%
- 后端 P1 模块（M01/M06）：行覆盖率 ≥ 75%
- 前端：组件可测性（不设强制覆盖率指标）

### 关键测试场景（必须覆盖）

```
后端 P0:
- 已知答案 → 大五分数与预期一致（精确到小数点后 1 位）
- 全部选 3（中立）→ 所有域得分在中间范围
- 全部选 1 / 全部选 5 → 极端范围
- E 域高分 → E/I 中 E 概率 > 0.5
- 彩蛋 1000 次调用 → 触发率 7%~13%（10% ± 3%）
- API 提交 → 返回完整 Report，字段非空
- share_token 查询 → 命中返回正确报告，不存在返回 404
- 反向计分题目 → 值正确反转（1↔5, 2↔4, 3不变）
- 答案数量不符（119/301）→ 422
- 答案值越界（0/6）→ 422

前端 P1:
- 雷达图渲染 → 5 域 + 30 子维度全部显示
- 语言切换 → 所有 UI 文本切换为目标语言
- 结果卡片导出 → 生成图片文件
```

---

## 6. 依赖关系与数据契约

### 模块间调用矩阵

| 调用方 | → | 被调用方 | 传递的数据 |
|--------|---|---------|-----------|
| M07 API | → | M01 问卷 | `mode` + `lang` → `QuestionnaireItem[]` |
| M07 API | → | M02 计分 | `answers[]` + `mode` → `ScoringResult` |
| M07 API | → | M03 MBTI | `ScoringResult` → `MBTIResult` |
| M07 API | → | M04 报告 | `ScoringResult` + `MBTIResult` + `easter_egg` + `lang` + `session_id` + `mode` → `Report` |
| M07 API | → | M05 彩蛋 | `lang` → `str` 或 `None` |
| M07 API | → | M06 持久化 | `Session` + `answers[]` + `Report` → DB 写入 |

### 核心数据契约（Pydantic 模型）

```python
class AnswerItem:
    item_id: str    # "ipip_01"
    value: int      # 1~5

class SubmitRequest:
    mode: str       # "standard" | "advanced"
    lang: str       # "zh" | "en"
    answers: list[AnswerItem]

class QuestionnaireItem:
    item_id: str
    dimension: str  # O/C/E/A/N
    facet: str      # O_imagination, ...
    text: str       # 当前语言文本
    reversed: bool

class ScoringResult:
    raw_scores: dict[str, float]    # {"O": 48, ...}
    t_scores: dict[str, float]      # {"O": 55, ...}
    facet_scores: dict[str, float]  # {"O_imagination": 52, ...}

class MBTIDimension:
    label_a: str    # "E"
    label_b: str    # "I"
    prob_a: float   # 0.73
    prob_b: float   # 0.27

class MBTIResult:
    dimensions: list[MBTIDimension]  # 4 对 (E/I, S/N, T/F, J/P)
    confidence: float                # 0~1
    type_code: str                   # "ENFP" (展示用)

class Interpretation:
    dimension: str    # "O"
    title_zh: str
    title_en: str
    body_zh: str
    body_en: str

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

### 模块间接口契约检查点

| CP | 涉及模块 | 验证内容 |
|----|---------|---------|
| CP-01 | M01 → M07 | QuestionnaireItem 字段完整，lang 参数透传正确 |
| CP-02 | M02 → M03 | ScoringResult 字段名与 MBTI 权重 key 一致 |
| CP-03 | M02 → M04 | domain/facet 命名与解读模板 key 一致 |
| CP-04 | M03 → M04 | MBTIResult 字段与 Report 定义一致 |
| CP-05 | M05 → M04 | easter_egg 类型 `str | None` |
| CP-06 | M04 → M06 | Report JSON 字段与 DB 模型一致 |
| CP-07 | M07 → M08 | API 响应 JSON 与前端数据模型一致 |

---

## 7. 已知确认事项（不可复议）

以下决策已确认，如实现过程中发现矛盾直接引用纠偏，不复议：

| ID | 决策内容 |
|----|---------|
| B-01 | Web 测评工具，不做 App/CLI |
| B-02 | 大五人格（Big Five），不做其他模型 |
| B-03 | IPIP-120（标准），IPIP-300（高级模式可选） |
| B-04 | 题目 Public Domain，可自由使用/翻译/修改 |
| B-05 | MBTI 基于 McCrae & Costa (1989) 概率映射，输出置信度 |
| B-06 | 后端 Python FastAPI，前端 Vue 3 + Vite + ECharts |
| B-07 | 数据库 SQLite 起步，按需 PostgreSQL |
| B-08 | 微信小程序未来用 uni-app 迁移 |
| B-09 | 双语言 zh/en，右上角一键切换 |
| B-10 | 无需用户注册登录 |
| B-11 | 极简+卡片风格，结果卡片可导出图片 |
| B-12 | 彩蛋 10% 概率，短文案形式 |
| B-13 | 彩蛋由用户编写（10~15 短 + 3~5 中等） |
| B-14 | 部署方案待定（不阻塞代码） |
| B-15 | 跨设备：share_token 分享链接；同设备：localStorage 最近 5 条 |
| B-16 | ORM: SQLAlchemy 2.0 |
| B-17 | share_token: 8 位 base62 |
| B-18 | T-score 标准化 (M=50, SD=10) |
| B-19 | 路由: Vue Router hash mode |
| B-20 | DB: sessions → answers / sessions → reports |
| B-21 | 所有内容存 JSON 配置文件 |
| B-22 | 前后端各持一份语言包 |

> **纠偏规则**：如 SubAgent 产出与 `docs/brief.md` 矛盾，Orchestrator 直接引用对应 B 编号纠偏，不复议。

---

## 8. 目标目录结构

```
open-personality/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI 入口
│   │   ├── config.py              # 配置（DATABASE_URL, CORS, ENV, DATA_DIR）
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── questionnaire.py   # M07: 问卷 + 提交端点
│   │   │   └── report.py          # M07: 报告查询 + i18n 端点
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── scoring.py         # M02: 大五计分引擎
│   │   │   ├── mbti.py            # M03: MBTI 推断
│   │   │   ├── report_gen.py      # M04: 报告生成
│   │   │   └── easter_egg.py      # M05: 彩蛋引擎
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py        # M06: 引擎初始化 + get_db
│   │   │   ├── models.py          # M06: SQLAlchemy ORM 模型
│   │   │   └── repository.py      # M06: ReportRepository
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── models.py          # Pydantic 数据模型
│   ├── data/
│   │   ├── items/
│   │   │   ├── ipip120_zh.json
│   │   │   ├── ipip120_en.json
│   │   │   ├── ipip300_zh.json
│   │   │   └── ipip300_en.json
│   │   ├── mbti_mapping.json
│   │   ├── norms.json
│   │   ├── interpretations_zh.json
│   │   ├── interpretations_en.json
│   │   └── easter_eggs.json
│   ├── requirements.txt
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_scoring.py
│       ├── test_mbti.py
│       ├── test_easter_egg.py
│       ├── test_report_gen.py
│       └── test_api.py
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── views/
│   │   │   ├── HomePage.vue
│   │   │   ├── QuestionnairePage.vue
│   │   │   └── ReportPage.vue
│   │   ├── components/
│   │   │   ├── RadarChart.vue
│   │   │   ├── ResultCard.vue
│   │   │   ├── LanguageSwitch.vue
│   │   │   ├── EasterEggBanner.vue
│   │   │   ├── ShareLink.vue
│   │   │   └── ShareCodeInput.vue
│   │   ├── composables/
│   │   │   ├── useApi.js
│   │   │   ├── useI18n.js
│   │   │   └── useRecentReports.js
│   │   ├── i18n/
│   │   │   ├── zh.json
│   │   │   └── en.json
│   │   └── utils/
│   │       ├── api.js
│   │       └── exportImage.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── docs/
│   ├── brief.md
│   ├── design.md
│   ├── proposal.md
│   └── tasks/
│       ├── task-progress.md
│       ├── task-infra.md
│       ├── task-data.md
│       ├── task-M01.md ~ task-M08.md
├── AGENTS.md
├── status.md
├── prompt.md                    ← 本文件
├── requirements.txt
└── README.md
```

---

## 9. 验收标准（DoD Checklist）

### 来自 docs/brief.md 逐条核对

- [ ] B-01: 项目是 Web 工具形态，非 App/CLI
- [ ] B-02: 大五人格计分正确（5 域 + 30 子维度）
- [ ] B-03: 标准模式 IPIP-120 / 高级模式 IPIP-300 可选
- [ ] B-04: 题目为 Public Domain，自由使用
- [ ] B-05: MBTI 概率化映射 + 输出置信度
- [ ] B-06: FastAPI + Vue 3 + Vite + ECharts
- [ ] B-07: SQLite 起步
- [ ] B-08: 前端代码壳/核分层，支持 uni-app 迁移
- [ ] B-09: 右上角一键切换 zh/en
- [ ] B-10: 无用户注册、登录、密码
- [ ] B-11: 极简 + 卡片风格，结果卡片可导出图片
- [ ] B-12: 彩蛋 10% 概率触发
- [ ] B-13: 彩蛋池 ≥10 条短 + ≥3 条中等
- [ ] B-14: 部署方案待定（不阻塞代码）
- [ ] B-15: 跨设备分享码 + 同设备 localStorage 最近 5 条
- [ ] B-16: SQLAlchemy 2.0 ORM
- [ ] B-17: share_token 8 位 base62
- [ ] B-18: T-score 标准化 (M=50, SD=10)
- [ ] B-19: Vue Router hash mode
- [ ] B-20: sessions → answers / sessions → reports
- [ ] B-21: 全部内容（题目/权重/解读/彩蛋）存 JSON 配置文件
- [ ] B-22: 前后端各持一份语言包

### 来自 docs/frontend.md §10 未定检查点

- [ ] 主题：默认浅色主题（§10 未定 → 使用浏览器默认/无自定义主题）
- [ ] 图标：未定 → 使用文本或 Unicode 符号替代
- [ ] 响应式：P2 延后，优先桌面端（> 768px）
- [ ] 动画：P2 延后（页面过渡 + 彩蛋动画）

### 功能验收

- [ ] 完整用户流程：首页 → 选择模式 → 答题（120/300 题）→ 提交 → 报告展示
- [ ] 报告包含：大五雷达图（5 域 + 30 子维度）+ MBTI 概率 + 文字解读 + 彩蛋（条件）
- [ ] 结果卡片导出为 PNG 图片
- [ ] 分享链接复制功能正常
- [ ] 分享码查询（有效码 → 报告页；无效码 → 404 提示）
- [ ] 同设备最近 5 条记录（localStorage）
- [ ] 语言切换后全部 UI + 解读文本切换
- [ ] API 错误（数量不符/值越界/无效 mode）返回 422
- [ ] pytest 全部通过（后端）
- [ ] 后端行覆盖率 ≥ 85%（P0 模块）

---

## 10. API 端点汇总

| 方法 | 路径 | 请求 | 响应 (200) | 错误 |
|------|------|------|-----------|------|
| `GET` | `/api/questionnaires/items` | `?mode=standard&lang=zh` | `{ items: QuestionnaireItem[] }` | 422 |
| `POST` | `/api/questionnaires/submit` | Body: `SubmitRequest` | `Report` | 422 |
| `GET` | `/api/report/{share_token}` | Path: 8 位 base62 | `Report` | 404 |
| `GET` | `/api/i18n/{lang}` | Path: `zh` / `en` | `{ [key]: string }` | 404 |

### 错误响应格式

```json
{ "error": "error_code", "detail": "human readable message" }
```

| 场景 | 状态码 | error_code |
|------|--------|-----------|
| 答案数量不符 (120/300) | 422 | `item_count_mismatch` |
| 答案值超出 1-5 | 422 | `invalid_value` |
| share_token 不存在 | 404 | `report_not_found` |
| 内部计分错误 | 500 | `scoring_failed` |

---

## 11. 数据库结构

```
sessions ──1:N── answers
    │
    1:1
    │
reports
```

```sql
CREATE TABLE sessions (
    id          TEXT PRIMARY KEY,           -- UUID
    mode        TEXT NOT NULL,              -- 'standard' | 'advanced'
    lang        TEXT NOT NULL DEFAULT 'zh',
    share_token TEXT NOT NULL UNIQUE,       -- 8 位 base62
    created_at  TEXT NOT NULL               -- ISO 8601
);

CREATE TABLE answers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL REFERENCES sessions(id),
    item_id     TEXT NOT NULL,
    value       INTEGER NOT NULL CHECK(value BETWEEN 1 AND 5)
);

CREATE TABLE reports (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT NOT NULL UNIQUE REFERENCES sessions(id),
    big_five_scores TEXT NOT NULL,           -- JSON
    mbti_result     TEXT NOT NULL,           -- JSON
    interpretations TEXT NOT NULL,           -- JSON
    easter_egg      TEXT,
    created_at      TEXT NOT NULL
);
```

### 事务规则（不可违反）

> **数据库写入只有一个入口**——`ReportRepository.save_complete_session`。计算成功前绝不碰数据库，计算成功后一次事务写入全部数据。无单独的 `save_session`/`save_answers`/`save_report` 方法，杜绝部分写入导致的孤儿数据。

---

## 12. 数据文件格式

所有配置文件为 JSON，放在 `backend/data/` 下：

| 文件 | 用途 | 来源参考 |
|------|------|---------|
| `items/ipip120_zh.json` | IPIP-120 中文题目 | design.md §9.1 |
| `items/ipip120_en.json` | IPIP-120 英文原版 | design.md §9.1 |
| `items/ipip300_zh.json` | IPIP-300 中文题目（P2） | design.md §9.1 |
| `items/ipip300_en.json` | IPIP-300 英文原版（P2） | design.md §9.1 |
| `mbti_mapping.json` | McCrae & Costa 1989 映射权重 | design.md §9.2 |
| `norms.json` | T-score 标准化 M/SD | design.md §9 |
| `interpretations_zh.json` | 中文解读模板（高/低分） | design.md §9 |
| `interpretations_en.json` | 英文解读模板 | design.md §9 |
| `easter_eggs.json` | 彩蛋文案 + trigger_rate | design.md §9.3 |

---

## 13. 已知未定项（不阻塞开发）

- **部署方案**：阶段四后决定（B-14）
- **主题/图标**：默认浅色主题，图标用文本/Unicode 替代
- **响应式**：P2 延后，优先桌面端
- **动画**：P2 延后
- **CI 配置**：P2（INFRA-08）

---

## 14. 政策引用

> 如输出与 `docs/brief.md` 矛盾，Orchestrator 直接引用 brief.md 对应编号纠偏，不复议。

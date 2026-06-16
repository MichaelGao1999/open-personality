# Open Personality

> 基于大五人格（Big Five）模型的在线人格测评工具。支持三档题量（30/120/300 题）、中英文双语、深色模式、进度保存与恢复。

---

## ✨ 功能

| 功能 | 说明 |
|------|------|
| **三种测评模式** | 极速模式（IPIP-30, ~3分钟）/ 标准模式（IPIP-120, ~10分钟）/ 完整模式（IPIP-300, ~25分钟） |
| **中英文双语** | 全界面中英文切换，题目语言独立可配 |
| **深色模式** | 完整支持浅色/深色主题切换 |
| **进度保存与恢复** | 云端保存分享码 + 本地 LocalStorage 自动恢复 |
| **中断恢复** | 答题中途可退出，下次从断点继续 |
| **性格画像报告** | 雷达图 + 柱状图展示五维度分数，含高分/低分解读 + MBTI 概率映射 |
| **彩蛋系统** | 根据测评结果触发趣味彩蛋提示 |
| **报告导出** | 将结果卡片导出为图片分享 |
| **分享码** | 每个报告生成唯一 8 位分享码，方便分享给他人 |
| **后端管理 API** | 自定义映射权重、题目数据、解读模板均可独立配置 |

### 大五人格五维度

| 维度 | 高分倾向 | 低分倾向 |
|------|---------|---------|
| **O - 开放性** | 想象力丰富、喜欢创新 | 务实、循规蹈矩 |
| **C - 严谨性** | 自律、高效、追求完美 | 随性、容易拖延 |
| **E - 外向性** | 热情、社交达人 | 内敛、享受独处 |
| **A - 宜人性** | 信任他人、利他、善于协作 | 竞争心强、理性批判 |
| **N - 神经质** | 敏感、情绪波动大 | 情绪稳定、冷静 |

---

## 🏗️ 技术栈

| 层 | 技术 |
|---|------|
| 前端 | Vue 3 + Vite |
| 后端 | Python FastAPI + SQLAlchemy + SQLite |
| 图表 | ECharts |
| 国际化 | 自实现 i18n composable（JSON 语言包） |
| 代码检查 | ruff (Python) + ESLint (JS) |
| CI/CD | GitHub Actions（lint + test + build） |

---

## 🚀 快速开始

### 前置要求

- Python 3.12+
- Node.js 20+
- npm

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

后端默认运行在 `http://localhost:8000`，API 文档访问 `http://localhost:8000/docs`。

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端默认运行在 `http://localhost:5173`。

### 3. 使用

1. 打开浏览器访问前端地址
2. 选择测评模式（极速/标准/完整）
3. 逐题作答（可随时中断/暂停）
4. 提交后查看性格画像报告
5. 分享报告给他人

---

## 📁 项目结构

```
open-personality/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 入口 + CORS + 路由注册
│   │   ├── config.py            # 环境配置（数据库/数据目录/CORS）
│   │   ├── api/                  # API 端点（问卷提交 + 报告查询 + i18n）
│   │   ├── core/                 # 计分引擎 + MBTI 映射 + 报告生成 + 彩蛋
│   │   ├── db/                   # ORM 模型 + Repository + 初始化
│   │   └── schemas/              # Pydantic 数据模型
│   ├── data/
│   │   ├── items/                # 题目数据（ipip30/120/300 × zh/en）
│   │   ├── norms.json            # 常模数据
│   │   ├── mbti_mapping.json     # MBTI 映射权重
│   │   └── interpretations/      # 维度解读模板（zh/en）
│   └── tests/                    # 41 个后端测试
├── frontend/
│   ├── src/
│   │   ├── views/                # 3 个页面（首页/问卷/报告）
│   │   ├── components/           # 组件（雷达图、结果卡片、设置菜单等）
│   │   ├── composables/          # 组合式函数（i18n、最近报告）
│   │   ├── i18n/                 # 中英文语言包
│   │   ├── utils/                # API 客户端 + 图片导出
│   │   └── styles/               # 全局 CSS（深色模式变量）
│   └── vite.config.js
├── docs/
│   ├── proposal.md               # 需求文档
│   ├── design.md                 # 概要设计
│   ├── brief.md                  # 大白话决策记录
│   ├── frontend.md               # 前端设计文档
│   └── tasks/                    # 任务分解
├── scripts/                      # 辅助脚本
└── .github/workflows/ci.yml      # CI 配置
```

---

## 📊 API 概览

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/questionnaire/start` | POST | 获取题目列表 |
| `/api/questionnaire/submit` | POST | 提交答案 |
| `/api/questionnaire/save-partial` | POST | 保存答题进度 |
| `/api/report/{share_token}` | GET | 获取报告 |
| `/api/i18n/interpretations/{lang}` | GET | 获取解读模板 |
| `/api/i18n/items/{lang}/{mode}` | GET | 获取题目数据 |

完整 API 文档启动后端后访问 `http://localhost:8000/docs`。

---

## 🧪 测试

```bash
# 后端测试（项目根目录执行）
PYTHONPATH=. pytest backend/tests/

# 前端构建验证
cd frontend && npm run build
```

---

## 📝 License

MIT

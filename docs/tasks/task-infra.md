# task-infra: 项目基础设施 & 工具链

> 对应文档：`docs/design.md` §7 项目目录结构

---

## 依赖

- **前置**：无
- **后置**：所有模块，M07/M08 依赖本模块的骨架

---

## 子任务

### INFRA-01 项目骨架搭建 [P1]

- 创建完整目录结构（backend/app/{api,core,db,schemas}, backend/data, backend/tests, frontend/src/{views,components,composables,i18n,utils}, frontend/public）
- 创建各 `__init__.py` 空文件
- 创建 `.gitignore`（忽略 `__pycache__`, `*.db`, `node_modules`, `.env`）
- 创建 `backend/app/__init__.py` + `backend/app/main.py` 空 FastAPI 应用占位

### INFRA-02 后端依赖清单 [P1]

- 编写 `backend/requirements.txt`：
  - `fastapi`, `uvicorn[standard]`, `sqlalchemy>=2.0`, `pydantic`
  - `httpx`（测试）, `pytest`, `pytest-asyncio`
- 验证 `pip install -r requirements.txt` 可正常安装

### INFRA-03 前端依赖初始化 [P1]

- `npm create vite@latest frontend -- --template vue` 或手动创建
- 安装依赖：`vue-router@4`, `echarts`, `vue-echarts`, `axios`, `html2canvas`
- 配置 `vite.config.js`（端口、proxy 到后端）
- 安装 Dev 依赖：`vitest`, `@playwright/test`

### INFRA-04 FastAPI 入口 [P1]

- `backend/app/main.py`：创建 FastAPI 实例
- 配置生命周期事件（startup: 初始化数据库 / shutdown: 关闭连接）
- 注册路由前缀 `/api`
- 配置 CORS（开发阶段允许 localhost:5173）

### INFRA-05 前端入口 [P1]

- `frontend/index.html`：入口 HTML
- `frontend/src/main.js`：挂载 App + Router
- `frontend/src/App.vue`：根组件（RouterView + LanguageSwitch）

### INFRA-06 配置模块 [P1]

- `backend/app/config.py`：基于环境变量 + `.env` 文件
  - `DATABASE_URL`（默认 `sqlite:///./data/open_personality.db`）
  - `CORS_ORIGINS`
  - `ENV`（development / production）
  - `DATA_DIR`（数据文件路径）
- 异常：环境变量缺失时使用默认值，不阻断启动

### INFRA-07 数据库初始化 [P1]

- `backend/app/db/database.py`：引擎创建 + session factory + 表创建
- 支持 `python -m backend.app.db.database` 手动初始化
- 测试：启动后检查表是否存在

### INFRA-08 CI 配置 [P2]

- GitHub Actions 或 GitLab CI 配置
- 触发条件：push / PR 到 master
- Job：install → lint（flake8/ruff） → test（pytest）
- Job：前端 install → test（vitest）

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| `pip install -r requirements.txt` 无错误 | INFRA-02 |
| `npm install` 无错误 | INFRA-03 |
| FastAPI 应用启动（`uvicorn backend.app.main:app`）正常 | INFRA-04 |
| SQLite 数据库初始化后表存在 | INFRA-07 |
| CI 配置文件语法正确 | INFRA-08 |

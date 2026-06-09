# [项目名] — 反模式检查清单

> 阶段二设计时，AI 必须扫描母库 `lessons-learned.md`，按标签过滤与本项目相关的经验，逐一回答以下检查项。
> 本清单确保"上次踩过的坑，这次不再踩"。

---

## 使用说明

1. 读取母库 `lessons-learned.md` 的「技术经验」表格
2. 根据本项目的技术栈和功能特征，筛选相关标签：
   - 本项目有列表/表格/分页 → 关注 `TAG:pagination`
   - 本项目有前端状态管理 → 关注 `TAG:state-management`
   - 本项目有多语言 → 关注 `TAG:i18n`
   - 本项目有删除/确认操作 → 关注 `TAG:security`
   - ...（按实际情况筛选）
3. 对每条 `CRITICAL` 和 `WARNING` 级经验，回答以下四个问题
4. 将结果写入本文件

---

## 检查汇总

| 标签 | 相关经验数 | 本项目是否涉及 | 规避方案已设计 | design.md 章节 |
|------|-----------|---------------|---------------|----------------|
| TAG:pagination | 9 | ❌ 否 | — | — |
| TAG:state-management | 3 ✅涉及 | ✅ 是 | ✅ | 第8章 前端路由 |
| TAG:i18n | 7 ✅涉及 | ✅ 是 | ✅ | 第4章 API / 第8章 设计决策 |
| TAG:testing | 12 ✅涉及 | ✅ 是 | ✅ | 第11章 测试策略 |
| TAG:dom | 9 | ❌ 否（Vue 管理 DOM） | — | — |
| TAG:api-design | 6 ✅涉及 | ✅ 是 | ✅ | 第4章 接口契约 |
| TAG:build-env | 7 | ❌ 否（标准 Python/Node 项目） | — | — |
| TAG:ux | 5 ✅涉及 | ✅ 是 | ✅ | 第1章 UI 风格（proposal） |
| TAG:security | 1 | ❌ 否（无删除操作/无认证） | — | — |
| TAG:data | 4 ✅涉及 | ✅ 是 | ✅ | 第9章 数据文件格式 |
| TAG:architecture | 5 ✅涉及 | ✅ 是 | ✅ | 第2章 模块划分 / 第10章 调用矩阵 |
| TAG:debugging | 4 | ❌ 否 | — | — |
| TAG:ai-workflow | 10 | ❌ 否（AI 工作流已有 AGENTS.md） | — | — |
| TAG:cross-platform | 6 ✅涉及 | ✅ 是 | ✅ | 第13章 可扩展点 |
| TAG:performance | 1 | ❌ 否（数据量极小） | — | — |

---

## 详细检查项

> 以下模板条目可根据本项目实际情况增删。每条检查项对应母库中的一条或多条经验。

---

### [TAG:pagination] [CRITICAL] 分页 + 批量操作的数据一致性

- **来源经验**：lessons-learned.md #86-94（french-exit）
- **核心规则**：
  1. 选中状态必须单一数据源
  2. 全选/取消必须范围对称
  3. 确认页必须遍历决策集合，而非展示数据
- **本项目是否涉及**：❌ 否
- **理由**：本项目无需分页、无批量操作、无列表选中。单次答题 120/300 道题，一次性展示所有结果报告，不涉及跨页操作。

---

### [TAG:state-management] [CRITICAL] SPA 状态管理 — 避免 React 类陷阱

- **来源经验**：lessons-learned.md #59-61（french-exit）
- **核心规则**：
  1. setState updater 内禁止调用 dispatch/其他 setState
  2. useEffect 依赖布尔条件易死循环
  3. 批量初始化优先用 useRef/onMounted
- **本项目是否涉及**：✅ 是
- **本项目如何规避**：
  - Vue 3 使用 `onMounted` 替代 `useEffect` 类模式，天然避免依赖数组死循环
  - composable 函数用 `ref()`/`reactive()` + `watch()` 显式管理，不嵌套触发
  - 答题状态用本地 `reactive` 对象管理，不依赖全局 store
- **相关模块/接口**：`frontend/src/views/QuestionnairePage.vue`

---

### [TAG:security] [CRITICAL] 默认安全 > 默认便利

- **来源经验**：lessons-found.md #88（french-exit）
- **核心规则**：
  1. 涉及删除/不可逆操作的工具，禁止默认自动勾选
  2. 所有选择必须用户显式操作
- **本项目是否涉及**：❌ 否
- **理由**：本项目无删除操作、无不可逆批量操作。唯一持久化操作是答题提交（用户主动点击提交），不做自动提交或默认勾选。

---

### [TAG:i18n] [CRITICAL] i18n 分散架构导致翻译遗漏

- **来源经验**：lessons-learned.md #18-22（blindfold-chess）
- **核心规则**：
  1. 必须单一字典源（禁止"全局字典 + 模块私有字典 + 硬编码"并存）
  2. JS 中的用户可见字符串必须有显式翻译标记
  3. 翻译检查必须是独立任务
- **本项目是否涉及**：✅ 是
- **本项目如何规避**：
  - 前端 UI 文本：单一 JSON 字典（`i18n/zh.json` + `i18n/en.json`），Vue 模板中全部通过 `$t()` 函数引用，零硬编码
  - 后端解读文本：作为数据文件（`data/interpretations_zh/en.json`）由后端加载，前端不介入解读文本的翻译
  - 前后端分离：UI 字典前端管，解读文本后端管，职责清晰不交叉
  - 题目文本：也作为数据文件（`data/items/ipip120/en/zh.json`），双语均有，由后端下发
- **相关模块/接口**：`M01 问卷管理`, `M04 报告生成`, `M08 前端视图`, `frontend/src/i18n/`

---

### [TAG:ux] [CRITICAL] UI 布局不要猜测用户意图

- **来源经验**：lessons-learned.md #12（blindfold-chess）
- **核心规则**：
  1. 设计阶段出草图或描述供用户确认，再编码
  2. 避免反复修改同一 UI 元素
- **本项目是否涉及**：✅ 是
- **本项目如何规避**：
  - 阶段三（任务分解）会产生各页面的线框图/布局描述
  - 已确认 UI 风格：极简 + 卡片（B-11），结果可导出图片
  - 阶段五编码前会出页面结构描述供用户确认
- **相关模块/接口**：`M08 前端视图`

---

### [TAG:testing] [CRITICAL] 删除功能/fallback 前评估测试依赖

- **来源经验**：lessons-learned.md #25（blindfold-chess）
- **核心规则**：
  1. 架构统一重构必须同时改代码+测试
  2. 只改一边会导致测试雪崩
- **本项目是否涉及**：✅ 是
- **本项目如何规避**：
  - 测试策略已在 design.md 第11章明确定义：分层测试（单元→集成→E2E）
  - 每个模块单独可测（M02~M05 纯逻辑，无外部依赖）
  - 测试作为阶段五的交付物，与源码同步产出，避免"先写代码后补测试"的脱节
  - CRITICAL 原则：任何生产代码变更必须同步变更对应测试
- **相关模块/接口**：`backend/tests/`, `frontend/`

---

### [TAG:cross-platform] [CRITICAL] 中文路径 + 编译失败

- **来源经验**：lessons-learned.md #70-71, #75（french-exit）
- **核心规则**：
  1. Rust/Tauri 项目在中文路径下编译可能失败
  2. `cargo check --lib` 不需要链接，中文路径可跑
- **本项目是否涉及**：❌ 否
- **理由**：本项目为 Python FastAPI + Vue 3，无 Rust/Tauri 组件。Python 和 Node.js 在中文路径下无已知编译问题。微信小程序迁移（uni-app）也基于 JS，无原生编译依赖。

---

## 自定义检查项

> 根据本项目特征，从母库 lessons-learned.md 中补充其他相关检查项。

### [TAG:xxx] [SEVERITY] 检查项标题

- **来源经验**：lessons-learned.md #[编号]
- **核心规则**：
  1. [规则]
- **本项目是否涉及**：❌ 否 / ✅ 是
- **本项目如何规避**：
  - [规避方案描述]
- **相关模块/接口**：`[模块名]`

---

## 检查结论

| 级别 | 涉及数 | 已规避数 | 待处理 |
|------|--------|---------|--------|
| CRITICAL | 7 | 7 | 0 |
| WARNING | 0 | 0 | 0 |
| INFO | 0 | 0 | 0 |

> **强制要求**：所有 CRITICAL 级检查项必须回答"本项目如何规避"。如本项目不涉及，需明确说明理由。以上 7 项已全部完成评估与规避方案设计。

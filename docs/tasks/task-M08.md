# task-M08: 前端视图 (Frontend UI)

> 对应文档：`docs/design.md` §7 项目目录结构（frontend/）· `docs/proposal.md` §10 UI 风格
> 路径：`frontend/src/` 全部文件

---

## 依赖

- **前置**：M07（API 层稳定后开始，或先 Mock API 并行开发）
- **调用方**：浏览器终端用户

---

## 子任务 (核心 — P1)

### M08-01 Vue 3 + Vite 项目初始化 [P1]

- `npm create vite@latest` 初始化 Vue 3 项目
- 安装依赖：`vue-router@4`, `axios`, `echarts`, `vue-echarts`, `html2canvas`
- 配置 `vite.config.js`（proxy `/api` → `http://localhost:8000`）
- 确认 `npm run dev` 可启动

### M08-02 Vue Router 配置 [P1]

- 三种模式：hash mode（符合 B-19 决策）
- 三个路由：
  - `/` → HomePage
  - `/questionnaire` → QuestionnairePage（可传 ?mode=standard|advanced）
  - `/report/:share_token` → ReportPage

### M08-03 API 工具函数 [P1]

- `frontend/src/utils/api.js`：axios 实例（baseURL, timeout）
- 四个函数：
  - `getItems(mode, lang)` → GET `/api/questionnaires/items`
  - `submitAnswers(mode, lang, answers)` → POST `/api/questionnaires/submit`
  - `getReport(shareToken)` → GET `/api/report/{token}`
  - `getI18n(lang)` → GET `/api/i18n/{lang}`

### M08-04 useI18n composable [P1]

- 响应式存储当前语言（`ref('zh')`）
- `t(key)` 函数：从语言包字典取对应文案
- 语言切换时自动触发 UI 更新
- 从 URL 参数或浏览器偏好初始化默认语言

### M08-05 前端语言包 [P1]

- `frontend/src/i18n/zh.json`：按钮文字、提示、标签、错误文案
- `frontend/src/i18n/en.json`：英文对应
- 键名按功能分组（nav, questionnaire, report, home, error, common）

### M08-06 LanguageSwitch 组件 [P1]

- 右上角固定位置
- 当前语言高亮显示
- 点击切换，自动触发 `useI18n` 切换
- 过渡动画（可选）

### M08-07 HomePage 视图 [P1]

- 模式选择卡片（标准 / 高级）
- 语言选择（继承自全局 LanguageSwitch）
- "开始测评"按钮 → 跳转 `/questionnaire?mode=xxx`
- 展示品牌名称和简短描述

### M08-08 ShareCodeInput 组件 [P1]

- 输入框 + 查询按钮
- 8 位 base62 格式前端校验
- 调用 `getReport(token)` → 命中跳转 ReportPage，未命中提示"分享码无效"

### M08-09 useRecentReports composable [P1]

- localStorage CRUD：存/取/删
- 数据格式：`{ share_token, created_at }` 数组
- 自动保留最近 5 条，超出时移除最旧

### M08-10 首页最近记录列表 [P1]

- 从 `useRecentReports` 读取并展示
- 点击跳转 ReportPage
- 有记录时展示区块，无记录时隐藏

### M08-11 QuestionnairePage 视图 [P1]

- 从 URL 参数读取 mode
- 调用 `getItems(mode, lang)` 加载题目
- 分页展示（每页 10 题）或长滚动
- 进度条指示完成比例

### M08-12 答题状态管理 [P1]

- 响应式存储答案（`Map<item_id, value>`）
- 缓存已选答案，翻页不丢失
- 全部答完前"提交"按钮禁用
- 提交前二次确认

### M08-13 提交交互动画 [P1]

- 提交时 loading 状态
- 请求完成 → 调用 `useRecentReports.add()` 记录
- 自动跳转 ReportPage

### M08-14 RadarChart 组件 [P1]

- ECharts 雷达图
- 5 个域 + 得分标注
- 支持中英文字段
- 响应式尺寸

### M08-15 ResultCard 组件 [P1]

- 卡片式展示各域得分（进度条或数值）
- MBTI 概率映射结果展示（带置信度标注）
- "导出图片"按钮

### M08-16 exportImage 工具 [P1]

- `frontend/src/utils/exportImage.js`
- 使用 html2canvas 将结果卡片区截图
- 触发浏览器下载
- 支持中英文文案

### M08-17 EasterEggBanner 组件 [P1]

- 彩蛋触发时展示（条件渲染 v-if）
- 未触发时不显示任何内容（无 fallback 替代文案）
- 动画效果（淡入/弹出）
- 显示彩蛋文案文本

### M08-18 ReportPage 视图 [P1]

- 从路由参数 `share_token` 加载报告
- 调用 `getReport(token)` 获取数据
- 组装全部子组件：RadarChart + ResultCard + EasterEggBanner + ShareLink
- 加载态 / 出错态 / 空态

### M08-19 ShareLink 组件 [P1]

- 当前页面完整 URL（含 hash）可复制
- "复制链接"按钮（`navigator.clipboard.writeText`）
- 复制后提示"已复制"

## 子任务 (增强 — P2)

### M08-20 E2E 测试 [P2]

- Playwright 配置
- 测试场景：
  - 完整答题流程 → 提交 → 报告展示
  - 语言切换后全部 UI 文本切换
  - 结果卡片导出图片
  - 首页分享码查询
  - 最近记录显示

### M08-21 响应式布局 [P2]

- 移动端适配（< 768px）
- 卡片在移动端纵向排列
- 雷达图在移动端尺寸适配
- 答题页在移动端的触摸友好

### M08-22 页面过渡动画 [P2]

- 答题页 → 报告页切换动画
- 雷达图载入动画
- 彩蛋出现动画

---

## 组件树

```
App.vue
├── LanguageSwitch.vue (fixed top-right)
└── RouterView
    ├── HomePage.vue
    │   ├── ShareCodeInput.vue
    │   └── 最近记录列表（inline）
    ├── QuestionnairePage.vue
    │   └── 题目列表（inline）
    └── ReportPage.vue
        ├── RadarChart.vue
        ├── ResultCard.vue
        ├── EasterEggBanner.vue
        └── ShareLink.vue
```

---

## 测试点

| 测试项 | 覆盖 |
|--------|------|
| 3 个路由正常跳转 | M08-02 |
| 题目加载并分页展示 | M08-11 |
| 作答状态翻页不丢失 | M08-12 |
| 语言切换全 UI 更新 | M08-06 |
| 雷达图 5 域渲染 | M08-14 |
| 结果卡片导出图片 | M08-16 |
| 彩蛋条件渲染 | M08-17 |
| 分享码查询命中/未命中 | M08-08 |
| 最近记录 localStorage 持久化 | M08-09 |
| E2E 答题→报告→导出全流程 | M08-20 |
| 移动端布局正常 | M08-21 |

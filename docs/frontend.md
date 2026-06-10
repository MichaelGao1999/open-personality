# open-personality — 前端设计文档

> 阶段二产出（条件性，T-05②）：界面层设计文档
> 状态：✅ 回补完成
> 与 `design.md` 的边界：`design.md` 描述模块划分和接口契约（前后端通用），本文件描述界面层设计（组件/页面/交互）

---

## 1. 界面类型声明

**Web SPA**（Single Page Application），基于 Vue 3 + Vite 构建。

目标浏览器：现代浏览器（Chrome / Firefox / Safari / Edge 最新两个大版本）。
未来可迁移至微信小程序（uni-app），见 §9。

---

## 2. 技术选型

| 类别 | 选型 | 版本/说明 |
|------|------|----------|
| 框架 | Vue 3 | Composition API |
| 构建工具 | Vite | 开发服务器 + 生产构建 |
| 路由 | vue-router@4 | hash mode（B-19） |
| HTTP 客户端 | axios | API 通信 |
| 图表 | ECharts + vue-echarts | 雷达图渲染 |
| 图片导出 | html2canvas | 结果卡片截图导出 |
| 状态管理 | 无全局 store | composables + 组件内 reactive state |
| 国际化 | 自实现（useI18n composable） | 前端驱动 UI 文本（B-22） |

---

## 3. 页面/视图清单

| 页面 | 路由 | 职责 |
|------|------|------|
| **HomePage** | `/` | 入口页：模式选择（标准/高级）、品牌展示、分享码查询入口、最近记录列表 |
| **QuestionnairePage** | `/questionnaire?mode=standard\|advanced` | 答题页：题目加载与分页展示、答题进度、状态缓存、提交 |
| **ReportPage** | `/report/:share_token` | 报告页：雷达图 + 结果卡片 + MBTI 概率 + 解读文字 + 彩蛋 + 分享链接 |

---

## 4. 组件树

```
App.vue
├── LanguageSwitch.vue (fixed top-right)
└── RouterView
    ├── HomePage.vue
    │   ├── ShareCodeInput.vue      -- 8位分享码输入 + 查询
    │   └── 最近记录列表（inline）   -- localStorage 最近 5 条
    ├── QuestionnairePage.vue
    │   └── 题目列表（inline）      -- 分页/长滚动 + 进度条
    └── ReportPage.vue
        ├── RadarChart.vue          -- ECharts 大五雷达图
        ├── ResultCard.vue          -- 域得分 + MBTI 概率 + 导出按钮
        ├── EasterEggBanner.vue     -- 彩蛋条件渲染（v-if）
        └── ShareLink.vue           -- 当前 URL 复制分享
```

### 组件职责

| 组件 | 职责 | 关键 props / events |
|------|------|-------------------|
| LanguageSwitch | 右上角语言切换（zh/en） | 切换时触发 useI18n 更新 |
| ShareCodeInput | 分享码输入 + 查询 | emit: `found(token)` / 提示"无效" |
| RadarChart | 5 域雷达图（ECharts） | props: `scores`, `lang` |
| ResultCard | 域得分进度条 + MBTI 概率 + 导出 | props: `report`, `lang` |
| EasterEggBanner | 彩蛋文案展示 | props: `text`；条件渲染 |
| ShareLink | 分享 URL 复制 | 读取 `window.location.href` |

---

## 5. 路由/导航结构

| 路径 | 组件 | 参数 | 说明 |
|------|------|------|------|
| `/` | HomePage | — | 首页入口 |
| `/questionnaire` | QuestionnairePage | `?mode=standard\|advanced` | 答题页 |
| `/report/:share_token` | ReportPage | 8 位 base62 token | 报告页 |

**导航流程**：
```
HomePage ──选择模式──→ /questionnaire?mode=standard
                      /questionnaire?mode=advanced
         ──输入分享码──→ /report/{token}
         ──点击最近记录──→ /report/{token}

QuestionnairePage ──提交完成──→ /report/{token}

ReportPage ──复制链接──→ 分享给他人（同 URL 直接访问）
```

路由使用 **hash mode**（B-19），无需服务端配置，分享链接可直接访问。

---

## 6. 状态管理方案

**无全局状态管理库**（如 Pinia/Vuex），使用 composables 模式：

| composable | 职责 | 持久化 |
|-----------|------|--------|
| `useApi` | axios 实例封装、错误处理 | 无 |
| `useI18n` | 当前语言 `ref('zh')`、`t(key)` 翻译函数 | localStorage 缓存语言偏好 |
| `useRecentReports` | 最近 5 条报告记录 CRUD | localStorage |

**页面级状态**：答题状态（`Map<item_id, value>`）由 QuestionnairePage 组件内部管理，不跨页面共享。

---

## 7. 交互流程

### 7.1 答题 → 报告（主流程）

```
1. HomePage 选择模式（standard/advanced）
2. 跳转 /questionnaire?mode=xxx
3. 加载题目列表（getItems）
4. 分页答题，进度条指示
5. 全部答完 → "提交"按钮激活
6. 提交前二次确认
7. 调用 submitAnswers → loading 状态
8. 成功 → useRecentReports.add() 记录
9. 自动跳转 /report/{share_token}
10. 渲染：雷达图 + 结果卡片 + 解读文字 + 彩蛋（条件）+ 分享链接
```

### 7.2 分享码查询

```
1. HomePage → ShareCodeInput 输入 8 位码
2. 前端校验格式（8 位 base62）
3. 调用 getReport(token)
4. 命中 → 跳转 /report/{token}
5. 未命中 → 提示"分享码无效"
```

### 7.3 最近记录

```
1. 答题成功后，{ share_token, created_at } 写入 localStorage
2. HomePage 加载时读取，展示最近 5 条
3. 点击任一条 → 跳转 /report/{token}
4. 超出 5 条自动移除最旧
```

### 7.4 语言切换

```
1. 右上角 LanguageSwitch 点击
2. useI18n.lang 切换（zh ↔ en）
3. 所有 UI 文本响应式更新
4. 同时影响 API 请求的 lang 参数
```

---

## 8. i18n 策略

**前后端各持一份语言包**（B-22）：

| 语言包位置 | 驱动内容 | 格式 |
|-----------|---------|------|
| 后端 `data/interpretations_{lang}.json` | 解读文本（域/子维度描述） | JSON |
| 前端 `src/i18n/{lang}.json` | UI 文本（按钮、标签、提示、错误） | JSON |

前端语言包键名按功能分组：`nav` / `questionnaire` / `report` / `home` / `error` / `common`。

---

## 9. 小程序迁移策略（uni-app）

> 从 `design.md` §13.1 迁入。design.md 中保留引用指向本节。

前端代码按「壳/核」分层：

```
frontend/src/
├── views/            ← 【壳】页面级视图组件（迁移时需按 uni-app 重写）
│   ├── HomePage.vue
│   ├── QuestionnairePage.vue
│   └── ReportPage.vue
├── components/       ← 【壳】展示型组件（部分需 uni-app 适配）
│   ├── RadarChart.vue       ← ECharts → echarts-for-weixin
│   ├── ResultCard.vue       ← DOM 导出 → Canvas API
│   ├── EasterEggBanner.vue  ← 纯展示，低风险
│   ├── ShareLink.vue        ← 纯展示，低风险
│   └── LanguageSwitch.vue   ← 纯交互，低风险
├── composables/      ← 【核】纯逻辑，零 DOM 依赖，100% 复用 ✅
│   ├── useApi.js
│   └── useI18n.js
├── i18n/             ← 【核】语言字典文件，100% 复用 ✅
│   ├── zh.json
│   └── en.json
└── utils/            ← 【核/壳混合】
    ├── api.js              ← 【核】axios → uni.request，接口签名不变
    └── exportImage.js      ← 【壳】html2canvas → Canvas API，需重写
```

**迁移工作量预估**：

| 层 | 行数占比 | 需重写比例 | 说明 |
|----|---------|-----------|------|
| views | ~30% | 100% | 路由机制、页面生命周期不同 |
| components | ~25% | 20-80% | 雷达图和导出需重写，其余几乎不改 |
| composables | ~15% | 0% | 纯逻辑，零改动 |
| i18n | ~10% | 0% | 字典文件直接复制 |
| utils | ~20% | ~30% | api.js 改请求库，exportImage 重写 |

**核心原则**：「核」代码（composables / i18n / 数据模型）禁止出现 `window`、`document`、`DOM` 操作，确保零成本复用。

---

## 10. UI 规范

| 项 | 规范 |
|----|------|
| 风格 | 极简 + 卡片（B-11） |
| 响应式 | P2 延后，优先桌面端；移动端适配 < 768px（M08-21） |
| 主题 | 待定，默认浅色主题 |
| 图标 | 待定 |
| 动画 | 页面过渡 + 彩蛋出现动画（P2，M08-22） |

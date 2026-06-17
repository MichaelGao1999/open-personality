# 好友对比功能 — 设计文档

> 状态：📝 设计已审查
> 版本：v0.2
> 关联：`docs/frontend.md`
> 对应需求：分享码/图片分享给好友后，好友可查看并对比两人结果

---

## 1. 用户故事

### 1.1 查看好友结果

```
小明测完，把 8 位分享码 AbCd1234 发给小红。
小红打开首页 → 输入分享码 → 看到小明的报告。
底部显示「你还没测，要测一下然后对比吗？」
小红点「我也要测」→ 答题 → 自动进入对比视图。
```

### 1.2 双人对比

```
小红测完后，再次输入小明的分享码（或从历史记录点击）。
两人结果并列显示：雷达图叠加 + 维度对照 + 差异高亮。
小红可以截图分享对比结果。
```

### 1.3 图片 + 二维码（后续）

```
小明导出报告图片，图片底部自带二维码。
好友扫码 → 打开网页版报告 → 触发「我也要测」→ 对比。
```

---

## 2. 数据流

```
┌──────────┐   分享码         ┌──────────┐
│  小明    │ ──────────────→ │   好友    │
│ tokenA   │   AbCd1234      │          │
└──────────┘                 └────┬─────┘
                                  │ ① 输入分享码
                       ┌──────────┴──────────┐
                       │  GET /report/{token} │  ← 已有
                       │  看到小明报告        │
                       └──────────┬──────────┘
                                  │ ② 「我也要测」
                       ┌──────────┴──────────┐
                       │  跳问卷页            │
                       │  ?mode=advanced     │
                       │  &friendToken=AbCd  │  ← 关键：把好友token带过去
                       └──────────┬──────────┘
                                  │ 答题 → 提交
                       ┌──────────┴──────────┐
                       │  POST /questionnaire │
                       │  返回 tokenB         │
                       └──────────┬──────────┘
                                  │ ③ 问卷回调
                       ┌──────────┴──────────┐
                       │  检查 route.query   │
                       │  .friendToken 存在?  │
                       │  → /compare/{tokenB}│
                       │    /{friendToken}   │
                       └──────────┬──────────┘
                                  │ ④ 对比页
                       ┌──────────┴──────────┐
                       │  并行加载两份 report │
                       │  Promise.all([       │
                       │   getReport(myT),   │
                       │   getReport(friendT) │
                       │  ])                  │
                       │  前端计算差异        │
                       │  渲染对比视图        │
                       └─────────────────────┘
```

**关键决策**：对比逻辑全在前端——只需两份 `report` JSON，前端算差值，无需新增 API。

---

## 3. 页面 & 路由设计

### 3.1 路由表

| 路由 | 页面 | 说明 |
|------|------|------|
| `/report/{token}?friend=1` | 好友报告页 | 显示好友报告 +「我也要测」按钮 |
| `/compare/{myToken}/{friendToken}` | 对比页 | 双人并列对比视图 |
| `/report/{token}` | 个人报告页 | 不变 |

### 3.2 好友报告页（改造 `ReportPage.vue`）

当 `?friend=1` 时：

- 顶部标题改为「好友的结果」
- `ResultCard` 正常渲染好友的报告
- 卡片下方显示「我也要测」引导区

```
┌──────────────────────────────────┐
│  [👤 好友的结果]                  │
│                                  │
│  ┌──────────────────────────┐    │
│  │  雷达图 + 柱状图          │    │
│  │  (好友的数据)             │    │
│  └──────────────────────────┘    │
│                                  │
│  ┌──────────────────────────┐    │
│  │  💡 你还没测！            │    │
│  │  测一下看看你和好友的     │    │
│  │  性格差异有多大           │    │
│  │                          │    │
│  │  [🚀 我也要测 → 对比]    │    │
│  │  [← 返回首页]            │    │
│  └──────────────────────────┘    │
└──────────────────────────────────┘
```

**「我也要测」按钮跳转**：
```js
// 跳转时把好友的 token 带过去
router.push({
  path: '/questionnaire',
  query: {
    mode: 'advanced',
    friendToken: route.params.token  // ← friend token 不能丢
  }
})
```

### 3.3 问卷页回调改造（`QuestionnairePage.vue`）

在 `submit()` 成功后：

```js
// 原来：直接跳个人报告页
// 改为：检查是否有 friendToken
if (route.query.friendToken) {
  router.replace(`/compare/${res.data.share_token}/${route.query.friendToken}`)
} else {
  router.push(`/report/${res.data.share_token}`)
}
```

同样逻辑适用于 `viewPartialResult()`。

### 3.4 双人对比页（新增 `ComparePage.vue`）

```
┌──────────────────────────────────────────┐
│  🔄 性格对比                   时间戳      │
│  你 vs 好友                               │
├──────────────────────────────────────────┤
│  ┌─────────── 雷达图叠加 ──────────┐      │
│  │  ── 你 (实线)  颜色A             │     │
│  │  - - 好友 (虚线) 颜色B           │     │
│  └──────────────────────────────────┘      │
│                                           │
│  ── 五大维度 ──                            │
│  开放性    72 ━━━━━━━━━━━━ 55 ━━━━━━━    │
│  严谨性    48 ━━━━━━     61 ━━━━━━━━━   │
│  外向性    55 ━━━━━━━    50 ━━━━━━━━    │
│  宜人性    38 ━━━        72 ━━━━━━━━━   │  ← 差异最大
│  神经质    65 ━━━━━━━    42 ━━━━━       │
│                                           │
│  ── 差异最大的子维度 ──                    │
│  🔺 顺从度      38 vs 72  (+34)          │
│  🔺 信任倾向度  42 vs 70  (+28)          │
│  🔻 成就欲      68 vs 42  (-26)          │
│  🔻 条理性      35 vs 60  (-25)          │
│  ...                                      │
│                                           │
│  整体相似度: 73%                           │
│  你和好友在性格上有不少共同点，             │
│  但在宜人性(+34)和成就欲(-26)上            │
│  有明显差异。                              │
│                                           │
│  [📷 导出对比图]                           │
└──────────────────────────────────────────┘
```

**加载逻辑**：

```js
// 并行加载两个 report
const [myRes, friendRes] = await Promise.all([
  getReport(myToken),
  getReport(friendToken),
])
// 任一个失败 → 显示错误状态
```

**错误状态**：如果任一 token 无效（404），显示友好的错误提示和一个返回首页的按钮。

**未测用户引导**：如果 `myToken` 是无效的或过期（report 不存在），页面提示「你没有自己的报告，先去测一个 →」并跳转到首页。

### 3.5 边界状态矩阵

| 场景 | 表现 | 处理方式 |
|------|------|---------|
| 一方 token 404 | 全页报错，不部分渲染 | 两个 `getReport` 任一个失败 → 显示错误卡片 + 返回首页按钮 |
| 双方 token 相同 | 自己 vs 自己 | `ComparePage` 检测 `myToken === friendToken` → 提示「这是同一个人」+ 显示单一报告 |
| 网络超时/失败 | 加载中→超时 | 显示 loading spinner → 超时后显示错误 + 重试按钮 |
| 对方 facetScores 缺少 | `compare.js` 计算时取到 `undefined` | `compare.js` 内 `getScore(k) || 0` 防御，不抛异常 |
| 自己未测（myToken 无效） | 无自己的 report | 检测到 404 → 引导「先去测一个」 |
| 对方未测（friendToken 无效） | 无好友报告 | 显示「好友的报告不存在，请确认分享码」 |

---

## 4. 跳转链条（文件级）

> 三个文件之间的参数传递必须显式串联，否则流程断裂。

### 4.1 起点：输入分享码 → `ShareCodeInput.vue`

```js
// 当前：router.push(`/report/${token}`)              ← 无 ?friend=1
// 改为：
function search() {
  const token = code.value.trim()
  if (token) {
    router.push(`/report/${token}?friend=1`)          // ← 标记为好友报告
  }
}
```

### 4.2 中继：好友报告页 → `ReportPage.vue`

```js
// 当前：
function continueTest() {
  router.push({ path: '/questionnaire', query: { mode: 'advanced', resume: report.value.share_token } })
}

// 改为——从 ?friend=1 页面跳转时带上 friendToken：
function continueTest() {
  const query = { mode: 'advanced', resume: report.value.share_token }
  if (route.query.friend === '1') {
    query.friendToken = route.params.token             // ← 好友 token 传递到问卷页
  }
  router.push({ path: '/questionnaire', query })
}
```

### 4.3 终点：问卷提交回调 → `QuestionnairePage.vue`

`submit()` 成功后：

```js
// 当前：router.push(`/report/${res.data.share_token}`)
// 改为：
if (route.query.friendToken) {
  router.replace(`/compare/${res.data.share_token}/${route.query.friendToken}`)
} else {
  router.push(`/report/${res.data.share_token}`)
}
```

`viewPartialResult()` 同理：

```js
// 改为：
if (route.query.friendToken) {
  router.replace(`/compare/${report.share_token}/${route.query.friendToken}`)
} else {
  router.push({ path: `/report/${report.share_token}`, query: { partial: '1', mode } })
}
```

### 4.4 跳转全貌

```
ShareCodeInput.vue                 ReportPage.vue                    QuestionnairePage.vue
┌─────────────────┐               ┌──────────────────┐              ┌──────────────────────┐
│ search()         │               │ continueTest()   │              │ submit()              │
│                  │               │                  │              │                       │
│ /report/{token}  │ ──────────→  │ 检测 ?friend=1   │              │ 检测 friendToken     │
│ ?friend=1        │               │ 传 friendToken   │ ──────────→ │ 有 → /compare/{my}/{f}│
└─────────────────┘               │ 到 questionnaire │              │ 无 → /report/{my}     │
                                  └──────────────────┘              └──────────────────────┘
```

### 4.5 `?friend=1` 的区分作用

| 场景 | URL | 含义 |
|------|-----|------|
| 自己测完查看 | `/report/AbCd1234` | 个人报告 |
| 好友输入分享码查看 | `/report/AbCd1234?friend=1` | 好友的报告，显示「我也要测」 |
| 从历史记录点击 | `/report/AbCd1234` | 个人报告 |

无用户认证系统，`?friend=1` 是唯一的区分方式。

---

## 5. 组件树

```
src/
├── views/
│   ├── ReportPage.vue          ← 改造：?friend=1 模式 + 传 friendToken 到问卷
│   ├── ComparePage.vue         ← 新增：双人对比页
│   └── QuestionnairePage.vue   ← 改造：submit 成功后检查 friendToken
│
├── components/
│   ├── CompareView.vue         ← 新增：对比视图核心
│   ├── RadarChart.vue          ← 改造：props.scores 支持数组（双数据叠加）
│   └── ...
│
└── utils/
    ├── api.js                  ← 不变
    ├── compare.js              ← 新增：差异计算工具函数
    ├── facetMeta.js            ← 新增：从 ResultCard.vue 提取的共享常量
    │                             含 facetMeta, dimLabelCn, dimLabelEn, dimColors
    └── exportImage.js          ← 改造：支持导出对比图
```

---

## 5. 常量共享

从 `ResultCard.vue` 提取 `facetMeta`、`dimLabelCn`、`dimLabelEn`、`dimColors`、`dimensionOrder` 到 `utils/facetMeta.js`，让 `compare.js` 和 `CompareView.vue` 可以直接引用子维度中文名。

```js
// utils/facetMeta.js
export const dimLabelCn = { O: '开放性', C: '严谨性', E: '外向性', A: '宜人性', N: '神经质' }
export const dimLabelEn = { O: 'Openness', C: 'Conscientiousness', E: 'Extraversion', A: 'Agreeableness', N: 'Neuroticism' }

export const facetMeta = {
  O_imagination:    { userTranslation: '想象力' },
  O_aesthetics:     { userTranslation: '审美敏感度' },
  // ... 全部 30 个子维度
}
```

---

## 6. 对比计算逻辑

### 6.1 工具函数 `utils/compare.js`

```typescript
interface CompareResult {
  dimDiffs: Array<{
    dim: string
    label: string          // 中文名（从 facetMeta.js 获取）
    myScore: number
    friendScore: number
    diff: number
  }>
  facetDiffs: Array<{
    facet: string
    label: string          // 中文名
    myScore: number
    friendScore: number
    diff: number
  }>
  similarity: number       // 0-100
  summary: string          // 一句话解读，如「你们在宜人性上差异最大(+34)」
  topDiffDim: string       // 差异最大的维度名
}
```

### 6.2 评分规则

| 计算项 | 公式 |
|--------|------|
| 维度/子维度差值 | `diff = myScore - friendScore` |
| 差异排序 | 按 `\|diff\|` 降序 |
| 整体相似度 | `100 - avg(\|diff\| for 5 dims)` |
| 一句话解读 | 取 `\|diff\|` 最大的维度生成 |

### 6.3 无新增 API

对比只需两份 `GET /report/{token}` 的返回值，前端 `compare()` 函数纯计算。

---

## 7. RadarChart 双 series 改造

### 7.1 Props 接口定义（精确契约）

```js
// 当前 props（仅单数据）
props: {
  scores: { type: Object, required: true },    // { t_scores: {...}, facet_scores: {...} }
  lang:   { type: String, default: 'zh' },
}

// 改造后——mode 切换单/双模式
props: {
  mode:         { type: String, default: 'single' },   // 'single' | 'compare'
  myScores:     { type: Object, required: true },       // 你的 t_scores
  friendScores: { type: Object, default: null },        // 对比方 t_scores
  myLabel:      { type: String, default: '你' },
  friendLabel:  { type: String, default: '好友' },
  lang:         { type: String, default: 'zh' },
}
```

### 7.2 双 series 渲染逻辑

```js
const seriesData = []

// 主数据（实线）
seriesData.push({
  name: props.myLabel,
  type: 'radar',
  lineStyle: { width: 2, type: 'solid' },
  areaStyle: { opacity: 0.15, color: '#7B2FF7' },
  data: [props.myScores],
})

// 对比数据（虚线），仅在 compare 模式添加
if (props.mode === 'compare' && props.friendScores) {
  seriesData.push({
    name: props.friendLabel,
    type: 'radar',
    lineStyle: { width: 2, type: 'dashed' },
    areaStyle: { opacity: 0.1, color: '#FF006E' },
    data: [props.friendScores],
  })
}

option.legend = { data: [props.myLabel, props.friendLabel] }
```

### 7.3 向后兼容

```js
// 保留对旧 props 的支持
const effectiveMode = computed(() => {
  if (props.mode === 'compare') return 'compare'
  return 'single'
})
```

---

## 8. i18n 新增键

| key | zh | en | 使用位置 |
|-----|----|----|---------|
| `compare.title` | 性格对比 | Personality Comparison | `ComparePage` 标题 |
| `compare.me` | 你 | Me | 雷达图/柱状图图例 |
| `compare.friend` | 好友 | Friend | 对比对方 |
| `compare.dim_title` | 五大维度 | Big Five Dimensions | 维度对照区块标题 |
| `compare.facet_title` | 差异最大的子维度 | Biggest Facet Differences | 差异列表标题 |
| `compare.similarity` | 整体相似度: {n}% | Overall Similarity: {n}% | 相似度分数 |
| `compare.export` | 导出对比图 | Export Comparison | 导出按钮 |
| `report.friend_badge` | 好友的结果 | Friend's Results | `?friend=1` 报告页标识 |
| `report.friend_prompt` | 你还没测！测一下看看你和好友的性格差异有多大 | You haven't taken the test! See how you compare with your friend | 引导文字 |
| `report.friend_take_test` | 我也要测 → 对比 | Take Test & Compare | 引导按钮 |
| `compare.no_report` | 你没有自己的报告，先去测一个 → | You don't have a report yet, take the test first → | 无效 myToken 引导 |
| `compare.error` | 加载对比数据失败，请确认分享码有效 | Failed to load comparison data, please check share codes | 404/超时 |

---

## 9. 导出对比图

在 `exportCard()` 基础上扩展 `exportCompareCard(container)`：

- 截取对比视图 DOM 区域 → Canvas
- 底部追加二维码（对比页链接）
- 使用 `html2canvas`（已在 `package.json` 和 `exportImage.js` 中使用）不额外引入依赖

---

## 11. 分步实施

| 步骤 | 内容 | 涉及文件 | 预估 |
|------|------|---------|------|
| **P0** | 提取 `utils/facetMeta.js` 共享常量 | `utils/facetMeta.js`, `ResultCard.vue` 改 import | 30min |
| **P1** | 好友报告页 + friendToken 传递 + 问卷回调改造 | `ReportPage.vue`, `QuestionnairePage.vue` | 半天 |
| **P2** | RadarChart 双 series 改造 | `RadarChart.vue` | 半天 |
| **P3** | 对比页 + 差异计算 + CompareView | `ComparePage.vue`, `CompareView.vue`, `utils/compare.js` | 1天 |
| **P4** | 导出对比图 + 二维码 | `utils/exportImage.js` | 半天 |

**建议 P0+P1+P2+P3 一起做**，形成完整闭环：好友查看 → 自己也测 → 自动对比。

---

## 12. 审查修复记录

| 审查问题 | v0.1 问题 | v0.2 修复 |
|----------|-----------|-----------|
| ① friendToken 丢失 | 问卷页回调不知道跳哪个 token 对比 | 跳转问卷时传 `?friendToken=xxx`，提交后读取 |
| ② 404 降级 | 无错误处理 | `ComparePage` 并行 `Promise.all` + 错误状态 |
| ③ ECharts 双 series | 未说明具体改造方式 | 第 7 节详细配置（legend + 双 series + 实线/虚线） |
| ④ 子维度中文名来源 | 未说明 label 从哪里拿 | `utils/facetMeta.js` 共享常量 + `compare.js` 引用 |
| ⑤ 相似度无解读 | 只显示百分比 | 加 `summary` 字段 + 一句话文字解读 |
| ⑥ 对比页无测入口 | 未测用户直接进对比页无引导 | 检测 myToken 有效性，无效则引导去首页 |
| ⑦ html-to-image vs html2canvas | 设计稿写错依赖名 | 修正为 `html2canvas`（已有依赖） |
| ⑧ RadarChart props 未定义 | 接口契约模糊 | §7.1 完整定义 props（mode/myScores/friendScores/myLabel/friendLabel） |
| ⑨ i18n 键未提及 | 10+ key 零提及 | §8 完整中英文对照表 |
| ⑩ 边界状态未设计 | 6 种异常场景无处理 | §3.5 边界状态矩阵（404/重复token/超时/数据缺失） |

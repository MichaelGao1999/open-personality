# 微信小程序全面审查与补全方案

> **执行状态**: 📝 活跃 | 2026-06-24
>
> 基于 miniapp/ 与 frontend/ 全量代码逐文件对比，评估微信小程序版与 Web 版的功能差距，制定分阶段补全计划。

---

## 目标

将 miniapp（uni-app 微信小程序）从当前 MVP（约 60% 功能覆盖）补全至可上线状态，优先修复阻塞性 Bug（P0），再补齐重要体验缺失（P1），最后按需实现增强功能（P2）。

## 当前完成度评估

| 维度 | frontend | miniapp | 覆盖率 |
|------|----------|---------|--------|
| 核心流程（首页→答题→报告） | ✅ 完整 | ✅ 基本可用 | ~90% |
| 报告内容（维度+子维度+MBTI+彩蛋） | ✅ 完整 | ⚠️ 缺子维度+彩蛋 | ~50% |
| i18n 多语言 | ✅ 中英双语包 | ⚠️ 内嵌中文字符串，无切换入口 | ~30% |
| 深色模式 | ✅ 完整 | ❌ 未实现 | 0% |
| 社交功能（对比+分享） | ✅ 对比页+分享链接 | ⚠️ 仅复制分享码，无原生分享，无对比 | ~20% |
| 设置/反馈 | ✅ 设置面板+反馈弹窗 | ❌ 未实现 | 0% |
| **综合** | **100%** | — | **~60%** |

---

## 差距分析

### P0 — 阻塞性 Bug（必须修复，否则无法正常使用）

| # | 问题 | 文件 | 说明 | 难度 |
|---|------|------|------|------|
| 1 | 答案提交格式不兼容 | `miniapp/src/utils/api.js` submitAnswers() | miniapp 提交纯数组 `[1,3,5,...]`，后端 `SubmitRequest` 期望 `[{item_id, value}]` 对象数组。**答题提交会直接 422 报错** | 低 |
| 2 | BASE_URL 硬编码 `127.0.0.1:8000` | `miniapp/src/utils/api.js` | 真机预览时无法访问后端，需改为环境变量或配置文件 | 低 |
| 3 | `urlCheck: true` 域名校验 | `miniapp/src/manifest.json` mp-weixin.setting | 开发阶段本地地址会被拦截，需设为 `false` | 低 |
| 4 | 报告数据字段映射不匹配 | `miniapp/src/pages/report/report.vue` | miniapp 读 `report.scores` / `report.interpretations[key]`，后端返回 `scoring.t_scores` / `interpretations` 为数组非对象。**报告页可能显示空白** | 中 |

### P1 — 重要体验缺失

| # | 缺失功能 | 对标 frontend | 难度 | 说明 |
|---|---------|---------------|------|------|
| 5 | 子维度(Facet)解读展示 | ResultCard.vue 30 子维度柱状图 + 弹窗 | 高 | 需新建 facet 展示区域，读取 `scoring.facet_scores`，包含柱状图和解释弹窗 |
| 6 | 彩蛋模块 | EasterEggBanner.vue 条件触发 + 16 条 | 中 | 读取 `report.easter_egg` 并渲染彩蛋横幅 |
| 7 | 部分提交(Partial Submit) | QuestionnairePage partial 模式 | 中 | 答一部分后查看结果，需添加"查看当前结果"按钮和 partial 提交逻辑 |
| 8 | 维度详情弹窗 | ResultCard openInterpretation() | 中 | 点击维度分数条弹出高/低分解读弹窗，`openInterpretation` 函数已实现但模板未绑定 |
| 9 | 微信原生分享 | ShareLink.vue | 中 | 实现 `onShareAppMessage` 分享报告链接，比复制分享码体验更好 |
| 10 | MBTI 帮助弹窗 i18n | MBTI help modal | 低 | 当前 MBTI 帮助文案硬编码中文，需走 i18n |

### P2 — 增强功能

| # | 缺失功能 | 难度 | 说明 |
|---|---------|------|------|
| 11 | 深色模式 | 高 | CSS 变量切换 + 持久化 + 全页面适配，可借 `wx.getSystemInfo` 获取系统主题 |
| 12 | 语言切换 UI | 中 | 页面内添加切换按钮或设置页 |
| 13 | 双人对比页 | 高 | 新建 compare 页面 + 双人雷达图叠图 + 维度差异计算 |
| 14 | 导出图片/分享海报 | 高 | 无 html2canvas，需 Canvas 手动绘制海报 + `wx.canvasToTempFilePath` |
| 15 | 反馈系统 | 中 | 可用微信客服按钮替代，或新建反馈页调用后端 API |
| 16 | 模式帮助弹窗ⓘ | 低 | 首页模式卡片 ⓘ 图标 + 点击弹窗 |
| 17 | 最近记录"继续答题"按钮 | 低 | 列表项增加续答按钮 |
| 18 | "继续到300题"按钮 | 低 | 最近记录为 speed/standard 模式时显示 |
| 19 | 选项标签优化 | 低 | 5 级量表文字标注嵌入选项按钮内 |
| 20 | 404 错误页 | 低 | 加载失败时显示专门错误页面 |

### 微信小程序特有要求

| 项目 | 状态 | 说明 |
|------|------|------|
| manifest.json 配置 | ⚠️ | appid 已配置，urlCheck 需关闭 |
| pages.json 配置 | ✅ | 3 页面注册正确 |
| `<view>/<text>` 标签 | ✅ | 正确使用小程序原生标签 |
| `uni.request` 网络请求 | ✅ | |
| rpx 适配 | ✅ | 全局使用 rpx |
| 微信原生分享 `onShareAppMessage` | ❌ | 未实现 |
| Canvas 2D API | ✅ | RadarChart 正确使用 |
| DOM 操作规避 | ✅ | 无 document/window 引用 |

### API 调用对比

| API 端点 | frontend | miniapp | 差异 |
|----------|----------|---------|------|
| `GET /questionnaires/items` | ✅ | ✅ | 一致 |
| `POST /questionnaires/submit` | ✅ complete+partial | ✅ 仅 complete（格式还不兼容） | **P0** |
| `GET /questionnaires/resume/{token}` | ✅ | ✅ | 一致 |
| `GET /report/{share_token}` | ✅ | ✅ | 字段映射待确认（P0#4） |
| `GET /i18n/{lang}` | ✅ | ⚠️ 定义未使用 | i18n 用内嵌字符串 |
| `POST /api/feedback` | ✅ | ❌ | P2 |

---

## 方案（分阶段执行）

### 阶段一：P0 Bug 修复（阻塞上线）

修复 4 个阻塞性问题，确保核心流程可跑通。

### 阶段二：P1 体验补全

按优先级补齐子维度、彩蛋、部分提交、弹窗绑定、原生分享等功能。

### 阶段三：P2 增强（按需）

深色模式、语言切换、对比页等高级功能，可根据运营需求取舍。

## 验收标准

- [ ] P0 全部修复：答题提交成功 + 报告页数据正确显示 + 真机可预览
- [ ] P1 全部修复：子维度展示 + 彩蛋 + 部分提交 + 维度弹窗 + 原生分享
- [ ] `uni build mp-weixin` 构建成功
- [ ] 微信开发者工具预览无报错
- [ ] 核心流程走通：首页→选模式→答题→提交→查看报告（含子维度+彩蛋+MBTI）

## 依赖

- 后端 API 无需修改（miniapp 适配后端 schema）
- 微信小程序 appid 已配置
- 真机预览需后端公网可达或开启「不校验合法域名」

## 变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `miniapp/src/utils/api.js` | 修改 | P0#1 修复 submitAnswers 格式 + P0#2 BASE_URL 可配置 |
| `miniapp/src/manifest.json` | 修改 | P0#3 urlCheck 设为 false |
| `miniapp/src/pages/report/report.vue` | 修改 | P0#4 字段映射修复 + P1#5 子维度 + P1#6 彩蛋 + P1#8 弹窗绑定 |
| `miniapp/src/pages/question/question.vue` | 修改 | P1#7 部分提交 + P1#19 选项标签优化 |
| `miniapp/src/pages/index/index.vue` | 修改 | P1#16 模式帮助弹窗 + P1#17 续答按钮 + P1#18 继续300题 |
| `miniapp/src/utils/i18n.js` | 修改 | P1#10 MBTI i18n + 补充缺失 key |
| `miniapp/src/pages/report/report.vue` | 修改 | P1#9 onShareAppMessage 实现 |

## 执行步骤

### 阶段一：P0 Bug 修复

- [ ] Step 1: 修复 `api.js` submitAnswers() — 将答案数组转为 `[{item_id, value}]` 对象数组格式
- [ ] Step 2: `api.js` BASE_URL 改为环境变量 `VITE_API_BASE_URL`，提供默认值和配置说明
- [ ] Step 3: `manifest.json` 中 `mp-weixin.setting.urlCheck` 改为 `false`
- [ ] Step 4: 核对后端 ReportResponse schema，修复 `report.vue` 中字段映射（`scores` → `scoring.t_scores` 等）
- [ ] Step 5: 构建验证 `uni build mp-weixin` + 开发者工具预览核心流程

### 阶段二：P1 体验补全

- [ ] Step 6: report.vue 新增子维度展示区域（30 facet 柱状图 + facetMeta 中文标注）
- [ ] Step 7: report.vue 绑定 openInterpretation 弹窗（维度+子维度点击弹出解读）
- [ ] Step 8: report.vue 新增彩蛋横幅组件（条件触发 + 展开动画）
- [ ] Step 9: question.vue 添加"查看当前结果"按钮 + partial 提交逻辑
- [ ] Step 10: report.vue / question.vue 实现 `onShareAppMessage` 微信原生分享
- [ ] Step 11: i18n.js 补充 MBTI 帮助弹窗文案 + 缺失 key
- [ ] Step 12: 构建验证 + 开发者工具全流程测试

### 阶段三：P2 增强（按需）

- [ ] Step 13: 深色模式（CSS 变量 + 系统主题检测 + 持久化）
- [ ] Step 14: 语言切换 UI + i18n 外部化
- [ ] Step 15: 首页模式帮助弹窗ⓘ + 续答按钮 + 继续300题
- [ ] Step 16: 双人对比页（compare 页面 + 叠图雷达 + 差异计算）
- [ ] Step 17: 分享海报（Canvas 绘制 + canvasToTempFilePath）
- [ ] Step 18: 反馈系统（微信客服或自建页面）

## 风险

| 风险 | 等级 | 应对 |
|------|------|------|
| 后端 ReportResponse 结构与 miniapp 消费方式不匹配 | 高 | Step 4 先核对 schema 再修复，必要时调整后端 |
| 子维度 30 项在小程序中渲染性能 | 中 | 使用虚拟列表或分屏懒加载 |
| 微信原生分享需要配置服务器域名白名单 | 中 | 提前确认域名已备案且在微信后台配置 |
| Canvas 海报绘制兼容性问题 | 中 | 优先使用 `wx.canvasToTempFilePath` 新版 API |
| i18n 内嵌字符串膨胀 | 低 | P2 阶段考虑外部化为 JSON 文件 |

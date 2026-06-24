# 微信小程序版 — 与 Web 版差异文档

> 2026-06-24 新建。记录了 `miniapp/` 与现有 Web 前端的差异点。

## 一、技术栈对照

| 维度 | Web 版 | 小程序版 (uni-app) |
|------|--------|-------------------|
| 框架 | Vue 3 + Vite | uni-app 3.x (Vue 3 + Vite) |
| 路由 | vue-router (history) | pages.json + uni.navigateTo |
| HTTP | axios | uni.request |
| 存储 | localStorage | uni.getStorageSync / setStorageSync |
| 图表 | ECharts (vue-echarts) | Canvas 2D 自绘 |
| 图片导出 | html2canvas | ❌ 不支持（改原生分享） |
| 构建输出 | dist/ | dist/build/mp-weixin/ |
| 调试工具 | DebugDock | ❌ 砍掉 |

## 二、页面映射

| Web 版 | 小程序版 | 状态 |
|--------|---------|------|
| HomePage.vue | pages/index/index.vue | ✅ MVP 完成 |
| QuestionnairePage.vue | pages/question/question.vue | ✅ MVP 完成 |
| ReportPage.vue | pages/report/report.vue | ✅ MVP 完成（缺子维度弹窗绑定） |
| ComparePage.vue | — | ❌ 未实现 |
| ShareCodeInput.vue | 内嵌首页 | ✅ |
| SettingsMenu.vue | — | ❌ 未实现（小程序原生菜单替代） |
| FeedbackModal.vue | — | ❌ 未实现（改微信客服） |
| EasterEggBanner.vue | — | ❌ 未实现 |
| DebugDock.vue | — | ❌ 砍掉 |
| RadarChart.vue | RadarChart.vue (Canvas) | ✅ 重写 |
| ResultCard.vue | — | ❌ 未实现（报告内容直接写在 report.vue） |
| ShareLink.vue | — | ❌ 砍掉（小程序用原生分享） |

## 三、功能差异

### 3.1 已剔除的功能
- **导出图片** — 小程序不支持 html2canvas，改为微信原生截图/分享
- **SettingsMenu** — 主题/语言切换暂未做，后续通过原生菜单或页面内设置页实现
- **飞书双通道反馈** — 改为微信开发者工具自带反馈或微信客服
- **DebugDock** — 小程序调试工具，不影响用户体验
- **Dynamic Island 胶囊动画** — 纯 CSS 效果，小程序精简

### 3.2 简化的功能
- **雷达图** — 从 ECharts 交互式改为 Canvas 2D 静态图，不支持悬停/缩放
- **首页动画** — 取消了 fadeInUp 等入场动画，小程序以性能优先
- **答题转场** — 无切题 slide 动画，直接切换

### 3.3 不完全的功能
- **子维度解读弹窗** — openInterpretation 函数已实现但模板未绑定 @click
- **选项标签** — 5 级量表的文字标注（非常不同意→非常同意）未显示在界面上
- **云端续答** — 代码实现但未充分测试

## 四、已知限制
1. 后端需公网可达（或开启开发者工具「不校验合法域名」）
2. 不支持 DOM 操作（v-html、document、window）
3. CSS 有限制（无 :root、无 * 选择器、无 :hover）
4. 部分 npm 包可能不兼容小程序运行时

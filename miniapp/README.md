# Open Personality - 微信小程序版

基于 uni-app 3.x (Vue 3) 构建的大五人格测评微信小程序。

## 快速开始

```bash
# 安装依赖
npm install

# 开发模式（热更新，需微信开发者工具配合）
npm run dev:mp-weixin

# 构建生产版本
npm run build:mp-weixin
```

## 导入微信开发者工具

1. 打开 **微信开发者工具**
2. 选择 **导入项目**
3. 目录选择 `miniapp/dist/build/mp-weixin/`
4. AppID 自动识别：`wx130f512388ffeb89`
5. 点击导入即可预览

## 项目结构

```
miniapp/
├── src/
│   ├── pages/
│   │   ├── index/index.vue      # 首页（模式选择 + 分享码查询）
│   │   ├── question/question.vue # 答题页（核心流程）
│   │   └── report/report.vue     # 报告页（分数 + 雷达图 + 解读）
│   ├── components/
│   │   └── RadarChart.vue        # Canvas 雷达图组件
│   ├── utils/
│   │   ├── api.js                # 后端 API 封装（uni.request）
│   │   ├── i18n.js               # 国际化（中/英）
│   │   └── facetMeta.js          # 维度元数据
│   ├── App.vue                   # 根组件 + 全局样式
│   ├── main.js                   # 入口
│   ├── pages.json                # 路由配置
│   └── manifest.json             # 应用配置（含 AppID）
├── package.json
└── vite.config.js
```

## 后端地址配置

编辑 `src/utils/api.js` 中的 `BASE_URL` 为你的后端实际地址：

```js
const BASE_URL = 'http://你的服务器地址:8000'
```

## MVP 功能

- ✅ 三种模式选择（极速 30 / 标准 120 / 完整 300）
- ✅ 完整答题流程（逐题作答 + 跳转 + 总览 + 提交）
- ✅ 报告展示（维度分数 + MBTI + Canvas 雷达图）
- ✅ 分享码查询报告
- ✅ 本地进度保存（续答）
- ✅ 中英文切换

## 后续迭代

- [ ] 彩蛋模块
- [ ] 好友对比功能
- [ ] 微信客服反馈
- [ ] 动画/过渡优化

# 前端调试 Dock — 规范文档

> 适用于所有 Vue 3 + Vite 项目。一个固定浮窗，提供页面跳转、测试数据生成、动画调试等开发工具。

---

## 安装方式

### 1. 复制组件

将 `DebugDock.vue` 放入项目的 `src/components/` 目录。

### 2. 注册到 App.vue

```vue
<template>
  <DebugDock />
  <div id="app-root">
    <router-view />
  </div>
</template>

<script setup>
import DebugDock from './components/DebugDock.vue'
</script>
```

### 3. （可选）在 global.css 添加慢速模式支持

```css
body.dd-slow-mo * {
  animation-duration: 3s !important;
  animation-delay: 0s !important;
  transition-duration: 0.9s !important;
}
```

---

## 功能清单

| 分类 | 按钮 | 实现方式 |
|------|------|---------|
| 📍 页面跳转 | 首页 / 各模式答题 / 404 错误页 | `router.push()` |
| 📋 报告页 | 输入分享码跳转 / 生成全3分报告 / 生成极端报告 | `fetch → POST /submit → router.push` |
| 🎲 彩蛋 | 强制触发生成带彩蛋的报告 | 循环提交直到后端返回 `easter_egg` 非空 |
| 🎬 动画 | 慢速模式（放慢 3 倍） | 给 body 加 `.dd-slow-mo` class，CSS 全局覆盖 |
| 🌐 环境 | 切换语言 | 调用 `useI18n().setLang()` |
| 🗃️ 数据 | 清除答题进度 / 清除最近记录 | `localStorage.removeItem()` |

---

## 条件编译

组件始终加载但仅在开发环境显示完整功能的方式：

```vue
<script setup>
// 方式一：通过 Vite 环境变量
const isDev = import.meta.env.DEV
</script>
```

---

## 设计约束

| 约束 | 值 |
|------|-----|
| 定位 | `fixed`，左下角 `20px` |
| 宽度 | 220px |
| 最大高度 | `80vh`，超出滚动 |
| 层级 | `z-index: 9999` |
| 配色 | 深色半透明背景 `rgba(26,26,46,0.92)` + 紫罗兰边框 |
| 折叠态 | 收起为 36px 宽条，只留展开按钮 |

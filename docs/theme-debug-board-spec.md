# 主题调试看板 — 规范文档

> 一个纯 HTML 页面，可视化展示项目的所有设计 Token（颜色、字体、圆角、阴影、按钮、动画）。
> 开发者改完 CSS 变量后刷新即可预览效果。

---

## 安装方式

### 1. 复制文件

将 `theme-debug.html` 放入 `frontend/public/` 目录。

### 2. 访问

```
http://localhost:5173/theme-debug.html
```

> 放在 `public/` 下由 Vite 直接托管，无需注册路由。

---

## 看板展示内容

| 区块 | 展示内容 | 对应 CSS 变量 |
|------|---------|--------------|
| **主色** | 主题色色块 + 色值 | `--color-accent` |
| **五维度色** | 5 个维度色块 + 名称 | `--color-openness` ~ `--color-neuroticism` |
| **表面色** | 背景/卡片/文字/边框色块 | `--color-bg`, `--color-surface`, `--color-text`, `--color-text-secondary`, `--color-border` |
| **渐变** | 彩虹渐变条 | `--gradient-rainbow` |
| **字体** | Display / Body / Mono 三组示例文本 | `--font-display`, `--font-body`, `--font-mono` |
| **圆角** | sm / md / lg / full 四个圆角方块 | `--radius-sm` ~ `--radius-full` |
| **阴影** | sm / md / lg 三个阴影卡片 | `--shadow-sm` ~ `--shadow-lg` |
| **按钮** | 实色按钮 + 描边按钮 | `.dopamine-btn`, `.dopamine-btn-outline` |
| **卡片** | 示例卡片 | `.dopamine-card` |
| **动画** | bounceIn + shimmer 动画演示 | `@keyframes bounceIn`, `@keyframes shimmer` |

---

## 设计规范

### 样式来源

看板通过 `<link rel="stylesheet" href="/src/styles/global.css">` 直接引用项目的主 CSS 文件。

**不要**在看板内复制 CSS 变量值——始终从 `global.css` 读取，确保看板与项目真实效果一致。

### 色值显示

色块下方自动显示对应 CSS 变量的计算后值（通过 JS 读取 `getComputedStyle`）：

```html
<script>
  const style = getComputedStyle(document.documentElement)
  document.getElementById('val-accent').textContent =
    style.getPropertyValue('--color-accent').trim()
</script>
```

### 字体加载

看板通过 Google Fonts 加载项目中使用的字体：

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display...&family=Inter...&family=JetBrains+Mono..." rel="stylesheet">
```

---

## 注意事项

| 事项 | 说明 |
|------|------|
| 构建产物 | `npm run build` 时 Vite 不会处理 `public/` 下的 HTML，保持原样复制 |
| 字体 CDN | 看板依赖 Google Fonts 在线加载，离线环境需要自行托管字体 |
| 路径问题 | CSS 引用路径是 `/src/styles/global.css`，仅在 Vite dev server 下有效 |

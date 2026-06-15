# Lessons Learned

> 跨项目可复用的经验沉淀，避免重复踩坑。

---

## CSS · 弹窗标题居中：绝对定位元素不需不对称 padding

**TAG**: `css`, `modal`, `layout`

**问题**：弹窗标题用 `padding-right: 30px` 想避开右上角的关闭按钮，导致标题视觉上偏左。

**根因**：关闭按钮使用 `position: absolute`，已脱离文档流——它不占据空间，不需要用 padding 来「让开」。不对称 padding 破坏了标题的居中对称性。

**解决方案**：去掉不对称 padding，直接用 `text-align: center` 居中。绝对定位的关闭按钮不会影响文本流。

**适用场景**：任何使用 `position: absolute` 定位的关闭按钮/装饰元素旁的文本居中问题。

---

## CSS · 图标不占位的文本居中：用 absolute 抽离附属元素

**TAG**: `css`, `layout`, `inline-icon`

**问题**：卡片标题文字后加 ⓘ 帮助图标，文字不再居中——图标占据了文本流空间，把文字挤向左侧。

**根因**：inline 元素（图标）跟在文本后，在 `text-align: center` 下，文本+图标整体居中，而非文本单独居中。

**解决方案**：保持标题 `text-align: center`，将图标设为 `position: absolute` 脱离文档流。图标不占位，文字自然居中，图标定位在文字右侧。

```css
.title {
  text-align: center;
  position: relative;
}
.title .icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  margin-left: 4px;
}
```

**适用场景**：标题/标签文字后有附属图标（ⓘ、❓、⏵ 等），要求文字独立居中、图标附在右侧不占位。

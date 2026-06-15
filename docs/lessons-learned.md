# Lessons Learned

> 跨项目可复用的经验沉淀，避免重复踩坑。

---

## CSS · 弹窗标题居中：绝对定位元素不需不对称 padding

**TAG**: `css`, `modal`, `layout`

**问题**：弹窗标题用 `padding-right: 30px` 想避开右上角的关闭按钮，导致标题视觉上偏左。

**根因**：关闭按钮使用 `position: absolute`，已脱离文档流——它不占据空间，不需要用 padding 来「让开」。不对称 padding 破坏了标题的居中对称性。

**解决方案**：去掉不对称 padding，直接用 `text-align: center` 居中。绝对定位的关闭按钮不会影响文本流。

**适用场景**：任何使用 `position: absolute` 定位的关闭按钮/装饰元素旁的文本居中问题。

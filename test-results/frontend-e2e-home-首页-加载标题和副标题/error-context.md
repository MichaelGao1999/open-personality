# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend/e2e/home.spec.ts >> 首页 >> 加载标题和副标题
- Location: frontend/e2e/home.spec.ts:8:3

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test'
  2  | 
  3  | test.describe('首页', () => {
  4  |   test.beforeEach(async ({ page }) => {
> 5  |     await page.goto('/')
     |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  6  |   })
  7  | 
  8  |   test('加载标题和副标题', async ({ page }) => {
  9  |     await expect(page.getByText('Open Personality')).toBeVisible()
  10 |     await expect(page.getByText('大五人格测评')).toBeVisible()
  11 |   })
  12 | 
  13 |   test('三种模式卡片可见', async ({ page }) => {
  14 |     await expect(page.getByText('极速模式')).toBeVisible()
  15 |     await expect(page.getByText('标准模式')).toBeVisible()
  16 |     await expect(page.getByText('完整（高级）')).toBeVisible()
  17 |   })
  18 | 
  19 |   test('选择标准模式 → 卡片高亮', async ({ page }) => {
  20 |     await page.getByText('标准模式').click()
  21 |     await expect(page.getByText('标准模式').locator('..')).toHaveClass(/selected/)
  22 |   })
  23 | 
  24 |   test('开始按钮跳转到答题页', async ({ page }) => {
  25 |     await page.getByText('开始测评').click()
  26 |     await expect(page).toHaveURL(/\/questionnaire/)
  27 |   })
  28 | 
  29 |   test('ⓘ 大五人格解释弹窗', async ({ page }) => {
  30 |     await page.locator('.help-icon').click()
  31 |     await expect(page.getByText('大五人格是什么？')).toBeVisible()
  32 |     await expect(page.getByText('为什么值得你尝试？')).toBeVisible()
  33 |     // 关闭弹窗
  34 |     await page.locator('.modal-overlay').click({ position: { x: 10, y: 10 } })
  35 |     await expect(page.getByText('大五人格是什么？')).not.toBeVisible()
  36 |   })
  37 | 
  38 |   test('模式卡片 ⓘ 弹窗', async ({ page }) => {
  39 |     // 极速模式 ⓘ
  40 |     const smIcons = page.locator('.help-icon-sm')
  41 |     await smIcons.first().click()
  42 |     await expect(page.locator('.modal-card')).toBeVisible()
  43 |     await page.locator('.modal-close').click()
  44 |     await expect(page.locator('.modal-card')).not.toBeVisible()
  45 |   })
  46 | 
  47 |   test('设置菜单开关', async ({ page }) => {
  48 |     await page.locator('.gear-btn').click()
  49 |     await expect(page.getByText('语言')).toBeVisible()
  50 |     await expect(page.getByText('主题')).toBeVisible()
  51 |     // 关闭
  52 |     await page.locator('.sp-backdrop').click()
  53 |     await expect(page.getByText('语言')).not.toBeVisible()
  54 |   })
  55 | 
  56 |   test('深色模式切换', async ({ page }) => {
  57 |     await page.locator('.gear-btn').click()
  58 |     // 找到深色按钮并点击
  59 |     const darkBtn = page.locator('.sp-toggle-btn').last()
  60 |     await darkBtn.click()
  61 |     await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark')
  62 |   })
  63 | 
  64 |   test('语言切换为英文', async ({ page }) => {
  65 |     await page.locator('.gear-btn').click()
  66 |     await page.getByText('EN').click()
  67 |     await expect(page.getByText('Select Mode')).toBeVisible()
  68 |   })
  69 | })
  70 | 
```
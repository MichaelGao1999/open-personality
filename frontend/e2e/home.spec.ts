import { test, expect } from '@playwright/test'

test.describe('首页', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('加载标题和副标题', async ({ page }) => {
    await expect(page.getByText('Open Personality')).toBeVisible()
    await expect(page.getByText('大五人格测评')).toBeVisible()
  })

  test('三种模式卡片可见', async ({ page }) => {
    await expect(page.getByText('极速模式')).toBeVisible()
    await expect(page.getByText('标准模式')).toBeVisible()
    await expect(page.getByText('完整模式')).toBeVisible()
  })

  test('选择标准模式 → 卡片高亮', async ({ page }) => {
    await page.getByText('标准模式').click()
    await expect(page.getByText('标准模式').locator('..')).toHaveClass(/selected/)
  })

  test('开始按钮跳转到答题页', async ({ page }) => {
    await page.getByText('开始测评').click()
    await expect(page).toHaveURL(/\/questionnaire/)
  })

  test('ⓘ 大五人格解释弹窗', async ({ page }) => {
    await page.locator('.help-icon').click()
    await expect(page.getByText('大五人格是什么？')).toBeVisible()
    await expect(page.getByText('为什么值得你尝试？')).toBeVisible()
    // 关闭弹窗
    await page.locator('.modal-overlay').click({ position: { x: 10, y: 10 } })
    await expect(page.getByText('大五人格是什么？')).not.toBeVisible()
  })

  test('模式卡片 ⓘ 弹窗', async ({ page }) => {
    // 极速模式 ⓘ
    const smIcons = page.locator('.help-icon-sm')
    await smIcons.first().click()
    await expect(page.locator('.modal-card')).toBeVisible()
    await page.locator('.modal-close').click()
    await expect(page.locator('.modal-card')).not.toBeVisible()
  })

  test('设置菜单开关', async ({ page }) => {
    await page.locator('.gear-btn').click()
    await expect(page.locator('.settings-panel')).toBeVisible()
    await expect(page.locator('.sp-label').first()).toBeVisible()
    // 关闭
    await page.locator('.sp-backdrop').click()
    await expect(page.locator('.settings-panel')).not.toBeVisible()
  })

  test('深色模式切换', async ({ page }) => {
    await page.locator('.gear-btn').click()
    await expect(page.locator('.settings-panel')).toBeVisible()
    // 找到暗色模式的 SVG 月亮图标按钮（每个 sp-toggle-group 中第三个按钮组里的第二个按钮）
    const darkBtn = page.locator('.sp-row').nth(1).locator('.sp-toggle-btn').nth(1)
    await darkBtn.click()
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark')
  })

  test('语言切换为英文', async ({ page }) => {
    await page.locator('.gear-btn').click()
    await expect(page.locator('.settings-panel')).toBeVisible()
    await page.locator('.sp-row').first().locator('.sp-toggle-btn').nth(1).click()
    // 关闭面板，等待页面文字更新
    await page.locator('.sp-backdrop').click()
    await expect(page.getByText('Start Test')).toBeVisible({ timeout: 5000 })
  })
})

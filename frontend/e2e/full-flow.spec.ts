import { test, expect } from '@playwright/test'

test.describe('全流程 + 报告页', () => {
  test('完整答题流程 → 报告页展示', async ({ page }) => {
    // 1. 首页 → 选择极速模式
    await page.goto('/#/questionnaire?mode=speed')
    await expect(page.locator('.question-card')).toBeVisible({ timeout: 10000 })

    // 2. 完成30题（选答案后自动翻页）
    await expect(page.locator('.question-card')).toBeVisible({ timeout: 10000 })
    for (let i = 0; i < 30; i++) {
      await expect(page.locator('.q-text')).toBeVisible()
      await page.locator('.option-btn').nth(2).click()
      if (i < 29) {
        await page.waitForTimeout(100)
      }
    }

    // 3. 答题总览 → 确认提交
    await expect(page.getByText('提交答案')).toBeVisible({ timeout: 8000 })
    await page.getByText('提交答案').click()
    await expect(page.getByRole('button', { name: '确认提交' })).toBeVisible({ timeout: 5000 })
    await page.getByRole('button', { name: '确认提交' }).click()

    // 4. 等待报告页
    await expect(page).toHaveURL(/\/report\//, { timeout: 20000 })

    // 5. 验证报告页内容
    await expect(page.locator('.card-title')).toBeVisible({ timeout: 10000 })
    await expect(page.locator('.interp-btn')).toBeVisible()
    // 验证五个维度标签
    await expect(page.getByText('开放性')).toBeVisible()
    await expect(page.getByText('严谨性')).toBeVisible()
    await expect(page.getByText('外向性')).toBeVisible()
    await expect(page.getByText('宜人性')).toBeVisible()
    await expect(page.getByText('神经质')).toBeVisible()
  })

  test('报告页 - 维度解读弹窗', async ({ page }) => {
    // 先完成答题获得报告
    await page.goto('/#/questionnaire?mode=speed')
    await expect(page.locator('.question-card')).toBeVisible({ timeout: 10000 })
    for (let i = 0; i < 30; i++) {
      await expect(page.locator('.q-text')).toBeVisible()
      await page.locator('.option-btn').nth(2).click()
      if (i < 29) {
        await page.waitForTimeout(100)
      }
    }
    await page.getByText('提交答案').click()
    await page.getByRole('button', { name: '确认提交' }).click()
    await expect(page).toHaveURL(/\/report\//, { timeout: 20000 })

    // 打开维度解读弹窗
    await expect(page.getByText('维度解读')).toBeVisible({ timeout: 10000 })
    await page.getByText('维度解读').click()
    await expect(page.locator('.interp-panel-item h4').first()).toBeVisible()

    // 验证高分/低分说明存在
    await expect(page.locator('.dim-help-badge.high').first()).toBeVisible()
    await expect(page.locator('.dim-help-badge.low').first()).toBeVisible()

    // 关闭弹窗
    await page.locator('.interp-close').click()
  })

  test('报告页 - 工具栏和设置菜单', async ({ page }) => {
    // 答题获取报告
    await page.goto('/#/questionnaire?mode=speed')
    await expect(page.locator('.question-card')).toBeVisible({ timeout: 10000 })
    for (let i = 0; i < 30; i++) {
      await expect(page.locator('.q-text')).toBeVisible()
      await page.locator('.option-btn').nth(2).click()
      if (i < 29) {
        await page.waitForTimeout(100)
      }
    }
    await page.getByText('提交答案').click()
    await page.getByRole('button', { name: '确认提交' }).click()
    await expect(page).toHaveURL(/\/report\//, { timeout: 20000 })

    // 验证顶部工具栏存在
    await expect(page.locator('.app-toolbar')).toBeVisible()
    await expect(page.getByText('open')).toBeVisible()
    await expect(page.getByText('personality')).toBeVisible()

    // 工具栏齿轮按钮可点击
    await page.locator('.gear-btn').click()
    await expect(page.locator('.sp-label').first()).toBeVisible()
    await page.locator('.sp-backdrop').click()
  })
})

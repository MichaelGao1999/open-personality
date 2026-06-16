import { test, expect } from '@playwright/test'

test.describe('答题页', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/#/questionnaire?mode=speed')
  })

  test('加载题目和进度显示', async ({ page }) => {
    await expect(page.locator('.progress-text')).toBeVisible()
    await expect(page.locator('.progress-bar')).toBeVisible()
    await expect(page.locator('.question-card')).toBeVisible()
  })

  test('进度提示文字可见', async ({ page }) => {
    await expect(page.getByText('无需纠结，凭直觉选择')).toBeVisible()
  })

  test('完成极速模式30题并提交', async ({ page }) => {
    // 等待题目加载完成
    await expect(page.locator('.question-card')).toBeVisible({ timeout: 10000 })
    await expect(page.locator('.q-text')).toBeVisible()

    // 逐题作答（共30题），选答案后自动跳到下一题
    for (let i = 0; i < 30; i++) {
      // 等待当前题目可见
      await expect(page.locator('.q-text')).toBeVisible()

      // 点击第3个选项（中间值）
      await page.locator('.option-btn').nth(2).click()

      // 非最后一题：等待题目文字变化（自动进入下一题）
      if (i < 29) {
        // 短暂等待新题目渲染
        await page.waitForTimeout(100)
      }
    }

    // 最后一题后进入答题总览
    await page.getByText('提交答案').click()

    // 确认弹窗
    await expect(page.getByRole('button', { name: '确认提交' })).toBeVisible({ timeout: 5000 })
    await page.getByRole('button', { name: '确认提交' }).click()

    // 等待跳转到报告页
    await expect(page).toHaveURL(/\/report\//, { timeout: 15000 })
  })

  test('展示答题总览后再提交', async ({ page }) => {
    await expect(page.locator('.question-card')).toBeVisible({ timeout: 10000 })

    // 答完所有题（自动翻页）
    for (let i = 0; i < 30; i++) {
      await expect(page.locator('.q-text')).toBeVisible()
      await page.locator('.option-btn').nth(2).click()
      if (i < 29) {
        await page.waitForTimeout(100)
      }
    }

    // 应该在答题总览页
    await expect(page.getByText('提交答案')).toBeVisible()
  })
})

<template>
  <view class="question-page">
    <!-- 加载状态 -->
    <view v-if="loading" class="loading-state">
      <view class="loading-spinner"></view>
      <text>{{ t('questionnaire.loading') }}</text>
    </view>

    <!-- 答题内容 -->
    <view v-else class="q-content">
      <!-- 进度 -->
      <view class="progress-section">
        <text class="progress-text">
          {{ t('questionnaire.progress') }} {{ currentIndex + 1 }}{{ t('questionnaire.of') }}{{ items.length }}
        </text>
        <view class="progress-bar">
          <view class="progress-fill" :style="{ width: progress + '%' }"></view>
        </view>
      </view>

      <text class="q-hint">{{ t('questionnaire.hint') }}</text>

      <!-- 题目卡片 -->
      <view v-if="!showSummary" class="question-card dopamine-card">
        <text class="q-text">{{ currentItem.text }}</text>
        <view class="options">
          <view
            v-for="(label, idx) in hintLabels"
            :key="idx"
            class="option-btn"
            :class="{ active: answers[currentItem.item_id] === idx + 1 }"
            @click="selectAnswer(currentItem.item_id, idx + 1)"
          >
            <text class="option-value">{{ idx + 1 }}</text>
            <text class="option-label">{{ label }}</text>
          </view>
        </view>

        <view class="nav-buttons">
          <button v-if="currentIndex > 0" class="dopamine-btn-outline" @click="prev">
            <text>{{ t('questionnaire.prev') }}</text>
          </button>
          <view style="flex:1"></view>
          <button class="dopamine-btn-outline partial-btn" @click="viewSummary">
            <text>{{ t('questionnaire.summary_title') }}</text>
          </button>
        </view>
      </view>

      <!-- 答题总览 -->
      <view v-if="showSummary" class="summary-section">
        <text class="summary-title">{{ t('questionnaire.summary_title') }}</text>
        <text class="summary-desc">{{ t('questionnaire.summary_desc') }}</text>

        <scroll-view scroll-y class="summary-grid">
          <view
            v-for="(item, idx) in items"
            :key="item.item_id"
            class="summary-item"
            :class="{ answered: answers[item.item_id] }"
            @click="jumpTo(idx)"
          >
            <text class="summary-num">{{ idx + 1 }}</text>
            <text class="summary-text">{{ item.text }}</text>
            <text v-if="answers[item.item_id]" class="summary-value">{{ answers[item.item_id] }}</text>
            <text v-else class="summary-unanswered">{{ t('questionnaire.summary_unanswered') }}</text>
          </view>
        </scroll-view>

        <view class="summary-footer">
          <text class="stats-answered">{{ answeredCount }}/{{ items.length }}</text>
          <button class="dopamine-btn" :disabled="!allAnswered" @click="confirmSubmit">
            <text>{{ t('questionnaire.summary_submit') }}</text>
          </button>
        </view>
      </view>
    </view>

    <!-- 确认提交弹窗 -->
    <view v-if="showConfirm" class="modal-overlay" @click="showConfirm = false">
      <view class="modal-card" @click.stop>
        <view :style="{ textAlign: 'center' }">
          <text class="modal-title">{{ t('questionnaire.confirm_title') }}</text>
          <text class="modal-body" style="display:block;margin:20rpx 0">{{ t('questionnaire.confirm_body') }}</text>
          <view class="modal-actions" style="display:flex;gap:20rpx;justify-content:center;margin-top:40rpx">
            <button class="dopamine-btn-outline" @click="showConfirm = false">
              <text>{{ t('questionnaire.cancel') }}</text>
            </button>
            <button class="dopamine-btn" @click="submit">
              <text>{{ t('questionnaire.confirm') }}</text>
            </button>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useI18n } from '../../utils/i18n'
import { getItems, submitAnswers, resumeSession } from '../../utils/api'

const { t, getLang } = useI18n()

const STORAGE_KEY = 'open_personality_session'

const items = ref([])
const answers = ref({})
const currentIndex = ref(0)
const sessionId = ref(null)
const loading = ref(true)
const showConfirm = ref(false)
const showSummary = ref(false)
const submitting = ref(false)

const mode = ref('standard')
const resumeToken = ref(null)

const langLabels = {
  zh: ['非常不同意', '不同意', '中立', '同意', '非常同意'],
  en: ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'],
}

const currentItem = computed(() => items.value[currentIndex.value])
const progress = computed(() => ((currentIndex.value + 1) / items.value.length) * 100)
const allAnswered = computed(() => items.value.length > 0 && items.value.every((item) => answers.value[item.item_id]))
const answeredCount = computed(() => items.value.filter((item) => answers.value[item.item_id]).length)
const hintLabels = computed(() => langLabels[getLang()] || langLabels.zh)

onLoad((query) => {
  mode.value = query.mode || 'standard'
  resumeToken.value = query.resume || null
  if (resumeToken.value && resumeToken.value !== 'local') {
    restoreFromCloud(resumeToken.value)
  } else {
    loadItems()
  }
})

async function loadItems() {
  loading.value = true
  try {
    const data = await getItems(mode.value, getLang())
    items.value = data.items || data
    // 尝试恢复本地进度
    restoreFromLocal()
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' })
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function restoreFromCloud(token) {
  loading.value = true
  try {
    const data = await resumeSession(token)
    items.value = data.items || []
    answers.value = data.answers || {}
    sessionId.value = data.session_id
    if (data.current_index !== undefined) {
      currentIndex.value = data.current_index
    }
  } catch (e) {
    uni.showToast({ title: '恢复失败', icon: 'none' })
    await loadItems()
  } finally {
    loading.value = false
  }
}

function restoreFromLocal() {
  try {
    const raw = uni.getStorageSync(STORAGE_KEY)
    if (raw) {
      const data = JSON.parse(raw)
      if (data.mode === mode.value && data.items === items.value.length) {
        answers.value = data.answers || {}
        currentIndex.value = data.currentIndex || 0
        sessionId.value = data.sessionId
      }
    }
  } catch { /* ignore */ }
}

function saveToLocal() {
  try {
    const data = {
      mode: mode.value,
      answers: answers.value,
      currentIndex: currentIndex.value,
      totalItems: items.value.length,
      sessionId: sessionId.value,
      savedAt: Date.now(),
    }
    uni.setStorageSync(STORAGE_KEY, JSON.stringify(data))
  } catch { /* ignore */ }
}

function selectAnswer(itemId, value) {
  answers.value = { ...answers.value, [itemId]: value }
  saveToLocal()
  // 自动跳到下一题（如果不是最后一题）
  if (currentIndex.value < items.value.length - 1) {
    setTimeout(() => { currentIndex.value++ }, 200)
  }
}

function prev() {
  if (currentIndex.value > 0) currentIndex.value--
}

function viewSummary() {
  showSummary.value = true
}

function jumpTo(idx) {
  currentIndex.value = idx
  showSummary.value = false
}

function confirmSubmit() {
  showConfirm.value = true
}

async function submit() {
  if (submitting.value) return
  submitting.value = true
  showConfirm.value = false

  try {
    // Convert answers object to array format
    const answerArray = items.value.map((item) => answers.value[item.item_id] || null)

    const result = await submitAnswers(
      mode.value,
      getLang(),
      answerArray,
      'complete',
      sessionId.value
    )

    // Save to recent reports
    try {
      const shareToken = result.share_token
      const recentRaw = uni.getStorageSync('open_personality_recent')
      let recent = recentRaw ? JSON.parse(recentRaw) : []
      recent = recent.filter(r => r.share_token !== shareToken)
      recent.unshift({ share_token: shareToken, created_at: Date.now(), mode: mode.value })
      uni.setStorageSync('open_personality_recent', JSON.stringify(recent.slice(0, 10)))
    } catch { /* ignore */ }

    // Clear saved session
    uni.removeStorageSync(STORAGE_KEY)

    // Navigate to report
    if (result.share_token) {
      uni.redirectTo({ url: `/pages/report/report?share_token=${result.share_token}` })
    }
  } catch (e) {
    uni.showToast({ title: '提交失败，请重试', icon: 'none' })
    console.error(e)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.question-page {
  min-height: 100vh;
  padding: 40rpx 32rpx;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 200rpx 0;
  color: var(--color-text-secondary);
  font-size: 28rpx;
}

.loading-spinner {
  width: 48rpx;
  height: 48rpx;
  border: 4rpx solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 24rpx;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 进度 */
.progress-section {
  margin-bottom: 24rpx;
}

.progress-text {
  font-size: 24rpx;
  color: var(--color-text-secondary);
  display: block;
  margin-bottom: 12rpx;
}

.progress-bar {
  height: 6rpx;
  background: var(--color-border);
  border-radius: 3rpx;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: 3rpx;
  transition: width 0.3s;
}

.q-hint {
  display: block;
  text-align: center;
  color: var(--color-text-secondary);
  font-size: 24rpx;
  margin-bottom: 32rpx;
}

/* 题目卡片 */
.question-card {
  padding: 40rpx;
  margin-bottom: 32rpx;
}

.q-text {
  font-size: 32rpx;
  font-weight: 500;
  line-height: 1.6;
  display: block;
  margin-bottom: 48rpx;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  margin-bottom: 40rpx;
}

.option-btn {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 24rpx 32rpx;
  border-radius: var(--radius-md);
  border: 2rpx solid var(--color-border);
  transition: all 0.15s;
}

.option-btn:active {
  opacity: 0.7;
}

.option-btn.active {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
}

.option-value {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: var(--color-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: 700;
  color: var(--color-accent);
  flex-shrink: 0;
  text-align: center;
  line-height: 48rpx;
}

.option-btn.active .option-value {
  background: var(--color-accent);
  color: #fff;
}

.option-label {
  font-size: 28rpx;
  color: var(--color-text);
}

.nav-buttons {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.partial-btn {
  font-size: 24rpx !important;
  padding: 16rpx 28rpx !important;
}

/* 答题总览 */
.summary-section {
  padding-top: 20rpx;
}

.summary-title {
  font-size: 36rpx;
  font-weight: 700;
  color: var(--color-accent);
  display: block;
  text-align: center;
  margin-bottom: 12rpx;
}

.summary-desc {
  font-size: 26rpx;
  color: var(--color-text-secondary);
  display: block;
  text-align: center;
  margin-bottom: 32rpx;
}

.summary-grid {
  max-height: 600rpx;
  margin-bottom: 32rpx;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 16rpx 20rpx;
  border-bottom: 1rpx solid var(--color-border);
}

.summary-item:active {
  background: var(--color-accent-light);
}

.summary-num {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  font-weight: 600;
  flex-shrink: 0;
  text-align: center;
  line-height: 48rpx;
}

.summary-item.answered .summary-num {
  background: var(--color-accent-light);
  color: var(--color-accent);
}

.summary-text {
  flex: 1;
  font-size: 24rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary-value {
  width: 40rpx;
  height: 40rpx;
  border-radius: var(--radius-sm);
  background: var(--color-accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
  font-weight: 700;
  flex-shrink: 0;
  text-align: center;
  line-height: 40rpx;
}

.summary-unanswered {
  font-size: 22rpx;
  color: var(--color-text-secondary);
  flex-shrink: 0;
}

.summary-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24rpx;
}

.stats-answered {
  font-size: 26rpx;
  color: var(--color-accent);
  font-weight: 600;
}

.modal-actions button {
  min-width: 200rpx;
}
</style>

<template>
  <view class="home-page">
    <!-- 首屏 -->
    <view class="hero">
      <text class="hero-title">Open Personality</text>
      <text class="hero-subtitle">{{ t('app.subtitle') }}</text>
    </view>

    <!-- 这是什么？ -->
    <view class="what-is-this" @click="showWhatIs = true">
      <text>{{ t('home.what_is_this') }}</text>
    </view>

    <!-- 模式选择 -->
    <view class="mode-select">
      <view
        v-for="m in modes"
        :key="m.key"
        class="mode-card dopamine-card"
        :class="{ selected: selectedMode === m.key }"
        @click="selectedMode = m.key"
      >
        <text class="mode-icon">{{ m.icon }}</text>
        <text class="mode-name">{{ t(m.labelKey) }}</text>
        <text class="mode-desc">{{ t(m.descKey) }}</text>
      </view>
    </view>

    <!-- 开始按钮 -->
    <button class="dopamine-btn start-btn" @click="startTest">
      <text>{{ t('home.start') }}</text>
    </button>

    <!-- 分享码查询 -->
    <view class="divider">
      <view class="divider-line"></view>
      <text class="divider-text">OR</text>
      <view class="divider-line"></view>
    </view>

    <view class="share-row">
      <input
        class="share-input"
        v-model="shareCode"
        :placeholder="t('home.share_code_placeholder')"
      />
      <button class="dopamine-btn-outline share-btn" @click="lookupShareCode">
        <text>{{ t('home.share_code_button') }}</text>
      </button>
    </view>

    <!-- 恢复横幅 -->
    <view v-if="savedSession" class="resume-banner dopamine-card">
      <view class="resume-info">
        <text class="resume-text">{{ t('home.resume_banner') }}</text>
        <text class="resume-detail">{{ savedSession.mode }} · {{ savedSession.answered }}/{{ savedSession.total }}</text>
      </view>
      <view class="resume-actions">
        <button class="dopamine-btn resume-btn" @click="resumeTest">
          <text>{{ t('home.resume_btn') }}</text>
        </button>
        <button class="dopamine-btn-outline dismiss-btn" @click="dismissResume">
          <text>{{ t('home.resume_dismiss') }}</text>
        </button>
      </view>
    </view>

    <!-- 最近记录 -->
    <view class="recent-section" v-if="reports.length">
      <text class="recent-title">{{ t('home.recent_title') }}</text>
      <view
        v-for="r in reports"
        :key="r.share_token"
        class="recent-item dopamine-card"
        @click="viewReport(r.share_token)"
      >
        <text class="recent-code">{{ r.share_token }}</text>
        <text class="recent-date">{{ formatDate(r.created_at) }}</text>
      </view>
    </view>
    <text v-else class="no-recent">{{ t('home.no_recent') }}</text>

    <!-- 大五人格解释弹窗 -->
    <view v-if="showWhatIs" class="modal-overlay" @click="showWhatIs = false">
      <view class="modal-card" @click.stop>
        <view class="modal-close" @click="showWhatIs = false">&times;</view>
        <text class="modal-title">{{ t('home.why_big_title_1') }}</text>
        <text class="modal-body">{{ t('home.why_big_body_1') }}</text>
        <text class="modal-title" style="margin-top: 30rpx">{{ t('home.why_big_title_2') }}</text>
        <text class="modal-body">{{ t('home.why_big_body_2') }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useI18n } from '../../utils/i18n'

const { t, getLang } = useI18n()

const STORAGE_KEY = 'open_personality_session'
const RECENT_KEY = 'open_personality_recent'

const selectedMode = ref('standard')
const shareCode = ref('')
const savedSession = ref(null)
const reports = ref([])
const showWhatIs = ref(false)

const modes = [
  { key: 'speed', icon: '⚡', labelKey: 'home.speed', descKey: 'home.speed_desc' },
  { key: 'standard', icon: '📊', labelKey: 'home.standard', descKey: 'home.standard_desc' },
  { key: 'advanced', icon: '🎯', labelKey: 'home.advanced', descKey: 'home.advanced_desc' },
]

function loadSavedSession() {
  try {
    const raw = uni.getStorageSync(STORAGE_KEY)
    if (raw) {
      const data = JSON.parse(raw)
      const age = Date.now() - (data.savedAt || 0)
      if (age < 7 * 24 * 60 * 60 * 1000) {
        savedSession.value = data
      } else {
        uni.removeStorageSync(STORAGE_KEY)
      }
    }
  } catch { /* ignore */ }
}

function loadRecentReports() {
  try {
    const raw = uni.getStorageSync(RECENT_KEY)
    if (raw) {
      reports.value = JSON.parse(raw).slice(0, 5)
    }
  } catch { reports.value = [] }
}

function saveRecentReport(report) {
  const raw = uni.getStorageSync(RECENT_KEY)
  let list = raw ? JSON.parse(raw) : []
  list = list.filter(r => r.share_token !== report.share_token)
  list.unshift({ share_token: report.share_token, created_at: report.created_at || Date.now(), mode: report.mode })
  uni.setStorageSync(RECENT_KEY, JSON.stringify(list.slice(0, 10)))
}

function startTest() {
  uni.navigateTo({
    url: `/pages/question/question?mode=${selectedMode.value}`,
  })
}

function resumeTest() {
  if (!savedSession.value) return
  const s = savedSession.value
  if (s.share_token) {
    uni.navigateTo({ url: `/pages/question/question?mode=advanced&resume=${s.share_token}` })
  } else {
    uni.navigateTo({ url: `/pages/question/question?mode=${s.mode}&resume=local` })
  }
}

function dismissResume() {
  uni.removeStorageSync(STORAGE_KEY)
  savedSession.value = null
}

function lookupShareCode() {
  const code = shareCode.value.trim()
  if (!code) return
  viewReport(code)
}

function viewReport(shareToken) {
  uni.navigateTo({ url: `/pages/report/report?share_token=${shareToken}` })
}

function formatDate(ts) {
  const d = new Date(ts)
  return `${d.getMonth() + 1}/${d.getDate()}`
}

onShow(() => {
  loadSavedSession()
  loadRecentReports()
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  padding: 100rpx 40rpx 60rpx;
  text-align: center;
}

.hero {
  margin-bottom: 24rpx;
}

.hero-title {
  font-size: 72rpx;
  font-weight: 700;
  letter-spacing: -2rpx;
  color: var(--color-text);
  display: block;
}

.hero-subtitle {
  font-size: 30rpx;
  color: var(--color-text-secondary);
  display: block;
  margin-top: 12rpx;
}

.what-is-this {
  display: inline-block;
  padding: 12rpx 32rpx;
  border-radius: 32rpx;
  border: 2rpx solid var(--color-border);
  color: var(--color-text-secondary);
  font-size: 26rpx;
  font-weight: 600;
  margin-bottom: 48rpx;
}

.mode-select {
  display: flex;
  gap: 16rpx;
  justify-content: center;
  margin-bottom: 48rpx;
}

.mode-card {
  flex: 1;
  max-width: 220rpx;
  padding: 24rpx 16rpx;
  border: 3rpx solid transparent;
  transition: all 0.2s;
}

.mode-card.selected {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 6rpx rgba(123, 47, 247, 0.12);
}

.mode-card:active {
  border-color: var(--color-text-secondary);
}

.mode-icon {
  font-size: 48rpx;
  display: block;
  margin-bottom: 12rpx;
}

.mode-name {
  font-size: 28rpx;
  font-weight: 600;
  display: block;
  margin-bottom: 8rpx;
}

.mode-desc {
  font-size: 22rpx;
  color: var(--color-text-secondary);
  display: block;
}

.start-btn {
  width: 60%;
  margin-bottom: 48rpx;
}

.divider {
  display: flex;
  align-items: center;
  gap: 24rpx;
  margin-bottom: 32rpx;
}

.divider-line {
  flex: 1;
  height: 2rpx;
  background: var(--color-border);
}

.divider-text {
  color: var(--color-text-secondary);
  font-size: 22rpx;
  font-weight: 600;
  letter-spacing: 4rpx;
}

.share-row {
  display: flex;
  gap: 16rpx;
  align-items: center;
  justify-content: center;
  margin-bottom: 40rpx;
}

.share-input {
  flex: 1;
  max-width: 400rpx;
  height: 72rpx;
  padding: 0 24rpx;
  border-radius: var(--radius-md);
  border: 2rpx solid var(--color-border);
  background: var(--color-surface);
  font-size: 26rpx;
}

.share-btn {
  padding: 16rpx 32rpx !important;
  font-size: 24rpx !important;
}

.resume-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
  padding: 20rpx 24rpx;
  margin-bottom: 32rpx;
  border: 3rpx solid var(--color-conscientiousness);
  background: rgba(0, 180, 216, 0.05);
}

.resume-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4rpx;
}

.resume-text {
  font-size: 26rpx;
  font-weight: 500;
}

.resume-detail {
  color: var(--color-text-secondary);
  font-size: 22rpx;
}

.resume-actions {
  display: flex;
  gap: 12rpx;
  flex-shrink: 0;
}

.resume-btn {
  padding: 16rpx 32rpx !important;
  font-size: 24rpx !important;
}

.dismiss-btn {
  padding: 16rpx 24rpx !important;
  font-size: 24rpx !important;
}

.recent-section {
  margin-top: 40rpx;
}

.recent-title {
  font-size: 28rpx;
  font-weight: 600;
  color: var(--color-text-secondary);
  display: block;
  margin-bottom: 24rpx;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 24rpx;
  margin-bottom: 12rpx;
}

.recent-item:active {
  opacity: 0.7;
}

.recent-code {
  font-size: 24rpx;
  font-weight: 600;
  font-family: var(--font-mono);
}

.recent-date {
  font-size: 22rpx;
  color: var(--color-text-secondary);
}

.no-recent {
  color: var(--color-text-secondary);
  font-size: 26rpx;
  display: block;
  margin-top: 40rpx;
}
</style>

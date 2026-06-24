<template>
  <view class="report-page">
    <!-- 加载 -->
    <view v-if="loading" class="loading-state">
      <view class="loading-spinner"></view>
      <text>{{ t('report.loading') }}</text>
    </view>

    <!-- 报告内容 -->
    <scroll-view v-else scroll-y class="report-scroll">
      <!-- 标题 -->
      <view class="report-header">
        <text class="report-title">{{ t('report.title') }}</text>
        <text v-if="report.is_partial" class="partial-badge">{{ t('report.partial_badge') }}</text>
        <text v-if="report.is_partial" class="partial-note">{{ t('report.partial_note') }}</text>
      </view>

      <!-- 雷达图 -->
      <view class="chart-card dopamine-card">
        <text class="section-title">{{ t('report.big_five') }}</text>
        <view class="radar-wrapper">
          <RadarChart :scores="dimScores" :labels="dimLabels" />
        </view>
      </view>

      <!-- 维度分数条 -->
      <view v-for="(dim, idx) in dims" :key="dim.key" class="dim-card dopamine-card">
        <view class="dim-header">
          <text class="dim-label" :style="{ color: dim.color }">{{ dim.label }}</text>
          <text class="dim-score">{{ dim.score }}</text>
        </view>
        <view class="dim-bar-bg">
          <view
            class="dim-bar-fill"
            :style="{
              width: dim.barPercent + '%',
              backgroundColor: dim.color,
            }"
          ></view>
        </view>
        <text class="dim-desc">{{ dim.interpretation }}</text>
      </view>

      <!-- MBTI -->
      <view v-if="mbtiLabel" class="mbti-card dopamine-card" @click="showMbtiHelp = true">
        <text class="section-title">{{ t('report.mbti') }}</text>
        <text class="mbti-result">{{ mbtiLabel }}</text>
        <text class="mbti-probs">{{ mbtiProbs }}</text>
      </view>

      <!-- 分享码 -->
      <view class="share-card dopamine-card">
        <text class="section-title">{{ t('report.share_code_label') }}</text>
        <view class="share-code-row">
          <text class="share-code">{{ shareToken }}</text>
          <button class="dopamine-btn-outline copy-btn" @click="copyShareCode">
            <text>{{ t('report.share') }}</text>
          </button>
        </view>
      </view>

      <!-- 继续答题按钮（部分结果） -->
      <button
        v-if="report.is_partial"
        class="dopamine-btn continue-btn"
        @click="continueTest"
      >
        <text>{{ t('report.continue_test') }}</text>
      </button>

      <!-- 返回首页 -->
      <button class="dopamine-btn-outline home-btn" @click="goHome">
        <text>{{ t('report.back_home') }}</text>
      </button>

      <!-- 维度解读弹窗 -->
      <view v-if="showInterpretation" class="modal-overlay" @click="showInterpretation = false">
        <view class="modal-card" @click.stop>
          <view class="modal-close" @click="showInterpretation = false">&times;</view>
          <text class="modal-title">{{ interpretationTitle }}</text>
          <text class="modal-body" style="display:block">{{ interpretationBody }}</text>
        </view>
      </view>

      <!-- MBTI 帮助弹窗 -->
      <view v-if="showMbtiHelp" class="modal-overlay" @click="showMbtiHelp = false">
        <view class="modal-card" @click.stop>
          <view class="modal-close" @click="showMbtiHelp = false">&times;</view>
          <text class="modal-title">{{ t('report.mbti') }}</text>
          <text class="modal-body" style="display:block">基于大五人格的五个维度分数映射到 MBTI 的四个维度（E/I、S/N、T/F、J/P），输出概率值而非硬性分类。</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useI18n } from '../../utils/i18n'
import { dimColors, dimensionOrder, dimLabel } from '../../utils/facetMeta'
import { getReport } from '../../utils/api'
import RadarChart from '../../components/RadarChart.vue'

const { t, getLang } = useI18n()

const shareToken = ref('')
const loading = ref(true)
const report = ref({})
const showInterpretation = ref(false)
const showMbtiHelp = ref(false)
const interpretationTitle = ref('')
const interpretationBody = ref('')

onLoad((query) => {
  shareToken.value = query.share_token || ''
  if (shareToken.value) {
    fetchReport()
  } else {
    loading.value = false
    uni.showToast({ title: '缺少分享码', icon: 'none' })
  }
})

async function fetchReport() {
  try {
    const data = await getReport(shareToken.value)
    report.value = data
  } catch (e) {
    uni.showToast({ title: '加载报告失败', icon: 'none' })
    console.error(e)
  } finally {
    loading.value = false
  }
}

const isZh = computed(() => getLang() === 'zh')

const dims = computed(() => {
  if (!report.value.scores) return []
  const scores = report.value.scores
  const interpretations = report.value.interpretations || {}

  return dimensionOrder.map((key, idx) => {
    const score = scores[key] || 50
    // t-score 范围 ~20-80，映射到 0-100%
    const barPercent = Math.max(0, Math.min(100, ((score - 20) / 60) * 100))
    const label = isZh.value ? dimLabel[key].zh : dimLabel[key].en
    const interp = interpretations[key]?.body || ''
    return {
      key,
      label,
      score: Math.round(score),
      barPercent,
      color: dimColors[idx],
      interpretation: interp ? (isZh.value ? interp : interpretations[key]?.body_en || interp) : '',
    }
  })
})

const dimScores = computed(() => {
  if (!report.value.scores) return []
  return dimensionOrder.map(key => report.value.scores[key] || 50)
})

const dimLabels = computed(() => {
  return dimensionOrder.map(key => isZh.value ? dimLabel[key].zh : dimLabel[key].en)
})

const mbtiLabel = computed(() => {
  if (!report.value.mbti) return ''
  return report.value.mbti.mbti_type || ''
})

const mbtiProbs = computed(() => {
  if (!report.value.mbti?.probabilities) return ''
  const probs = report.value.mbti.probabilities
  return Object.entries(probs)
    .map(([k, v]) => `${k}: ${Math.round(v * 100)}%`)
    .join(' · ')
})

function openInterpretation(dimKey) {
  const interps = report.value.interpretations || {}
  const data = interps[dimKey]
  if (!data) return
  interpretationTitle.value = isZh.value ? dimLabel[dimKey].zh : dimLabel[dimKey].en
  interpretationBody.value = data.body || ''
  showInterpretation.value = true
}

function copyShareCode() {
  uni.setClipboardData({
    data: shareToken.value,
    success: () => {
      uni.showToast({ title: t('report.share_copied'), icon: 'success' })
    },
  })
}

function continueTest() {
  const mode = report.value.mode || 'advanced'
  uni.redirectTo({
    url: `/pages/question/question?mode=${mode}&resume=${shareToken.value}`,
  })
}

function goHome() {
  uni.reLaunch({ url: '/pages/index/index' })
}
</script>

<style scoped>
.report-page {
  min-height: 100vh;
  background: var(--color-bg);
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

.report-scroll {
  padding: 40rpx 32rpx 80rpx;
}

.report-header {
  text-align: center;
  margin-bottom: 40rpx;
}

.report-title {
  font-size: 40rpx;
  font-weight: 700;
  display: block;
  margin-bottom: 16rpx;
}

.partial-badge {
  display: inline-block;
  padding: 6rpx 20rpx;
  border-radius: var(--radius-full);
  background: var(--color-accent-light);
  color: var(--color-accent);
  font-size: 22rpx;
  font-weight: 600;
  margin-bottom: 12rpx;
}

.partial-note {
  display: block;
  font-size: 24rpx;
  color: var(--color-text-secondary);
}

/* 雷达图 */
.chart-card {
  padding: 32rpx;
  margin-bottom: 24rpx;
}

.radar-wrapper {
  width: 100%;
  height: 500rpx;
  margin-top: 16rpx;
}

.section-title {
  font-size: 28rpx;
  font-weight: 600;
  color: var(--color-text-secondary);
  display: block;
  margin-bottom: 16rpx;
}

/* 维度分数 */
.dim-card {
  margin-bottom: 20rpx;
  padding: 24rpx;
}

.dim-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.dim-label {
  font-size: 30rpx;
  font-weight: 700;
}

.dim-score {
  font-size: 36rpx;
  font-weight: 700;
}

.dim-bar-bg {
  height: 16rpx;
  background: var(--color-border);
  border-radius: 8rpx;
  overflow: hidden;
  margin-bottom: 12rpx;
}

.dim-bar-fill {
  height: 100%;
  border-radius: 8rpx;
  transition: width 0.6s ease;
}

.dim-desc {
  font-size: 24rpx;
  color: var(--color-text-secondary);
  display: block;
  line-height: 1.6;
}

/* MBTI */
.mbti-card {
  padding: 32rpx;
  margin-bottom: 24rpx;
  text-align: center;
}

.mbti-result {
  font-size: 48rpx;
  font-weight: 700;
  color: var(--color-accent);
  display: block;
  margin: 16rpx 0;
}

.mbti-probs {
  font-size: 24rpx;
  color: var(--color-text-secondary);
  display: block;
}

/* 分享 */
.share-card {
  padding: 24rpx;
  margin-bottom: 32rpx;
}

.share-code-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16rpx;
}

.share-code {
  font-size: 28rpx;
  font-weight: 600;
  font-family: var(--font-mono);
  color: var(--color-accent);
}

.copy-btn {
  padding: 12rpx 28rpx !important;
  font-size: 22rpx !important;
}

.continue-btn {
  width: 100%;
  margin-bottom: 20rpx;
}

.home-btn {
  width: 100%;
}
</style>

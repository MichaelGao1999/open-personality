<template>
  <div class="report-page">
    <LanguageSwitch />

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>{{ t('report.title') }}...</p>
    </div>

    <template v-if="!loading && report">
      <div class="report-header">
        <!-- 部分结果徽标 -->
        <div v-if="isPartial" class="partial-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
          </svg>
          {{ t('report.partial_badge') }}
        </div>
        <h2 class="report-title" :class="{ 'gradient-text': !isPartial }">
          {{ t('report.title') }}
        </h2>
        <p v-if="isPartial" class="partial-progress">
          {{ t('report.partial_progress', { answered: report.answered_count, total: report.total_items }) }}
        </p>
        <p v-if="isPartial" class="partial-note">
          {{ t('report.partial_note') }}
        </p>
      </div>

      <ResultCard :report="report" ref="resultCardRef" />

      <div class="interpretations">
        <h3 class="section-title">{{ t('report.interpretation') }}</h3>
        <div
          v-for="(interp, idx) in report.interpretations.slice(0, 5)"
          :key="interp.dimension"
          class="interp-item dopamine-card"
          :style="{ '--accent': interpColors[idx] }"
        >
          <div class="interp-accent"></div>
          <div class="interp-content">
            <h4>{{ report.lang === 'zh' ? interp.title_zh : interp.title_en }}</h4>
            <p>{{ report.lang === 'zh' ? interp.body_zh : interp.body_en }}</p>
          </div>
        </div>
      </div>

      <EasterEggBanner v-if="report.easter_egg" :text="report.easter_egg" />

      <div class="actions">
        <!-- 部分结果的继续答题按钮 -->
        <button v-if="isPartial" class="dopamine-btn continue-btn" @click="continueTest">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
          {{ t('report.continue_test') }}
        </button>

        <button class="dopamine-btn" :class="{ 'dopamine-btn-outline': isPartial }" @click="exportImage">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>
          </svg>
          {{ t('report.export') }}
        </button>
        <ShareLink :share-token="report.share_token" />
        <router-link to="/" class="back-link dopamine-btn-outline">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          {{ t('report.back_home') }}
        </router-link>
      </div>
    </template>

    <div v-if="!loading && error" class="not-found">
      <div class="not-found-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF006E" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M16 16s-1.5-2-4-2-4 2-4 2M9 9h.01M15 9h.01"/>
        </svg>
      </div>
      <h2>{{ t('report.not_found') }}</h2>
      <p>{{ t('report.not_found_desc') }}</p>
      <router-link to="/" class="dopamine-btn">
        {{ t('report.back_home') }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { getReport } from '../utils/api'
import { exportCard } from '../utils/exportImage'
import LanguageSwitch from '../components/LanguageSwitch.vue'
import ResultCard from '../components/ResultCard.vue'
import EasterEggBanner from '../components/EasterEggBanner.vue'
import ShareLink from '../components/ShareLink.vue'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const report = ref(null)
const loading = ref(true)
const error = ref(false)
const resultCardRef = ref(null)

const interpColors = ['#7B2FF7', '#00B4D8', '#FFD60A', '#06D6A0', '#FF006E']

const isPartial = computed(() => route.query.partial === '1')

async function fetchReport() {
  const token = route.params.token
  if (!token) {
    loading.value = false
    return
  }
  try {
    const res = await getReport(token)
    report.value = res.data
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
}

async function exportImage() {
  if (resultCardRef.value?.cardRef) {
    await exportCard(resultCardRef.value.cardRef)
  }
}

function continueTest() {
  // 从部分结果继续答题
  const mode = route.query.mode || report.value?.mode || 'standard'
  router.push({
    path: '/questionnaire',
    query: { mode, resume: 'local' },
  })
}

onMounted(() => {
  const token = route.params.token
  if (token) {
    fetchReport()
  } else {
    loading.value = false
    error.value = true
  }
})
</script>

<style scoped>
.report-page {
  max-width: 680px;
  margin: 0 auto;
  padding: 80px 20px 60px;
  position: relative;
  z-index: 1;
}

.loading {
  text-align: center;
  padding: 120px 0;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-neuroticism);
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.report-header {
  text-align: center;
  margin-bottom: 32px;
  animation: fadeInUp 0.5s var(--ease-bounce);
}

.report-title {
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 700;
}

.partial-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  border-radius: var(--radius-full);
  background: rgba(0, 180, 216, 0.1);
  border: 1px solid var(--color-conscientiousness);
  color: var(--color-conscientiousness);
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 12px;
}

.partial-progress {
  color: var(--color-text-secondary);
  font-size: 15px;
  margin-top: 8px;
}

.partial-note {
  color: var(--color-text-secondary);
  font-size: 13px;
  margin-top: 4px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
}

.interpretations {
  margin-top: 32px;
  animation: fadeInUp 0.5s var(--ease-bounce) 0.2s both;
}

.interp-item {
  display: flex;
  padding: 0;
  margin-bottom: 12px;
  overflow: hidden;
  border: 2px solid var(--color-border);
}

.interp-accent {
  width: 5px;
  background: var(--accent);
  flex-shrink: 0;
}

.interp-content {
  padding: 16px 20px;
  flex: 1;
}

.interp-content h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--accent);
}

.interp-content p {
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
  margin-top: 40px;
  animation: fadeInUp 0.5s var(--ease-bounce) 0.4s both;
}

.continue-btn {
  background: linear-gradient(135deg, #00B4D8, #7B2FF7);
  box-shadow: 0 4px 16px rgba(0, 180, 216, 0.3);
}

.back-link {
  text-decoration: none;
}

.not-found {
  text-align: center;
  padding: 80px 0;
  animation: fadeInUp 0.5s var(--ease-bounce);
}

.not-found-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 0, 110, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
}

.not-found h2 {
  font-size: 24px;
  margin-bottom: 8px;
}

.not-found p {
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}
</style>

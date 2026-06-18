<template>
  <div class="report-page">

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>{{ t('report.title') }}...</p>
    </div>

    <template v-if="!loading && report">
      <div class="report-header">
        <div v-if="isPartial" class="partial-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
          </svg>
          {{ t('report.partial_badge') }}
        </div>
        <h2 class="report-title gradient-text">{{ t('report.title') }}</h2>
        <span v-if="isFriend" class="friend-badge">{{ t('report.friend_badge') }}</span>
        <p v-if="isPartial" class="partial-progress">
          {{ t('report.partial_progress', { answered: report.answered_count, total: report.total_items }) }}
        </p>
        <p v-if="isPartial" class="partial-note">{{ t('report.partial_note') }}</p>
      </div>

      <ResultCard :report="report" ref="resultCardRef" />

      <div class="actions">
        <button v-if="isPartial" class="dopamine-btn" @click="continueTest">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
          {{ t('report.continue_test') }}
        </button>

        <button class="dopamine-btn" @click="exportImage">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>
          </svg>
          {{ t('report.export') }}
        </button>
        <ShareLink :share-token="report.share_token" />

      </div>

      <div v-if="isFriend" class="friend-cta">
        <p class="friend-prompt">{{ t('report.friend_prompt') }}</p>
        <div class="friend-cta-actions">
          <button class="dopamine-btn start-btn" @click="continueTest">
            {{ t('report.friend_take_test') }}
          </button>
          <button
            v-if="reports.length > 0"
            class="dopamine-btn-outline compare-now-btn"
            @click="compareNow"
          >
            {{ t('report.compare_now') }}
          </button>
        </div>
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
      <router-link to="/" class="dopamine-btn">{{ t('report.back_home') }}</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { getReport } from '../utils/api'
import { exportCard } from '../utils/exportImage'
import { useRecentReports } from '../composables/useRecentReports'
import ResultCard from '../components/ResultCard.vue'
import ShareLink from '../components/ShareLink.vue'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const report = ref(null)
const loading = ref(true)
const error = ref(false)
const resultCardRef = ref(null)

const isPartial = computed(() => route.query.partial === '1')
const { reports } = useRecentReports()
const isFriend = computed(() => {
  const token = route.params.token
  if (!token) return false
  return !reports.some(r => r.share_token === token)
})

async function fetchReport() {
  const token = route.params.token
  if (!token) { loading.value = false; return }
  try {
    const res = await getReport(token)
    report.value = res.data
  } catch { error.value = true }
  finally { loading.value = false }
}

async function exportImage() {
  const card = resultCardRef.value
  if (!card?.cardRef) return
  await exportCard(card.cardRef)
}

function continueTest() {
  const query = { mode: 'advanced', resume: report.value.share_token }
  if (isFriend.value) {
    query.friendToken = route.params.token
  }
  router.push({ path: '/questionnaire', query })
}

function compareNow() {
  router.push(`/compare/${reports[0].share_token}/${route.params.token}`)
}

onMounted(() => {
  const token = route.params.token
  if (token) fetchReport()
  else { loading.value = false; error.value = true }
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
.loading { text-align: center; padding: 120px 0; }
.loading-spinner {
  width: 48px; height: 48px; border: 4px solid var(--color-border);
  border-top-color: var(--color-neuroticism); border-radius: 50%;
  margin: 0 auto 16px; animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.report-header { text-align: center; margin-bottom: 32px; animation: fadeInUp 0.8s var(--ease-bounce); }
.report-title { font-family: var(--font-display); font-size: 36px; font-weight: 700; }
.partial-badge {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px;
  border-radius: var(--radius-full); background: rgba(0, 180, 216, 0.1);
  border: 1px solid var(--color-conscientiousness); color: var(--color-conscientiousness);
  font-size: 13px; font-weight: 600; margin-bottom: 12px;
  animation: fadeInUp 0.6s var(--ease-bounce) 0.15s both;
}
.partial-progress { color: var(--color-text-secondary); font-size: 15px; margin-top: 8px; }
.partial-note { color: var(--color-text-secondary); font-size: 13px; margin-top: 4px; }
.friend-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  background: var(--color-accent-light);
  color: var(--color-accent);
  font-size: 12px;
  font-weight: 600;
  margin-left: 8px;
  vertical-align: middle;
}
.friend-cta {
  margin-top: 32px;
  padding: 24px;
  border-radius: var(--radius-md);
  background: var(--color-accent-light);
  text-align: center;
  animation: fadeInUp 0.8s var(--ease-bounce) 0.6s both;
}
.friend-prompt {
  font-size: 16px;
  font-weight: 500;
  color: var(--color-accent);
  margin-bottom: 16px;
  line-height: 1.5;
}
.friend-cta-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}
.compare-now-btn {
  padding: 16px 32px;
  font-size: 16px;
}
.actions { display: flex; flex-direction: column; gap: 12px; align-items: center; margin-top: 40px; animation: fadeInUp 0.8s var(--ease-bounce) 0.6s both; }
.not-found { text-align: center; padding: 80px 0; animation: fadeInUp 0.5s var(--ease-bounce); }
.not-found-icon {
  width: 80px; height: 80px; border-radius: 50%;
  background: rgba(255, 0, 110, 0.1); display: flex; align-items: center;
  justify-content: center; margin: 0 auto 24px;
}

/* 加载态→内容过渡 */
.fade-enter-active { transition: opacity 0.25s ease; }
.fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }

.not-found h2 { font-size: 24px; margin-bottom: 8px; }
.not-found p { color: var(--color-text-secondary); margin-bottom: 24px; }

/* ═══════════════════════════════════════════
   Responsive: mobile < 520px
   ═══════════════════════════════════════════ */
@media (max-width: 520px) {
  .report-page {
    padding: 60px 16px 40px;
  }

  .report-title {
    font-size: 30px;
  }
}
</style>

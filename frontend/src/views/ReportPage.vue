<template>
  <div class="report-page">
    <LanguageSwitch />

    <div v-if="loading" class="loading">{{ t('report.title') }}...</div>

    <template v-if="!loading && report">
      <div class="report-header">
        <h2>{{ t('report.title') }}</h2>
      </div>

      <ResultCard :report="report" ref="resultCardRef" />

      <div class="interpretations">
        <h3>{{ t('report.interpretation') }}</h3>
        <div v-for="interp in report.interpretations.slice(0, 5)" :key="interp.dimension" class="interp-item">
          <h4>{{ report.lang === 'zh' ? interp.title_zh : interp.title_en }}</h4>
          <p>{{ report.lang === 'zh' ? interp.body_zh : interp.body_en }}</p>
        </div>
      </div>

      <EasterEggBanner v-if="report.easter_egg" :text="report.easter_egg" />

      <div class="actions">
        <button @click="exportImage">{{ t('report.export') }}</button>
        <ShareLink :share-token="report.share_token" />
        <router-link to="/" class="back-link">{{ t('report.back_home') }}</router-link>
      </div>
    </template>

    <div v-if="!loading && error" class="not-found">
      <h2>{{ t('report.not_found') }}</h2>
      <p>{{ t('report.not_found_desc') }}</p>
      <router-link to="/">{{ t('report.back_home') }}</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { getReport } from '../utils/api'
import { exportCard } from '../utils/exportImage'
import LanguageSwitch from '../components/LanguageSwitch.vue'
import ResultCard from '../components/ResultCard.vue'
import EasterEggBanner from '../components/EasterEggBanner.vue'
import ShareLink from '../components/ShareLink.vue'

const { t } = useI18n()
const route = useRoute()
const report = ref(null)
const loading = ref(true)
const error = ref(false)
const resultCardRef = ref(null)

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
.report-page { max-width: 640px; margin: 0 auto; padding: 60px 16px; }
.report-header { text-align: center; margin-bottom: 24px; }
.loading { text-align: center; padding: 80px 0; font-size: 18px; color: #666; }
.interpretations { margin-top: 24px; }
.interpretations h3 { margin-bottom: 16px; }
.interp-item { background: #f9f9f9; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; }
.interp-item h4 { margin: 0 0 4px; font-size: 15px; }
.interp-item p { margin: 0; color: #555; font-size: 14px; line-height: 1.5; }
.actions { display: flex; flex-direction: column; gap: 12px; align-items: center; margin-top: 24px; }
.actions button {
  padding: 10px 24px; background: #4a90d9; color: #fff;
  border: none; border-radius: 6px; cursor: pointer; font-size: 14px;
}
.back-link { color: #4a90d9; text-decoration: none; font-size: 14px; }
.not-found { text-align: center; padding: 80px 0; }
.not-found h2 { margin-bottom: 8px; }
.not-found p { color: #666; margin-bottom: 16px; }
</style>

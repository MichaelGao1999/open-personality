<template>
  <div ref="cardRef" class="result-card">
    <h2>{{ t('report.title') }}</h2>
    <RadarChart :scores="report.scoring" :lang="report.lang" />
    <div class="mbti-section">
      <h3>{{ t('report.mbti') }}: {{ report.mbti.type_code }}</h3>
      <div class="mbti-dims">
        <span v-for="dim in report.mbti.dimensions" :key="dim.label_a + dim.label_b" class="mbti-dim">
          {{ dim.label_a }}{{ (dim.prob_a * 100).toFixed(0) }}% / {{ dim.label_b }}{{ (dim.prob_b * 100).toFixed(0) }}%
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from '../composables/useI18n'
import RadarChart from './RadarChart.vue'

const props = defineProps({
  report: { type: Object, required: true },
})

const { t } = useI18n()
const cardRef = ref(null)

defineExpose({ cardRef })
</script>

<style scoped>
.result-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  max-width: 600px;
  margin: 0 auto;
}
.mbti-section { margin-top: 16px; text-align: center; }
.mbti-dims { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 8px; }
.mbti-dim { background: #f0f4f8; padding: 4px 12px; border-radius: 16px; font-size: 14px; }
</style>

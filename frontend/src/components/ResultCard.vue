<template>
  <div ref="cardRef" class="result-card dopamine-card">
    <div class="card-top-border"></div>
    <h2 class="card-title">{{ t('report.title') }}</h2>

    <RadarChart :scores="report.scoring" :lang="report.lang" />

    <div class="mbti-section">
      <h3 class="mbti-title">{{ t('report.mbti') }}</h3>
      <div class="mbti-code">{{ report.mbti.type_code }}</div>
      <div class="mbti-dims">
        <span
          v-for="(dim, index) in report.mbti.dimensions"
          :key="dim.label_a + dim.label_b"
          class="mbti-dim"
          :style="{ background: dimColors[index % dimColors.length] }"
        >
          <span class="dim-label">{{ dim.label_a }}</span>
          <span class="dim-value">{{ (dim.prob_a * 100).toFixed(0) }}%</span>
        </span>
      </div>
    </div>

    <div class="scores-section">
      <div
        v-for="(dim, key) in dimensionOrder"
        :key="key"
        class="score-item"
      >
        <div class="score-header">
          <span class="score-label">{{ dimLabels[key] }}</span>
          <span class="score-value" :style="{ color: dimColors[dimensionOrder.indexOf(dim)] }">
            {{ getScore(key) }}
          </span>
        </div>
        <div class="score-bar-container">
          <div
            class="score-bar"
            :style="{
              width: getScore(key) + '%',
              background: dimColors[dimensionOrder.indexOf(dim)]
            }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import RadarChart from './RadarChart.vue'

const props = defineProps({
  report: { type: Object, required: true },
})

const { t } = useI18n()
const cardRef = ref(null)

const dimColors = [
  '#7B2FF7', // Openness - 亮紫
  '#00B4D8', // Conscientiousness - 电光蓝
  '#FFD60A', // Extraversion - 阳光黄
  '#06D6A0', // Agreeableness - 翡翠绿
  '#FF006E', // Neuroticism - 热力粉
]

const dimensionOrder = ['O', 'C', 'E', 'A', 'N']

const dimLabels = {
  O: t('report.openness') || '开放性',
  C: t('report.conscientiousness') || '严谨性',
  E: t('report.extraversion') || '外向性',
  A: t('report.agreeableness') || '宜人性',
  N: t('report.neuroticism') || '神经质',
}

function getScore(dim) {
  return Math.round(props.report.scoring?.t_scores?.[dim] ?? props.report.scoring?.[dim] ?? 50)
}

defineExpose({ cardRef })
</script>

<style scoped>
.result-card {
  max-width: 640px;
  margin: 0 auto;
  padding: 0;
  overflow: hidden;
  border: 2px solid var(--color-border);
  animation: bounceIn 0.6s var(--ease-bounce);
}

.card-top-border {
  height: 6px;
  background: var(--color-accent);
}

.card-title {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text);
  text-align: center;
  margin: 24px 0;
  letter-spacing: 0.5px;
}

.mbti-section {
  margin: 0 24px;
  text-align: center;
  padding: 20px;
  background: rgba(123, 47, 247, 0.05);
  border-radius: var(--radius-md);
  border: 1px solid rgba(123, 47, 247, 0.1);
}

.mbti-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.mbti-code {
  font-family: var(--font-mono);
  font-size: 32px;
  font-weight: 700;
  color: var(--color-accent);
  margin-bottom: 16px;
}

.mbti-dims {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.mbti-dim {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 16px;
  border-radius: var(--radius-full);
  color: #fff;
  min-width: 72px;
  transition: transform 0.25s var(--ease-bounce);
}

.mbti-dim:hover {
  transform: scale(1.08);
}

.dim-label {
  font-size: 11px;
  font-weight: 500;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.dim-value {
  font-family: var(--font-mono);
  font-size: 18px;
  font-weight: 700;
}

.scores-section {
  padding: 24px;
}

.score-item {
  margin-bottom: 20px;
}

.score-item:last-child {
  margin-bottom: 0;
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.score-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
}

.score-value {
  font-family: var(--font-mono);
  font-size: 18px;
  font-weight: 700;
}

.score-bar-container {
  height: 10px;
  background: var(--color-border);
  border-radius: 5px;
  overflow: hidden;
}

.score-bar {
  height: 100%;
  border-radius: 5px;
  transition: width 0.8s var(--ease-bounce);
  position: relative;
}

.score-bar::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shimmer 2s linear infinite;
}
</style>

<template>
  <div ref="compareRef" class="compare-view">
    <!-- 雷达图双人对比 -->
    <RadarChart
      :scores="myReport.scoring"
      :friend-scores="friendReport.scoring"
      :friend-label="t('compare.friend')"
      :lang="myReport.lang"
    />

    <!-- 五大维度对比 -->
    <div class="compare-section">
      <h3 class="section-title">{{ t('compare.dim_title') }}</h3>
      <div class="dim-rows">
        <div v-for="d in result.dimDiffs" :key="d.dim" class="dim-row">
          <div class="dim-label">{{ d.label }}</div>
          <div class="dim-bars">
            <div class="bar-group">
              <span class="bar-label me">{{ t('compare.me') }}</span>
              <div class="bar-track">
                <div
                  class="bar-fill me-fill"
                  :style="{ width: Math.max(d.myScore, 2) + '%', backgroundColor: dimColor(d.dim) }"
                ></div>
              </div>
              <span class="bar-value">{{ d.myScore }}</span>
            </div>
            <div class="bar-group">
              <span class="bar-label friend-label-bar">{{ t('compare.friend') }}</span>
              <div class="bar-track">
                <div
                  class="bar-fill friend-fill"
                  :style="{ width: Math.max(d.friendScore, 2) + '%', backgroundColor: dimColor(d.dim) }"
                ></div>
              </div>
              <span class="bar-value">{{ d.friendScore }}</span>
            </div>
          </div>
          <div class="dim-diff" :class="d.diff > 0 ? 'diff-positive' : 'diff-negative'">
            {{ d.diff > 0 ? '+' : '' }}{{ d.diff }}
          </div>
        </div>
      </div>
    </div>

    <!-- 差异最大的子维度 -->
    <div v-if="result.facetDiffs.length" class="compare-section">
      <h3 class="section-title">{{ t('compare.facet_title') }}</h3>
      <div class="facet-rows">
        <div v-for="f in result.facetDiffs.slice(0, 8)" :key="f.key" class="facet-row">
          <span class="facet-diff-icon" :class="f.diff > 0 ? 'icon-up' : 'icon-down'">
            {{ f.diff > 0 ? '▲' : '▼' }}
          </span>
          <span class="facet-label">{{ f.label }}</span>
          <span class="facet-scores">
            <span class="me-score">{{ f.myScore }}</span>
            <span class="vs">vs</span>
            <span class="friend-score">{{ f.friendScore }}</span>
          </span>
          <span class="facet-diff-val" :class="f.diff > 0 ? 'diff-positive' : 'diff-negative'">
            {{ f.diff > 0 ? '+' : '' }}{{ f.diff }}
          </span>
        </div>
      </div>
    </div>

    <!-- 整体相似度 -->
    <div class="similarity-section">
      <div class="similarity-ring">
        <svg viewBox="0 0 100 100" class="similarity-svg">
          <circle cx="50" cy="50" r="42" stroke="var(--color-border)" stroke-width="8" fill="none" />
          <circle
            cx="50" cy="50" r="42"
            stroke="url(#simGrad)"
            stroke-width="8"
            fill="none"
            stroke-linecap="round"
            :stroke-dasharray="result.similarity * 2.64 + ', 264'"
            transform="rotate(-90 50 50)"
          />
          <defs>
            <linearGradient id="simGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#7B2FF7" />
              <stop offset="100%" stop-color="#06D6A0" />
            </linearGradient>
          </defs>
        </svg>
        <div class="similarity-text">
          <span class="similarity-value">{{ result.similarity }}%</span>
          <span class="similarity-label">{{ t('compare.similarity', { n: result.similarity }) }}</span>
        </div>
      </div>
    </div>

    <!-- 导出按钮 -->
    <button class="dopamine-btn export-compare-btn" @click="handleExport">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>
      </svg>
      {{ t('compare.export') }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import { compare } from '../utils/compare.js'
import { dimColors } from '../utils/facetMeta.js'
import { exportCompareCard } from '../utils/exportImage.js'
import RadarChart from './RadarChart.vue'

const props = defineProps({
  myReport: { type: Object, required: true },
  friendReport: { type: Object, required: true },
})

const { t } = useI18n()
const compareRef = ref(null)

const result = computed(() => compare(props.myReport, props.friendReport, props.myReport.lang))

function dimColor(dim) {
  const order = { O: 0, C: 1, E: 2, A: 3, N: 4 }
  return dimColors[order[dim]] || '#7B2FF7'
}

async function handleExport() {
  if (!compareRef.value) return
  await exportCompareCard(compareRef.value)
}
</script>

<style scoped>
.compare-view {
  max-width: 680px;
  margin: 0 auto;
  animation: fadeInUp 0.6s var(--ease-bounce);
}

.compare-section {
  margin-top: 32px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--color-text);
}

/* ---- 维度对比条 ---- */
.dim-rows {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dim-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dim-label {
  width: 60px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
  flex-shrink: 0;
}

.dim-bars {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bar-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.bar-label {
  font-size: 11px;
  width: 22px;
  flex-shrink: 0;
  color: var(--color-text-secondary);
}

.bar-label.me {
  color: #7B2FF7;
}

.bar-label.friend-label-bar {
  color: #FF006E;
}

.bar-track {
  flex: 1;
  height: 10px;
  border-radius: 5px;
  background: var(--color-bg);
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 5px;
  transition: width 0.6s var(--ease-bounce);
}

.me-fill {
  opacity: 0.85;
}

.friend-fill {
  opacity: 0.6;
}

.bar-value {
  width: 28px;
  font-size: 12px;
  font-weight: 600;
  text-align: right;
  flex-shrink: 0;
}

.dim-diff {
  width: 40px;
  font-size: 14px;
  font-weight: 700;
  text-align: right;
  flex-shrink: 0;
}

.diff-positive {
  color: var(--color-agreeableness);
}

.diff-negative {
  color: var(--color-neuroticism);
}

/* ---- 子维度差异列表 ---- */
.facet-rows {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.facet-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 10px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}

.facet-diff-icon {
  font-size: 12px;
  width: 16px;
  text-align: center;
}

.icon-up {
  color: var(--color-agreeableness);
}

.icon-down {
  color: var(--color-neuroticism);
}

.facet-label {
  flex: 1;
  font-size: 13px;
  font-weight: 500;
}

.facet-scores {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.me-score {
  color: #7B2FF7;
  font-weight: 600;
}

.friend-score {
  color: #FF006E;
  font-weight: 600;
}

.vs {
  color: var(--color-text-secondary);
  font-size: 10px;
}

.facet-diff-val {
  width: 36px;
  font-size: 13px;
  font-weight: 700;
  text-align: right;
}

/* ---- 相似度 ---- */
.similarity-section {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.similarity-ring {
  position: relative;
  width: 140px;
  height: 140px;
}

.similarity-svg {
  width: 100%;
  height: 100%;
}

.similarity-text {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.similarity-value {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
}

.similarity-label {
  font-size: 11px;
  color: var(--color-text-secondary);
  margin-top: 2px;
}

/* ---- 导出按钮 ---- */
.export-compare-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 32px auto 0;
}

/* ═══════════════════════════════════════════
   Responsive: mobile < 520px
   ═══════════════════════════════════════════ */
@media (max-width: 520px) {
  .dim-label {
    width: 50px;
    font-size: 12px;
  }

  .dim-diff {
    width: 32px;
    font-size: 12px;
  }

  .facet-row {
    flex-wrap: wrap;
  }

  .similarity-ring {
    width: 120px;
    height: 120px;
  }

  .similarity-value {
    font-size: 24px;
  }
}
</style>

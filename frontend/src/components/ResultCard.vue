<template>
  <div class="result-card-wrapper">
    <!-- 解读弹窗 -->
    <Transition name="modal">
      <div v-if="showInterpret" class="interp-overlay" @click.self="showInterpret = false">
        <div class="interp-panel dopamine-card">
          <div class="interp-panel-header">
            <h3>{{ t('report.interpretation') }}</h3>
            <button class="interp-close" @click="showInterpret = false">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <div class="interp-panel-body">
            <p v-if="lang === 'zh'" class="interp-notice">
              部分子维度名称重新翻译，详见<a class="interp-link" @click.stop="showTermGlossary = true">术语对照表</a>
            </p>
            <div v-for="(dim, didx) in dimensionOrder" :key="dim" class="facet-group">
              <div class="facet-group-header">
                <span class="facet-group-title" :style="{ color: dimColors[didx] }">
                  {{ lang === 'en' ? dimLabelEn[dim] : dimLabelCn[dim] + ' (' + dim + ')' }}
                </span>
                <span class="facet-group-score" :style="{ color: dimColors[didx] }">{{ getScore(dim) }}</span>
              </div>
              <div
                v-for="facetKey in facetGroups[dim]" :key="facetKey"
                class="facet-bar-item"
                @click.stop="toggleFacetPopup(facetKey)"
              >
                <span class="facet-bar-label">{{ lang === 'en' ? facetMeta[facetKey].english : facetMeta[facetKey].userTranslation }}</span>
                <div class="facet-bar-track">
                  <div
                    class="facet-bar-fill"
                    :style="{ width: getFacetScore(facetKey) + '%', background: dimColors[didx] }"
                  ></div>
                </div>
                <span class="facet-bar-score">{{ getFacetScore(facetKey) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 结果卡片（导出的范围） -->
    <div ref="cardRef" class="result-card dopamine-card">
      <!-- 顶栏：标题 + 解读按钮 -->
      <div class="card-topbar">
        <h2 class="card-title">{{ t('report.title') }}</h2>
        <button class="interp-btn" @click="showInterpret = true" :title="t('report.interpretation')">
          {{ t('report.interpretation') }}
        </button>
      </div>

      <!-- 图表区：雷达图 + 柱状图 左右排列 -->
      <div class="charts-row">
        <div class="chart-radar">
          <RadarChart :scores="report.scoring" :lang="report.lang" />
        </div>
        <div class="chart-bars">
          <div
            v-for="(dim) in dimensionOrder" :key="dim" class="bar-item"
            @click="toggleDimPopup(dim)"
          >
            <div class="bar-header">
              <span class="bar-label">{{ lang === 'en' ? dimLabelEn[dim] : dimLabelCn[dim] }}</span>
              <span class="bar-value" :style="{ color: dimColors[dimensionOrder.indexOf(dim)] }">
                {{ getScore(dim) }}
              </span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: getScore(dim) + '%', background: dimColors[dimensionOrder.indexOf(dim)] }"></div>
            </div>

          </div>
        </div>
      </div>

      <!-- 彩蛋 -->
      <Transition name="egg">
        <div v-if="showEgg && displayEgg" class="card-egg">
          <p>{{ displayEgg }}</p>
        </div>
      </Transition>

      <!-- MBTI 解读 -->
      <div class="mbti-area">
        <div class="mbti-label">
        {{ t('report.mbti_label') }}: <strong>{{ report.mbti.type_code }}</strong>
        <span class="help-icon-sm" @click.stop="showMbtiHelp = true">&#9432;</span>
      </div>
        <div class="mbti-dims">
          <span v-for="(dim, idx) in report.mbti.dimensions" :key="dim.label_a + dim.label_b" class="mbti-dim" :style="{ background: dimColors[idx % dimColors.length] }">
            <span class="mbti-dim-label">{{ dim.label_a }}</span>
            <span class="mbti-dim-val">{{ (dim.prob_a * 100).toFixed(0) }}%</span>
            <span class="mbti-dim-divider">/</span>
            <span class="mbti-dim-label">{{ dim.label_b }}</span>
            <span class="mbti-dim-val">{{ (dim.prob_b * 100).toFixed(0) }}%</span>
          </span>
        </div>
      </div>
    </div>


    <!-- 维度解读弹窗 -->
    <div v-if="activeDimKey" class="modal-overlay" @click.self="activeDimKey = null">
      <div class="modal-card">
        <button class="modal-close" @click="activeDimKey = null">&times;</button>
        <h2 class="modal-title" :style="{ color: dimColors[dimensionOrder.indexOf(activeDimKey)] }">
          {{ lang === 'en' ? dimLabelEn[activeDimKey] : dimLabelCn[activeDimKey] + ' (' + activeDimKey + ')' }}
          <span class="modal-score">{{ getScore(activeDimKey) }}</span>
        </h2>
        <div class="facet-popup-body">
          <p class="dim-definition" v-if="lang === 'en' ? facetInterpretation(activeDimKey)?.definition_en : facetInterpretation(activeDimKey)?.definition_zh">
            {{ lang === 'en' ? facetInterpretation(activeDimKey)?.definition_en : facetInterpretation(activeDimKey)?.definition_zh }}
          </p>
          <div class="facet-popup-row">
            <span class="dim-help-badge high">{{ lang === 'en' ? 'High' : '高分' }}</span>
            <p class="dim-help-text">
              {{ (lang === 'en' ? facetInterpretation(activeDimKey)?.body_high_en : facetInterpretation(activeDimKey)?.body_high_zh) || (lang === 'en' ? facetInterpretation(activeDimKey)?.body_en : facetInterpretation(activeDimKey)?.body_zh) }}
            </p>
          </div>
          <div class="facet-popup-row">
            <span class="dim-help-badge low">{{ lang === 'en' ? 'Low' : '低分' }}</span>
            <p class="dim-help-text">
              {{ (lang === 'en' ? facetInterpretation(activeDimKey)?.body_low_en : facetInterpretation(activeDimKey)?.body_low_zh) || (lang === 'en' ? facetInterpretation(activeDimKey)?.body_en : facetInterpretation(activeDimKey)?.body_zh) }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 子维度解读弹窗 -->
    <div v-if="activeFacetKey" class="modal-overlay" @click.self="activeFacetKey = null">
      <div class="modal-card facet-modal-card">
        <button class="modal-close" @click="activeFacetKey = null">&times;</button>
        <h2 class="modal-title" style="color: var(--color-accent)">
          {{ lang === 'en' ? facetMeta[activeFacetKey]?.english : facetMeta[activeFacetKey]?.userTranslation }}
          <span class="modal-score">{{ lang === 'en' ? 'Score' : '得分' }} {{ getFacetScore(activeFacetKey) }}</span>
        </h2>
        <div class="facet-popup-body">
          <div class="facet-popup-row">
            <span class="dim-help-badge high">{{ lang === 'en' ? 'High' : '高分' }}</span>
            <p class="dim-help-text">
              {{ (lang === 'en' ? facetInterpretation(activeFacetKey)?.body_high_en : facetInterpretation(activeFacetKey)?.body_high_zh) || (lang === 'en' ? facetInterpretation(activeFacetKey)?.body_en : facetInterpretation(activeFacetKey)?.body_zh) }}
            </p>
          </div>
          <div class="facet-popup-row">
            <span class="dim-help-badge low">{{ lang === 'en' ? 'Low' : '低分' }}</span>
            <p class="dim-help-text">
              {{ (lang === 'en' ? facetInterpretation(activeFacetKey)?.body_low_en : facetInterpretation(activeFacetKey)?.body_low_zh) || (lang === 'en' ? facetInterpretation(activeFacetKey)?.body_en : facetInterpretation(activeFacetKey)?.body_zh) }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- MBTI 解释弹窗 -->
    <div v-if="showMbtiHelp" class="modal-overlay" @click.self="showMbtiHelp = false">
      <div class="modal-card">
        <button class="modal-close" @click="showMbtiHelp = false">&times;</button>
        <h2 class="modal-title" style="color: var(--color-accent)">{{ t('report.mbti_help_title') }}</h2>
        <p class="modal-body" style="white-space: pre-line">{{ t('report.mbti_help_body') }}</p>
      </div>
    </div>
    <!-- 术语对照表弹窗 -->
    <div v-if="showTermGlossary" class="modal-overlay" @click.self="showTermGlossary = false">
      <div class="modal-card glossary-card">
        <button class="modal-close" @click="showTermGlossary = false">&times;</button>
        <table class="glossary-table">
          <thead>
            <tr>
              <th>英文</th>
              <th>调整版</th>
              <th>学术版</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(dim, didx) in dimensionOrder" :key="dim">
              <tr class="glossary-domain-row">
                <td colspan="3" :style="{ color: dimColors[didx], borderBottomColor: dimColors[didx] }">
                  {{ lang === 'en' ? dimLabelEn[dim] : dimLabelCn[dim] + ' (' + dim + ')' }}
                </td>
              </tr>
              <tr v-for="facetKey in facetGroups[dim]" :key="facetKey">
                <td class="glossary-en">{{ facetMeta[facetKey].english }}</td>
                <td class="glossary-mine">{{ facetMeta[facetKey].userTranslation }}</td>
                <td class="glossary-academic">{{ facetMeta[facetKey].academicTranslation }}</td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from '../composables/useI18n'
import RadarChart from './RadarChart.vue'
import { dimColors, dimensionOrder, dimLabelCn, dimLabelEn, facetMeta, facetGroups } from '../utils/facetMeta.js'

const props = defineProps({
  report: { type: Object, required: true },
})

const { t, lang } = useI18n()
const cardRef = ref(null)
const showInterpret = ref(false)
const showMbtiHelp = ref(false)
const showTermGlossary = ref(false)

// 子维度详情弹窗
const activeFacetKey = ref(null)

// 维度详情弹窗（主卡片柱状条）
const activeDimKey = ref(null)

function facetInterpretation(facetKey) {
  return props.report.interpretations?.find(i => i.dimension === facetKey) ?? null
}

function toggleFacetPopup(facetKey) {
  activeFacetKey.value = activeFacetKey.value === facetKey ? null : facetKey
}

function toggleDimPopup(dim) {
  activeDimKey.value = activeDimKey.value === dim ? null : dim
}

const displayEgg = computed(() => {
  return props.report.easter_egg || null
})

const showEgg = ref(false)
onMounted(() => {
  setTimeout(() => { showEgg.value = true }, 2000)
})

function getScore(dim) {
  return Math.round(props.report.scoring?.t_scores?.[dim] ?? props.report.scoring?.[dim] ?? 50)
}

function getFacetScore(facetKey) {
  return Math.round(props.report.scoring?.facet_scores?.[facetKey] ?? 50)
}

defineExpose({ cardRef })
</script>

<style scoped>
.result-card-wrapper { position: relative; }

.result-card {
  max-width: 640px;
  margin: 0 auto;
  padding: 0;
  overflow: hidden;
  border: 2px solid var(--color-border);
  animation: bounceIn 0.6s var(--ease-smooth-spring);
}

/* ===== 顶栏 ===== */
.card-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 0;
  animation: fadeInUp 0.6s var(--ease-bounce) 0.1s both;
}
.card-title {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: 0.5px;
  margin: 0;
}
.interp-btn {
  display: inline-block;
  padding: 6px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}
.interp-btn:hover { border-color: var(--color-accent); color: var(--color-accent); }

/* ===== 图表行 ===== */
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  padding: 16px 16px 8px;
  align-items: start;
}
.chart-radar { min-height: 260px; animation: fadeInUp 0.8s var(--ease-bounce) 0s both; }
.chart-bars { display: flex; flex-direction: column; gap: 14px; padding-top: 12px; animation: fadeInUp 0.8s var(--ease-bounce) 0.15s both; }
.bar-item {
  position: relative;
  cursor: pointer;
  padding: 6px 8px;
  margin: 0 -8px;
  border-radius: 10px;
  transition: background 0.2s;
}
.bar-item:hover {
  background: var(--color-bg);
}
.bar-item:active {
  background: var(--color-border);
}
.bar-item:nth-child(1) { animation: fadeInUp 0.6s var(--ease-bounce) 0.2s both; }
.bar-item:nth-child(2) { animation: fadeInUp 0.6s var(--ease-bounce) 0.27s both; }
.bar-item:nth-child(3) { animation: fadeInUp 0.6s var(--ease-bounce) 0.34s both; }
.bar-item:nth-child(4) { animation: fadeInUp 0.6s var(--ease-bounce) 0.41s both; }
.bar-item:nth-child(5) { animation: fadeInUp 0.6s var(--ease-bounce) 0.48s both; }

.bar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}
.bar-label { font-size: 13px; font-weight: 600; color: var(--color-text); }
.bar-label-en { font-size: 10px; font-weight: 400; color: var(--color-text-secondary); margin-left: 4px; }
.bar-value { font-family: var(--font-mono); font-size: 16px; font-weight: 700; }
.bar-track { height: 8px; background: var(--color-border); border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.8s var(--ease-smooth-spring); }

/* ===== 彩蛋 ===== */
.card-egg {
  margin: 12px 24px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, rgba(123, 47, 247, 0.06), rgba(255, 0, 110, 0.06));
  border: 1px solid rgba(123, 47, 247, 0.15);
  max-height: 200px;
}
.card-egg p { font-size: 13px; line-height: 1.5; color: var(--color-text); margin: 0; }

/* ===== 彩蛋展开动画 ===== */
.egg-enter-active {
  transition: all 0.5s ease-out;
  overflow: hidden;
}
.egg-leave-active {
  transition: all 0.3s ease-in;
  overflow: hidden;
}
.egg-enter-from {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
  margin-top: 0;
  margin-bottom: 0;
  border-top-width: 0;
  border-bottom-width: 0;
}
.egg-leave-to {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
  margin-top: 0;
  margin-bottom: 0;
  border-top-width: 0;
  border-bottom-width: 0;
}

/* ===== MBTI ===== */
.mbti-area { margin: 12px 24px 20px; text-align: center; animation: fadeInUp 0.8s var(--ease-bounce) 0.55s both; }
.mbti-label { font-size: 14px; color: var(--color-text-secondary); margin-bottom: 10px; }
.mbti-label strong { font-family: var(--font-mono); font-size: 22px; color: var(--color-accent); margin-left: 4px; }
.mbti-dims { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; }
.mbti-dim {
  display: flex; align-items: center; gap: 4px;
  padding: 6px 12px; border-radius: var(--radius-full);
  color: #fff; font-size: 13px;
}
.mbti-dim:hover { transform: scale(1.05); }
.mbti-dim-label { font-weight: 500; opacity: 0.9; }
.mbti-dim-val { font-family: var(--font-mono); font-weight: 700; }
.mbti-dim-divider { opacity: 0.3; margin: 0 2px; }

/* ===== 解读弹窗 ===== */
.interp-overlay {
  position: fixed; inset: 0;
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  z-index: 200;
}
.interp-panel {
  max-width: 520px; width: 94%; max-height: 80vh; overflow-y: auto;
  padding: 0; border: 2px solid var(--color-border);
}
.interp-panel-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px; border-bottom: 1px solid var(--color-border);
}
.interp-panel-header h3 { font-size: 18px; font-weight: 700; }
.interp-close {
  width: 32px; height: 32px; border: none; border-radius: 8px;
  background: transparent; color: var(--color-text-secondary); cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.interp-close:hover { background: var(--color-bg); }
.interp-panel-body { padding: 16px 24px 24px; }
.interp-panel-item { margin-bottom: 20px; }
.interp-panel-item:last-child { margin-bottom: 0; }
.interp-panel-item h4 { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
.interp-panel-item p { font-size: 14px; line-height: 1.6; color: var(--color-text-secondary); }

/* ===== 弹窗动画 ===== */
.modal-enter-active { animation: bounceIn 0.5s var(--ease-smooth-spring); }
.modal-leave-active { animation: fadeIn 0.3s ease reverse; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }

/* ===== 帮助图标 ===== */
.help-icon-sm {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  font-size: 10px;
  border-radius: 50%;
  cursor: pointer;
  color: var(--color-accent);
  background: var(--color-accent-light);
  margin-left: 4px;
  vertical-align: middle;
  transition: transform 0.35s;
  user-select: none;
  flex-shrink: 0;
}

.help-icon-sm:hover {
  transform: scale(1.25);
}

/* ===== 弹窗遮罩 ===== */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

.modal-card {
  background: var(--color-surface);
  border-radius: 16px;
  padding: 32px;
  max-width: 420px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  margin-top: 40px;
  box-shadow: 0 25px 80px rgba(0,0,0,0.25);
  animation: slideUp 0.5s var(--ease-bounce);
}

.modal-close {
  position: absolute;
  top: 12px;
  right: 16px;
  background: none;
  border: none;
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
  color: var(--color-text-secondary);
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.modal-close:hover {
  background: var(--color-border);
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-accent);
  margin-bottom: 12px;
  padding-right: 30px;
}

.modal-score {
  font-family: var(--font-mono);
  font-size: 16px;
  font-weight: 700;
  margin-left: 8px;
  opacity: 0.7;
}

.modal-body {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text);
  white-space: pre-line;
}

/* ===== 维度解释：上下对照 ===== */
.facet-popup-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.facet-popup-row {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.dim-help-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 6px;
}

.dim-help-badge.high {
  background: rgba(123, 47, 247, 0.12);
  color: var(--color-accent);
}

.dim-help-badge.low {
  background: rgba(255, 0, 110, 0.10);
  color: #FF006E;
}

.dim-help-badge.medium {
  background: rgba(128, 128, 128, 0.10);
  color: var(--color-text-secondary);
}

/* ===== 解读弹窗：提示文字 ===== */
.interp-notice {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin: 0 0 20px 0;
  padding: 8px 12px;
  background: rgba(123, 47, 247, 0.05);
  border-radius: 8px;
  border: 1px dashed rgba(123, 47, 247, 0.18);
}
.interp-link {
  color: var(--color-accent);
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 2px;
}
.interp-link:hover { opacity: 0.8; }

/* ===== 解读弹窗：子维度柱状图组 ===== */
.facet-group {
  margin-bottom: 24px;
}
.facet-group:last-child { margin-bottom: 0; }

.facet-group-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 10px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--color-border);
}
.facet-group-title {
  font-size: 15px;
  font-weight: 700;
}
.facet-group-score {
  font-family: var(--font-mono);
  font-size: 16px;
  font-weight: 700;
}

.facet-bar-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  position: relative;
  cursor: pointer;
}
.facet-modal-card {
  max-width: 480px;
}

.facet-bar-item:hover .facet-bar-fill {
  opacity: 0.9;
}
.facet-bar-label {
  width: 64px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text);
  text-align: right;
  flex-shrink: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.facet-bar-track {
  flex: 1;
  height: 6px;
  background: var(--color-border);
  border-radius: 3px;
  overflow: hidden;
}
.facet-bar-fill {
  height: 100%;
  border-radius: 3px;
  opacity: 0.65;
  transition: width 0.8s var(--ease-smooth-spring);
}
.facet-bar-score {
  width: 28px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--color-text-secondary);
  text-align: left;
  flex-shrink: 0;
}


  background: var(--color-surface);
  border: 1px solid var(--color-border);

.dim-help-text {
  font-size: 12px;
  line-height: 1.6;
  color: var(--color-text-secondary);
  margin: 4px 0 0;
}

.dim-definition {
  font-size: 13px;
  line-height: 1.6;
  color: var(--color-text);
  font-style: italic;
  margin: 0 0 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border);
}



/* ===== 弹窗飞入动画 ===== */


/* ===== 术语对照表 ===== */
.glossary-card {
  max-width: 560px;
  padding: 28px;
}
.glossary-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  margin-top: 12px;
}
.glossary-table th {
  text-align: left;
  padding: 8px 12px;
  font-weight: 600;
  font-size: 12px;
  color: var(--color-text-secondary);
  border-bottom: 2px solid var(--color-border);
  background: var(--color-bg);
  position: sticky;
  top: 0;
}
.glossary-table td {
  padding: 8px 12px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  line-height: 1.5;
}
.glossary-table tbody tr:hover { background: var(--color-bg); }
.glossary-en {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--color-text-secondary);
}
.glossary-mine {
  font-weight: 600;
  color: var(--color-accent);
}
.glossary-academic {
  color: var(--color-text-secondary);
  font-style: italic;
}
.glossary-domain-row td {
  font-weight: 700;
  font-size: 14px;
  padding: 12px 12px 8px;
  background: var(--color-bg);
  border-bottom: 2px solid;
}
.glossary-domain-row:not(:first-child) td {
  padding-top: 18px;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ═══════════════════════════════════════════
   Responsive: mobile < 520px
   ═══════════════════════════════════════════ */
@media (max-width: 520px) {
  .charts-row {
    grid-template-columns: 1fr;
    gap: 4px;
    padding: 12px 12px 4px;
  }

  .chart-radar {
    min-height: 220px;
  }

  .chart-bars {
    gap: 10px;
    padding-top: 8px;
  }

  .card-title {
    font-size: 20px;
  }

  .card-topbar {
    padding: 16px 16px 0;
  }

  .bar-label {
    font-size: 12px;
  }

  .bar-value {
    font-size: 14px;
  }

  .mbti-area {
    margin: 10px 16px 16px;
  }

  .mbti-label strong {
    font-size: 20px;
  }

  .card-egg {
    margin: 10px 16px;
    padding: 10px 14px;
  }


}
</style>

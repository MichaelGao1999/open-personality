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
            <div v-for="interp in domainInterpretations" :key="interp.dimension" class="interp-panel-item">
              <h4 :style="{ color: dimColors[dimensionOrder.indexOf(interp.dimension)] }">
                {{ report.lang === 'zh' ? interp.title_zh : interp.title_en }}
              </h4>
              <p>{{ report.lang === 'zh' ? interp.body_zh : interp.body_en }}</p>
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
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>
          </svg>
          {{ t('report.interpretation') }}
        </button>
      </div>

      <!-- 图表区：雷达图 + 柱状图 左右排列 -->
      <div class="charts-row">
        <div class="chart-radar">
          <RadarChart :scores="report.scoring" :lang="report.lang" />
        </div>
        <div class="chart-bars">
          <div v-for="(dim) in dimensionOrder" :key="dim" class="bar-item">
            <div class="bar-header">
              <span class="bar-label">{{ dimLabelCn[dim] }} <span class="bar-label-en">{{ dimLabelEn[dim] }}</span></span>
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

      <!-- 彩蛋 / 趣味提示 -->
      <div class="card-egg" :class="{ 'no-egg': !displayEgg }">
        <div class="egg-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <p>{{ displayEgg }}</p>
      </div>

      <!-- MBTI 解读 -->
      <div class="mbti-area">
        <div class="mbti-label">{{ t('report.mbti_label') }}: <strong>{{ report.mbti.type_code }}</strong></div>
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
const showInterpret = ref(false)

const dimColors = ['#7B2FF7', '#00B4D8', '#FFD60A', '#06D6A0', '#FF006E']
const dimensionOrder = ['O', 'C', 'E', 'A', 'N']

// 默认趣味提示（无彩蛋时展示）
const defaultTips = [
  '人格是流动的——今天的你和明天的你可能不同，这正是成长的意义。',
  '了解自己是改变的第一步。你正在做一件很有勇气的事。',
  '没有人格是"好的"或"坏的"——每种特质都有它的优势和挑战。',
  '人格测试只是一个起点，真正的发现来自于日常的自我观察。',
]

const dimLabelCn = { O: '开放性', C: '严谨性', E: '外向性', A: '宜人性', N: '神经质' }
const dimLabelEn = { O: 'Openness', C: 'Conscientiousness', E: 'Extraversion', A: 'Agreeableness', N: 'Neuroticism' }

const domainInterpretations = computed(() => {
  return props.report.interpretations?.slice(0, 5) || []
})

const displayEgg = computed(() => {
  if (props.report.easter_egg) return props.report.easter_egg
  const tip = defaultTips[Math.floor(Math.random() * defaultTips.length)]
  return '💡 ' + tip
})

function getScore(dim) {
  return Math.round(props.report.scoring?.t_scores?.[dim] ?? props.report.scoring?.[dim] ?? 50)
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
  display: inline-flex;
  align-items: center;
  gap: 6px;
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
.chart-radar { min-height: 260px; }
.chart-bars { display: flex; flex-direction: column; gap: 14px; padding-top: 12px; }
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
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin: 12px 24px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, rgba(123, 47, 247, 0.06), rgba(255, 0, 110, 0.06));
  border: 1px solid rgba(123, 47, 247, 0.15);
  animation: bounceIn 0.5s var(--ease-smooth-spring);
}
.card-egg.no-egg {
  background: rgba(128, 128, 128, 0.04);
  border-color: var(--color-border);
}
.card-egg.no-egg .egg-icon { background: var(--color-text-secondary); }
.card-egg.no-egg p { font-style: normal; opacity: 0.7; }
.egg-icon {
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--gradient-primary);
  display: flex; align-items: center; justify-content: center; color: #fff; flex-shrink: 0;
}
.card-egg p { font-size: 13px; line-height: 1.5; color: var(--color-text); margin: 4px 0 0; }

/* ===== MBTI ===== */
.mbti-area { margin: 12px 24px 20px; text-align: center; }
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
  max-width: 420px; width: 90%; max-height: 80vh; overflow-y: auto;
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
.modal-enter-active { animation: bounceIn 0.3s var(--ease-smooth-spring); }
.modal-leave-active { animation: fadeIn 0.2s ease reverse; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }
</style>

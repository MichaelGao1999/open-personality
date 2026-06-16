<template>
  <div class="questionnaire-page">
    <SettingsMenu />

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>{{ t('questionnaire.loading') }}</p>
    </div>

    <!-- 答题模式 -->
    <template v-if="!loading && items.length && !showSummary">
      <div class="progress-section">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%', background: currentDimColor }"></div>
        </div>
        <p class="progress-text">
          {{ t('questionnaire.progress') }}
          <span class="progress-num">{{ currentIndex + 1 }}</span>
          {{ t('questionnaire.of') }}
          <span class="progress-num">{{ items.length }}</span>
        </p>
      </div>

      <p class="questionnaire-hint">{{ t('questionnaire.hint') }}</p>

      <Transition name="question-slide" mode="out-in">
        <div class="question-card dopamine-card" :key="currentIndex">
          <p class="q-text">{{ currentItem.text }}</p>
          <div class="options">
            <button
              v-for="(val, idx) in [1,2,3,4,5]"
              :key="val"
              class="option-btn"
              :class="{ active: answers[currentItem.item_id] === val }"
              :style="{ '--dim-color': dimColors[idx] }"
              @mouseenter="hoveredIdx = idx"
              @mouseleave="hoveredIdx = -1"
              @click="selectAnswer(currentItem.item_id, val)"
            >
              <span class="option-value">{{ val }}</span>
            </button>
          </div>
          <div class="option-hints">
            <span
              v-for="(hint, idx) in hintLabels"
              :key="idx"
              class="hint-item"
              :class="{ visible: hoveredIdx === idx }"
              :style="{ '--hint-color': dimColors[idx] }"
            >{{ hint }}</span>
          </div>
        </div>
      </Transition>

      <div class="nav-buttons">
        <button
          v-if="currentIndex > 0"
          class="dopamine-btn-outline"
          @click="prev"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          {{ t('questionnaire.prev') }}
        </button>
        <div style="flex:1"></div>
        <button
          class="dopamine-btn-outline partial-btn"
          :disabled="answeredCount === 0"
          @click="viewPartialResult"
        >
          {{ t('questionnaire.partial_view') }}
        </button>
      </div>
    </template>

    <!-- 总览模式 -->
    <template v-if="!loading && items.length && showSummary">
      <div class="summary-section">
        <div class="summary-header">
          <h2 class="summary-title gradient-text">{{ t('questionnaire.summary_title') }}</h2>
          <p class="summary-desc">{{ t('questionnaire.summary_desc') }}</p>
        </div>

        <div class="summary-grid">
          <button
            v-for="(item, idx) in items"
            :key="item.item_id"
            class="summary-item dopamine-card"
            :class="{ answered: answers[item.item_id], 'has-accent': answers[item.item_id] }"
            :style="answers[item.item_id] ? { '--accent': dimColors[answers[item.item_id] - 1] } : {}"
            @click="jumpTo(idx)"
          >
            <span class="summary-num">{{ idx + 1 }}</span>
            <span class="summary-text" :title="item.text">{{ item.text }}</span>
            <span class="summary-value" v-if="answers[item.item_id]">
              {{ answers[item.item_id] }}
            </span>
            <span class="summary-unanswered" v-else>
              {{ t('questionnaire.summary_unanswered') }}
            </span>
          </button>
        </div>

        <div class="summary-footer">
          <div class="summary-stats">
            <span class="stats-answered">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-conscientiousness)" stroke-width="3">
                <path d="M20 6L9 17l-5-5"/>
              </svg>
              {{ answeredCount }}/{{ items.length }}
            </span>
          </div>
          <button
            class="dopamine-btn summary-submit"
            @click="confirmSubmit"
            :disabled="!allAnswered"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
            {{ t('questionnaire.summary_submit') }}
          </button>
          <button class="dopamine-btn-outline" @click="viewPartialResult" :disabled="answeredCount === 0">
            {{ t('questionnaire.partial_view') }}
          </button>
        </div>
      </div>
    </template>

    <!-- 确认弹窗 -->
    <Transition name="modal">
      <div v-if="showConfirm" class="modal-overlay" @click.self="showConfirm = false">
        <div class="modal dopamine-card">
          <div class="modal-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7B2FF7" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <h3>{{ t('questionnaire.confirm_title') }}</h3>
          <p>{{ t('questionnaire.confirm_body') }}</p>
          <div class="modal-actions">
            <button class="dopamine-btn-outline" @click="showConfirm = false">
              {{ t('questionnaire.cancel') }}
            </button>
            <button class="dopamine-btn" @click="submit">
              {{ t('questionnaire.confirm') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { useRecentReports } from '../composables/useRecentReports'
import { getItems, submitAnswers } from '../utils/api'
import SettingsMenu from '../components/SettingsMenu.vue'

const { t, lang } = useI18n()
const route = useRoute()
const router = useRouter()
const { add } = useRecentReports()

const STORAGE_KEY = 'open_personality_session'

const mode = route.query.mode || 'standard'
const isResume = route.query.resume === 'local'
const items = ref([])
const answers = ref({})
const currentIndex = ref(0)
const loading = ref(false)
const showConfirm = ref(false)
const showSummary = ref(false)
const lastAnswerTime = ref(0)

// 选项颜色：不同意(靛蓝) → 中立(灰) → 同意(琥珀)
const dimColors = ['#6366f1', '#a5b4fc', '#9ca3af', '#fde68a', '#f59e0b']
const hoveredIdx = ref(-1)
const hintLabels = computed(() => {
  const isZh = lang.value === 'zh'
  return isZh
    ? ['非常不同意', '不同意', '中立', '同意', '非常同意']
    : ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
})

const currentItem = computed(() => items.value[currentIndex.value])
const progress = computed(() => ((currentIndex.value + 1) / items.value.length) * 100)
const allAnswered = computed(() => items.value.length > 0 && items.value.every((item) => answers.value[item.item_id]))
const answeredCount = computed(() => items.value.filter((item) => answers.value[item.item_id]).length)

// ---- localStorage 自动保存 ----
function saveToLocalStorage() {
  try {
    const data = {
      mode,
      lang: lang.value,
      answers: { ...answers.value },
      currentIndex: currentIndex.value,
      total: items.value.length,
      savedAt: Date.now(),
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch { /* ignore quota errors */ }
}

// 监听答案变化，自动保存（防抖 500ms）
watch(answers, () => { saveToLocalStorage() }, { deep: true })

// ---- 答题逻辑 ----
function selectAnswer(itemId, value) {
  answers.value[itemId] = value
  const currentPos = items.value.findIndex((item) => item.item_id === itemId)
  if (currentPos < items.value.length - 1) {
    currentIndex.value = currentPos + 1
  } else {
    showSummary.value = true
  }
}

function prev() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

function jumpTo(idx) {
  currentIndex.value = idx
  showSummary.value = false
}

// ---- 查看当前结果 / 保存到云端 ----
async function viewPartialResult() {
  if (answeredCount.value === 0) return
  const ansList = Object.entries(answers.value).map(([item_id, value]) => ({ item_id, value }))
  // 保存到后端，获取 share_token
  loading.value = true
  try {
    const res = await submitAnswers(mode, lang.value, ansList, 'partial')
    const report = res.data
    // 清理 localStorage 中的当前进度（已保存到云端）
    localStorage.removeItem(STORAGE_KEY)
    // 跳转到报告页，标记为 partial
    router.push({
      path: `/report/${report.share_token}`,
      query: { partial: '1', mode },
    })
  } catch {
    // 如果你只想看本地结果预览，可以不提交——但为了准确度我们提交了
    // 如果失败，回退到本地粗略计算
    alert(t('error.422') || '提交失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

function confirmSubmit() {
  showConfirm.value = true
}

async function submit() {
  showConfirm.value = false
  loading.value = true
  try {
    const ansList = Object.entries(answers.value).map(([item_id, value]) => ({ item_id, value }))
    const res = await submitAnswers(mode, lang.value, ansList, 'complete')
    add(res.data)
    localStorage.removeItem(STORAGE_KEY)
    router.push(`/report/${res.data.share_token}`)
  } catch {
    alert(t('error.422'))
  } finally {
    loading.value = false
  }
}

// ---- 恢复已有进度 ----
function restoreFromLocalStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return false
    const saved = JSON.parse(raw)
    if (saved.mode !== mode) return false
    // 恢复答案
    for (const [id, val] of Object.entries(saved.answers)) {
      answers.value[id] = val
    }
    currentIndex.value = saved.currentIndex || 0
    return true
  } catch { return false }
}

// ---- 初始化 ----
onMounted(async () => {
  try {
    const res = await getItems(mode, lang.value)
    items.value = res.data.items
    // 如果是恢复模式，还原答案
    if (isResume) {
      restoreFromLocalStorage()
    }
  } catch {
    alert('Failed to load questions')
  }
})
</script>

<style scoped>
.questionnaire-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 80px 20px 60px;
  position: relative;
  z-index: 1;
}

/* ===== 加载 ===== */
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

.loading p {
  color: var(--color-text-secondary);
  font-size: 16px;
}

/* ===== 进度条 ===== */
.progress-section {
  margin-bottom: 32px;
  animation: fadeInUp 0.6s var(--ease-bounce);
}

.progress-bar {
  height: 10px;
  background: var(--color-border);
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  border-radius: 5px;
  transition: width 0.6s var(--ease-smooth);
}

.progress-text {
  text-align: center;
  color: var(--color-text-secondary);
  font-size: 14px;
}

.progress-num {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--color-text);
}

/* ===== 题目卡片 ===== */
.question-card {
  padding: 32px;
  margin-bottom: 24px;
  border: 2px solid var(--color-border);
  position: relative;
  overflow: hidden;
}

.q-text {
  font-size: 20px;
  line-height: 1.6;
  margin-bottom: 28px;
}

.options {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.option-btn {
  flex: 1;
  height: 54px;
  border-radius: var(--radius-md);
  border: 2px solid var(--color-border);
  background: var(--color-surface);
  cursor: pointer;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-secondary);
  transition: all 0.35s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-btn:hover {
  background: var(--dim-color);
  border-color: color-mix(in srgb, var(--dim-color) 60%, transparent);
  color: #fff;
  box-shadow: 0 4px 12px color-mix(in srgb, var(--dim-color) 30%, transparent);
}

.option-btn.active {
  background: var(--dim-color);
  border-color: color-mix(in srgb, var(--dim-color) 60%, transparent);
  color: white;
  transform: scale(1.06);
  box-shadow: 0 4px 16px color-mix(in srgb, var(--dim-color) 40%, transparent);
}

.option-hints {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
  min-height: 24px;
}

.hint-item {
  flex: 1;
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: transparent;
  transition: color 0.4s ease;
  max-width: 90px;
}

.hint-item.visible {
  color: var(--hint-color, var(--color-accent));
}

/* ===== 底部导航 ===== */
.nav-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
}

.partial-btn {
  font-size: 13px !important;
  padding: 8px 16px !important;
}

.partial-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* ===== 答题提示 ===== */
.questionnaire-hint {
  text-align: center;
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0 auto 16px;
  padding: 6px 16px;
  background: var(--color-accent-light);
  border-radius: var(--radius-full);
}

/* ===== 题目切换动画 ===== */
.question-slide-enter-active {
  transition: opacity 0.35s var(--ease-smooth), transform 0.35s var(--ease-smooth);
}

.question-slide-leave-active {
  transition: opacity 0.12s ease-in, transform 0.12s ease-in;
}

.question-slide-enter-from {
  opacity: 0;
  transform: translateX(12px);
}

.question-slide-leave-to {
  opacity: 0;
  transform: translateX(-12px);
}

/* ===== 总览 ===== */
.summary-section {
  animation: fadeInUp 0.7s var(--ease-bounce);
}

.summary-header {
  text-align: center;
  margin-bottom: 32px;
}

.summary-title {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 8px;
}

.summary-desc {
  color: var(--color-text-secondary);
  font-size: 15px;
}

.summary-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 32px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  border: 2px solid var(--color-border);
  transition: all 0.35s var(--ease-bounce);
  text-align: left;
  font-family: inherit;
  font-size: inherit;
  width: 100%;
}

.summary-item.answered {
  border-left: 4px solid var(--accent, var(--color-conscientiousness));
}

.summary-item:hover {
  transform: translateX(4px);
  border-color: var(--color-conscientiousness);
}

.summary-num {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-secondary);
  min-width: 28px;
}

.summary-text {
  flex: 1;
  font-size: 14px;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.summary-value {
  font-family: var(--font-mono);
  font-size: 16px;
  font-weight: 700;
  color: var(--accent, var(--color-conscientiousness));
  min-width: 24px;
  text-align: center;
}

.summary-unanswered {
  font-size: 12px;
  color: var(--color-neuroticism);
  font-weight: 500;
  min-width: 48px;
  text-align: right;
}

.summary-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.summary-stats {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-text-secondary);
  font-size: 14px;
}

.stats-answered {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  color: var(--color-conscientiousness);
}

.summary-submit:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

/* ===== 确认弹窗 ===== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.modal {
  max-width: 400px;
  width: 90%;
  padding: 32px;
  text-align: center;
  border: 2px solid var(--color-border);
}

.modal-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(123, 47, 247, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.modal h3 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
}

.modal p {
  color: var(--color-text-secondary);
  font-size: 14px;
  margin-bottom: 24px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

/* ===== 动画 ===== */
.modal-enter-active { animation: bounceIn 0.6s var(--ease-smooth-spring); }
.modal-leave-active { animation: pageOut 0.3s ease-in; }

/* ═══════════════════════════════════════════
   Responsive: mobile < 520px
   ═══════════════════════════════════════════ */
@media (max-width: 520px) {
  .questionnaire-page {
    padding: 60px 16px 40px;
  }

  .q-text {
    font-size: 18px;
  }

  .question-card {
    padding: 24px 16px;
  }

  .options {
    gap: 8px;
  }

  .option-btn {
    height: 48px;
    border-radius: 14px;
    font-size: 16px;
  }

  .option-hints {
    gap: 4px;
    flex-wrap: wrap;
  }

  .hint-item {
    max-width: none;
    font-size: 11px;
    flex: 1 1 auto;
    min-width: 0;
    color: var(--color-text-secondary);
  }

  .questionnaire-hint {
    font-size: 12px;
    padding: 6px 12px;
  }

  .summary-title {
    font-size: 28px;
  }
}
</style>

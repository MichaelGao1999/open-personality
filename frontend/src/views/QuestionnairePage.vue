<template>
  <div class="questionnaire-page">
    <LanguageSwitch />

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>{{ t('questionnaire.loading') }}</p>
    </div>

    <template v-if="!loading && items.length">
      <div class="progress-section">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <p class="progress-text">
          {{ t('questionnaire.progress') }}
          <span class="progress-num">{{ currentIndex + 1 }}</span>
          {{ t('questionnaire.of') }}
          <span class="progress-num">{{ items.length }}</span>
        </p>
      </div>

      <div class="question-card dopamine-card">
        <div class="question-number">{{ currentIndex + 1 }}</div>
        <p class="q-text">{{ currentItem.text }}</p>
        <div class="options">
          <button
            v-for="(val, idx) in [1,2,3,4,5]"
            :key="val"
            class="option-btn"
            :class="{ active: answers[currentItem.item_id] === val }"
            :style="{ '--dim-color': dimColors[idx] }"
            @click="selectAnswer(currentItem.item_id, val)"
          >
            <span class="option-value">{{ val }}</span>
            <span class="option-label" v-if="idx === 0">1</span>
            <span class="option-label" v-if="idx === 4">5</span>
          </button>
        </div>
        <div class="option-labels">
          <span>Strongly Disagree</span>
          <span>Strongly Agree</span>
        </div>
      </div>

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
        <button
          v-if="currentIndex < items.length - 1"
          class="dopamine-btn nav-next"
          @click="next"
          :disabled="!answers[currentItem.item_id]"
        >
          {{ t('questionnaire.next') }}
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </button>
        <button
          v-if="currentIndex === items.length - 1"
          class="dopamine-btn submit-btn"
          @click="confirmSubmit"
          :disabled="!allAnswered"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
          {{ t('questionnaire.submit') }}
        </button>
      </div>
    </template>

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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { useRecentReports } from '../composables/useRecentReports'
import { getItems, submitAnswers } from '../utils/api'
import LanguageSwitch from '../components/LanguageSwitch.vue'

const { t, lang } = useI18n()
const route = useRoute()
const router = useRouter()
const { add } = useRecentReports()

const mode = route.query.mode || 'standard'
const items = ref([])
const answers = ref({})
const currentIndex = ref(0)
const loading = ref(false)
const showConfirm = ref(false)

const dimColors = ['#7B2FF7', '#00B4D8', '#FFD60A', '#56CFE1', '#FF006E']

const currentItem = computed(() => items.value[currentIndex.value])
const progress = computed(() => ((currentIndex.value + 1) / items.value.length) * 100)
const allAnswered = computed(() => items.value.length > 0 && items.value.every((item) => answers.value[item.item_id]))

function selectAnswer(itemId, value) {
  answers.value[itemId] = value
}

function next() {
  if (currentIndex.value < items.value.length - 1) {
    currentIndex.value++
  }
}

function prev() {
  if (currentIndex.value > 0) {
    currentIndex.value--
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
    const res = await submitAnswers(mode, lang.value, ansList)
    add(res.data)
    router.push(`/report/${res.data.share_token}`)
  } catch {
    alert(t('error.422'))
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const res = await getItems(mode, lang.value)
    items.value = res.data.items
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

.progress-section {
  margin-bottom: 32px;
  animation: fadeInUp 0.4s var(--ease-bounce);
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
  background: var(--gradient-rainbow);
  background-size: 200% 100%;
  border-radius: 5px;
  transition: width 0.4s var(--ease-smooth);
  animation: shimmer 3s linear infinite;
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

.question-card {
  padding: 32px;
  margin-bottom: 24px;
  border: 2px solid var(--color-border);
  animation: bounceIn 0.5s var(--ease-bounce);
  position: relative;
  overflow: hidden;
}

.question-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-rainbow);
}

.question-number {
  position: absolute;
  top: 16px;
  right: 20px;
  font-family: var(--font-mono);
  font-size: 48px;
  font-weight: 700;
  color: var(--color-border);
  opacity: 0.3;
}

.q-text {
  font-size: 20px;
  line-height: 1.6;
  margin-bottom: 28px;
  padding-right: 40px;
}

.options {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.option-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 3px solid var(--color-border);
  background: var(--color-surface);
  cursor: pointer;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-secondary);
  transition: all 0.25s var(--ease-bounce);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  position: relative;
}

.option-label {
  font-size: 9px;
  opacity: 0.5;
}

.option-btn:hover {
  border-color: var(--dim-color);
  color: var(--dim-color);
  transform: scale(1.1);
}

.option-btn.active {
  background: var(--dim-color);
  border-color: var(--dim-color);
  color: white;
  transform: scale(1.15);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}

.option-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  font-size: 12px;
  color: var(--color-text-secondary);
}

.nav-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.nav-next:disabled,
.submit-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

.submit-btn {
  background: linear-gradient(135deg, #56CFE1, #00B4D8);
  box-shadow: 0 4px 16px rgba(0, 180, 216, 0.3);
}

/* Modal */
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

/* Modal transition */
.modal-enter-active { animation: bounceIn 0.3s var(--ease-bounce); }
.modal-leave-active { animation: pageOut 0.2s ease-in; }
</style>

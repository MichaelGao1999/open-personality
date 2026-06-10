<template>
  <div class="questionnaire-page">
    <LanguageSwitch />

    <div v-if="loading" class="loading">{{ t('questionnaire.loading') }}</div>

    <template v-if="!loading && items.length">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
      </div>
      <p class="progress-text">
        {{ t('questionnaire.progress') }} {{ currentIndex + 1 }}{{ t('questionnaire.of') }}{{ items.length }}
      </p>

      <div class="question-card">
        <p class="q-text">{{ currentItem.text }}</p>
        <div class="options">
          <button
            v-for="val in [1,2,3,4,5]"
            :key="val"
            :class="{ active: answers[currentItem.item_id] === val }"
            @click="selectAnswer(currentItem.item_id, val)"
          >
            {{ val === 1 ? '1' : val === 2 ? '2' : val === 3 ? '3' : val === 4 ? '4' : '5' }}
          </button>
        </div>
      </div>

      <div class="nav-buttons">
        <button v-if="currentIndex > 0" @click="prev">{{ t('questionnaire.prev') }}</button>
        <button v-if="currentIndex < items.length - 1" @click="next" :disabled="!answers[currentItem.item_id]">
          {{ t('questionnaire.next') }}
        </button>
        <button v-if="currentIndex === items.length - 1" @click="confirmSubmit" :disabled="!allAnswered">
          {{ t('questionnaire.submit') }}
        </button>
      </div>
    </template>

    <div v-if="showConfirm" class="modal-overlay">
      <div class="modal">
        <h3>{{ t('questionnaire.confirm_title') }}</h3>
        <p>{{ t('questionnaire.confirm_body') }}</p>
        <div class="modal-actions">
          <button @click="showConfirm = false">{{ t('questionnaire.cancel') }}</button>
          <button class="primary" @click="submit">{{ t('questionnaire.confirm') }}</button>
        </div>
      </div>
    </div>
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
.questionnaire-page { max-width: 600px; margin: 0 auto; padding: 60px 16px; }
.progress-bar { height: 6px; background: #e0e0e0; border-radius: 3px; margin-bottom: 8px; }
.progress-fill { height: 100%; background: #4a90d9; border-radius: 3px; transition: width 0.3s; }
.progress-text { text-align: center; color: #888; font-size: 14px; margin-bottom: 24px; }
.question-card { background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 24px; }
.q-text { font-size: 18px; margin-bottom: 20px; line-height: 1.6; }
.options { display: flex; gap: 8px; justify-content: center; }
.options button {
  width: 48px; height: 48px; border-radius: 50%; border: 2px solid #ddd;
  background: #fff; cursor: pointer; font-size: 16px; transition: all 0.2s;
}
.options button.active { background: #4a90d9; color: #fff; border-color: #4a90d9; }
.nav-buttons { display: flex; gap: 12px; justify-content: center; }
.nav-buttons button {
  padding: 10px 24px; border: 1px solid #ccc; border-radius: 6px;
  background: #fff; cursor: pointer; font-size: 14px;
}
.nav-buttons button:disabled { opacity: 0.4; cursor: default; }
.loading { text-align: center; padding: 80px 0; font-size: 18px; color: #666; }
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center; z-index: 200;
}
.modal { background: #fff; border-radius: 12px; padding: 24px; max-width: 360px; text-align: center; }
.modal-actions { display: flex; gap: 12px; justify-content: center; margin-top: 16px; }
.modal-actions button { padding: 8px 20px; border-radius: 6px; border: 1px solid #ccc; cursor: pointer; }
.modal-actions .primary { background: #4a90d9; color: #fff; border-color: #4a90d9; }
</style>

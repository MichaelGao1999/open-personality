<template>
  <div class="compare-page">
    <SettingsMenu />

    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>{{ t('compare.loading') }}</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#FF006E" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <path d="M16 16s-1.5-2-4-2-4 2-4 2M9 9h.01M15 9h.01"/>
        </svg>
      </div>
      <h2>{{ error }}</h2>
      <button class="dopamine-btn" @click="$router.push('/')">{{ t('home.back') || '返回首页' }}</button>
    </div>

    <template v-else>
      <div class="compare-header">
        <h1 class="compare-title gradient-text">{{ t('compare.title') }}</h1>
        <p class="compare-subtitle">{{ t('compare.subtitle') }}</p>
      </div>

      <CompareView :my-report="myReport" :friend-report="friendReport" />
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { getReport } from '../utils/api'
import SettingsMenu from '../components/SettingsMenu.vue'
import CompareView from '../components/CompareView.vue'

const { t } = useI18n()
const route = useRoute()

const loading = ref(true)
const error = ref('')
const myReport = ref(null)
const friendReport = ref(null)

onMounted(async () => {
  const myToken = route.params.myToken
  const friendToken = route.params.friendToken

  if (myToken === friendToken) {
    error.value = t('compare.same_person')
    loading.value = false
    return
  }

  try {
    const [myRes, friendRes] = await Promise.all([
      getReport(myToken),
      getReport(friendToken),
    ])
    myReport.value = myRes.data
    friendReport.value = friendRes.data
  } catch (e) {
    error.value = t('compare.error')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.compare-page {
  max-width: 680px;
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

.compare-header {
  text-align: center;
  margin-bottom: 32px;
  animation: fadeInUp 0.8s var(--ease-bounce);
}

.compare-title {
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 700;
}

.compare-subtitle {
  color: var(--color-text-secondary);
  font-size: 16px;
  margin-top: 8px;
}

.error-state {
  text-align: center;
  padding: 80px 0;
  animation: fadeInUp 0.5s var(--ease-bounce);
}

.error-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255, 0, 110, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
}

.error-state h2 {
  font-size: 20px;
  margin-bottom: 16px;
}

@media (max-width: 520px) {
  .compare-page {
    padding: 60px 16px 40px;
  }

  .compare-title {
    font-size: 28px;
  }
}
</style>

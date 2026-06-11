<template>
  <div class="home-page">
    <LanguageSwitch />

    <div class="hero">
      <h1 class="hero-title gradient-text">{{ t('app.title') }}</h1>
      <p class="hero-subtitle">{{ t('app.subtitle') }}</p>
      <div class="hero-dots">
        <span class="dot" style="background: #7B2FF7"></span>
        <span class="dot" style="background: #00B4D8"></span>
        <span class="dot" style="background: #FFD60A"></span>
        <span class="dot" style="background: #56CFE1"></span>
        <span class="dot" style="background: #FF006E"></span>
      </div>
    </div>

    <div class="mode-select">
      <div
        class="mode-card dopamine-card"
        :class="{ selected: mode === 'standard' }"
        @click="mode = 'standard'"
      >
        <div class="mode-icon" style="background: var(--gradient-primary)">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <h3>{{ t('home.standard') }}</h3>
        <p>{{ t('home.standard_desc') }}</p>
      </div>
      <div
        class="mode-card dopamine-card"
        :class="{ selected: mode === 'advanced' }"
        @click="mode = 'advanced'"
      >
        <div class="mode-icon" style="background: linear-gradient(135deg, #00B4D8, #56CFE1)">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
        </div>
        <h3>{{ t('home.advanced') }}</h3>
        <p>{{ t('home.advanced_desc') }}</p>
      </div>
    </div>

    <button class="dopamine-btn start-btn" @click="startTest">
      {{ t('home.start') }}
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M5 12h14M12 5l7 7-7 7"/>
      </svg>
    </button>

    <div class="divider">
      <span></span>
      <span class="divider-text">OR</span>
      <span></span>
    </div>

    <ShareCodeInput />

    <div class="recent-section" v-if="reports.length">
      <h3 class="recent-title">{{ t('home.recent_title') }}</h3>
      <div class="recent-list">
        <div
          v-for="r in reports"
          :key="r.share_token"
          class="recent-item dopamine-card"
          @click="$router.push(`/report/${r.share_token}`)"
        >
          <div class="recent-code">{{ r.share_token }}</div>
          <div class="recent-date">{{ new Date(r.created_at).toLocaleDateString() }}</div>
        </div>
      </div>
    </div>
    <p v-else class="no-recent">{{ t('home.no_recent') }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { useRecentReports } from '../composables/useRecentReports'
import LanguageSwitch from '../components/LanguageSwitch.vue'
import ShareCodeInput from '../components/ShareCodeInput.vue'

const { t } = useI18n()
const router = useRouter()
const { reports } = useRecentReports()
const mode = ref('standard')

function startTest() {
  router.push({ path: '/questionnaire', query: { mode: mode.value } })
}
</script>

<style scoped>
.home-page {
  max-width: 520px;
  margin: 0 auto;
  padding: 80px 20px 60px;
  text-align: center;
  position: relative;
  z-index: 1;
}

.hero {
  margin-bottom: 40px;
  animation: fadeInUp 0.6s var(--ease-bounce);
}

.hero-title {
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 700;
  letter-spacing: -1px;
  margin-bottom: 12px;
}

.hero-subtitle {
  color: var(--color-text-secondary);
  font-size: 18px;
  font-weight: 400;
}

.hero-dots {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 20px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
.dot:nth-child(4) { animation-delay: 0.6s; }
.dot:nth-child(5) { animation-delay: 0.8s; }

.mode-select {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 32px;
}

.mode-card {
  flex: 1;
  max-width: 220px;
  padding: 28px 20px;
  cursor: pointer;
  transition: all 0.3s var(--ease-bounce);
  border: 2px solid var(--color-border);
}

.mode-card.selected {
  border-color: var(--color-neuroticism);
  box-shadow: 0 0 0 4px rgba(255, 0, 110, 0.1), var(--shadow-md);
}

.mode-card:hover {
  transform: translateY(-4px);
}

.mode-icon {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.mode-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 6px;
}

.mode-card p {
  color: var(--color-text-secondary);
  font-size: 14px;
}

.start-btn {
  font-size: 18px;
  padding: 16px 48px;
  margin-bottom: 32px;
}

.divider {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.divider span:first-child,
.divider span:last-child {
  flex: 1;
  height: 1px;
  background: var(--color-border);
}

.divider-text {
  color: var(--color-text-secondary);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
}

.recent-section {
  margin-top: 40px;
  animation: fadeInUp 0.6s var(--ease-bounce) 0.2s both;
}

.recent-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--color-text-secondary);
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.recent-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  cursor: pointer;
  border: 2px solid transparent;
}

.recent-item:hover {
  border-color: var(--color-conscientiousness);
}

.recent-code {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--color-text);
}

.recent-date {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.no-recent {
  color: var(--color-text-secondary);
  font-size: 14px;
  margin-top: 40px;
}
</style>

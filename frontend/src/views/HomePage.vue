<template>
  <div class="home-page">
    <LanguageSwitch />
    <div class="hero">
      <h1>{{ t('app.title') }}</h1>
      <p class="subtitle">{{ t('app.subtitle') }}</p>
    </div>

    <div class="mode-select">
      <div class="mode-card" :class="{ selected: mode === 'standard' }" @click="mode = 'standard'">
        <h3>{{ t('home.standard') }}</h3>
        <p>{{ t('home.standard_desc') }}</p>
      </div>
      <div class="mode-card" :class="{ selected: mode === 'advanced' }" @click="mode = 'advanced'">
        <h3>{{ t('home.advanced') }}</h3>
        <p>{{ t('home.advanced_desc') }}</p>
      </div>
    </div>

    <button class="start-btn" @click="startTest">{{ t('home.start') }}</button>

    <ShareCodeInput />

    <div class="recent-section">
      <h3>{{ t('home.recent_title') }}</h3>
      <ul v-if="reports.length" class="recent-list">
        <li v-for="r in reports" :key="r.share_token" @click="$router.push(`/report/${r.share_token}`)">
          {{ r.share_token }} · {{ new Date(r.created_at).toLocaleDateString() }}
        </li>
      </ul>
      <p v-else class="no-recent">{{ t('home.no_recent') }}</p>
    </div>
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
.home-page { max-width: 480px; margin: 0 auto; padding: 60px 16px; text-align: center; }
.hero { margin-bottom: 32px; }
.hero h1 { font-size: 28px; margin-bottom: 8px; }
.subtitle { color: #666; font-size: 16px; }
.mode-select { display: flex; gap: 12px; justify-content: center; margin-bottom: 24px; }
.mode-card {
  flex: 1; padding: 20px; border: 2px solid #e0e0e0; border-radius: 12px;
  cursor: pointer; transition: all 0.2s; max-width: 200px;
}
.mode-card.selected { border-color: #4a90d9; background: #f0f7ff; }
.mode-card h3 { margin: 0 0 8px; font-size: 16px; }
.mode-card p { margin: 0; color: #888; font-size: 13px; }
.start-btn {
  padding: 12px 48px; font-size: 16px; background: #4a90d9; color: #fff;
  border: none; border-radius: 8px; cursor: pointer; margin-bottom: 24px;
}
.recent-section { margin-top: 32px; }
.recent-list { list-style: none; padding: 0; }
.recent-list li {
  padding: 8px 12px; background: #f5f5f5; border-radius: 6px;
  margin-bottom: 6px; cursor: pointer; font-size: 14px;
}
.recent-list li:hover { background: #e8e8e8; }
.no-recent { color: #999; font-size: 14px; }
</style>

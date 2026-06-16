<template>
  <div class="home-page">
    <SettingsMenu />

    <!-- 恢复横幅 -->
    <div v-if="savedSession" class="resume-banner dopamine-card">
      <div class="resume-info">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--color-conscientiousness)" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
        </svg>
        <span>{{ t('home.resume_banner') }}</span>
        <span class="resume-detail">{{ savedSession.mode }} · {{ savedSession.answered }}/{{ savedSession.total }}</span>
      </div>
      <div class="resume-actions">
        <button class="dopamine-btn resume-btn" @click="resumeTest">{{ t('home.resume_btn') }}</button>
        <button class="dopamine-btn-outline dismiss-btn" @click="dismissResume">{{ t('home.resume_dismiss') }}</button>
      </div>
    </div>

    <div class="hero">
      <h1 class="hero-title">{{ t('app.title') }}</h1>
      <p class="hero-subtitle">
        {{ t('app.subtitle') }}
        <span class="help-icon" @click.stop="showWhyBig = true">&#9432;</span>
      </p>
    </div>

    <!-- 大五人格解释弹窗 -->
    <div v-if="showWhyBig" class="modal-overlay" @click.self="showWhyBig = false">
      <div class="modal-card">
        <button class="modal-close" @click="showWhyBig = false">&times;</button>
        <h2 class="modal-title">{{ t('home.why_big_title_1') }}</h2>
        <p class="modal-body">{{ t('home.why_big_body_1') }}</p>
        <h2 class="modal-title" style="margin-top: 20px">{{ t('home.why_big_title_2') }}</h2>
        <p class="modal-body" style="white-space: pre-line">{{ t('home.why_big_body_2') }}</p>
      </div>
    </div>

    <div class="mode-select">
      <div
        class="mode-card dopamine-card"
        :class="{ selected: mode === 'speed' }"
        @click="mode = 'speed'"
      >
        <div class="mode-icon" style="color: var(--color-openness)">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
          </svg>
        </div>
        <h3>
          {{ t('home.speed') }}
          <span class="help-icon-sm" @click.stop="showModeHelp = 'speed'">&#9432;</span>
        </h3>
        <p>{{ t('home.speed_desc') }}</p>
      </div>
      <div
        class="mode-card dopamine-card"
        :class="{ selected: mode === 'standard' }"
        @click="mode = 'standard'"
      >
        <div class="mode-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <h3>
          {{ t('home.standard') }}
          <span class="help-icon-sm" @click.stop="showModeHelp = 'standard'">&#9432;</span>
        </h3>
        <p>{{ t('home.standard_desc') }}</p>
      </div>
      <div
        class="mode-card dopamine-card"
        :class="{ selected: mode === 'advanced' }"
        @click="mode = 'advanced'"
      >
        <div class="mode-icon" style="color: var(--color-openness)">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M12 2L2 9l10 13L22 9z"/>
            <path d="M2 9h20"/>
            <path d="M7 9l5-6 5 6"/>
            <path d="M12 22V9"/>
            <path d="M5 12l3 4M19 12l-3 4"/>
          </svg>
        </div>
        <h3>
          {{ t('home.advanced') }}
          <span class="help-icon-sm" @click.stop="showModeHelp = 'advanced'">&#9432;</span>
        </h3>
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

    <!-- 模式说明弹窗 -->
    <div v-if="showModeHelp" class="modal-overlay" @click.self="showModeHelp = false">
      <div class="modal-card">
        <button class="modal-close" @click="showModeHelp = false">&times;</button>
        <h2 class="modal-title">{{ t('home.' + showModeHelp) }}</h2>
        <p class="modal-body">{{ t('home.' + showModeHelp + '_help') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'
import { useRecentReports } from '../composables/useRecentReports'
import SettingsMenu from '../components/SettingsMenu.vue'
import ShareCodeInput from '../components/ShareCodeInput.vue'

const { t } = useI18n()
const router = useRouter()
const { reports } = useRecentReports()
const mode = ref('standard')
const savedSession = ref(null)
const showWhyBig = ref(false)
const showModeHelp = ref(false)
const STORAGE_KEY = 'open_personality_session'

function loadSavedSession() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const data = JSON.parse(raw)
      // 检查是否已过期（超过 7 天）
      const age = Date.now() - (data.savedAt || 0)
      if (age > 7 * 24 * 60 * 60 * 1000) {
        localStorage.removeItem(STORAGE_KEY)
        return null
      }
      return data
    }
  } catch { /* ignore */ }
  return null
}

function resumeTest() {
  if (savedSession.value) {
    router.push({
      path: '/questionnaire',
      query: {
        mode: savedSession.value.mode,
        resume: 'local',
      },
    })
  }
}

function dismissResume() {
  localStorage.removeItem(STORAGE_KEY)
  savedSession.value = null
}

function startTest() {
  router.push({ path: '/questionnaire', query: { mode: mode.value } })
}

onMounted(() => {
  savedSession.value = loadSavedSession()
})
</script>

<style scoped>
.home-page {
  max-width: 580px;
  margin: 0 auto;
  padding: 80px 20px 60px;
  text-align: center;
  position: relative;
  z-index: 1;
}

/* ===== 恢复横幅 ===== */
.resume-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 20px;
  margin-bottom: 24px;
  border: 2px solid var(--color-conscientiousness);
  background: rgba(0, 180, 216, 0.05);
  animation: bounceIn 0.45s var(--ease-smooth-spring);
}

.resume-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
}

.resume-detail {
  color: var(--color-text-secondary);
  font-size: 13px;
}

.resume-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.resume-btn {
  padding: 8px 18px !important;
  font-size: 13px !important;
}

.dismiss-btn {
  padding: 8px 12px !important;
  font-size: 13px !important;
}

/* ===== 首屏 ===== */
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
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ===== 模式选择 ===== */
.mode-select {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 32px;
}

.mode-card {
  flex: 1;
  max-width: 180px;
  padding: 24px 14px;
  cursor: pointer;
  transition: all 0.25s var(--ease-bounce);
  border: 2px solid var(--color-border);
}

.mode-card.selected {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 4px var(--color-accent-light), var(--shadow-md);
}

.mode-card:hover {
  border-color: var(--color-text-secondary);
}

.mode-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
}

.mode-icon svg {
  stroke: currentColor;
  width: 20px;
  height: 20px;
}

.mode-card h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  text-align: center;
  position: relative;
}

.mode-card h3 .help-icon-sm {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  margin-left: 4px;
}

.mode-card p {
  color: var(--color-text-secondary);
  font-size: 12px;
}

/* ===== 开始按钮 ===== */
.start-btn {
  font-size: 18px;
  padding: 16px 48px;
  margin-bottom: 32px;
}

/* ===== 分割线 ===== */
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

/* ===== 最近记录 ===== */
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

/* ===== 帮助图标 ===== */
.help-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  font-size: 14px;
  border-radius: 50%;
  cursor: pointer;
  color: var(--color-accent);
  background: var(--color-accent-light);
  margin-left: 8px;
  vertical-align: middle;
  transition: transform 0.2s;
  user-select: none;
}

.help-icon:hover {
  transform: scale(1.2);
}

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
  transition: transform 0.2s;
  user-select: none;
}

.help-icon-sm:hover {
  transform: scale(1.2);
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
  animation: fadeIn 0.2s ease;
}

.modal-card {
  background: var(--color-surface);
  border-radius: 16px;
  padding: 32px;
  max-width: 480px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  box-shadow: var(--shadow-lg, 0 20px 60px rgba(0,0,0,0.3));
  animation: slideUp 0.3s var(--ease-bounce);
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
  margin-bottom: 8px;
  text-align: center;
}

.modal-body {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text);
  white-space: pre-line;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ═══════════════════════════════════════════
   Responsive: mobile < 520px
   ═══════════════════════════════════════════ */
@media (max-width: 520px) {
  .home-page {
    padding: 60px 16px 40px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 14px;
  }

  .mode-select {
    gap: 10px;
  }

  .mode-card {
    padding: 18px 16px;
  }

  .resume-banner {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
    text-align: center;
  }

  .resume-info {
    justify-content: center;
  }

  .resume-actions {
    justify-content: center;
  }
}
</style>

<template>
  <div class="settings-menu" :class="{ open: isOpen }">
    <!-- 齿轮按钮 -->
    <button class="gear-btn" @click="isOpen = !isOpen" :title="t('app.settings')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="3"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
      </svg>
    </button>

    <!-- 下拉面板 -->
    <Transition name="settings-fade">
      <div v-if="isOpen" class="settings-panel dopamine-card">
        <div class="sp-header">
          <span class="sp-title">{{ t('app.settings') }}</span>
          <button class="sp-close" @click="isOpen = false">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- 语言 -->
        <div class="sp-row">
          <span class="sp-label">{{ t('app.lang') }}</span>
          <div class="sp-toggle-group">
            <button class="sp-toggle-btn" :class="{ active: lang === 'zh' }" @click="switchLang('zh')">中文</button>
            <button class="sp-toggle-btn" :class="{ active: lang === 'en' }" @click="switchLang('en')">EN</button>
          </div>
        </div>

        <!-- 深色模式 -->
        <div class="sp-row">
          <span class="sp-label">{{ t('app.theme') }}</span>
          <div class="sp-toggle-group">
            <button class="sp-toggle-btn" :class="{ active: !isDark }" @click="setTheme('light')" title="浅色">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
              </svg>
            </button>
            <button class="sp-toggle-btn" :class="{ active: isDark }" @click="setTheme('dark')" title="深色">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- 反馈 -->
        <div class="sp-row">
          <span class="sp-label">{{ t('app.feedback') }}</span>
          <div class="sp-toggle-group">
            <button class="sp-toggle-btn" @click="openFeedback('bug')">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><path d="M16 16s-1.5-2-4-2-4 2-4 2M9 9h.01M15 9h.01"/>
              </svg>
              {{ t('app.bug') }}
            </button>
            <button class="sp-toggle-btn" @click="openFeedback('feature')">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14M5 12h14"/>
              </svg>
              {{ t('app.feature') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 点击外部关闭 -->
    <div v-if="isOpen" class="sp-backdrop" @click="isOpen = false"></div>

    <FeedbackModal :visible="showFeedback" :initial-type="feedbackInitialType" @close="showFeedback = false" />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useI18n } from '../composables/useI18n'
import FeedbackModal from './FeedbackModal.vue'

const { t, lang, setLang } = useI18n()

const isOpen = ref(false)
const isDark = ref(false)
const showFeedback = ref(false)
const feedbackInitialType = ref('bug')

// 初始化主题
onMounted(() => {
  const saved = localStorage.getItem('open_personality_theme')
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.setAttribute('data-theme', 'dark')
  }
})

function switchLang(l) {
  setLang(l)
}

function openFeedback(type) {
  isOpen.value = false
  feedbackInitialType.value = type
  showFeedback.value = true
}

function setTheme(theme) {
  isDark.value = theme === 'dark'
  if (isDark.value) {
    document.documentElement.setAttribute('data-theme', 'dark')
    localStorage.setItem('open_personality_theme', 'dark')
  } else {
    document.documentElement.removeAttribute('data-theme')
    localStorage.setItem('open_personality_theme', 'light')
  }
}
</script>

<style scoped>
.settings-menu {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
}

/* ===== 齿轮按钮 ===== */
.gear-btn {
  width: 42px;
  height: 42px;
  border: none;
  border-radius: 50%;
  background: var(--color-surface);
  color: var(--color-text-secondary);
  box-shadow: var(--shadow-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s var(--ease-smooth-spring, ease);
  border: 2px solid var(--color-border);
}

.gear-btn:hover {
  color: var(--color-accent);
  transform: rotate(30deg);
}

.settings-menu.open .gear-btn {
  transform: rotate(60deg);
  color: var(--color-accent);
}

/* ===== 下拉面板 ===== */
.settings-panel {
  position: absolute;
  top: 54px;
  right: 0;
  width: 240px;
  padding: 16px;
  border: 2px solid var(--color-border);
  z-index: 101;
}

.sp-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.sp-title {
  font-weight: 700;
  font-size: 14px;
  color: var(--color-text);
}

.sp-close {
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sp-close:hover { background: var(--color-bg); }

/* ===== 每一行 ===== */
.sp-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.sp-label {
  font-size: 14px;
  color: var(--color-text);
  font-weight: 500;
}

/* ===== 语言切换组 ===== */
.sp-toggle-group {
  display: flex;
  gap: 2px;
  padding: 2px;
  background: var(--color-bg);
  border-radius: 8px;
}

.sp-toggle-btn {
  padding: 5px 14px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--font-body);
}

.sp-toggle-btn.active {
  background: var(--color-accent);
  color: #fff;
}

/* ===== 动画 ===== */
.settings-fade-enter-active { animation: fadeIn 0.2s ease; }
.settings-fade-leave-active { animation: fadeIn 0.15s ease reverse; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== 点击外部关闭 ===== */
.sp-backdrop {
  position: fixed;
  inset: 0;
  z-index: 99;
}
</style>

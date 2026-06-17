<template>
  <Transition name="logo">
    <div v-if="showToolbar" class="app-toolbar">
      <!-- Logo (左) -->
      <div class="toolbar-logo" @click="goHome" role="link" tabindex="0" aria-label="回到首页" @keydown.enter="goHome">
        <span class="logo-brand">open</span>
        <span class="logo-name">personality</span>
      </div>

      <!-- 设置按钮 (右) -->
      <div class="toolbar-settings" :class="{ open: isOpen }">
        <button class="gear-btn" @click="isOpen = !isOpen" :title="t('app.settings')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
        </button>

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
            <div class="sp-row">
              <span class="sp-label">{{ t('app.lang') }}</span>
              <div class="sp-toggle-group">
                <button class="sp-toggle-btn" :class="{ active: lang === 'zh' }" @click="switchLang('zh')">中文</button>
                <button class="sp-toggle-btn" :class="{ active: lang === 'en' }" @click="switchLang('en')">EN</button>
              </div>
            </div>
            <div class="sp-row">
              <span class="sp-label">{{ t('app.theme') }}</span>
              <div class="sp-toggle-group">
                <button class="sp-toggle-btn" :class="{ active: !isDark }" @click="setTheme('light')" title="浅色">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
                </button>
                <button class="sp-toggle-btn" :class="{ active: isDark }" @click="setTheme('dark')" title="深色">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
                </button>
              </div>
            </div>
            <div class="sp-row">
              <span class="sp-label">{{ t('app.feedback') }}</span>
              <div class="sp-toggle-group">
                <button class="sp-toggle-btn" @click="openUrl(bugUrl)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 16s-1.5-2-4-2-4 2-4 2M9 9h.01M15 9h.01"/></svg>
                  使用障碍
                </button>
                <button class="sp-toggle-btn" @click="openUrl(featureUrl)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
                  功能建议
                </button>
              </div>
            </div>
          </div>
        </Transition>

        <div v-if="isOpen" class="sp-backdrop" @click="isOpen = false"></div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'

const route = useRoute()
const router = useRouter()
const { t, lang, setLang } = useI18n()

const isOpen = ref(false)
const isDark = ref(false)

const repo = 'https://github.com/MichaelGao1999/open-personality'
const bugUrl = repo + '/issues/new?template=bug_report.md'
const featureUrl = repo + '/issues/new?template=feature_request.md'

const showToolbar = computed(() => route.path !== '/')

onMounted(() => {
  const saved = localStorage.getItem('open_personality_theme')
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.setAttribute('data-theme', 'dark')
  }
})

function goHome() {
  router.push('/')
}

function switchLang(l) {
  setLang(l)
}

function openUrl(url) {
  window.open(url, '_blank', 'noopener')
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
/* ===== 顶部工具栏 ===== */
.app-toolbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 24px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  backdrop-filter: blur(8px);
}

/* ===== Logo (左) ===== */
.toolbar-logo {
  display: flex;
  align-items: baseline;
  gap: 4px;
  cursor: pointer;
  user-select: none;
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: var(--color-text);
  transition: opacity 0.35s ease;
}

.toolbar-logo:hover {
  opacity: 0.75;
}

.logo-brand {
  font-weight: 700;
}

.logo-name {
  font-weight: 400;
  opacity: 0.55;
}

/* ===== 设置按钮 (右) ===== */
.toolbar-settings {
  position: relative;
}

.gear-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: var(--color-bg);
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.35s var(--ease-smooth-spring), color 0.35s;
  border: 1px solid var(--color-border);
}

.gear-btn:hover {
  color: var(--color-accent);
  transform: rotate(30deg);
}

.toolbar-settings.open .gear-btn {
  transform: rotate(60deg);
  color: var(--color-accent);
}

/* ===== 下拉面板 ===== */
.settings-panel {
  position: absolute;
  top: 50px;
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

/* ===== 点击外部关闭 ===== */
.sp-backdrop {
  position: fixed;
  inset: 0;
  z-index: 99;
}

/* ===== 动画 ===== */
.logo-enter-active {
  animation: toolbarIn 0.4s var(--ease-smooth-spring);
}

.logo-leave-active {
  animation: toolbarOut 0.25s ease-in;
}

.settings-fade-enter-active { animation: fadeIn 0.2s ease; }
.settings-fade-leave-active { animation: fadeIn 0.15s ease reverse; }

@keyframes toolbarIn {
  from { opacity: 0; transform: translateY(-16px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes toolbarOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-12px); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 520px) {
  .app-toolbar {
    padding: 10px 16px;
  }
  .toolbar-logo {
    font-size: 22px;
  }
  .gear-btn {
    width: 36px;
    height: 36px;
  }
}
</style>

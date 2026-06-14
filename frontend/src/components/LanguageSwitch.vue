<template>
  <div class="lang-switch">
    <button
      :class="{ active: lang === 'zh' }"
      @click="switchLang('zh')"
      class="lang-btn"
    >
      {{ t('common.chinese') || '中文' }}
    </button>
    <button
      :class="{ active: lang === 'en' }"
      @click="switchLang('en')"
      class="lang-btn"
    >
      {{ t('common.english') || 'EN' }}
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'

const { t, lang, setLang } = useI18n()

function switchLang(l) {
  setLang(l)
}
</script>

<style scoped>
.lang-switch {
  position: fixed;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 4px;
  z-index: 100;
  padding: 4px;
  background: var(--color-surface);
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-md);
  border: 2px solid var(--color-border);
}

.lang-btn {
  padding: 8px 18px;
  border: none;
  border-radius: var(--radius-full);
  background: transparent;
  color: var(--color-text-secondary);
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s var(--ease-bounce);
}

.lang-btn:hover {
  background: var(--color-bg);
  color: var(--color-text);
}

.lang-btn.active {
  background: var(--gradient-primary);
  color: #fff;
  box-shadow: 0 2px 12px rgba(255, 0, 110, 0.3);
}

.lang-btn.active:hover {
  transform: scale(1.05);
}
</style>

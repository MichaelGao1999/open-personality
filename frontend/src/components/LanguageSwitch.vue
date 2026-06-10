<template>
  <div class="lang-switch">
    <button :class="{ active: lang === 'zh' }" @click="switchLang('zh')">中文</button>
    <button :class="{ active: lang === 'en' }" @click="switchLang('en')">EN</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'

const { lang, setLang } = useI18n()

function switchLang(l) {
  setLang(l)
}
</script>

<style scoped>
.lang-switch {
  position: fixed;
  top: 16px;
  right: 16px;
  display: flex;
  gap: 4px;
  z-index: 100;
}
.lang-switch button {
  padding: 4px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 13px;
}
.lang-switch button.active {
  background: #4a90d9;
  color: #fff;
  border-color: #4a90d9;
}
</style>

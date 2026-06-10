<template>
  <div id="app-root">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useI18n } from './composables/useI18n'

const { setLang } = useI18n()

onMounted(() => {
  const saved = localStorage.getItem('open_personality_lang')
  if (saved) setLang(saved)
})
</script>

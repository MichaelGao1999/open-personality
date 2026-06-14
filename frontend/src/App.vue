<template>
  <DebugDock />
  <div id="app-root">
    <router-view v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <component :is="Component" />
      </Transition>
    </router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useI18n } from './composables/useI18n'
import DebugDock from './components/DebugDock.vue'

const { setLang } = useI18n()

onMounted(() => {
  const saved = localStorage.getItem('open_personality_lang')
  if (saved) setLang(saved)
})
</script>

<style scoped>
#app-root {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* Scoped styles intentionally minimal — bg-decoration blobs removed */
#app-root {
  min-height: 100vh;
  position: relative;
}
</style>

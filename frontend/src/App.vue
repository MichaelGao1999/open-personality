<template>
  <div id="app-root">
    <div class="bg-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>
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

.bg-decoration {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  animation: blobFloat 20s ease-in-out infinite;
}

.blob-1 {
  width: 400px;
  height: 400px;
  background: #FF006E;
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.blob-2 {
  width: 350px;
  height: 350px;
  background: #7B2FF7;
  bottom: -80px;
  left: -80px;
  animation-delay: -7s;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background: #00B4D8;
  top: 40%;
  left: 50%;
  animation-delay: -14s;
}

@keyframes blobFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.05); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}
</style>

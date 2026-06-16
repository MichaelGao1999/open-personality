<template>
  <Transition name="logo">
    <div
      v-if="showCorner"
      class="app-logo"
      @click="goHome"
      role="link"
      tabindex="0"
      aria-label="回到首页"
      @keydown.enter="goHome"
    >
      <span class="logo-brand">open</span>
      <span class="logo-name">personality</span>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const showCorner = computed(() => route.path !== '/')

function goHome() {
  router.push('/')
}
</script>

<style scoped>
.app-logo {
  position: fixed;
  top: env(safe-area-inset-top, 20px);
  left: 20px;
  z-index: 50;
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: baseline;
  gap: 4px;
  font-family: var(--font-body);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.3px;
  color: var(--color-text-secondary);
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.app-logo:hover {
  opacity: 1;
  color: var(--color-text);
}

.logo-brand {
  font-weight: 600;
}

.logo-name {
  font-weight: 400;
  opacity: 0.65;
}

/* ===== Logo transition ===== */
.logo-enter-active {
  animation: logoIn 0.4s var(--ease-smooth-spring);
}

.logo-leave-active {
  animation: logoOut 0.25s ease-in;
}

@keyframes logoIn {
  from {
    opacity: 0;
    transform: translateY(-12px);
  }
  to {
    opacity: 0.7;
    transform: translateY(0);
  }
}

@keyframes logoOut {
  from {
    opacity: 0.7;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-8px);
  }
}

@media (max-width: 520px) {
  .app-logo {
    left: 16px;
    font-size: 12px;
  }
}
</style>

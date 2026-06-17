<template>
  <div class="share-code-input">
    <input
      v-model="code"
      :placeholder="t('home.share_code_placeholder')"
      maxlength="8"
      @keyup.enter="search"
    />
    <button class="dopamine-btn-outline share-btn" @click="resume">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M5 12h14M12 5l7 7-7 7"/>
      </svg>
      {{ t('home.continue_button') }}
    </button>
    <button class="dopamine-btn share-btn" @click="search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/>
        <path d="M21 21l-4.35-4.35"/>
      </svg>
      {{ t('home.share_code_button') }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
const router = useRouter()
const code = ref('')

function search() {
  const token = code.value.trim()
  if (token) {
    router.push(`/report/${token}`)
  }
}

function resume() {
  const token = code.value.trim()
  if (token) {
    router.push({ path: '/questionnaire', query: { mode: 'advanced', resume: token } })
  }
}
</script>

<style scoped>
.share-code-input {
  display: flex;
  gap: 10px;
  justify-content: center;
  align-items: center;
  animation: fadeInUp 0.8s var(--ease-bounce) 0.6s both;
}

.share-code-input input {
  padding: 14px 20px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-full);
  font-family: var(--font-mono);
  font-size: 16px;
  font-weight: 500;
  width: 200px;
  text-align: center;
  letter-spacing: 3px;
  color: var(--color-text);
  background: var(--color-surface);
  transition: all 0.25s var(--ease-bounce);
}

.share-code-input input:focus {
  outline: none;
  border-color: var(--color-conscientiousness);
  box-shadow: 0 0 0 4px rgba(0, 180, 216, 0.15);
}

.share-code-input input::placeholder {
  letter-spacing: 0;
  font-family: var(--font-body);
  font-weight: 400;
  color: var(--color-text-secondary);
}

.share-btn {
  padding: 14px 24px;
  font-size: 14px;
}

/* ═══════════════════════════════════════════
   Responsive: mobile < 520px
   ═══════════════════════════════════════════ */
@media (max-width: 520px) {
  .share-code-input input {
    width: 140px;
    max-width: 100%;
    padding: 12px 14px;
    font-size: 14px;
    letter-spacing: 2px;
  }

  .share-btn {
    padding: 12px 18px;
    font-size: 13px;
  }
}
</style>

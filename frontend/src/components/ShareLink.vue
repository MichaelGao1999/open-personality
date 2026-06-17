<template>
  <div class="share-link">
    <p v-if="shareToken" class="share-label">
      {{ t('report.share_code_label') }}:
      <span class="share-code">{{ shareToken }}</span>
    </p>
    <button class="share-btn" :class="{ copied }" @click="copyLink">
      <svg v-if="!copied" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
      </svg>
      <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M20 6L9 17l-5-5"/>
      </svg>
      {{ copied ? t('report.share_copied') : t('report.share') }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from '../composables/useI18n'

const props = defineProps({
  shareToken: { type: String, required: true },
})

const { t } = useI18n()
const copied = ref(false)

function copyLink() {
  navigator.clipboard.writeText(props.shareToken).then(() => {
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  })
}
</script>

<style scoped>
.share-link {
  text-align: center;
}

.share-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.share-code {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--color-text);
}

.share-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-surface);
  color: var(--color-text);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s var(--ease-bounce);
}

.share-btn:hover {
  border-color: var(--color-openness);
  color: var(--color-openness);
  transform: scale(1.03);
}

.share-btn.copied {
  border-color: var(--color-agreeableness);
  color: var(--color-agreeableness);
  background: rgba(86, 207, 225, 0.1);
}
</style>

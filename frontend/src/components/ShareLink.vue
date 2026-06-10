<template>
  <div class="share-link">
    <p v-if="shareToken">
      {{ t('report.share_code_label') }}: <strong>{{ shareToken }}</strong>
    </p>
    <button @click="copyLink">
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
  const url = `${window.location.origin}${window.location.pathname}#/report/${props.shareToken}`
  navigator.clipboard.writeText(url).then(() => {
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  })
}
</script>

<style scoped>
.share-link { text-align: center; margin-top: 16px; }
.share-link button {
  padding: 8px 20px;
  background: #4a90d9;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}
</style>

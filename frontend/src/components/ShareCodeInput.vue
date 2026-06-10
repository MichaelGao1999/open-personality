<template>
  <div class="share-code-input">
    <input
      v-model="code"
      :placeholder="t('home.share_code_placeholder')"
      maxlength="8"
      @keyup.enter="search"
    />
    <button @click="search">{{ t('home.share_code_button') }}</button>
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
</script>

<style scoped>
.share-code-input {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 16px;
}
.share-code-input input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  width: 160px;
  text-align: center;
  letter-spacing: 2px;
}
.share-code-input button {
  padding: 8px 16px;
  background: #4a90d9;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>

<template>
  <div v-if="text" class="easter-egg">
    <p>{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  text: { type: String, default: null },
})
</script>

<style scoped>
.easter-egg {
  background: linear-gradient(135deg, #fdf6e3, #f5e6cc);
  border: 1px solid #e8d5b5;
  border-radius: 8px;
  padding: 12px 16px;
  margin-top: 16px;
  font-style: italic;
  text-align: center;
}
</style>

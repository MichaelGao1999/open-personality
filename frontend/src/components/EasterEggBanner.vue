<template>
  <div v-if="text" class="easter-egg">
    <div class="easter-egg-icon">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
      </svg>
    </div>
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
  background: linear-gradient(135deg, rgba(123, 47, 247, 0.1), rgba(255, 0, 110, 0.1));
  border: 2px solid rgba(123, 47, 247, 0.2);
  border-radius: var(--radius-md);
  padding: 20px;
  margin-top: 20px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  animation: bounceIn 0.5s var(--ease-bounce);
}

.easter-egg-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.easter-egg p {
  font-style: italic;
  color: var(--color-text);
  line-height: 1.6;
  font-size: 15px;
}
</style>

<template>
  <Transition name="modal">
    <div v-if="visible" class="feedback-overlay" @click.self="close">
      <div class="feedback-modal dopamine-card">
        <div class="fm-header">
          <span class="fm-title">{{ t('feedback.title') }}</span>
          <button class="fm-close" @click="close">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- 类型选择 -->
        <div class="fm-row">
          <span class="fm-label">{{ t('feedback.type') }}</span>
          <div class="sp-toggle-group">
            <button class="sp-toggle-btn" :class="{ active: feedbackType === 'bug' }" @click="feedbackType = 'bug'">
              {{ t('app.bug') }}
            </button>
            <button class="sp-toggle-btn" :class="{ active: feedbackType === 'feature' }" @click="feedbackType = 'feature'">
              {{ t('app.feature') }}
            </button>
          </div>
        </div>

        <!-- 文本输入 -->
        <textarea
          v-model="content"
          class="fm-textarea"
          :placeholder="t('feedback.placeholder')"
          rows="4"
        ></textarea>

        <!-- 提交 -->
        <div class="fm-actions">
          <button class="fm-submit" :disabled="!content.trim() || submitting" @click="handleSubmit">
            {{ submitting ? '...' : t('feedback.submit') }}
          </button>
        </div>

        <!-- 成功提示 -->
        <Transition name="settings-fade">
          <div v-if="submitted" class="fm-success">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
            {{ t('feedback.success') }}
          </div>
        </Transition>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from '../composables/useI18n'
import { submitFeedback } from '../utils/api'

const { t } = useI18n()

const props = defineProps({
  visible: { type: Boolean, default: false },
  initialType: { type: String, default: 'bug' },
})
const emit = defineEmits(['close'])

const altUrl = 'https://www.feishu.cn/share/base/form/shrcnExampleFeedbackForm'

const feedbackType = ref('bug')
const content = ref('')
const submitting = ref(false)
const submitted = ref(false)

// 每次打开重置表单
watch(() => props.visible, (val) => {
  if (val) {
    feedbackType.value = props.initialType || 'bug'
    content.value = ''
    submitting.value = false
    submitted.value = false
  }
})

async function handleSubmit() {
  if (!content.value.trim() || submitting.value) return
  submitting.value = true
  try {
    await submitFeedback(feedbackType.value, content.value.trim())
  } catch {
    // 静默处理
  }
  window.open(altUrl, '_blank', 'noopener')
  submitted.value = true
  content.value = ''
  feedbackType.value = 'bug'
  submitting.value = false
}

function close() {
  emit('close')
}
</script>

<style scoped>
.feedback-overlay {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(4px);
}

.feedback-modal {
  width: 360px;
  max-width: 90vw;
  padding: 24px;
  border: 2px solid var(--color-border);
}

.fm-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.fm-title {
  font-weight: 700;
  font-size: 16px;
  color: var(--color-text);
}

.fm-close {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.fm-close:hover { background: var(--color-bg); }

.fm-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.fm-label {
  font-size: 14px;
  color: var(--color-text);
  font-weight: 500;
}

.fm-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 14px;
  font-family: var(--font-body);
  resize: vertical;
  min-height: 100px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;
}

.fm-textarea:focus {
  border-color: var(--color-accent);
}

.fm-textarea::placeholder {
  color: var(--color-text-secondary);
  opacity: 0.6;
}

.fm-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.fm-submit {
  padding: 8px 24px;
  border: none;
  border-radius: 8px;
  background: var(--color-accent);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  font-family: var(--font-body);
}

.fm-submit:hover { opacity: 0.85; }
.fm-submit:disabled { opacity: 0.5; cursor: not-allowed; }

.fm-success {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  background: var(--color-bg);
  color: var(--color-accent);
  font-size: 14px;
  font-weight: 500;
}

/* ===== 动画 ===== */
.modal-enter-active { animation: modalIn 0.25s ease; }
.modal-leave-active { animation: modalIn 0.2s ease reverse; }

@keyframes modalIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

/* 复用 sp-toggle 样式 */
.sp-toggle-group {
  display: flex;
  gap: 2px;
  padding: 2px;
  background: var(--color-bg);
  border-radius: 8px;
}

.sp-toggle-btn {
  padding: 5px 14px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: var(--font-body);
}

.sp-toggle-btn.active {
  background: var(--color-accent);
  color: #fff;
}

.settings-fade-enter-active { animation: fadeIn 0.2s ease; }
.settings-fade-leave-active { animation: fadeIn 0.15s ease reverse; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

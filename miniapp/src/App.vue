<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('App Launch')
})
onShow(() => {
  console.log('App Show')
})
onHide(() => {
  console.log('App Hide')
})
</script>

<style>
/* ===== 全局样式（uni-app 小程序） ===== */
page {
  --color-accent: #7B2FF7;
  --color-accent-light: rgba(123, 47, 247, 0.1);
  --color-bg: #F8F8FC;
  --color-surface: #FFFFFF;
  --color-text: #1A1A2E;
  --color-text-secondary: #8E8EA0;
  --color-border: #E8E8F0;
  --color-openness: #7B2FF7;
  --color-conscientiousness: #00B4D8;
  --color-extraversion: #FFD60A;
  --color-agreeableness: #06D6A0;
  --color-neuroticism: #FF006E;

  --font-display: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
  --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', monospace;

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 999px;

  background-color: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-body);
  font-size: 28rpx;
  line-height: 1.5;
  box-sizing: border-box;
}

view, text, image, button, input, scroll-view {
  box-sizing: border-box;
}

button::after {
  border: none;
}

/* ===== 通用工具类 ===== */
.dopamine-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.06);
}

.dopamine-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  padding: 20rpx 48rpx;
  border-radius: var(--radius-full);
  background: var(--color-accent);
  color: #FFFFFF;
  font-size: 28rpx;
  font-weight: 600;
  border: none;
  transition: opacity 0.2s;
}

.dopamine-btn:active {
  opacity: 0.8;
}

.dopamine-btn-outline {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  padding: 18rpx 36rpx;
  border-radius: var(--radius-full);
  background: transparent;
  color: var(--color-text);
  font-size: 26rpx;
  font-weight: 500;
  border: 2rpx solid var(--color-border);
  transition: all 0.2s;
}

.dopamine-btn-outline:active {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

/* ===== 弹窗遮罩 ===== */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx;
}

.modal-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: 48rpx;
  max-width: 600rpx;
  width: 100%;
  max-height: 70vh;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 16rpx;
  right: 24rpx;
  font-size: 40rpx;
  color: var(--color-text-secondary);
  padding: 8rpx 16rpx;
  line-height: 1;
}

.modal-title {
  font-size: 32rpx;
  font-weight: 700;
  color: var(--color-accent);
  margin-bottom: 16rpx;
  text-align: center;
}

.modal-body {
  font-size: 28rpx;
  line-height: 1.6;
  color: var(--color-text);
}

/* ===== 动画 ===== */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(40rpx); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

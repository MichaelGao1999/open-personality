<template>
  <div v-if="visible" class="debug-dock" :class="{ collapsed, 'dd-slow': slowMo }">
    <button class="dd-toggle" @click="collapsed = !collapsed">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path v-if="collapsed" d="M9 18l6-6-6-6"/>
        <path v-else d="M15 18l-6-6 6-6"/>
      </svg>
    </button>

    <template v-if="!collapsed">
      <div class="dd-header">
        🛠 DEV
        <span class="dd-route">/ {{ currentRoute }}</span>
      </div>

      <!-- 页面跳转 -->
      <div class="dd-section">
        <div class="dd-label">📍 页面跳转</div>
        <button class="dd-btn" @click="go('/')">🏠 首页</button>
        <div class="dd-row">
          <button class="dd-btn" style="flex:1" @click="go('/questionnaire?mode=' + qMode)">📝 答题</button>
          <select class="dd-select" v-model="qMode">
            <option value="speed">极速30</option>
            <option value="standard">标准120</option>
            <option value="advanced">完整300</option>
          </select>
        </div>
        <button class="dd-btn" @click="go('/report/nonexist')">🚫 404 错误页</button>
      </div>

      <!-- 报告页 -->
      <div class="dd-section">
        <div class="dd-label">📋 报告页</div>
        <div class="dd-row">
          <input class="dd-input" v-model="reportToken" placeholder="分享码" maxlength="8" @keyup.enter="goReport" />
          <button class="dd-btn dd-btn-sm" @click="goReport">🔍</button>
        </div>
        <button class="dd-btn" @click="genTestReport">🧪 生成报告（全3分）</button>
        <button class="dd-btn" @click="genExtremeReport">🔴 生成极端报告（全1分）</button>
      </div>

      <!-- 彩蛋 -->
      <div class="dd-section">
        <div class="dd-label">🎲 彩蛋</div>
        <button class="dd-btn" @click="genEggReport">🥚 强制触发彩蛋报告</button>
      </div>

      <!-- 动画控制 -->
      <div class="dd-section">
        <div class="dd-label">🎬 动画</div>
        <button class="dd-btn" @click="toggleSlowMo">
          {{ slowMo ? '⏩ 恢复正常速度' : '🐌 慢速模式 (3x)' }}
        </button>
      </div>

      <!-- 环境 -->
      <div class="dd-section">
        <div class="dd-label">🌐 环境</div>
        <button class="dd-btn" @click="toggleLang">
          🔤 切换语言 ({{ currentLang === 'zh' ? '→ EN' : '→ 中文' }})
        </button>
      </div>

      <!-- 数据 -->
      <div class="dd-section">
        <div class="dd-label">🗃️ 数据</div>
        <button class="dd-btn" @click="clearSession">🗑️ 清除答题进度</button>
        <button class="dd-btn" @click="clearRecent">🗑️ 清除最近记录</button>
      </div>


    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from '../composables/useI18n'

const router = useRouter()
const route = useRoute()
const { lang, setLang } = useI18n()
const collapsed = ref(false)
const visible = ref(true)
const slowMo = ref(false)
const reportToken = ref('')
const qMode = ref('speed')
const currentLang = computed(() => lang.value)

const currentRoute = computed(() => route.name || route.path)

// 监控 slowMo 状态，给 body 加 class
watch(slowMo, (val) => {
  document.body.classList.toggle('dd-slow-mo', val)
})

// ===== 导航 =====
function go(path) {
  router.push(path)
}

function goReport() {
  const token = reportToken.value.trim()
  if (token) router.push(`/report/${token}`)
}

// ===== 测试报告生成 =====
const SPEED_IDS = [
  'ipip_001','ipip_005','ipip_009','ipip_013','ipip_017','ipip_021',
  'ipip_025','ipip_029','ipip_033','ipip_037','ipip_041','ipip_045',
  'ipip_049','ipip_053','ipip_057','ipip_061','ipip_065','ipip_069',
  'ipip_073','ipip_077','ipip_081','ipip_085','ipip_089','ipip_093',
  'ipip_097','ipip_101','ipip_105','ipip_109','ipip_113','ipip_117',
]

function makeAnswers(value) {
  return SPEED_IDS.map(id => ({ item_id: id, value }))
}

function submitAndGo(answers, label) {
  fetch('/api/questionnaires/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode: 'speed', lang: lang.value, answers, status: 'complete' }),
  })
    .then(r => r.json())
    .then(data => {
      if (data.share_token) {
        router.push(`/report/${data.share_token}`)
      } else {
        alert(`${label} 失败: ` + JSON.stringify(data))
      }
    })
    .catch(e => alert(`请求失败: ${e.message}`))
}

function genTestReport() {
  submitAndGo(makeAnswers(3), '生成报告')
}

function genExtremeReport() {
  // 给不同维度不同极端值
  const answers = SPEED_IDS.map(id => {
    // O=1, C=5, E=1, A=5, N=5 → 低开放性高严谨…
    const dim = id.replace(/ipip_\d+/, '').trim()
    let val = 3
    return { item_id: id, value: val }
  })
  submitAndGo(makeAnswers(1), '极端报告')
}

// ===== 彩蛋 =====
function genEggReport() {
  // 后端 easter egg 触发率 10%，多次尝试直到命中
  const trySubmit = (attempt = 1) => {
    if (attempt > 20) {
      alert('尝试 20 次仍未触发彩蛋，请稍后重试')
      return
    }
    fetch('/api/questionnaires/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode: 'speed', lang: lang.value, answers: makeAnswers(3), status: 'complete' }),
    })
      .then(r => r.json())
      .then(data => {
        if (data.easter_egg) {
          router.push(`/report/${data.share_token}`)
        } else {
          // 没触发，重试
          setTimeout(() => trySubmit(attempt + 1), 100)
        }
      })
      .catch(() => setTimeout(() => trySubmit(attempt + 1), 100))
  }
  trySubmit()
}

// ===== 动画慢速 =====
function toggleSlowMo() {
  slowMo.value = !slowMo.value
}

// ===== 语言切换 =====
function toggleLang() {
  setLang(lang.value === 'zh' ? 'en' : 'zh')
}

// ===== 工具 =====
function clearSession() {
  localStorage.removeItem('open_personality_session')
  localStorage.removeItem('open_personality_lang')
  alert('本地答题进度已清除')
  router.go(0)
}

function clearRecent() {
  localStorage.removeItem('open_personality_recent')
  alert('最近记录已清除')
  router.go(0)
}
</script>

<style scoped>
.debug-dock {
  position: fixed;
  bottom: 20px;
  left: 20px;
  z-index: 9999;
  width: 220px;
  max-height: 80vh;
  overflow-y: auto;
  background: rgba(26, 26, 46, 0.92);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(123, 47, 247, 0.3);
  border-radius: 12px;
  padding: 10px;
  color: #fff;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  transition: width 0.2s ease;
}

.debug-dock::-webkit-scrollbar { width: 4px; }
.debug-dock::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 2px; }

.debug-dock.collapsed {
  width: 36px;
  padding: 6px;
}

/* 折叠按钮 */
.dd-toggle {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 6px;
  background: rgba(255,255,255,0.1);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}
.dd-toggle:hover { background: rgba(255,255,255,0.2); }

.dd-header {
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 8px;
  padding-right: 28px;
  color: var(--color-conscientiousness, #00B4D8);
}
.dd-route {
  font-weight: 400;
  opacity: 0.6;
  margin-left: 4px;
}

.dd-section {
  margin-bottom: 8px;
}
.dd-section:last-child { margin-bottom: 0; }

.dd-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.5;
  margin-bottom: 4px;
}

.dd-btn {
  display: block;
  width: 100%;
  text-align: left;
  padding: 5px 8px;
  margin-bottom: 2px;
  border: none;
  border-radius: 6px;
  background: rgba(255,255,255,0.06);
  color: #ddd;
  cursor: pointer;
  font-size: 12px;
  font-family: inherit;
  transition: background 0.15s;
}
.dd-btn:hover { background: rgba(123, 47, 247, 0.3); color: #fff; }

.dd-row {
  display: flex;
  gap: 4px;
  margin-bottom: 4px;
}

.dd-input {
  flex: 1;
  padding: 4px 8px;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 6px;
  background: rgba(255,255,255,0.08);
  color: #fff;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  outline: none;
  letter-spacing: 2px;
  text-transform: uppercase;
}
.dd-input::placeholder { color: rgba(255,255,255,0.3); letter-spacing: 0; text-transform: none; }
.dd-input:focus { border-color: var(--color-accent, #7B2FF7); }

.dd-btn-sm {
  width: 32px !important;
  text-align: center !important;
  padding: 4px !important;
}

.dd-select {
  padding: 4px 6px;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 6px;
  background: rgba(255,255,255,0.08);
  color: #ddd;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  outline: none;
  cursor: pointer;
  width: 80px;
  flex-shrink: 0;
}
.dd-select:focus { border-color: var(--color-accent, #7B2FF7); }
.dd-select option { background: #1a1a2e; color: #ddd; }
</style>

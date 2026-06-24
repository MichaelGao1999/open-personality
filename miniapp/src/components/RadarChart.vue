<template>
  <canvas
    type="2d"
    id="radarCanvas"
    class="radar-canvas"
    :style="{ width: canvasWidth + 'px', height: canvasHeight + 'px' }"
  ></canvas>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'

const props = defineProps({
  scores: {
    type: Array,
    default: () => [50, 50, 50, 50, 50],
  },
  labels: {
    type: Array,
    default: () => ['O', 'C', 'E', 'A', 'N'],
  },
})

const canvasWidth = ref(320)
const canvasHeight = ref(320)

const dimColors = ['#7B2FF7', '#00B4D8', '#FFD60A', '#06D6A0', '#FF006E']

function draw() {
  nextTick(() => {
    const query = uni.createSelectorQuery()
    query.select('#radarCanvas')
      .fields({ node: true, size: true })
      .exec((res) => {
        if (!res || !res[0]) return
        const canvas = res[0].node
        const ctx = canvas.getContext('2d')

        // Get DPR for sharp rendering
        const dpr = uni.getSystemInfoSync().pixelRatio || 2
        const width = res[0].width
        const height = res[0].height

        canvas.width = width * dpr
        canvas.height = height * dpr
        ctx.scale(dpr, dpr)

        const cx = width / 2
        const cy = height / 2
        const radius = Math.min(cx, cy) - 40
        const count = props.scores.length
        const angleStep = (Math.PI * 2) / count
        // Start from top (-90°)
        const startAngle = -Math.PI / 2

        // Clear
        ctx.clearRect(0, 0, width, height)

        // ---- Grid levels (0%, 25%, 50%, 75%, 100%) ----
        const levels = [0.2, 0.4, 0.6, 0.8, 1.0]
        for (const level of levels) {
          ctx.beginPath()
          for (let i = 0; i <= count; i++) {
            const angle = startAngle + angleStep * i
            const r = radius * level
            const x = cx + r * Math.cos(angle)
            const y = cy + r * Math.sin(angle)
            if (i === 0) ctx.moveTo(x, y)
            else ctx.lineTo(x, y)
          }
          ctx.closePath()
          ctx.strokeStyle = 'rgba(0,0,0,0.08)'
          ctx.lineWidth = 1
          ctx.stroke()
        }

        // ---- Axis lines ----
        for (let i = 0; i < count; i++) {
          const angle = startAngle + angleStep * i
          const x = cx + radius * Math.cos(angle)
          const y = cy + radius * Math.sin(angle)
          ctx.beginPath()
          ctx.moveTo(cx, cy)
          ctx.lineTo(x, y)
          ctx.strokeStyle = 'rgba(0,0,0,0.12)'
          ctx.lineWidth = 1
          ctx.stroke()
        }

        // ---- Data fill ----
        ctx.beginPath()
        for (let i = 0; i <= count; i++) {
          const idx = i % count
          const score = props.scores[idx] || 50
          // Normalize score (t-score 20-80 → 0-1)
          const normalized = Math.max(0, Math.min(1, (score - 20) / 60))
          const angle = startAngle + angleStep * idx
          const r = radius * normalized
          const x = cx + r * Math.cos(angle)
          const y = cy + r * Math.sin(angle)
          if (i === 0) ctx.moveTo(x, y)
          else ctx.lineTo(x, y)
        }
        ctx.closePath()

        // Fill with gradient-like opacity
        const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius)
        gradient.addColorStop(0, 'rgba(123, 47, 247, 0.3)')
        gradient.addColorStop(1, 'rgba(123, 47, 247, 0.1)')
        ctx.fillStyle = gradient
        ctx.fill()

        // Data outline
        ctx.strokeStyle = '#7B2FF7'
        ctx.lineWidth = 2
        ctx.stroke()

        // ---- Data points ----
        for (let i = 0; i < count; i++) {
          const score = props.scores[i] || 50
          const normalized = Math.max(0, Math.min(1, (score - 20) / 60))
          const angle = startAngle + angleStep * i
          const r = radius * normalized
          const x = cx + r * Math.cos(angle)
          const y = cy + r * Math.sin(angle)

          ctx.beginPath()
          ctx.arc(x, y, 4, 0, Math.PI * 2)
          ctx.fillStyle = dimColors[i]
          ctx.fill()
        }

        // ---- Labels ----
        ctx.font = '12px -apple-system, "Helvetica Neue", sans-serif'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'

        for (let i = 0; i < count; i++) {
          const angle = startAngle + angleStep * i
          const labelOffset = 24
          const r = radius + labelOffset
          const x = cx + r * Math.cos(angle)
          const y = cy + r * Math.sin(angle)

          // Adjust text alignment based on position
          if (angle > -Math.PI / 2 + 0.1 && angle < Math.PI / 2 - 0.1) {
            ctx.textAlign = 'left'
          } else if (angle > Math.PI / 2 + 0.1 || angle < -Math.PI / 2 - 0.1) {
            ctx.textAlign = 'right'
          } else {
            ctx.textAlign = 'center'
          }

          ctx.fillStyle = '#666'
          ctx.fillText(props.labels[i] || '', x, y)
        }
      })
  })
}

onMounted(() => {
  draw()
})

watch(() => props.scores, () => {
  draw()
}, { deep: true })
</script>

<style scoped>
.radar-canvas {
  width: 320px;
  height: 320px;
  display: block;
  margin: 0 auto;
}
</style>

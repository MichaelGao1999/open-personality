<template>
  <div ref="chartRef" class="radar-chart-container"></div>
</template>

<script setup>
import { ref, onMounted, watch, shallowRef } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  scores: { type: Object, required: true },
  facetScores: { type: Object, default: () => ({}) },
  lang: { type: String, default: 'zh' },
  friendScores: { type: Object, default: null },
  friendLabel: { type: String, default: '好友' },
})

const chartRef = ref(null)
const chart = shallowRef(null)

const dimLabels = {
  zh: ['开放性 O', '严谨性 C', '外向性 E', '宜人性 A', '神经质 N'],
  en: ['Openness O', 'Conscientiousness C', 'Extraversion E', 'Agreeableness A', 'Neuroticism N'],
}

const dimKeys = ['O', 'C', 'E', 'A', 'N']

function mapScores(source) {
  return dimKeys.map(d => {
    const ts = source?.t_scores?.[d] ?? source?.[d] ?? 50
    return Math.round(ts)
  })
}

const dimColors = [
  '#7B2FF7', // Openness - 亮紫
  '#00B4D8', // Conscientiousness - 电光蓝
  '#FFD60A', // Extraversion - 阳光黄
  '#06D6A0', // Agreeableness - 翡翠绿
  '#FF006E', // Neuroticism - 热力粉
]

function render() {
  if (!chart.value) return
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
  const labels = dimLabels[props.lang] || dimLabels.zh
  const mainValues = mapScores(props.scores)
  const hasFriend = props.friendScores !== null
  const axisColor = isDark ? '#f0f0f5' : '#1A1A2E'
  const splitLineColors = isDark
    ? ['#1e1e30', '#1e1e30', '#151525', '#151525', '#101020']
    : ['#D1D5DB', '#D1D5DB', '#E5E7EB', '#E5E7EB', '#F3F4F6']
  const splitAreaColors = isDark
    ? ['#0d0d14', '#0a0a12', '#080810', '#0d0d14', '#0a0a12']
    : ['#FFFFFF', '#F8F9FF', '#F0F2FF', '#FFFFFF', '#F8F9FF']
  const axisLineColor = isDark ? '#2a2a44' : '#9CA3AF'
  chart.value.setOption({
    radar: {
      indicator: labels.map((name, i) => ({
        name,
        max: 100,
        axisName: {
          color: axisColor,
          fontSize: 13,
          fontWeight: 600,
          fontFamily: 'Inter, sans-serif',
        },
        splitLine: {
          lineStyle: {
            color: splitLineColors,
          }
        },
        splitArea: {
          show: true,
          areaStyle: {
            color: splitAreaColors,
          }
        },
        axisLine: {
          lineStyle: {
            color: axisLineColor,
          }
        }
      })),
      center: ['50%', '50%'],
      radius: '65%',
    },
    series: [
      {
        type: 'radar',
        name: '你',
        data: [{
          value: mainValues,
          name: '你',
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: { width: 2, color: '#7B2FF7' },
          itemStyle: { color: '#7B2FF7', borderColor: '#fff', borderWidth: 2 },
          areaStyle: { color: 'rgba(123, 47, 247, 0.18)' },
        }],
        emphasis: {
          lineStyle: { width: 3 },
          areaStyle: { color: 'rgba(123, 47, 247, 0.28)' },
        },
      },
      ...(hasFriend ? [{
        type: 'radar',
        name: props.friendLabel,
        data: [{
          value: mapScores(props.friendScores),
          name: props.friendLabel,
          symbol: 'square',
          symbolSize: 8,
          lineStyle: { width: 2, type: 'dashed', color: '#FF006E' },
          itemStyle: { color: '#FF006E', borderColor: '#fff', borderWidth: 2 },
          areaStyle: { color: 'rgba(255, 0, 110, 0.12)' },
        }],
        emphasis: {
          lineStyle: { width: 3 },
          areaStyle: { color: 'rgba(255, 0, 110, 0.22)' },
        },
      }] : []),
    ],
    legend: hasFriend ? {
      show: true,
      bottom: 0,
      data: ['你', props.friendLabel],
      textStyle: { color: axisColor, fontSize: 12 },
    } : { show: false },
    tooltip: {
      backgroundColor: isDark ? 'rgba(13, 13, 20, 0.95)' : 'rgba(255, 255, 255, 0.95)',
      borderColor: isDark ? '#2a2a44' : '#E5E7EB',
      borderWidth: 1,
      borderRadius: 12,
      padding: [12, 16],
      textStyle: {
        color: isDark ? '#c0c0d8' : '#1A1A2E',
        fontSize: 14,
      },
    },
  })
}

onMounted(() => {
  chart.value = echarts.init(chartRef.value)
  render()

  const handleResize = () => {
    chart.value?.resize()
  }
  window.addEventListener('resize', handleResize)

  // 监听深色模式切换
  const observer = new MutationObserver(() => {
    chart.value?.dispose()
    chart.value = echarts.init(chartRef.value)
    render()
  })
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] })
})

watch(() => [props.scores, props.friendScores, props.lang], render, { deep: true })
</script>

<style scoped>
.radar-chart-container {
  width: 100%;
  height: 360px;
  animation: fadeInUp 0.5s var(--ease-bounce);
}
</style>

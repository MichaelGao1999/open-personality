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
})

const chartRef = ref(null)
const chart = shallowRef(null)

const dimLabels = {
  zh: ['开放性 O', '严谨性 C', '外向性 E', '宜人性 A', '神经质 N'],
  en: ['Openness O', 'Conscientiousness C', 'Extraversion E', 'Agreeableness A', 'Neuroticism N'],
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
  const labels = dimLabels[props.lang] || dimLabels.zh
  const scores = ['O', 'C', 'E', 'A', 'N'].map((d) => {
    const ts = props.scores?.t_scores?.[d] ?? props.scores?.[d] ?? 50
    return Math.round(ts)
  })
  chart.value.setOption({
    radar: {
      indicator: labels.map((name, i) => ({
        name,
        max: 100,
        axisName: {
          color: '#1A1A2E',
          fontSize: 13,
          fontWeight: 600,
        },
        splitLine: {
          lineStyle: {
            color: ['#F1F5F9', '#E5E7EB', '#D1D5DB', '#9CA3AF', '#6B7280'].reverse(),
          }
        },
        splitArea: {
          show: true,
          areaStyle: {
            color: ['#FAFAFA', '#F9FAFB', '#F3F4F6', '#FEFEFE', '#FFFFFF'],
          }
        },
        axisLine: {
          lineStyle: {
            color: '#E5E7EB',
          }
        }
      })),
      center: ['50%', '50%'],
      radius: '65%',
    },
    series: [{
      type: 'radar',
      data: [{
        value: scores,
        name: 'Big Five',
        symbol: 'circle',
        symbolSize: 10,
        lineStyle: {
          width: 3,
          color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
            { offset: 0, color: '#7B2FF7' },
            { offset: 0.25, color: '#00B4D8' },
            { offset: 0.5, color: '#FFD60A' },
            { offset: 0.75, color: '#06D6A0' },
            { offset: 1, color: '#FF006E' },
          ]),
        },
        itemStyle: {
          color: '#FF006E',
          borderColor: '#fff',
          borderWidth: 2,
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(123, 47, 247, 0.25)' },
            { offset: 0.5, color: 'rgba(0, 180, 216, 0.15)' },
            { offset: 1, color: 'rgba(255, 0, 110, 0.05)' },
          ]),
        },
      }],
      emphasis: {
        lineStyle: {
          width: 4,
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(123, 47, 247, 0.35)' },
            { offset: 1, color: 'rgba(255, 0, 110, 0.1)' },
          ]),
        },
      },
    }],
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#E5E7EB',
      borderWidth: 1,
      borderRadius: 12,
      padding: [12, 16],
      textStyle: {
        color: '#1A1A2E',
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
})

watch(() => [props.scores, props.lang], render, { deep: true })
</script>

<style scoped>
.radar-chart-container {
  width: 100%;
  height: 360px;
  animation: fadeInUp 0.5s var(--ease-bounce);
}
</style>

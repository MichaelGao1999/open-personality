<template>
  <div ref="chartRef" style="width: 100%; height: 360px"></div>
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

function render() {
  if (!chart.value) return
  const labels = dimLabels[props.lang] || dimLabels.zh
  const scores = ['O', 'C', 'E', 'A', 'N'].map((d) => {
    const ts = props.scores?.t_scores?.[d] ?? props.scores?.[d] ?? 50
    return Math.round(ts)
  })
  chart.value.setOption({
    radar: {
      indicator: labels.map((name, i) => ({ name, max: 100 })),
      center: ['50%', '50%'],
      radius: '65%',
    },
    series: [{
      type: 'radar',
      data: [{ value: scores, name: 'Big Five' }],
      areaStyle: { opacity: 0.2 },
      lineStyle: { width: 2 },
    }],
  })
}

onMounted(() => {
  chart.value = echarts.init(chartRef.value)
  render()
})

watch(() => [props.scores, props.lang], render, { deep: true })
</script>

import { ref } from 'vue'
import { getItems, submitAnswers, getReport, getI18n } from '../utils/api'

export function useApi() {
  const loading = ref(false)
  const error = ref(null)

  function wrap(fn) {
    return async (...args) => {
      loading.value = true
      error.value = null
      try {
        const res = await fn(...args)
        return res.data
      } catch (e) {
        const detail = e.response?.data?.detail
        error.value = typeof detail === 'string' ? detail : (detail?.detail || 'An error occurred')
        throw e
      } finally {
        loading.value = false
      }
    }
  }

  return {
    loading,
    error,
    fetchItems: wrap(getItems),
    submit: wrap(submitAnswers),
    fetchReport: wrap(getReport),
    fetchI18n: wrap(getI18n),
  }
}

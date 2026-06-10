import { computed, reactive } from 'vue'

const state = reactive({
  lang: 'zh',
  strings: {},
})

export function useI18n() {
  async function setLang(lang) {
    state.lang = lang
    try {
      const module = await import(`../i18n/${lang}.json`)
      state.strings = module.default
    } catch {
      state.strings = {}
    }
  }

  function t(key) {
    return state.strings[key] || key
  }

  if (!state.strings || Object.keys(state.strings).length === 0) {
    setLang('zh')
  }

  return {
    lang: computed(() => state.lang),
    t,
    setLang,
  }
}

import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

export function getItems(mode, lang) {
  return client.get('/questionnaires/items', { params: { mode, lang } })
}

export function submitAnswers(mode, lang, answers) {
  return client.post('/questionnaires/submit', { mode, lang, answers })
}

export function getReport(shareToken) {
  return client.get(`/report/${shareToken}`)
}

export function getI18n(lang) {
  return client.get(`/i18n/${lang}`)
}

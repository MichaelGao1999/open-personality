import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

export function getItems(mode, lang) {
  return client.get('/questionnaires/items', { params: { mode, lang } })
}

export function submitAnswers(mode, lang, answers, status = 'complete', sessionId = null) {
  const body = { mode, lang, answers, status }
  if (sessionId) body.session_id = sessionId
  return client.post('/questionnaires/submit', body)
}

export function resumeSession(shareToken) {
  return client.get(`/questionnaires/resume/${shareToken}`)
}

export function getReport(shareToken) {
  return client.get(`/report/${shareToken}`)
}

export function getI18n(lang) {
  return client.get(`/i18n/${lang}`)
}

export function submitFeedback(type, content) {
  return client.post('/api/feedback', { type, content })
}

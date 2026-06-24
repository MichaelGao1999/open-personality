/**
 * API 封装 — 基于 uni.request
 * 与 web 版共享相同后端接口
 */

// 后端地址
const BASE_URL = 'https://localhost:8000'

function buildUrl(path, params) {
  if (!params) return BASE_URL + path
  const qs = Object.entries(params)
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&')
  return BASE_URL + path + '?' + qs
}

function request(method, path, data) {
  return new Promise((resolve, reject) => {
    const url = method === 'GET' ? buildUrl(path, data) : BASE_URL + path
    uni.request({
      url,
      method,
      data: method === 'GET' ? undefined : data,
      dataType: 'json',
      header: { 'Content-Type': 'application/json' },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          reject(new Error(`API Error ${res.statusCode}: ${JSON.stringify(res.data)}`))
        }
      },
      fail: (err) => {
        reject(new Error(`Network Error: ${err.errMsg}`))
      },
    })
  })
}

/** 获取题目列表 */
export function getItems(mode, lang) {
  return request('GET', '/questionnaires/items', { mode, lang })
}

/** 提交答案 */
export function submitAnswers(mode, lang, answers, status = 'complete', sessionId = null) {
  const body = { mode, lang, answers, status }
  if (sessionId) body.session_id = sessionId
  return request('POST', '/questionnaires/submit', body)
}

/** 续答 */
export function resumeSession(shareToken) {
  return request('GET', `/questionnaires/resume/${shareToken}`)
}

/** 获取报告 */
export function getReport(shareToken) {
  return request('GET', `/report/${shareToken}`)
}

/** 获取 i18n 数据 */
export function getI18n(lang) {
  return request('GET', `/i18n/${lang}`)
}

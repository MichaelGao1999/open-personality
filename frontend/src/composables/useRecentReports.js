import { reactive } from 'vue'

const STORAGE_KEY = 'open_personality_recent'
const MAX_ITEMS = 5

function load() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  } catch {
    return []
  }
}

function save(items) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
}

export function useRecentReports() {
  const reports = reactive(load())

  function add(report) {
    reports.unshift({
      session_id: report.session_id,
      share_token: report.share_token,
      mode: report.mode,
      lang: report.lang,
      created_at: report.created_at,
    })
    while (reports.length > MAX_ITEMS) {
      reports.pop()
    }
    save([...reports])
  }

  function remove(token) {
    const idx = reports.findIndex((r) => r.share_token === token)
    if (idx !== -1) {
      reports.splice(idx, 1)
      save([...reports])
    }
  }

  return { reports, add, remove }
}

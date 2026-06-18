import { invoke } from '@tauri-apps/api/core'

// ── 日报 ──
export const reportApi = {
  getDates: () => invoke('get_report_dates'),
  get: (date) => invoke('get_report', { date }),
  save: (date, data) => invoke('save_report', { date, columns: data.columns, rows: data.rows }),
  delete: (date) => invoke('delete_report', { date }),
}

// ── 待办 ──
export const todoApi = {
  list: (status) => invoke('get_todos', { status }),
  create: (data) => invoke('create_todo', data),
  update: (id, data) => invoke('update_todo', { id, ...data }),
  delete: (id) => invoke('delete_todo', { id }),
}

// ── 笔记 ──
export const noteApi = {
  list: () => invoke('get_notes'),
  get: (id) => invoke('get_note', { id }),
  create: (data) => invoke('create_note', data),
  update: (id, data) => invoke('update_note', { id, ...data }),
  delete: (id) => invoke('delete_note', { id }),
  reorder: (ids) => invoke('reorder_notes', { ids }),
}

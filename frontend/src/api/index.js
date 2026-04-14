import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// ── 日报 ──
export const reportApi = {
  getDates: () => http.get('/reports/dates'),
  get: (date) => http.get(`/reports/${date}`),
  save: (date, data) => http.put(`/reports/${date}`, data),
  delete: (date) => http.delete(`/reports/${date}`),
}

// ── 待办 ──
export const todoApi = {
  list: (status) => http.get('/todos', { params: { status } }),
  create: (data) => http.post('/todos', data),
  update: (id, data) => http.put(`/todos/${id}`, data),
  delete: (id) => http.delete(`/todos/${id}`),
}

// ── 笔记 ──
export const noteApi = {
  list: () => http.get('/notes'),
  get: (id) => http.get(`/notes/${id}`),
  create: (data) => http.post('/notes', data),
  update: (id, data) => http.put(`/notes/${id}`, data),
  delete: (id) => http.delete(`/notes/${id}`),
}

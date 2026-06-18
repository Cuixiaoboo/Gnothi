import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ReportView from '../views/ReportView.vue'
import TodoView from '../views/TodoView.vue'
import NotesView from '../views/NotesView.vue'
import SettingsView from '../views/SettingsView.vue'
import ToolsView from '../views/ToolsView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/report', name: 'report', component: ReportView },
  { path: '/todo', name: 'todo', component: TodoView },
  { path: '/notes', name: 'notes', component: NotesView },
  { path: '/tools', name: 'tools', component: ToolsView },
  { path: '/settings', name: 'settings', component: SettingsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

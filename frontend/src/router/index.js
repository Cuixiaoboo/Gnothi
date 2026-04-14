import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ReportView from '../views/ReportView.vue'
import TodoView from '../views/TodoView.vue'
import NotesView from '../views/NotesView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/report', name: 'report', component: ReportView },
  { path: '/todo', name: 'todo', component: TodoView },
  { path: '/notes', name: 'notes', component: NotesView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

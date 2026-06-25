<template>
  <div class="view-wrapper">
    <div class="page-header">
      <div class="page-title">征服清单</div>
      <span class="count">{{ filteredTodos.length }} 项</span>
    </div>
    <div class="page-body">
      <div class="todo-layout">
        <TodoFilters :active="filter" @change="filter = $event" />
        <TodoAdd @add="addTodo" />
        <div class="todo-list">
          <TodoItem
            v-for="todo in filteredTodos"
            :key="todo.id"
            :todo="todo"
            :editing="editingId === todo.id"
            @toggle="toggleStatus"
            @edit="editingId = editingId === todo.id ? null : todo.id"
            @update="updateField"
            @delete="deleteTodo"
          />
          <div class="empty" v-if="filteredTodos.length === 0">
            <div class="empty-icon">✅</div>
            <p>{{ filter === 'all' ? '暂无征服清单' : '没有符合条件的待办' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { todoApi } from '../api'
import TodoFilters from '../components/todo/TodoFilters.vue'
import TodoAdd from '../components/todo/TodoAdd.vue'
import TodoItem from '../components/todo/TodoItem.vue'

const showToast = inject('showToast')
const showConfirm = inject('showConfirm')

const todos = ref([])
const filter = ref('all')
const editingId = ref(null)

const filteredTodos = computed(() => {
  if (filter.value === 'all') return todos.value
  return todos.value.filter((t) => t.status === filter.value)
})

async function loadTodos() {
  try {
    const data = await todoApi.list()
    todos.value = data
  } catch (e) {
    console.error(e)
  }
}

async function addTodo({ title, priority }) {
  // if (!title.trim()) return
  try {
    const data = await todoApi.create({ title, priority })
    todos.value.unshift(data)
    showToast('已添加待办')
  } catch {
    showToast('添加失败', 'error')
  }
}

async function toggleStatus(todo) {
  const newStatus = todo.status === 'completed' ? 'pending' : 'completed'
  try {
    const data = await todoApi.update(todo.id, { status: newStatus })
    const idx = todos.value.findIndex((t) => t.id === todo.id)
    if (idx >= 0) todos.value[idx] = data
  } catch {
    showToast('更新失败', 'error')
  }
}

let updateTimer = null
async function updateField(id, field, value) {
  const idx = todos.value.findIndex((t) => t.id === id)
  if (idx >= 0) todos.value[idx][field] = value
  clearTimeout(updateTimer)
  updateTimer = setTimeout(async () => {
    try {
      const data = await todoApi.update(id, { [field]: value })
      const i = todos.value.findIndex((t) => t.id === id)
      if (i >= 0) todos.value[i] = data
    } catch {
      showToast('更新失败', 'error')
    }
  }, 500)
}

async function deleteTodo(id) {
  const ok = await showConfirm('确定删除此待办吗？')
  if (!ok) return
  try {
    await todoApi.delete(id)
    todos.value = todos.value.filter((t) => t.id !== id)
    if (editingId.value === id) editingId.value = null
    showToast('已删除')
  } catch {
    showToast('删除失败', 'error')
  }
}

onMounted(loadTodos)
</script>

<style scoped>
.view-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.page-header {
  padding: 20px 28px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.count {
  font-size: 13px;
  color: var(--text-muted);
}

.page-body {
  flex: 1;
  overflow: auto;
  padding: 20px 28px 28px;
}

.todo-layout {
  width: 100%;
  max-width: 100%;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>

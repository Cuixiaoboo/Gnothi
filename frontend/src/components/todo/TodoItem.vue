<template>
  <div class="todo-item" :class="{ completed: todo.status === 'completed' }">
    <button
      class="todo-check"
      :class="{ checked: todo.status === 'completed' }"
      @click="$emit('toggle', todo)"
    ></button>
    <div class="todo-body">
      <div class="todo-title">{{ todo.title }}</div>
      <div class="todo-meta">
        <span class="badge" :class="'badge-' + todo.priority">{{ priorityLabel }}</span>
        <span class="badge" :class="'badge-' + todo.status">{{ statusLabel }}</span>
        <span v-if="todo.due_date">📅 截止日期 {{ todo.due_date }}</span>
        <!-- <span v-if="todo.completed_at">✓ {{ formatDate(todo.completed_at) }}</span> -->
      </div>
      <div class="todo-time-row">
        <span class="time-tag">🕐 创建: {{ formatDate(todo.created_at) }}</span>
        <span class="time-tag" v-if="todo.completed_at"
          >✅ 完成: {{ formatDate(todo.completed_at) }}</span
        >
      </div>
      <div class="todo-detail" v-if="editing">
        <div class="todo-detail-row">
          <select
            :value="todo.status"
            @change="$emit('update', todo.id, 'status', $event.target.value)"
          >
            <option value="hangup">挂起</option>
            <option value="pending">待处理</option>
            <option value="in_progress">进行中</option>
            <option value="completed">已完成</option>
          </select>
          <select
            :value="todo.priority"
            @change="$emit('update', todo.id, 'priority', $event.target.value)"
          >
            <option value="high">高优先级</option>
            <option value="medium">中优先级</option>
            <option value="low">低优先级</option>
          </select>
          <input
            type="date"
            :value="todo.due_date"
            @change="$emit('update', todo.id, 'due_date', $event.target.value)"
          />
        </div>
        <textarea
          :value="todo.notes"
          @input="$emit('update', todo.id, 'notes', $event.target.value)"
          placeholder="备注..."
          rows="2"
        ></textarea>
      </div>
    </div>
    <div class="todo-actions">
      <button class="btn-icon" @click="$emit('edit', todo.id)" title="编辑">
        <svg
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
        </svg>
      </button>
      <button class="btn-icon danger" @click="$emit('delete', todo.id)" title="删除">
        <svg
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <polyline points="3 6 5 6 21 6" />
          <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
          <path d="M10 11v6" />
          <path d="M14 11v6" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  todo: Object,
  editing: Boolean,
})
defineEmits(['toggle', 'edit', 'update', 'delete'])

const priorityLabel = computed(() => ({ high: '高', medium: '中', low: '低' })[props.todo.priority])
const statusLabel = computed(
  () =>
    ({ hangup: '挂起', pending: '待处理', in_progress: '进行中', completed: '已完成' })[
      props.todo.status
    ],
)

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getMonth() + 1}月${d.getDate()}日 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}
</script>

<style scoped>
.todo-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  transition: all 0.15s;
}

.todo-item:hover {
  border-color: var(--border-light);
}

.todo-check {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid var(--border-light);
  cursor: pointer;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
  background: transparent;
  margin-top: 2px;
}

.todo-check:hover {
  border-color: var(--accent);
}

.todo-check.checked {
  background: var(--green);
  border-color: var(--green);
}

.todo-check.checked::after {
  content: '✓';
  color: #fff;
  font-size: 12px;
  font-weight: 700;
}

.todo-body {
  flex: 1;
  min-width: 0;
}

.todo-title {
  font-weight: 500;
  color: var(--text);
  word-break: break-word;
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
  color: var(--text-muted);
}

.todo-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 4px;
  font-size: 12px;
  color: var(--text-muted);
  flex-wrap: wrap;
}

.todo-time-row {
  display: flex;
  gap: 12px;
  margin-top: 4px;
  flex-wrap: wrap;
}

.time-tag {
  font-size: 11px;
  color: var(--text-muted);
  font-family: var(--mono);
}

.todo-actions {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}

.todo-detail {
  margin-top: 8px;
  padding: 12px;
  background: var(--bg-surface-2);
  border-radius: var(--radius);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.todo-detail textarea {
  min-height: 60px;
  font-size: 13px;
}

.todo-detail select,
.todo-detail input {
  font-size: 13px;
}

.todo-detail-row {
  display: flex;
  gap: 8px;
}

.todo-detail-row > * {
  flex: 1;
}
</style>

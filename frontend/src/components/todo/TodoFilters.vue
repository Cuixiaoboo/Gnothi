<template>
  <div class="todo-filters">
    <button
      v-for="f in filters"
      :key="f.value"
      class="filter-btn"
      :class="{ active: active === f.value }"
      @click="$emit('change', f.value)"
    >
      {{ f.label }}
    </button>
  </div>
</template>

<script setup>
defineProps({ active: String })
defineEmits(['change'])

const filters = [
  { value: 'all', label: '全部' },
  { value: 'hangup', label: '挂起' },
  { value: 'pending', label: '待处理' },
  { value: 'in_progress', label: '进行中' },
  { value: 'completed', label: '已完成' },
]
</script>

<style scoped>
.todo-filters {
  display: flex;
  gap: 6px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-sec);
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s;
}

.filter-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.filter-btn.active {
  background: var(--accent-bg);
  color: var(--accent);
  border-color: var(--accent);
}
</style>


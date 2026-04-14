<template>
  <div class="todo-add">
    <input
      type="text"
      v-model="title"
      placeholder="添加新待办..."
      @keydown.enter="submit"
    />
    <select v-model="priority" class="priority-select">
      <option value="high">高</option>
      <option value="medium">中</option>
      <option value="low">低</option>
    </select>
    <button class="btn btn-primary" @click="submit">添加</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['add'])

const title = ref('')
const priority = ref('medium')

function submit() {
  emit('add', { title: title.value, priority: priority.value })
  title.value = ''
}
</script>

<style scoped>
.todo-add {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.todo-add input {
  flex: 1;
}

.priority-select {
  width: 90px;
  flex-shrink: 0;
}
</style>

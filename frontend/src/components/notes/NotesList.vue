<template>
  <div class="notes-list">
    <div class="notes-search">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
      <input
        type="search"
        :value="search"
        @input="$emit('search', $event.target.value)"
        placeholder="搜索笔记..."
      />
    </div>
    <div class="notes-items">
      <div
        v-for="note in notes"
        :key="note.id"
        class="note-card"
        :class="{ active: selectedId === note.id }"
        @click="$emit('select', note.id)"
      >
        <div class="note-card-title">{{ note.title || '无标题' }}</div>
        <div class="note-card-preview">{{ (note.content || '').slice(0, 60) || '空笔记' }}</div>
        <div class="note-card-date">{{ formatDate(note.updated_at) }}</div>
      </div>
      <div class="empty" v-if="notes.length === 0" style="padding: 30px 10px">
        <p>{{ search ? '没有匹配的笔记' : '点击「新建笔记」开始' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  notes: Array,
  selectedId: Number,
  search: String,
})
defineEmits(['select', 'search'])

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getMonth() + 1}月${d.getDate()}日 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}
</script>

<style scoped>
.notes-list {
  width: 260px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.notes-search {
  position: relative;
}

.notes-search input {
  padding-left: 32px;
}

.notes-search svg {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  color: var(--text-muted);
}

.notes-items {
  flex: 1;
  overflow: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.note-card {
  padding: 12px;
  border-radius: var(--radius);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.15s;
}

.note-card:hover {
  background: var(--bg-hover);
}

.note-card.active {
  background: var(--bg-active);
  border-color: var(--border-light);
}

.note-card-title {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-card-preview {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-card-date {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 4px;
  font-family: var(--mono);
}

@media (max-width: 768px) {
  .notes-list {
    width: 100%;
    max-height: 200px;
  }
}
</style>

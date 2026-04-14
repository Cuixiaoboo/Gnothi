<template>
  <div class="note-editor" v-if="note">
    <div class="note-editor-header">
      <input
        type="text"
        :value="note.title"
        @input="$emit('update', 'title', $event.target.value)"
        placeholder="笔记标题..."
      />
      <button class="btn-icon danger" @click="$emit('delete', note.id)" title="删除笔记">
        <svg
          width="16"
          height="16"
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
    <div class="note-editor-body">
      <textarea
        :value="note.content"
        @input="$emit('update', 'content', $event.target.value)"
        placeholder="开始编写笔记..."
      ></textarea>
    </div>
    <div class="note-editor-footer">
      <span>{{ (note.content || '').length }} 字</span>
      <span>{{ formatDate(note.updated_at) }}</span>
    </div>
  </div>
  <div class="note-editor empty-state" v-else>
    <div class="empty">
      <div class="empty-icon">📝</div>
      <p>选择或创建一篇笔记</p>
    </div>
  </div>
</template>

<script setup>
defineProps({ note: Object })
defineEmits(['update', 'delete'])

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getMonth() + 1}月${d.getDate()}日 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}
</script>

<style scoped>
.note-editor {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.note-editor.empty-state {
  align-items: center;
  justify-content: center;
}

.note-editor-header {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 10px;
}

.note-editor-header input {
  flex: 1;
  font-size: 18px;
  font-weight: 700;
  background: transparent;
  border: none;
  color: var(--text);
  padding: 0;
  outline: none;
}

.note-editor-header input::placeholder {
  color: var(--text-muted);
}

.note-editor-body {
  flex: 1;
}

.note-editor-body textarea {
  width: 100%;
  height: 100%;
  border: none;
  background: transparent;
  color: var(--text);
  padding: 16px;
  resize: none;
  outline: none;
  line-height: 1.8;
  font-size: 14px;
}

.note-editor-footer {
  padding: 8px 16px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
}
</style>

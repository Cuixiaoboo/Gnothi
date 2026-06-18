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
      <draggable
        v-model="localNotes"
        item-key="id"
        ghost-class="ghost"
        :animation="150"
        force-fallback="true"
        fallback-class="dragging"
        scroll-sensitivity="80"
        scroll-speed="10"
        @end="onDragEnd"
      >
        <template #item="{ element, index }">
          <div
            class="note-card"
            :class="{ active: selectedId === element.id }"
            @click="$emit('select', element.id)"
          >
            <div class="drag-handle">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                <circle cx="9" cy="6" r="1.5" />
                <circle cx="15" cy="6" r="1.5" />
                <circle cx="9" cy="12" r="1.5" />
                <circle cx="15" cy="12" r="1.5" />
                <circle cx="9" cy="18" r="1.5" />
                <circle cx="15" cy="18" r="1.5" />
              </svg>
            </div>
            <div class="note-card-body">
              <div class="note-card-title">{{ element.title || '无标题' }}</div>
              <div class="note-card-preview">
                {{ (element.content || '').slice(0, 60) || '空笔记' }}
              </div>
              <div class="note-card-date">{{ formatDate(element.updated_at) }}</div>
            </div>
          </div>
        </template>
      </draggable>
      <div class="empty" v-if="localNotes.length === 0" style="padding: 30px 10px">
        <p>{{ search ? '没有匹配的笔记' : '点击「新建笔记」开始' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import draggable from 'vuedraggable'

const props = defineProps({
  notes: {
    type: Array,
    default: () => []
  },
  selectedId: Number,
  search: String,
})

const emit = defineEmits(['select', 'search', 'reorder'])

// 创建本地副本供 draggable 的 v-model 绑定
const localNotes = ref([])

// 监听 props.notes 变化，同步到本地
watch(
  () => props.notes,
  (val) => {
    localNotes.value = [...val]
  },
  { immediate: true, deep: true },
)

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getMonth() + 1}月${d.getDate()}日 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function onDragEnd() {
  // 拖拽完成，把新顺序的 id 数组交给父组件
  emit(
    'reorder',
    localNotes.value.map((n) => n.id),
  )
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
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.note-card:hover {
  background: var(--bg-hover);
}

.note-card.active {
  background: var(--bg-active);
  border-color: var(--border-light);
}

/* 拖拽手柄 */
.drag-handle {
  flex-shrink: 0;
  cursor: grab;
  color: var(--text-muted);
  opacity: 0;
  padding: 2px 0;
  user-select: none;
}

.note-card:hover .drag-handle {
  opacity: 0.6;
}

.drag-handle:hover {
  opacity: 1 !important;
}

.drag-handle:active {
  cursor: grabbing;
}

.note-card-body {
  flex: 1;
  min-width: 0;
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

/* 拖拽占位符 */
.ghost {
  opacity: 0.4;
  background: var(--bg-active);
  border: 1px dashed var(--border-light);
}

/* 拖拽中的元素 */
.dragging {
  opacity: 0.9;
  background: var(--bg-surface);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .notes-list {
    width: 100%;
    max-height: 200px;
  }
}
</style>

<template>
  <div class="note-editor" v-if="note">
    <div class="note-editor-header">
      <input
        type="text"
        :value="note.title"
        @input="$emit('update', 'title', $event.target.value)"
        placeholder="笔记标题..."
      />
      <div class="header-search" v-if="showSearch">
        <input
          ref="searchInput"
          v-model="keyword"
          type="text"
          placeholder="搜索..."
          class="header-search-field"
          @keydown.enter.prevent="navigateNext"
          @keydown.shift.enter.prevent="navigatePrev"
          @keydown.esc="closeSearch"
        />
        <span class="match-count" v-if="keyword">
          {{ matchCount > 0 ? `${currentMatchIndex + 1}/${matchCount}` : '无' }}
        </span>
        <button class="btn-icon xs" @click="navigatePrev" :disabled="!matchCount" title="上一个">
          <svg
            width="12"
            height="12"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <polyline points="18 15 12 9 6 15" />
          </svg>
        </button>
        <button class="btn-icon xs" @click="navigateNext" :disabled="!matchCount" title="下一个">
          <svg
            width="12"
            height="12"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </button>
        <button class="btn-icon xs" @click="closeSearch" title="关闭">
          <svg
            width="12"
            height="12"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
      <button
        class="btn-icon"
        :class="{ active: showSearch }"
        @click="toggleSearch"
        title="查找 (Ctrl+F)"
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      </button>
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

    <!-- 编辑区 -->
    <div class="note-editor-body">
      <pre
        ref="backdrop"
        class="backdrop"
        aria-hidden="true"
        v-if="keyword && matchCount > 0"
      ><template v-for="(line, li) in highlightedLines" :key="li"><template v-if="li > 0">
</template><template v-for="(seg, si) in line" :key="si"><span v-if="seg.type === 'match'" class="match">{{ seg.text }}</span><span v-else-if="seg.type === 'current'" class="current">{{ seg.text }}</span><template v-else>{{ seg.text }}</template></template></template></pre>
      <textarea
        ref="textarea"
        :value="note.content"
        @input="onInput"
        @scroll="syncScroll"
        @keydown.ctrl.f.prevent="toggleSearch"
        placeholder="开始编写笔记..."
      ></textarea>
    </div>

    <div class="note-editor-footer">
      <span>{{ (note.content || '').length }} 字</span>
      <span v-if="keyword && matchCount > 0">找到 {{ matchCount }} 处匹配</span>
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
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({ note: Object })
const emit = defineEmits(['update', 'delete'])

const showSearch = ref(false)
const keyword = ref('')
const caseSensitive = ref(false)
const currentMatchIndex = ref(0)
const searchInput = ref(null)
const textarea = ref(null)
const backdrop = ref(null)

const matches = computed(() => {
  if (!keyword.value || !props.note?.content) return []
  const text = props.note.content
  const kw = caseSensitive.value ? keyword.value : keyword.value.toLowerCase()
  const src = caseSensitive.value ? text : text.toLowerCase()
  const result = []
  let pos = 0
  while ((pos = src.indexOf(kw, pos)) !== -1) {
    result.push(pos)
    pos += 1
  }
  return result
})

const matchCount = computed(() => matches.value.length)

watch(keyword, () => {
  currentMatchIndex.value = 0
})

const highlightedLines = computed(() => {
  if (!keyword.value || !props.note?.content) return []
  const text = props.note.content
  const kw = keyword.value
  const kwLen = kw.length
  const m = matches.value
  if (m.length === 0) return [[{ text, type: 'plain' }]]

  const rawSegments = []
  let lastEnd = 0
  for (let i = 0; i < m.length; i++) {
    const start = m[i]
    if (start > lastEnd) {
      rawSegments.push({ text: text.slice(lastEnd, start), type: 'plain' })
    }
    rawSegments.push({
      text: text.slice(start, start + kwLen),
      type: i === currentMatchIndex.value ? 'current' : 'match',
    })
    lastEnd = start + kwLen
  }
  if (lastEnd < text.length) {
    rawSegments.push({ text: text.slice(lastEnd), type: 'plain' })
  }

  const lines = [[]]
  for (const seg of rawSegments) {
    const parts = seg.text.split('\n')
    for (let i = 0; i < parts.length; i++) {
      if (i > 0) lines.push([])
      if (parts[i]) {
        lines[lines.length - 1].push({ text: parts[i], type: seg.type })
      }
    }
  }
  return lines
})


function syncScroll() {
  if (!textarea.value || !backdrop.value) return
  backdrop.value.scrollTop = textarea.value.scrollTop
  backdrop.value.scrollLeft = textarea.value.scrollLeft
}

function navigateNext() {
  if (!matchCount.value) return
  currentMatchIndex.value = (currentMatchIndex.value + 1) % matchCount.value
  scrollToCurrent()
}

function navigatePrev() {
  if (!matchCount.value) return
  currentMatchIndex.value = (currentMatchIndex.value - 1 + matchCount.value) % matchCount.value
  scrollToCurrent()
}

function scrollToCurrent() {
  nextTick(() => {
    if (!backdrop.value || !textarea.value) return
    const el = backdrop.value.querySelector('.current')
    if (el) {
      const viewH = textarea.value.clientHeight
      const elTop =
        el.getBoundingClientRect().top -
        backdrop.value.getBoundingClientRect().top +
        backdrop.value.scrollTop
      textarea.value.scrollTop = elTop - viewH / 2 + el.offsetHeight / 2
      syncScroll()
    }
  })
}

function toggleSearch() {
  showSearch.value = !showSearch.value
  if (showSearch.value) {
    nextTick(() => searchInput.value?.focus())
  } else {
    keyword.value = ''
  }
}

function closeSearch() {
  showSearch.value = false
  keyword.value = ''
  textarea.value?.focus()
}

function onInput(e) {
  emit('update', 'content', e.target.value)
}

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

/* ---- Header ---- */
.note-editor-header {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 8px;
}

.note-editor-header > input[type='text'] {
  flex: 1;
  font-size: 18px;
  font-weight: 700;
  background: transparent;
  border: none;
  color: var(--text);
  padding: 0;
  outline: none;
  min-width: 0;
}

.note-editor-header > input[type='text']::placeholder {
  color: var(--text-muted);
}

/* ---- Header 搜索框 ---- */
.header-search {
  display: flex;
  align-items: center;
  gap: 4px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1px 6px;
  animation: slideIn 0.15s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.header-search-field {
  width: 140px;
  font-size: 13px;
  border: none;
  background: transparent;
  color: var(--text);
  outline: none;
  padding: 4px 0;
}

.header-search-field::placeholder {
  color: var(--text-muted);
}

.match-count {
  font-size: 11px;
  color: var(--text-muted);
  white-space: nowrap;
  padding: 0 2px;
}

/* ---- 编辑区 ---- */
.note-editor-body {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.backdrop {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  overflow: hidden;
  margin: 0;
  padding: 16px;
  border: none;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.8;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
  tab-size: 4;
  box-sizing: border-box;
  scrollbar-gutter: stable;
  color: var(--text);
}

.note-editor-body textarea {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  border: none;
  background: transparent;
  caret-color: var(--text);
  padding: 16px;
  resize: none;
  outline: none;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.8;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
  tab-size: 4;
  box-sizing: border-box;
  scrollbar-gutter: stable;
}

/* 高亮样式 */
.match {
  background: rgba(255, 213, 0, 0.35);
  border-radius: 2px;
}

.current {
  background: rgba(255, 170, 0, 0.7);
  border-radius: 2px;
  outline: 1px solid rgba(255, 170, 0, 0.9);
}

/* ---- Footer ---- */
.note-editor-footer {
  padding: 8px 16px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
}

/* ---- 按钮通用 ---- */
.btn-icon {
  padding: 6px;
  border-radius: var(--radius);
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
  flex-shrink: 0;
}

.btn-icon:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.btn-icon.active {
  background: var(--bg-active);
  color: var(--accent);
}

.btn-icon.danger:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.btn-icon.xs {
  padding: 3px;
}

.btn-icon.xs:hover:not(:disabled) {
  background: var(--bg-active);
  color: var(--text);
}

.btn-icon.xs:disabled {
  opacity: 0.3;
  cursor: default;
}
</style>

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

    <!-- Block 编辑器 -->
    <div class="note-editor-body">
      <BlockEditor v-model="editorContent" />
    </div>

    <div class="note-editor-footer">
      <span>{{ wordCount }} 字</span>
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
import { ref, computed, watch } from 'vue'
import BlockEditor from './BlockEditor.vue'

const props = defineProps({ note: Object })
const emit = defineEmits(['update', 'delete'])

// 默认的空文档结构
const emptyDoc = {
  type: 'doc',
  content: [
    { type: 'paragraph' }
  ]
}

// 将纯文本转换为 Block 结构
function textToDoc(text) {
  if (!text || text.trim() === '') {
    return emptyDoc
  }
  
  // 尝试解析 JSON
  try {
    const parsed = JSON.parse(text)
    if (parsed.type === 'doc') {
      return parsed
    }
  } catch {
    // 不是 JSON，按 Markdown 格式处理
  }
  
  // 解析 Markdown 格式
  const lines = text.split('\n')
  const content = []
  let i = 0
  
  while (i < lines.length) {
    const line = lines[i]
    
    // 检查是否是标题
    const headingMatch = line.match(/^(#{1,3})\s+(.+)/)
    if (headingMatch) {
      const level = headingMatch[1].length
      const text = headingMatch[2]
      content.push({
        type: 'heading',
        attrs: { level },
        content: [{ type: 'text', text }]
      })
      i++
      continue
    }
    
    // 检查是否是代码块开始
    const codeBlockMatch = line.match(/^```(\w*)/)
    if (codeBlockMatch) {
      const language = codeBlockMatch[1] || ''
      const codeLines = []
      i++
      // 读取代码块内容直到结束标记
      while (i < lines.length && !lines[i].startsWith('```')) {
        // 反转义代码块内容中的结束标记
        let codeLine = lines[i]
        codeLine = codeLine.replace(/\\`\\`\\`/g, '```')
        codeLines.push(codeLine)
        i++
      }
      i++ // 跳过结束标记 ```
      content.push({
        type: 'codeBlock',
        attrs: { language },
        content: [{ type: 'text', text: codeLines.join('\n') }]
      })
      continue
    }
    
    // 普通段落
    content.push({
      type: 'paragraph',
      content: line ? [{ type: 'text', text: line }] : []
    })
    i++
  }
  
  return {
    type: 'doc',
    content: content.length > 0 ? content : [{ type: 'paragraph' }]
  }
}

// 将 Block 结构转换为纯文本（用于存储）
function docToText(doc) {
  if (!doc || !doc.content) return ''
  
  const lines = []
  for (const node of doc.content) {
    if (node.type === 'paragraph') {
      const text = extractText(node)
      lines.push(text)
    } else if (node.type === 'heading') {
      const level = node.attrs?.level || 1
      const prefix = '#'.repeat(level) + ' '
      const text = extractText(node)
      lines.push(prefix + text)
    } else if (node.type === 'codeBlock') {
      const language = node.attrs?.language || ''
      const text = extractText(node)
      // 转义代码块内容中的结束标记
      const escapedText = text.replace(/```/g, '\\`\\`\\`')
      lines.push('```' + language)
      lines.push(escapedText)
      lines.push('```')
    } else {
      const text = extractText(node)
      lines.push(text)
    }
  }
  
  return lines.join('\n')
}

// 从节点中提取文本
function extractText(node) {
  if (!node.content) return ''
  
  let text = ''
  for (const child of node.content) {
    if (child.type === 'text') {
      text += child.text || ''
    } else if (child.type === 'hardBreak') {
      text += '\n'
    } else {
      text += extractText(child)
    }
  }
  return text
}

// 编辑器内容
const editorContent = ref(emptyDoc)
let isInternalUpdate = false

// 监听笔记变化，更新编辑器内容
watch(() => props.note, (newNote) => {
  if (newNote && !isInternalUpdate) {
    editorContent.value = textToDoc(newNote.content)
  }
}, { immediate: true })

// 监听编辑器内容变化，触发更新
watch(editorContent, (newContent) => {
  if (props.note) {
    isInternalUpdate = true
    const text = docToText(newContent)
    emit('update', 'content', text)
    isInternalUpdate = false
  }
}, { deep: true })

// 字数统计
const wordCount = computed(() => {
  if (!props.note?.content) return 0
  // 尝试解析为 JSON 统计
  try {
    const doc = JSON.parse(props.note.content)
    return countDocWords(doc)
  } catch {
    // 纯文本统计
    return props.note.content.length
  }
})

function countDocWords(doc) {
  if (!doc || !doc.content) return 0
  let count = 0
  for (const node of doc.content) {
    count += countNodeWords(node)
  }
  return count
}

function countNodeWords(node) {
  let count = 0
  if (node.type === 'text') {
    count += (node.text || '').length
  }
  if (node.content) {
    for (const child of node.content) {
      count += countNodeWords(child)
    }
  }
  return count
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

/* ---- 编辑区 ---- */
.note-editor-body {
  flex: 1;
  overflow: hidden;
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
</style>

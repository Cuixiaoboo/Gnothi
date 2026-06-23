<template>
  <div class="block-editor">
    <editor-content :editor="editor" class="editor-content" />
    <div class="editor-menu" v-if="editor">
      <button
        class="menu-btn"
        :class="{ active: editor.isActive('heading', { level: 1 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
        title="标题 1"
      >
        H1
      </button>
      <button
        class="menu-btn"
        :class="{ active: editor.isActive('heading', { level: 2 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
        title="标题 2"
      >
        H2
      </button>
      <button
        class="menu-btn"
        :class="{ active: editor.isActive('heading', { level: 3 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
        title="标题 3"
      >
        H3
      </button>
      <div class="menu-divider"></div>
      <button
        class="menu-btn"
        :class="{ active: editor.isActive('codeBlock') }"
        @click="wrapInCodeBlock"
        title="代码块"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <polyline points="16 18 22 12 16 6" />
          <polyline points="8 6 2 12 8 18" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight'
import { common, createLowlight } from 'lowlight'

// 创建 lowlight 实例
const lowlight = createLowlight(common)

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      type: 'doc',
      content: [
        { type: 'paragraph' }
      ]
    })
  }
})

const emit = defineEmits(['update:modelValue'])

let isInternalUpdate = false

// 将选中的多行文本合并到一个代码块
function wrapInCodeBlock() {
  if (!editor.value) return
  
  const { state } = editor.value
  const { selection } = state
  const { from, to } = selection
  
  // 如果有选区
  if (from !== to) {
    // 获取选中的文本
    const selectedText = state.doc.textBetween(from, to, '\n')
    
    // 删除选中内容
    editor.value.chain()
      .focus()
      .deleteSelection()
      .run()
    
    // 插入一个代码块，包含所有文本
    editor.value.chain()
      .focus()
      .insertContent({
        type: 'codeBlock',
        content: [{ type: 'text', text: selectedText }]
      })
      .run()
  } else {
    // 没有选区，直接切换代码块
    editor.value.chain().focus().toggleCodeBlock().run()
  }
}

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit.configure({
      heading: {
        levels: [1, 2, 3]
      }
    }),
    Placeholder.configure({
      placeholder: '输入 / 命令，或直接开始输入...'
    }),
    CodeBlockLowlight.configure({
      lowlight,
      defaultLanguage: 'plaintext'
    })
  ],
  editorProps: {
    handlePaste: (view, event) => {
      // 获取粘贴的纯文本
      const text = event.clipboardData?.getData('text/plain')
      if (!text) return false
      
      // 清理多余的空行（将连续的换行符合并为单个）
      const cleanedText = text.replace(/\n\n+/g, '\n')
      
      // 如果文本被清理过，手动插入
      if (cleanedText !== text) {
        event.preventDefault()
        const { state } = view
        const { from, to } = state.selection
        
        // 插入清理后的文本
        view.dispatch(
          state.tr.insertText(cleanedText, from, to)
        )
        return true
      }
      
      return false
    },
    transformPastedHTML: (html) => {
      // 清理 HTML 中多余的空行
      // 移除空的 <p> 标签
      let cleaned = html.replace(/<p>\s*<\/p>/g, '')
      // 移除 <p> 标签之间的 <br>
      cleaned = cleaned.replace(/<\/p>\s*<br\s*\/?>\s*<p>/g, '</p><p>')
      // 移除连续的 <br>
      cleaned = cleaned.replace(/(<br\s*\/?>){2,}/g, '<br>')
      return cleaned
    },
    clipboardTextSerializer: (slice) => {
      // 自定义复制时的纯文本格式
      const lines = []
      
      slice.content.forEach((node) => {
        if (node.type.name === 'paragraph') {
          // 段落内容，提取文本
          const text = node.textContent
          lines.push(text)
        } else if (node.type.name === 'codeBlock') {
          // 代码块，保留内容
          lines.push(node.textContent)
        } else if (node.type.name === 'heading') {
          // 标题，提取文本
          lines.push(node.textContent)
        } else {
          // 其他类型，提取文本
          lines.push(node.textContent)
        }
      })
      
      // 用单个换行符连接，不添加额外空行
      return lines.join('\n')
    }
  },
  onUpdate: ({ editor }) => {
    isInternalUpdate = true
    emit('update:modelValue', editor.getJSON())
    isInternalUpdate = false
  }
})

// 监听外部内容变化，只在外部更新时设置内容
watch(() => props.modelValue, (newContent) => {
  if (editor.value && !isInternalUpdate) {
    // 只有当内容真正变化时才设置
    const currentContent = editor.value.getJSON()
    if (JSON.stringify(currentContent) !== JSON.stringify(newContent)) {
      editor.value.commands.setContent(newContent, false)
    }
  }
}, { deep: true })

// 自动聚焦
onMounted(() => {
  if (editor.value) {
    editor.value.commands.focus()
  }
})

onUnmounted(() => {
  editor.value?.destroy()
})
</script>

<style scoped>
.block-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.editor-content {
  flex: 1;
  overflow: auto;
  padding: 16px;
}

.editor-menu {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  border-top: 1px solid var(--border);
  background: var(--bg-surface);
}

.menu-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 10px;
  border: 1px solid transparent;
  border-radius: var(--radius);
  background: transparent;
  color: var(--text-sec);
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  font-family: var(--mono);
  transition: all 0.15s;
}

.menu-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.menu-btn.active {
  background: var(--accent-bg);
  color: var(--accent);
  border-color: var(--accent);
}

.menu-divider {
  width: 1px;
  height: 20px;
  background: var(--border);
  margin: 0 4px;
}

/* Tiptap 编辑器样式 */
.editor-content :deep(.tiptap) {
  outline: none;
  min-height: 100%;
}

.editor-content :deep(.tiptap p.is-editor-empty:first-child::before) {
  color: var(--text-muted);
  content: attr(data-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
}

.editor-content :deep(.tiptap h1) {
  font-size: 24px;
  font-weight: 700;
  margin: 16px 0 8px;
  color: var(--text);
}

.editor-content :deep(.tiptap h2) {
  font-size: 20px;
  font-weight: 600;
  margin: 14px 0 6px;
  color: var(--text);
}

.editor-content :deep(.tiptap h3) {
  font-size: 16px;
  font-weight: 600;
  margin: 12px 0 4px;
  color: var(--text);
}

.editor-content :deep(.tiptap p) {
  margin: 8px 0;
  line-height: 1.6;
  color: var(--text);
}

.editor-content :deep(.tiptap pre) {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 16px;
  margin: 12px 0;
  overflow-x: auto;
  font-family: var(--mono);
  font-size: 13px;
  line-height: 1.5;
}

.editor-content :deep(.tiptap pre code) {
  color: var(--text);
  background: transparent;
  padding: 0;
  font-size: inherit;
}

.editor-content :deep(.tiptap code) {
  background: var(--bg-surface-2);
  border-radius: 4px;
  padding: 2px 6px;
  font-family: var(--mono);
  font-size: 0.9em;
  color: var(--accent);
}

/* 代码块语法高亮 */
.editor-content :deep(.tiptap .hljs-keyword),
.editor-content :deep(.tiptap .hljs-selector-tag) {
  color: #c678dd;
}

.editor-content :deep(.tiptap .hljs-string),
.editor-content :deep(.tiptap .hljs-title),
.editor-content :deep(.tiptap .hljs-section),
.editor-content :deep(.tiptap .hljs-type) {
  color: #98c379;
}

.editor-content :deep(.tiptap .hljs-attribute),
.editor-content :deep(.tiptap .hljs-variable) {
  color: #e06c75;
}

.editor-content :deep(.tiptap .hljs-number),
.editor-content :deep(.tiptap .hljs-literal) {
  color: #d19a66;
}

.editor-content :deep(.tiptap .hljs-comment) {
  color: #5c6370;
  font-style: italic;
}

.editor-content :deep(.tiptap .hljs-function) {
  color: #61afef;
}

.editor-content :deep(.tiptap .hljs-built_in) {
  color: #e6c07b;
}

.editor-content :deep(.tiptap .hljs-params) {
  color: #abb2bf;
}

.editor-content :deep(.tiptap .hljs-meta) {
  color: #56b6c2;
}

.editor-content :deep(.tiptap .hljs-punctuation) {
  color: #abb2bf;
}
</style>

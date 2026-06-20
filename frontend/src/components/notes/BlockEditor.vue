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
        @click="editor.chain().focus().toggleCodeBlock().run()"
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
  onUpdate: ({ editor }) => {
    isInternalUpdate = true
    emit('update:modelValue', editor.getJSON())
    isInternalUpdate = false
  }
})

// 监听外部内容变化，只在外部更新时设置内容
watch(() => props.modelValue, (newContent) => {
  if (editor.value && !isInternalUpdate) {
    editor.value.commands.setContent(newContent, false)
  }
}, { deep: true })

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

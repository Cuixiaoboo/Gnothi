<template>
  <div class="cm-json-viewer" ref="viewerRef"></div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { EditorView, basicSetup } from 'codemirror'
import { EditorState } from '@codemirror/state'
import { json } from '@codemirror/lang-json'
import { foldGutter, foldCode, HighlightStyle, syntaxHighlighting } from '@codemirror/language'
import { tags } from '@lezer/highlight'

const props = defineProps({
  value: { type: [String, Object, Array, Number, Boolean, null], default: '' },
  expandDepth: { type: Number, default: 3 }
})

const viewerRef = ref(null)
let editorView = null

const customFoldGutter = foldGutter({ openText: '▶', closedText: '▼' })

function readCss(name, fallback) {
  if (typeof document === 'undefined') return fallback
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || fallback
}

function buildHighlight() {
  return syntaxHighlighting(HighlightStyle.define([
    { tag: tags.keyword, color: readCss('--sh-null', '#c678dd') },
    { tag: tags.atom,   color: readCss('--sh-boolean', '#56b6c2') },
    { tag: tags.bool,   color: readCss('--sh-boolean', '#56b6c2') },
    { tag: tags.number, color: readCss('--sh-number', '#d19a66') },
    { tag: tags.string, color: readCss('--sh-string', '#98c379') },
    { tag: tags.propertyName, color: readCss('--sh-key', '#e06c75') },
    { tag: tags.punctuation, color: readCss('--sh-punctuation', '#606060') },
    { tag: tags.separator,   color: readCss('--sh-punctuation', '#606060') },
    { tag: tags.brace,  color: readCss('--sh-bracket', '#606060') },
    { tag: tags.bracket, color: readCss('--sh-bracket', '#606060') },
  ]))
}

function toStr(val) {
  if (!val) return ''
  if (typeof val === 'string') return val
  return JSON.stringify(val, null, 2)
}

function initEditor(content) {
  if (!viewerRef.value || !content) return false

  const lines = content.split('\n')
  let depth = 0, start = -1
  const folds = []
  for (let i = 0; i < lines.length; i++) {
    const o = (lines[i].match(/[{[]/g) || []).length
    const c = (lines[i].match(/[}\]]/g) || []).length
    depth += o - c; if (depth < 0) depth = 0
    if (depth > props.expandDepth && start === -1) start = i
    if (depth <= props.expandDepth && start !== -1) { folds.push({ from: start + 1, to: i + 1 }); start = -1 }
  }

  const state = EditorState.create({
    doc: content,
    extensions: [
      basicSetup,
      json(),
      buildHighlight(),
      EditorView.editable.of(false),
    ]
  })
  editorView = new EditorView({ state, parent: viewerRef.value })

  if (folds.length > 0) {
    requestAnimationFrame(() => {
      for (const f of folds) {
        try { const l1 = editorView.state.doc.line(f.from); const l2 = editorView.state.doc.line(f.to); foldCode(editorView, { from: l1.from, to: l2.to }) } catch {}
      }
    })
  }
  return true
}

function updateContent(content) {
  if (content) {
    editorView.dispatch({ changes: { from: 0, to: editorView.state.doc.length, insert: content } })
  } else {
    editorView.dispatch({ changes: { from: 0, to: editorView.state.doc.length, insert: '' } })
  }
}

watch(() => props.value, (val) => {
  const content = toStr(val)
  if (editorView) {
    updateContent(content)
  } else if (content && viewerRef.value) {
    initEditor(content)
  } else if (content) {
    setTimeout(() => { if (content && viewerRef.value) initEditor(content) }, 50)
  }
})

onMounted(() => {
  const content = toStr(props.value)
  if (content) {
    initEditor(content)
  }
})

onUnmounted(() => {
  if (editorView) { editorView.destroy() }
})
</script>

<style>
.cm-json-viewer {
  height: 100%;
  overflow: auto;
}
.cm-json-viewer .cm-editor {
  height: 100%;
  outline: none;
}
.cm-json-viewer .cm-scroller {
  overflow: auto;
  font-family: var(--mono, 'DM Mono', Menlo, monospace) !important;
  font-size: 13px !important;
  line-height: 1.6 !important;
  color: var(--text, #e8e6e3) !important;
}
.cm-json-viewer .cm-content {
  caret-color: transparent !important;
  padding: 0 !important;
  font-family: inherit !important;
  font-size: inherit !important;
  line-height: inherit !important;
  color: inherit !important;
}
.cm-json-viewer .cm-gutters {
  background: transparent !important;
  border: none !important;
  color: var(--sh-bracket, #606060) !important;
}
.cm-json-viewer .cm-activeLineGutter,
.cm-json-viewer .cm-activeLine {
  background: transparent !important;
}
.cm-json-viewer .cm-foldPlaceholder {
  background: var(--bg-surface-2, #222228) !important;
  border: 1px solid var(--border, #2a2a32) !important;
  border-radius: 8px !important;
  color: var(--text-muted, #606060) !important;
  padding: 0 6px !important;
  font-size: 11px !important;
  cursor: pointer !important;
}
.cm-json-viewer .cm-foldPlaceholder:hover {
  background: var(--bg-hover, #2a2a32) !important;
  color: var(--text, #e8e6e3) !important;
}
</style>

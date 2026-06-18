<template>
  <div class="json-formatter">
    <div class="json-header">
      <h3>JSON 格式化</h3>
      <div class="json-actions">
        <button class="btn btn-sm" @click="format" :disabled="!input">格式化</button>
        <button class="btn btn-sm" @click="compress" :disabled="!input">压缩</button>
        <button class="btn btn-sm" @click="copy" :disabled="!output">复制</button>
        <button class="btn btn-sm" @click="clear">清空</button>
      </div>
    </div>

    <div class="json-body">
      <div class="json-input">
        <div class="panel-header">
          <span>输入</span>
          <span class="info-msg" v-if="isExtractInfo">{{ error }}</span>
          <span class="error-msg" v-else-if="error">{{ error }}</span>
          <span class="success-msg" v-if="!error && input">✓ 有效 JSON</span>
        </div>
        <textarea
          v-model="input"
          placeholder="粘贴 JSON 数据到这里..."
          spellcheck="false"
          @input="validate"
        ></textarea>
      </div>

      <div class="json-output">
        <div class="panel-header">
          <span>输出</span>
          <span class="copy-msg" v-if="copied">已复制!</span>
        </div>
        <pre v-if="output"><code>{{ output }}</code></pre>
        <div class="empty-output" v-else>
          <span>格式化后的 JSON 将显示在这里</span>
        </div>
      </div>
    </div>

    <div class="json-footer">
      <span class="footer-item">输入: {{ input.length }} 字符</span>
      <span class="footer-item">输出: {{ output.length }} 字符</span>
      <span class="footer-item">层级: {{ depth }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const STORAGE_KEY = 'json-formatter-input'

const input = ref('')
const output = ref('')
const error = ref('')
const copied = ref(false)
const isExtractInfo = ref(false)

// 从 localStorage 读取上次的内容
onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    input.value = saved
    // 自动验证并格式化
    validate()
  }
})

// 监听输入变化，保存到 localStorage
watch(input, (newValue) => {
  localStorage.setItem(STORAGE_KEY, newValue)
})

// 验证并尝试格式化
function validate() {
  isExtractInfo.value = false
  if (!input.value.trim()) {
    error.value = ''
    output.value = ''
    return
  }

  // 尝试直接解析
  try {
    const obj = JSON.parse(input.value)
    error.value = ''
    // 自动格式化展示
    output.value = JSON.stringify(obj, null, 2)
    return
  } catch {
    // 直接解析失败，尝试提取 JSON
  }

  // 提取 JSON
  extractJsonFromText(input.value)
}

// 尝试修复并格式化 JSON
function tryFixAndFormat(text) {
  try {
    // 移除可能的 BOM 和前后空白
    let cleaned = text.replace(/^[\uFEFF\s]+|[\s]+$/g, '')
    // 尝试解析
    const obj = JSON.parse(cleaned)
    return JSON.stringify(obj, null, 2)
  } catch {
    // 如果还是失败，返回原文本（带格式化）
    return formatText(text)
  }
}

// 简单的文本格式化
function formatText(text) {
  const lines = text.split('\n')
  let indent = 0
  const formatted = []

  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) {
      formatted.push('')
      continue
    }

    // 减少缩进
    if (trimmed.startsWith('}') || trimmed.startsWith(']')) {
      indent = Math.max(0, indent - 1)
    }

    formatted.push('  '.repeat(indent) + trimmed)

    // 增加缩进
    if (trimmed.endsWith('{') || trimmed.endsWith('[')) {
      indent++
    } else if (trimmed.endsWith('},') || trimmed.endsWith('],')) {
      // 下一行可能需要减少缩进
    }
  }

  return formatted.join('\n')
}

// 计算 JSON 深度
const depth = computed(() => {
  if (!input.value) return 0
  try {
    const obj = JSON.parse(input.value)
    return getDepth(obj)
  } catch {
    // 尝试计算嵌套层级
    return estimateDepth(input.value)
  }
})

function getDepth(obj) {
  if (typeof obj !== 'object' || obj === null) return 0
  let maxDepth = 0
  for (const key in obj) {
    const d = getDepth(obj[key])
    if (d > maxDepth) maxDepth = d
  }
  return maxDepth + 1
}

// 估算嵌套深度
function estimateDepth(text) {
  let maxDepth = 0
  let currentDepth = 0

  for (const char of text) {
    if (char === '{' || char === '[') {
      currentDepth++
      if (currentDepth > maxDepth) {
        maxDepth = currentDepth
      }
    } else if (char === '}' || char === ']') {
      currentDepth = Math.max(0, currentDepth - 1)
    }
  }

  return maxDepth
}

// 格式化
function format() {
  isExtractInfo.value = false
  if (!input.value.trim()) return

  // 尝试直接解析
  try {
    const obj = JSON.parse(input.value)
    output.value = JSON.stringify(obj, null, 2)
    error.value = ''
    return
  } catch {
    // 直接解析失败，尝试提取 JSON
  }

  // 提取 JSON
  extractJsonFromText(input.value)
}

// 压缩
function compress() {
  isExtractInfo.value = false
  if (!input.value.trim()) return

  // 尝试直接解析
  try {
    const obj = JSON.parse(input.value)
    output.value = JSON.stringify(obj)
    error.value = ''
    return
  } catch {
    // 直接解析失败，尝试提取 JSON
  }

  // 提取并压缩，保留完整文本结构
  extractJsonFromText(input.value, true)
}

// 复制
async function copy() {
  if (!output.value) return

  try {
    await navigator.clipboard.writeText(output.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (e) {
    console.error('复制失败:', e)
  }
}

// 清空
function clear() {
  input.value = ''
  output.value = ''
  error.value = ''
  isExtractInfo.value = false
  localStorage.removeItem(STORAGE_KEY)
}

// 从文本中提取 JSON
function extractJsonFromText(text, compressMode = false) {
  const segments = []

  // 预处理文本：替换中文引号为英文引号
  let cleanedText = text
    .replace(/[“”]/g, '"') // 替换中文双引号
    .replace(/[‘’]/g, "'") // 替换中文单引号
    .replace(/[，]/g, ',') // 替换中文逗号
    .replace(/[：]/g, ':') // 替换中文冒号

  // 匹配 JSON 对象或数组，同时记录位置
  let i = 0
  let lastEnd = 0

  while (i < cleanedText.length) {
    // 找到 JSON 开始标记
    if (cleanedText[i] === '{' || cleanedText[i] === '[') {
      const start = i
      const char = cleanedText[i]
      const endChar = char === '{' ? '}' : ']'
      let depth = 1
      let inString = false
      let escapeNext = false
      i++

      // 找到匹配的结束标记
      while (i < cleanedText.length && depth > 0) {
        const c = cleanedText[i]

        if (escapeNext) {
          escapeNext = false
        } else if (c === '\\') {
          escapeNext = true
        } else if (c === '"') {
          inString = !inString
        }

        if (!inString) {
          if (c === char) {
            depth++
          } else if (c === endChar) {
            depth--
          }
        }
        i++
      }

      if (depth === 0) {
        const jsonStr = cleanedText.substring(start, i)
        try {
          const obj = JSON.parse(jsonStr)
          // 添加 JSON 前面的非 JSON 文本
          if (start > lastEnd) {
            segments.push({ type: 'text', content: cleanedText.substring(lastEnd, start) })
          }
          // 添加格式化或压缩的 JSON
          const jsonContent = compressMode ? JSON.stringify(obj) : JSON.stringify(obj, null, 2)
          segments.push({ type: 'json', content: jsonContent })
          lastEnd = i
        } catch {
          // 尝试修复常见错误后解析
          try {
            const fixedStr = jsonStr
              .replace(/,\s*}/g, '}') // 移除尾部逗号
              .replace(/,\s*]/g, ']') // 移除数组尾部逗号
            const obj = JSON.parse(fixedStr)
            if (start > lastEnd) {
              segments.push({ type: 'text', content: cleanedText.substring(lastEnd, start) })
            }
            const jsonContent = compressMode ? JSON.stringify(obj) : JSON.stringify(obj, null, 2)
            segments.push({ type: 'json', content: jsonContent })
            lastEnd = i
          } catch {
            // 仍然无法解析，跳过
          }
        }
      }
    } else {
      i++
    }
  }

  // 添加剩余的非 JSON 文本
  if (lastEnd < cleanedText.length) {
    segments.push({ type: 'text', content: cleanedText.substring(lastEnd) })
  }

  if (segments.length === 0) {
    error.value = '未找到有效的 JSON 内容'
    output.value = ''
    return
  }

  // 检查是否提取到了 JSON
  const jsonCount = segments.filter((s) => s.type === 'json').length
  if (jsonCount === 0) {
    error.value = '未找到有效的 JSON 内容'
    output.value = ''
    return
  }

  // 合并所有片段
  output.value = segments.map((s) => s.content).join('')
  error.value = `提取了 ${jsonCount} 个 JSON 块`
  isExtractInfo.value = true
}
</script>

<style scoped>
.json-formatter {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.json-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
}

.json-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.json-actions {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 6px 12px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--bg-surface);
  color: var(--text-sec);
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s;
}

.btn:hover:not(:disabled) {
  background: var(--bg-hover);
  color: var(--text);
  border-color: var(--border-light);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.json-body {
  flex: 1;
  display: flex;
  gap: 16px;
  padding: 16px;
  overflow: hidden;
}

.json-input,
.json-output {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-bottom: none;
  border-radius: var(--radius) var(--radius) 0 0;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
}

.error-msg {
  color: var(--red);
  font-weight: 500;
}

.success-msg {
  color: var(--green);
  font-weight: 500;
}

.info-msg {
  color: var(--blue);
  font-weight: 500;
}

.copy-msg {
  color: var(--green);
  font-weight: 500;
}

.json-input textarea {
  flex: 1;
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 0 0 var(--radius) var(--radius);
  background: var(--bg);
  color: var(--text);
  font-family: var(--mono);
  font-size: 13px;
  line-height: 1.6;
  resize: none;
  outline: none;
  tab-size: 2;
}

.json-input textarea:focus {
  border-color: var(--accent);
}

.json-output pre {
  flex: 1;
  margin: 0;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 0 0 var(--radius) var(--radius);
  background: var(--bg);
  overflow: auto;
  font-family: var(--mono) !important;
  font-size: 13px !important;
  line-height: 1.6 !important;
  color: var(--text);
  white-space: pre-wrap;
  word-wrap: break-word;
  tab-size: 2;
}

.json-output pre code {
  font-family: inherit !important;
  font-size: inherit !important;
  line-height: inherit !important;
}

.empty-output {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 0 0 var(--radius) var(--radius);
  background: var(--bg);
  color: var(--text-muted);
  font-size: 13px;
}

.json-footer {
  padding: 8px 16px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  gap: 16px;
}

@media (max-width: 768px) {
  .json-body {
    flex-direction: column;
  }
}
</style>

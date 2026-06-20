<template>
  <div class="regex-tester">
    <div class="regex-header">
      <h3>正则表达式测试</h3>
      <div class="regex-actions">
        <button class="btn btn-sm" @click="generateFromText" :disabled="!testText" title="从测试文本生成正则">
          生成正则
        </button>
        <button class="btn btn-sm" @click="testRegex" :disabled="!pattern">测试</button>
        <button class="btn btn-sm" @click="clear">清空</button>
      </div>
    </div>

    <div class="regex-body">
      <!-- 正则表达式输入 -->
      <div class="regex-input-section">
        <div class="section-header">
          <span>正则表达式</span>
          <span class="error-msg" v-if="error">{{ error }}</span>
          <span class="success-msg" v-else-if="pattern && !error">✓ 有效正则</span>
        </div>
        <div class="regex-input-wrapper">
          <span class="regex-delimiter">/</span>
          <input
            v-model="pattern"
            type="text"
            placeholder="输入正则表达式..."
            spellcheck="false"
            @input="testRegex"
          />
          <span class="regex-delimiter">/</span>
          <input
            v-model="flags"
            type="text"
            placeholder="gim"
            class="flags-input"
            spellcheck="false"
            @input="testRegex"
          />
        </div>
      </div>

      <!-- 测试文本输入 -->
      <div class="test-text-section">
        <div class="section-header">
          <span>测试文本</span>
          <span class="match-count" v-if="matches.length > 0">
            找到 {{ matches.length }} 个匹配
          </span>
        </div>
        <textarea
          v-model="testText"
          placeholder="输入要测试的文本..."
          spellcheck="false"
          @input="testRegex"
        ></textarea>
      </div>

      <!-- 匹配结果 -->
      <div class="results-section" v-if="matches.length > 0">
        <div class="section-header">
          <span>匹配结果</span>
        </div>
        <div class="matches-list">
          <div class="match-item" v-for="(match, index) in matches" :key="index">
            <div class="match-index">#{{ index + 1 }}</div>
            <div class="match-content">
              <div class="match-text">{{ match.text }}</div>
              <div class="match-info">
                位置: {{ match.start }}-{{ match.end }}
                <span v-if="match.groups.length > 0">
                  | 分组: {{ match.groups.join(', ') }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 高亮预览 -->
      <div class="preview-section" v-if="testText && pattern">
        <div class="section-header">
          <span>高亮预览</span>
        </div>
        <div class="preview-content" v-html="highlightedText"></div>
      </div>
    </div>

    <div class="regex-footer">
      <span v-if="pattern">正则: /{{ pattern }}/{{ flags }}</span>
      <span v-if="testText">文本: {{ testText.length }} 字符</span>
      <span v-if="matches.length > 0">匹配: {{ matches.length }} 个</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const STORAGE_KEY_PATTERN = 'regex-tester-pattern'
const STORAGE_KEY_FLAGS = 'regex-tester-flags'
const STORAGE_KEY_TEXT = 'regex-tester-text'

const pattern = ref(localStorage.getItem(STORAGE_KEY_PATTERN) || '')
const flags = ref(localStorage.getItem(STORAGE_KEY_FLAGS) || 'g')
const testText = ref(localStorage.getItem(STORAGE_KEY_TEXT) || '')
const error = ref('')
const matches = ref([])

// 保存到 localStorage
function saveToStorage() {
  localStorage.setItem(STORAGE_KEY_PATTERN, pattern.value)
  localStorage.setItem(STORAGE_KEY_FLAGS, flags.value)
  localStorage.setItem(STORAGE_KEY_TEXT, testText.value)
}

// 测试正则
function testRegex() {
  saveToStorage()
  
  if (!pattern.value || !testText.value) {
    matches.value = []
    error.value = ''
    return
  }

  try {
    const regex = new RegExp(pattern.value, flags.value)
    error.value = ''
    
    const result = []
    let match
    
    // 重置 lastIndex
    regex.lastIndex = 0
    
    if (flags.value.includes('g')) {
      // 全局匹配
      while ((match = regex.exec(testText.value)) !== null) {
        result.push({
          text: match[0],
          start: match.index,
          end: match.index + match[0].length,
          groups: match.slice(1).map(g => g || '(空)')
        })
        
        // 防止无限循环
        if (match[0].length === 0) {
          regex.lastIndex++
        }
      }
    } else {
      // 单次匹配
      match = regex.exec(testText.value)
      if (match) {
        result.push({
          text: match[0],
          start: match.index,
          end: match.index + match[0].length,
          groups: match.slice(1).map(g => g || '(空)')
        })
      }
    }
    
    matches.value = result
  } catch (e) {
    error.value = e.message
    matches.value = []
  }
}

// 高亮预览
const highlightedText = computed(() => {
  if (!pattern.value || !testText.value) return ''
  
  try {
    const regex = new RegExp(pattern.value, flags.value)
    const escaped = testText.value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
    
    return escaped.replace(regex, '<span class="highlight">$&</span>')
  } catch {
    return testText.value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
  }
})

// 清空
function clear() {
  pattern.value = ''
  flags.value = 'g'
  testText.value = ''
  error.value = ''
  matches.value = []
  saveToStorage()
}

// 从测试文本生成正则表达式
function generateFromText() {
  if (!testText.value) return
  
  const text = testText.value.trim()
  
  // 常见模式识别
  const patterns = [
    // 邮箱
    {
      test: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
      regex: '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}',
      name: '邮箱'
    },
    // 手机号（中国）
    {
      test: /^1[3-9]\d{9}$/,
      regex: '1[3-9]\\d{9}',
      name: '手机号'
    },
    // URL
    {
      test: /^https?:\/\/[^\s]+$/,
      regex: 'https?:\/\/[^\\s]+',
      name: 'URL'
    },
    // IP 地址
    {
      test: /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/,
      regex: '\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}',
      name: 'IP 地址'
    },
    // 日期 (YYYY-MM-DD)
    {
      test: /^\d{4}-\d{2}-\d{2}$/,
      regex: '\\d{4}-\\d{2}-\\d{2}',
      name: '日期'
    },
    // 时间 (HH:MM:SS)
    {
      test: /^\d{2}:\d{2}:\d{2}$/,
      regex: '\\d{2}:\\d{2}:\\d{2}',
      name: '时间'
    },
    // 数字
    {
      test: /^\d+$/,
      regex: '\\d+',
      name: '数字'
    },
    // 中文
    {
      test: /^[\u4e00-\u9fa5]+$/,
      regex: '[\\u4e00-\\u9fa5]+',
      name: '中文'
    },
    // 英文
    {
      test: /^[a-zA-Z]+$/,
      regex: '[a-zA-Z]+',
      name: '英文'
    },
    // 字母数字
    {
      test: /^[a-zA-Z0-9]+$/,
      regex: '[a-zA-Z0-9]+',
      name: '字母数字'
    },
  ]
  
  // 检查是否匹配常见模式
  for (const p of patterns) {
    if (p.test.test(text)) {
      pattern.value = p.regex
      testRegex()
      return
    }
  }
  
  // 如果不匹配常见模式，生成精确匹配的正则
  // 转义特殊字符
  const escaped = text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  pattern.value = escaped
  testRegex()
}
</script>

<style scoped>
.regex-tester {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.regex-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
}

.regex-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.regex-actions {
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

.regex-body {
  flex: 1;
  overflow: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-header {
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

.match-count {
  color: var(--accent);
  font-weight: 500;
}

/* 正则输入 */
.regex-input-wrapper {
  display: flex;
  align-items: center;
  padding: 0 12px;
  border: 1px solid var(--border);
  border-radius: 0 0 var(--radius) var(--radius);
  background: var(--bg);
}

.regex-delimiter {
  color: var(--text-muted);
  font-family: var(--mono);
  font-size: 14px;
}

.regex-input-wrapper input {
  flex: 1;
  padding: 10px 8px;
  border: none;
  background: transparent;
  color: var(--text);
  font-family: var(--mono);
  font-size: 14px;
  outline: none;
}

.flags-input {
  width: 40px !important;
  flex: none !important;
  border-left: 1px solid var(--border) !important;
  margin-left: 4px;
  padding-left: 8px !important;
}

/* 测试文本 */
.test-text-section textarea {
  width: 100%;
  min-height: 100px;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 0 0 var(--radius) var(--radius);
  background: var(--bg);
  color: var(--text);
  font-family: var(--mono);
  font-size: 13px;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  tab-size: 2;
}

.test-text-section textarea:focus {
  border-color: var(--accent);
}

/* 匹配结果 */
.matches-list {
  border: 1px solid var(--border);
  border-radius: 0 0 var(--radius) var(--radius);
  background: var(--bg);
  max-height: 200px;
  overflow: auto;
}

.match-item {
  display: flex;
  gap: 12px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
}

.match-item:last-child {
  border-bottom: none;
}

.match-index {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  font-family: var(--mono);
  flex-shrink: 0;
}

.match-content {
  flex: 1;
  min-width: 0;
}

.match-text {
  font-size: 13px;
  font-family: var(--mono);
  color: var(--accent);
  word-break: break-all;
  margin-bottom: 2px;
}

.match-info {
  font-size: 11px;
  color: var(--text-muted);
  font-family: var(--mono);
}

/* 高亮预览 */
.preview-content {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 0 0 var(--radius) var(--radius);
  background: var(--bg);
  font-size: 13px;
  line-height: 1.6;
  color: var(--text);
  white-space: pre-wrap;
  word-break: break-all;
}

.preview-content :deep(.highlight) {
  background: rgba(224, 122, 58, 0.3);
  border-radius: 2px;
  padding: 0 2px;
}

.regex-footer {
  padding: 8px 16px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  gap: 16px;
}
</style>

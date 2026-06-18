<template>
  <div class="view-wrapper">
    <div class="page-body">
      <!-- 顶部欢迎区 -->
      <div class="hero">
        <div class="hero-left">
          <div class="greeting">{{ greetingText }}，今天记得开心哦！</div>
          <div class="hero-date">{{ todayStr }} {{ weekdayStr }}</div>
        </div>
        <div class="hero-right">
          <div class="stat-pill">
            <span class="stat-pill-num">{{ todos.length }}</span>
            <span class="stat-pill-label">待办</span>
          </div>
          <div class="stat-pill">
            <span class="stat-pill-num">{{ notes.length }}</span>
            <span class="stat-pill-label">笔记</span>
          </div>
          <div class="stat-pill">
            <span class="stat-pill-num">{{ reportCount }}</span>
            <span class="stat-pill-label">日报</span>
          </div>
        </div>
      </div>

      <!-- 快捷入口 -->
      <div class="section-title">快捷入口</div>
      <div class="quick-grid">
        <button class="quick-card" @click="$router.push({ name: 'report' })">
          <div class="qc-icon">📋</div>
          <div class="qc-text">
            <div class="qc-label">今日日报</div>
            <div class="qc-desc">记录今日工作内容</div>
          </div>
          <svg
            class="qc-arrow"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>
        <button class="quick-card" @click="$router.push({ name: 'todo' })">
          <div class="qc-icon">✅</div>
          <div class="qc-text">
            <div class="qc-label">待办事项</div>
            <div class="qc-desc">{{ pendingTodos.length }} 项待处理</div>
          </div>
          <svg
            class="qc-arrow"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>
        <button class="quick-card" @click="$router.push({ name: 'notes' })">
          <div class="qc-icon">📝</div>
          <div class="qc-text">
            <div class="qc-label">个人笔记</div>
            <div class="qc-desc">{{ notes.length }} 篇笔记</div>
          </div>
          <svg
            class="qc-arrow"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>
        <button class="quick-card" @click="$router.push({ name: 'tools' })">
          <div class="qc-icon">🛠️</div>
          <div class="qc-text">
            <div class="qc-label">工具箱</div>
            <div class="qc-desc">JSON 格式化等工具</div>
          </div>
          <svg
            class="qc-arrow"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>
      </div>

      <!-- 内容区 -->
      <div class="content-grid">
        <!-- 待办列表 -->
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">待办事项</div>
            <button class="panel-link" @click="$router.push({ name: 'todo' })">查看全部</button>
          </div>
          <div class="panel-body" v-if="pendingTodos.length > 0">
            <div class="todo-row" v-for="t in pendingTodos.slice(0, 6)" :key="t.id">
              <span class="todo-dot" :class="'dot-' + t.priority"></span>
              <span class="todo-text">{{ t.title }}</span>
              <span class="badge" :class="'badge-' + t.status">{{ statusLabel(t.status) }}</span>
            </div>
          </div>
          <div class="panel-empty" v-else>
            <div class="empty-icon">✅</div>
            <p>暂无待办，去添加一个吧</p>
          </div>
        </div>

        <!-- 笔记列表 -->
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">最近笔记</div>
            <button class="panel-link" @click="$router.push({ name: 'notes' })">查看全部</button>
          </div>
          <div class="panel-body" v-if="notes.length > 0">
            <div
              class="note-row"
              v-for="n in notes.slice(0, 6)"
              :key="n.id"
              @click="$router.push({ name: 'notes', query: { id: n.id } })"
            >
              <div class="note-title">{{ n.title }}</div>
              <div class="note-preview">{{ (n.content || '').slice(0, 40) || '空笔记' }}</div>
              <div class="note-date">{{ formatDate(n.updated_at) }}</div>
            </div>
          </div>
          <div class="panel-empty" v-else>
            <div class="empty-icon">📝</div>
            <p>暂无笔记，去创建一篇吧</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { todoApi, noteApi, reportApi } from '../api'

const todos = ref([])
const notes = ref([])
const reportCount = ref(0)

const pendingTodos = computed(() => todos.value.filter((t) => t.status !== 'completed'))

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

const todayStr = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
})

const weekdayStr = computed(() => {
  const d = new Date()
  return `星期${weekdays[d.getDay()]}`
})

const greetingText = computed(() => {
  const h = new Date().getHours()
  if (h < 6) return '夜深了'
  if (h < 12) return '早上好'
  if (h < 14) return '中午好'
  if (h < 18) return '下午好'
  return '晚上好'
})

function statusLabel(s) {
  return { hangup: '挂起', pending: '待处理', in_progress: '进行中', completed: '已完成' }[s] || s
}

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getMonth() + 1}月${d.getDate()}日`
}

onMounted(async () => {
  try {
    const [todoRes, noteRes, dateRes] = await Promise.all([
      todoApi.list(),
      noteApi.list(),
      reportApi.getDates(),
    ])
    todos.value = todoRes
    notes.value = noteRes
    reportCount.value = dateRes.length
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.view-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.page-body {
  flex: 1;
  overflow: hidden;
  padding: 24px 28px 28px;
  /* max-width: 880px; */
  display: flex;
  flex-direction: column;
}

/* ═══════════ Hero ═══════════ */
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}

.greeting {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
  margin-bottom: 4px;
}

.hero-date {
  font-size: 14px;
  color: var(--text-sec);
}

.hero-right {
  display: flex;
  gap: 12px;
}

.stat-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 6px 14px;
}

.stat-pill-num {
  font-size: 18px;
  font-weight: 700;
  color: var(--accent);
  font-family: var(--mono);
}

.stat-pill-label {
  font-size: 12px;
  color: var(--text-muted);
}

/* ═══════════ Section Title ═══════════ */
.section-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 12px;
}

/* ═══════════ Quick Grid ═══════════ */
.quick-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 28px;
}

.quick-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  color: var(--text);
  font-family: var(--font);
}

.quick-card:hover {
  border-color: var(--accent);
  background: var(--accent-bg);
  transform: translateY(-2px);
}

.qc-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.qc-text {
  flex: 1;
  min-width: 0;
}

.qc-label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 2px;
}

.qc-desc {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.qc-arrow {
  color: var(--text-muted);
  flex-shrink: 0;
  transition: transform 0.2s;
}

.quick-card:hover .qc-arrow {
  transform: translateX(3px);
  color: var(--accent);
}

/* ═══════════ Content Grid ═══════════ */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  flex: 1;
  min-height: 0;
}

.panel {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.panel-title {
  font-size: 14px;
  font-weight: 600;
}

.panel-link {
  background: none;
  border: none;
  color: var(--accent);
  font-size: 12px;
  cursor: pointer;
  font-family: var(--font);
}

.panel-link:hover {
  color: var(--accent-hover);
}

.panel-body {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

/* ═══════════ Todo Rows ═══════════ */
.todo-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-bottom: 1px solid var(--border);
}

.todo-row:last-child {
  border-bottom: none;
}

.todo-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-high {
  background: var(--red);
}

.dot-medium {
  background: var(--yellow);
}

.dot-low {
  background: var(--text-muted);
}

.todo-text {
  flex: 1;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ═══════════ Note Rows ═══════════ */
.note-row {
  padding: 10px 16px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background 0.15s;
}

.note-row:hover {
  background: var(--bg-hover);
}

.note-row:last-child {
  border-bottom: none;
}

.note-title {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.note-preview {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 4px;
}

.note-date {
  font-size: 11px;
  color: var(--text-muted);
  font-family: var(--mono);
}

/* ═══════════ Empty ═══════════ */
.panel-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 32px;
  margin-bottom: 8px;
  opacity: 0.5;
}

.panel-empty p {
  font-size: 13px;
}

/* ═══════════ Responsive ═══════════ */
@media (max-width: 768px) {
  .hero {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .quick-grid {
    grid-template-columns: 1fr;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>

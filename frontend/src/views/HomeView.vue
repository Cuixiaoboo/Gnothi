<template>
  <div class="view-wrapper">
    <div class="page-body">
      <!-- 顶部问候区 -->
      <div class="hero">
        <div class="hero-left">
          <div class="greeting">{{ greetingText }}，今天记得开心哦！</div>
          <div class="hero-date">{{ todayStr }} {{ weekdayStr }}</div>
        </div>
        <div class="hero-right">
          <div class="countdown" v-if="!isAfterWork">
            <div class="countdown-label">距离下班还有</div>
            <div class="countdown-time">{{ countdownText }}</div>
          </div>
          <div class="countdown done" v-else>
            <div class="countdown-label">好好休息哦！</div>
          </div>
        </div>
      </div>

      <!-- 统计栏 -->
      <div class="stats-bar">
        <div class="stat-item">
          <span class="stat-icon">🔴</span>
          <span class="stat-label">待办</span>
          <span class="stat-value">{{ todos.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-icon">📃</span>
          <span class="stat-label">笔记</span>
          <span class="stat-value">{{ notes.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-icon">📅</span>
          <span class="stat-label">日报</span>
          <span class="stat-value">{{ reportCount }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-icon">🧰</span>
          <span class="stat-label">工具</span>
          <span class="stat-value">1</span>
        </div>
      </div>

      <!-- 主要内容区域 -->
      <div class="main-content">
        <!-- 左侧：待办事项 -->
        <div class="content-panel">
          <div class="panel-header">
            <div class="panel-title">待办事项</div>
            <button class="panel-link" @click="$router.push({ name: 'todo' })">查看全部</button>
          </div>
          <div class="panel-body" v-if="pendingTodos.length > 0">
            <div class="todo-row" v-for="t in pendingTodos.slice(0, 5)" :key="t.id">
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

        <!-- 右侧：最近笔记 -->
        <div class="content-panel">
          <div class="panel-header">
            <div class="panel-title">最近笔记</div>
            <button class="panel-link" @click="$router.push({ name: 'notes' })">查看全部</button>
          </div>
          <div class="panel-body" v-if="notes.length > 0">
            <div
              class="note-row"
              v-for="n in notes.slice(0, 5)"
              :key="n.id"
              @click="$router.push({ name: 'notes', query: { id: n.id } })"
            >
              <div class="note-title">{{ n.title || '无标题' }}</div>
              <div class="note-preview">{{ (n.content || '').slice(0, 50) || '空笔记' }}</div>
            </div>
          </div>
          <div class="panel-empty" v-else>
            <div class="empty-icon">📝</div>
            <p>暂无笔记，去创建一篇吧</p>
          </div>
        </div>
      </div>

      <!-- 摸鱼名言 -->
      <div class="motto-section">
        <div class="motto-text">{{ currentMotto.text }}</div>
        <button class="motto-refresh" @click="refreshMotto" title="换一条">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <polyline points="23 4 23 10 17 10" />
            <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { todoApi, noteApi, reportApi, mottoApi } from '../api'

const todos = ref([])
const notes = ref([])
const reportCount = ref(0)
const currentTime = ref(new Date())

// 从 localStorage 获取下班时间，默认 18:00
const workEndTime = ref(localStorage.getItem('workEndTime') || '18:00')

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

// 计算下班时间
const workEndHour = computed(() => {
  const [h, m] = workEndTime.value.split(':').map(Number)
  return { hour: h, minute: m }
})

// 判断是否已下班
const isAfterWork = computed(() => {
  const now = currentTime.value
  const end = workEndHour.value
  return now.getHours() > end.hour || (now.getHours() === end.hour && now.getMinutes() >= end.minute)
})

// 倒计时文本
const countdownText = computed(() => {
  const now = currentTime.value
  const end = workEndHour.value
  
  let diff = (end.hour * 60 + end.minute) - (now.getHours() * 60 + now.getMinutes())
  
  if (diff <= 0) return '00:00:00'
  
  const hours = Math.floor(diff / 60)
  const minutes = diff % 60
  const seconds = 59 - now.getSeconds()
  
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

// 定时器
let timer = null

function statusLabel(s) {
  return { hangup: '挂起', pending: '待处理', in_progress: '进行中', completed: '已完成' }[s] || s
}

// 摸鱼名言
const mottos = ref([])
const mottoIndex = ref(Math.floor(Date.now() / 86400000))

const currentMotto = computed(() => {
  if (mottos.value.length === 0) {
    return { text: '工作是为了生活，而不是生活为了工作' }
  }
  const motto = mottos.value[mottoIndex.value % mottos.value.length]
  return { text: motto.content }
})

function refreshMotto() {
  if (mottos.value.length > 0) {
    mottoIndex.value = Math.floor(Math.random() * mottos.value.length)
  }
}

async function loadMottos() {
  try {
    mottos.value = await mottoApi.list()
  } catch (e) {
    console.error('加载名言失败:', e)
  }
}

onMounted(async () => {
  // 启动定时器，每秒更新时间
  timer = setInterval(() => {
    currentTime.value = new Date()
  }, 1000)
  
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
  
  // 加载名言
  await loadMottos()
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
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
  overflow: auto;
  padding: 24px 28px 5px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ═══════════ Hero ═══════════ */
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0;
}

.hero-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.greeting {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.hero-date {
  font-size: 14px;
  color: var(--text-sec);
}

.hero-right {
  display: flex;
  align-items: center;
}

.countdown {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.countdown-label {
  font-size: 12px;
  color: var(--text-muted);
}

.countdown-time {
  font-size: 28px;
  font-weight: 700;
  color: var(--accent);
  font-family: var(--mono);
  letter-spacing: 2px;
}

.countdown.done .countdown-label {
  font-size: 16px;
  color: var(--green);
}

.hero-right {
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

/* ═══════════ Stats Bar ═══════════ */
.stats-bar {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  flex: 1;
}

.stat-icon {
  font-size: 16px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-sec);
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
  font-family: var(--mono);
  margin-left: auto;
}

/* ═══════════ Main Content ═══════════ */
.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  flex: 1;
  min-height: 200px;
}

.content-panel {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
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
  padding: 12px 16px;
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
  padding: 12px 16px;
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
  margin-bottom: 4px;
  color: var(--text);
}

.note-preview {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

/* ═══════════ Motto ═══════════ */
.motto-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 24px;
  flex-shrink: 0;
}

.motto-text {
  font-size: 14px;
  color: var(--text-sec);
  font-style: italic;
  line-height: 1.6;
}

.motto-refresh {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.motto-refresh:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.motto-refresh:active {
  transform: rotate(180deg);
}

/* ═══════════ Responsive ═══════════ */
@media (max-width: 768px) {
  .stats-bar {
    flex-wrap: wrap;
  }

  .stat-item {
    flex: 1 1 calc(50% - 16px);
    min-width: 0;
  }

  .main-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stat-item {
    flex: 1 1 100%;
  }
}
</style>

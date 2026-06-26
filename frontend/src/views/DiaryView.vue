<template>
  <div class="view-wrapper">
    <div class="page-header">
      <div class="page-title">朝花夕拾</div>
      <button class="btn btn-primary btn-sm" @click="startNewDiary">
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        落笔
      </button>
    </div>
    <div class="page-body">
      <div class="diary-layout">
        <!-- 左侧列表 -->
        <div class="diary-sidebar">
          <!-- 日历 -->
          <Calendar
            :selected-date="selectedDate"
            :report-dates="diaryDatesSet"
            @select="selectDate"
            @change-year="changeYear"
            @change-month="changeMonth"
            @go-today="goToday"
            :year="calYear"
            :month="calMonth"
            :days="calendarDays"
          />

          <!-- 朝花夕拾列表 -->
          <div class="diary-list">
            <div class="list-header">
              <div class="list-search">
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8" />
                  <line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
                <input 
                  type="text" 
                  v-model="searchQuery" 
                  placeholder="搜索..." 
                  class="search-input"
                />
              </div>
              <div class="list-actions">
                <button 
                  class="btn-icon" 
                  :class="{ active: showPrivate }" 
                  @click="toggleShowPrivate"
                  :title="showPrivate ? '隐藏私密朝花夕拾' : '显示私密朝花夕拾'"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path v-if="showPrivate" d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle v-if="showPrivate" cx="12" cy="12" r="3" />
                    <path
                      v-if="!showPrivate"
                      d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"
                    />
                    <line v-if="!showPrivate" x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                </button>
                <span class="list-count">{{ filteredDiaries.length }}篇</span>
              </div>
            </div>
            <div class="list-content">
              <div
                v-for="diary in filteredDiaries"
                :key="diary.id"
                class="diary-item"
                :class="{ active: diary.date === selectedDate }"
                @click="selectDate(diary.date)"
              >
                <div class="item-info">
                  <div class="item-date">{{ formatShortDate(diary.date) }}</div>
                  <div class="item-preview">
                    {{ diary.content.slice(0, 50) }}{{ diary.content.length > 50 ? '...' : '' }}
                  </div>
                </div>
                <div class="item-meta">
                  <span class="item-mood">{{ getMoodEmoji(diary.mood) }}</span>
                  <span v-if="diary.is_private" class="item-private">🔒</span>
                </div>
              </div>
              <div v-if="diaries.length === 0" class="list-empty">
                <span>📝</span>
                <span>还没有朝花夕拾</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧内容 -->
        <div class="diary-content">
          <!-- 有朝花夕拾时 -->
          <div v-if="selectedDiary || isEditing" class="diary-view">
            <div class="diary-header">
              <div class="diary-date-row">
                <h2 class="diary-date">
                  {{
                    formatDate(
                      editingDiary
                        ? editingDiary.date
                        : selectedDiary
                          ? selectedDiary.date
                          : editorForm.date,
                    )
                  }}
                </h2>
                <div class="diary-actions">
                  <template v-if="isEditing">
                    <button class="btn btn-sm" @click="cancelEdit">取消</button>
                    <button
                      class="btn btn-sm btn-primary"
                      @click="saveDiary"
                      :disabled="!editorForm.content.trim()"
                    >
                      保存
                    </button>
                  </template>
                  <template v-else>
                    <button class="btn btn-sm" @click="startEdit">编辑</button>
                    <button class="btn btn-sm btn-danger" @click="confirmDelete(selectedDiary)">
                      删除
                    </button>
                  </template>
                </div>
              </div>
              <!-- 编辑模式：心情/天气/私密选择 -->
              <div v-if="isEditing" class="diary-edit-meta">
                <div class="meta-row">
                  <span class="meta-label">心情</span>
                  <div class="meta-options">
                    <button
                      v-for="m in moods"
                      :key="m.value"
                      class="meta-option"
                      :class="{ active: editorForm.mood === m.value }"
                      @click="editorForm.mood = m.value"
                    >
                      {{ m.emoji }}
                    </button>
                  </div>
                </div>
                <div class="meta-row">
                  <span class="meta-label">天气</span>
                  <div class="meta-options">
                    <button
                      v-for="w in weathers"
                      :key="w.value"
                      class="meta-option"
                      :class="{ active: editorForm.weather === w.value }"
                      @click="editorForm.weather = w.value"
                    >
                      {{ w.emoji }}
                    </button>
                  </div>
                </div>
                <div class="meta-row">
                  <span class="meta-label">状态</span>
                  <button
                    class="toggle-btn"
                    :class="{ active: editorForm.is_private }"
                    @click="togglePrivate"
                  >
                    {{ editorForm.is_private ? '🔒 私密' : '🔓 公开' }}
                  </button>
                </div>
              </div>
              <!-- 非编辑模式：显示元数据 -->
              <div v-else class="diary-meta">
                <span class="meta-item">
                  <span class="meta-icon">{{ getMoodEmoji(selectedDiary.mood) }}</span>
                  <span>{{ getMoodLabel(selectedDiary.mood) }}</span>
                </span>
                <span class="meta-item">
                  <span class="meta-icon">{{ getWeatherEmoji(selectedDiary.weather) }}</span>
                  <span>{{ getWeatherLabel(selectedDiary.weather) }}</span>
                </span>
                <span v-if="selectedDiary.is_private" class="meta-item private">
                  <span class="meta-icon">🔒</span>
                  <span>私密</span>
                </span>
              </div>
            </div>
            <!-- 内容区 -->
            <div class="diary-body">
              <textarea
                v-if="isEditing"
                v-model="editorForm.content"
                class="diary-textarea"
                placeholder="写下今天的朝花夕拾..."
              ></textarea>
              <div v-else class="diary-text">{{ selectedDiary.content }}</div>
            </div>
          </div>
          <!-- 无朝花夕拾时 -->
          <div v-else class="diary-empty">
            <div class="empty-icon">📖</div>
            <p>选择日期查看日记，或点击"落笔"创建新朝花夕拾</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <div v-if="showEditor" class="modal-overlay" @click.self="closeEditor">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ editingDiary ? '编辑朝花夕拾' : '写朝花夕拾' }}</h3>
          <button class="close-btn" @click="closeEditor">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group" style="display: none">
            <label>日期</label>
            <input type="date" v-model="editorForm.date" class="form-input" />
          </div>
          <div class="form-group">
            <label>心情</label>
            <div class="option-grid">
              <button
                v-for="m in moods"
                :key="m.value"
                class="option-btn"
                :class="{ active: editorForm.mood === m.value }"
                @click="editorForm.mood = m.value"
              >
                <span class="option-emoji">{{ m.emoji }}</span>
                <span class="option-label">{{ m.label }}</span>
              </button>
            </div>
          </div>
          <div class="form-group">
            <label>天气</label>
            <div class="option-grid">
              <button
                v-for="w in weathers"
                :key="w.value"
                class="option-btn"
                :class="{ active: editorForm.weather === w.value }"
                @click="editorForm.weather = w.value"
              >
                <span class="option-emoji">{{ w.emoji }}</span>
                <span class="option-label">{{ w.label }}</span>
              </button>
            </div>
          </div>
          <div class="form-group">
            <label>内容</label>
            <textarea
              v-model="editorForm.content"
              placeholder="写下今天的朝花夕拾..."
              rows="8"
              class="form-textarea"
            ></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">私密</label>
            <button
              class="toggle-btn"
              :class="{ active: editorForm.is_private }"
              @click="togglePrivate"
            >
              <span class="toggle-track">
                <span class="toggle-thumb"></span>
              </span>
              <span>{{ editorForm.is_private ? '🔒 私密朝花夕拾' : '🔓 公开朝花夕拾' }}</span>
            </button>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn" @click="closeEditor">取消</button>
          <button class="btn btn-primary" @click="saveDiary" :disabled="!editorForm.content.trim()">
            {{ editingDiary ? '保存修改' : '保存朝花夕拾' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { diaryApi } from '../api'
import { inject } from 'vue'
import Calendar from '../components/report/Calendar.vue'

const showToast = inject('showToast')
const showConfirm = inject('showConfirm')

const today = new Date()
const selectedDate = ref(fmtDate(today))
const calYear = ref(today.getFullYear())
const calMonth = ref(today.getMonth())
const diaries = ref([])
const showEditor = ref(false)
const editingDiary = ref(null)
const showPrivate = ref(false)
const isEditing = ref(false)
const searchQuery = ref('')

const moods = [
  { value: 'happy', emoji: '😊', label: '开心' },
  { value: 'calm', emoji: '😌', label: '平静' },
  { value: 'anxious', emoji: '😰', label: '焦虑' },
  { value: 'down', emoji: '😔', label: '低落' },
  { value: 'angry', emoji: '😡', label: '生气' },
  { value: 'thinking', emoji: '🤔', label: '思考' },
]

const weathers = [
  { value: 'sunny', emoji: '☀️', label: '晴' },
  { value: 'cloudy', emoji: '⛅', label: '多云' },
  { value: 'rainy', emoji: '🌧️', label: '雨' },
  { value: 'snowy', emoji: '❄️', label: '雪' },
  { value: 'foggy', emoji: '🌫️', label: '雾' },
  { value: 'windy', emoji: '🌪️', label: '大风' },
]

const editorForm = ref({
  date: fmtDate(today),
  content: '',
  mood: 'calm',
  weather: 'sunny',
  is_private: false,
})

function fmtDate(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const calendarDays = computed(() => {
  const year = calYear.value
  const month = calMonth.value
  const first = new Date(year, month, 1)
  const last = new Date(year, month + 1, 0)
  const startDay = first.getDay()
  const days = []

  for (let i = startDay - 1; i >= 0; i--) {
    const d = new Date(year, month, -i)
    days.push({ day: d.getDate(), dateStr: fmtDate(d), currentMonth: false, isToday: false })
  }

  for (let i = 1; i <= last.getDate(); i++) {
    const d = new Date(year, month, i)
    days.push({
      day: i,
      dateStr: fmtDate(d),
      currentMonth: true,
      isToday: fmtDate(d) === fmtDate(today),
    })
  }

  const remaining = 42 - days.length
  for (let i = 1; i <= remaining; i++) {
    const d = new Date(year, month + 1, i)
    days.push({ day: i, dateStr: fmtDate(d), currentMonth: false, isToday: false })
  }

  return days
})

const diaryDatesSet = computed(() => {
  return new Set(diaries.value.map((d) => d.date))
})

const filteredDiaries = computed(() => {
  if (!searchQuery.value.trim()) return diaries.value
  const query = searchQuery.value.toLowerCase()
  return diaries.value.filter(d => {
    const content = (d.content || '').toLowerCase()
    const date = (d.date || '').toLowerCase()
    const mood = getMoodLabel(d.mood).toLowerCase()
    const weather = getWeatherLabel(d.weather).toLowerCase()
    return content.includes(query) || date.includes(query) || mood.includes(query) || weather.includes(query)
  })
})

const selectedDiary = computed(() => {
  return diaries.value.find((d) => d.date === selectedDate.value) || null
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const parts = dateStr.split('-')
  return `${parts[0]}年${parseInt(parts[1])}月${parseInt(parts[2])}日`
}

function formatShortDate(dateStr) {
  if (!dateStr) return ''
  const parts = dateStr.split('-')
  return `${parseInt(parts[1])}月${parseInt(parts[2])}日`
}

function getMoodEmoji(mood) {
  const m = moods.find((m) => m.value === mood)
  return m ? m.emoji : '😌'
}

function getMoodLabel(mood) {
  const m = moods.find((m) => m.value === mood)
  return m ? m.label : '平静'
}

function getWeatherEmoji(weather) {
  const w = weathers.find((w) => w.value === weather)
  return w ? w.emoji : '☀️'
}

function getWeatherLabel(weather) {
  const w = weathers.find((w) => w.value === weather)
  return w ? w.label : '晴'
}

async function loadDiaries() {
  try {
    const allDiaries = await diaryApi.list()
    if (showPrivate.value) {
      diaries.value = allDiaries
    } else {
      diaries.value = allDiaries.filter((d) => !d.is_private)
    }
  } catch (e) {
    console.error('加载朝花夕拾失败:', e)
  }
}

function selectDate(dateStr) {
  selectedDate.value = dateStr
}

function prevMonth() {
  if (calMonth.value === 0) {
    calMonth.value = 11
    calYear.value--
  } else {
    calMonth.value--
  }
}

function nextMonth() {
  if (calMonth.value === 11) {
    calMonth.value = 0
    calYear.value++
  } else {
    calMonth.value++
  }
}

function goToday() {
  calYear.value = today.getFullYear()
  calMonth.value = today.getMonth()
  selectedDate.value = fmtDate(today)
}

function changeYear(y) {
  calYear.value = y
}

function changeMonth(m) {
  calMonth.value = m
}

function toggleShowPrivate() {
  showPrivate.value = !showPrivate.value
  loadDiaries()
}

function editDiary(diary) {
  editingDiary.value = diary
  editorForm.value = {
    date: diary.date,
    content: diary.content,
    mood: diary.mood,
    weather: diary.weather,
    is_private: diary.is_private,
  }
  showEditor.value = true
}

function startEdit() {
  if (!selectedDiary.value) return
  editingDiary.value = selectedDiary.value
  editorForm.value = {
    date: selectedDiary.value.date,
    content: selectedDiary.value.content,
    mood: selectedDiary.value.mood,
    weather: selectedDiary.value.weather,
    is_private: selectedDiary.value.is_private,
  }
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
  editingDiary.value = null
}

function startNewDiary() {
  editingDiary.value = null
  editorForm.value = {
    date: selectedDate.value,
    content: '',
    mood: 'calm',
    weather: 'sunny',
    is_private: false,
  }
  isEditing.value = true
}

function openEditor() {
  editingDiary.value = null
  editorForm.value = {
    date: selectedDate.value,
    content: '',
    mood: 'calm',
    weather: 'sunny',
    is_private: false,
  }
  showEditor.value = true
}

function togglePrivate() {
  const newVal = !editorForm.value.is_private
  editorForm.value = { ...editorForm.value, is_private: newVal }
}

function closeEditor() {
  showEditor.value = false
  editingDiary.value = null
  editorForm.value = {
    date: fmtDate(today),
    content: '',
    mood: 'calm',
    weather: 'sunny',
    is_private: false,
  }
}

async function saveDiary() {
  if (!editorForm.value.content.trim()) return

  try {
    if (editingDiary.value) {
      await diaryApi.update(editingDiary.value.id, {
        content: editorForm.value.content,
        mood: editorForm.value.mood,
        weather: editorForm.value.weather,
        isPrivate: editorForm.value.is_private,
      })
      showToast('朝花夕拾已更新')
    } else {
      await diaryApi.create({
        date: editorForm.value.date,
        content: editorForm.value.content,
        mood: editorForm.value.mood,
        weather: editorForm.value.weather,
        isPrivate: editorForm.value.is_private,
      })
      showToast('朝花夕拾已保存')
    }
    closeEditor()
    isEditing.value = false
    editingDiary.value = null
    await loadDiaries()
    // 如果当前选中的朝花夕拾是私密且不显示私密，则清除选中
    if (selectedDiary.value && selectedDiary.value.is_private && !showPrivate.value) {
      selectedDate.value = fmtDate(today)
    }
  } catch (e) {
    console.error('保存朝花夕拾失败:', e)
    showToast('保存失败: ' + e)
  }
}

async function confirmDelete(diary) {
  if (!showConfirm) {
    await deleteDiary(diary)
    return
  }
  const ok = await showConfirm('确定删除这篇朝花夕拾吗？')
  if (ok) {
    await deleteDiary(diary)
  }
}

async function deleteDiary(diary) {
  try {
    await diaryApi.delete(diary.id)
    showToast('朝花夕拾已删除')
    await loadDiaries()
  } catch (e) {
    console.error('删除朝花夕拾失败:', e)
    showToast('删除失败: ' + e)
  }
}

onMounted(() => {
  loadDiaries()
})
</script>

<style scoped>
.view-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.page-header {
  padding: 20px 28px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.page-body {
  flex: 1;
  overflow: auto;
  padding: 20px 28px 28px;
}

.diary-layout {
  display: flex;
  gap: 16px;
  height: 100%;
}

/* 左侧边栏 */
.diary-sidebar {
  width: 25%;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.diary-sidebar :deep(.calendar) {
  width: 100%;
}

/* 朝花夕拾列表 */
.diary-list {
  flex: 1;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.list-header {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: space-between;
}

.list-search {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  background: var(--bg-surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  transition: border-color 0.15s;
  /* width: 180px; */
  flex-shrink: 0;
}

.list-search:focus-within {
  border-color: var(--accent);
}

.search-icon {
  width: 14px;
  height: 14px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  min-width: 0;
  border: none;
  background: transparent;
  color: var(--text);
  font-size: 12px;
  outline: none;
  padding: 2px;
}

.search-input::placeholder {
  color: var(--text-muted);
}

.list-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.btn-icon {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.btn-icon:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.btn-icon.active {
  background: var(--accent-bg);
  color: var(--accent);
}

.btn-icon svg {
  width: 16px;
  height: 16px;
}

.list-count {
  font-size: 11px;
  color: var(--text-muted);
  background: var(--bg-surface-2);
  padding: 2px 6px;
  border-radius: 10px;
}

.list-content {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.diary-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.15s;
  margin-bottom: 2px;
}

.diary-item:hover {
  background: var(--bg-hover);
}

.diary-item.active {
  background: var(--bg-active);
  border: 1px solid var(--border-light);
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-date {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 2px;
}

.item-preview {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.item-mood {
  font-size: 16px;
}

.item-private {
  font-size: 11px;
}

.list-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 40px 20px;
  color: var(--text-muted);
  font-size: 13px;
}

/* 右侧内容区 */
.diary-content {
  flex: 1;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.diary-view {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.diary-header {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
}

.diary-date-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.diary-date {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  margin: 0;
}

.diary-actions {
  display: flex;
  gap: 8px;
}

.diary-meta {
  display: flex;
  gap: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-sec);
  padding: 4px 10px;
  background: var(--bg-surface-2);
  border-radius: 20px;
}

.meta-icon {
  font-size: 14px;
}

.diary-body {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.diary-text {
  font-size: 14px;
  line-height: 1.8;
  color: var(--text);
  white-space: pre-wrap;
  word-wrap: break-word;
}

.diary-textarea {
  width: 100%;
  height: 100%;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg-surface-2);
  color: var(--text);
  font-size: 14px;
  line-height: 1.8;
  resize: none;
  outline: none;
  transition: border-color 0.15s;
}

.diary-textarea:focus {
  border-color: var(--accent);
}

.diary-edit-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 12px 0;
  border-top: 1px solid var(--border);
  margin-top: 12px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.meta-label {
  font-size: 12px;
  color: var(--text-muted);
  min-width: 32px;
}

.meta-options {
  display: flex;
  gap: 4px;
}

.meta-option {
  width: 32px;
  height: 32px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.meta-option:hover {
  border-color: var(--accent);
  background: var(--accent-bg);
}

.meta-option.active {
  border-color: var(--accent);
  background: var(--accent-bg);
}

.toggle-btn {
  padding: 6px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg-surface-2);
  color: var(--text-sec);
  cursor: pointer;
  font-size: 12px;
  transition: all 0.15s;
}

.toggle-btn:hover {
  border-color: var(--accent);
}

.toggle-btn.active {
  border-color: var(--accent);
  background: var(--accent-bg);
  color: var(--accent);
}

/* 空状态 */
.diary-empty {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.diary-empty p {
  font-size: 14px;
  margin: 0;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  width: 500px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.modal-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.close-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: var(--radius);
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.close-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 16px 20px;
  border-top: 1px solid var(--border);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-sec);
}

.form-input {
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg-surface-2);
  color: var(--text);
  font-size: 14px;
  transition: border-color 0.15s;
}

.form-input:focus {
  outline: none;
  border-color: var(--accent);
}

.form-textarea {
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg-surface-2);
  color: var(--text);
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  min-height: 120px;
  transition: border-color 0.15s;
}

.form-textarea:focus {
  outline: none;
  border-color: var(--accent);
}

.option-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.option-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 6px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: transparent;
  color: var(--text);
  cursor: pointer;
  transition: all 0.15s;
}

.option-btn:hover {
  border-color: var(--accent);
  background: var(--accent-bg);
}

.option-btn.active {
  border-color: var(--accent);
  background: var(--accent-bg);
  color: var(--accent);
}

.option-emoji {
  font-size: 18px;
}

.option-label {
  font-size: 11px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-sec);
}

.toggle-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg-surface-2);
  color: var(--text-sec);
  cursor: pointer;
  font-size: 13px;
  transition: all 0.15s;
}

.toggle-btn:hover {
  border-color: var(--border-light);
}

.toggle-btn.active {
  border-color: var(--accent);
  background: var(--accent-bg);
  color: var(--accent);
}

.toggle-track {
  width: 36px;
  height: 20px;
  border-radius: 10px;
  background: var(--border-light);
  position: relative;
  transition: background 0.2s;
  flex-shrink: 0;
}

.toggle-btn.active .toggle-track {
  background: var(--accent);
}

.toggle-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.2s;
}

.toggle-btn.active .toggle-thumb {
  transform: translateX(16px);
}

.btn-danger {
  color: var(--red);
  border-color: var(--red);
}

.btn-danger:hover {
  background: var(--red-bg);
}

@media (max-width: 768px) {
  .diary-layout {
    flex-direction: column;
  }
  .diary-sidebar {
    width: 100%;
    max-height: 300px;
  }
}
</style>

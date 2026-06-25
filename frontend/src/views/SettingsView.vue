<template>
  <div class="view-wrapper">
    <div class="page-header">
      <div class="page-title">设置</div>
    </div>
    <div class="page-body">
      <div class="settings-layout">
        <!-- 左侧导航 -->
        <div class="settings-nav">
          <button
            v-for="section in sections"
            :key="section.id"
            class="nav-item"
            :class="{ active: activeSection === section.id }"
            @click="activeSection = section.id"
          >
            <span class="nav-label">{{ section.label }}</span>
          </button>
        </div>

        <!-- 右侧内容 -->
        <div class="settings-content">
          <!-- 关于 -->
          <div v-if="activeSection === 'about'" class="content-section">
            <!-- <h3>关于</h3> -->
            <div class="settings-card">
              <div class="setting-row">
                <span class="setting-label">应用名称</span>
                <span class="setting-value">Gnothi (观己)</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">版本号</span>
                <span class="setting-value">v0.2.4</span>
              </div>
              <!-- <div class="setting-row">
                <span class="setting-label">技术栈</span>
                <span class="setting-value">Tauri 2 + Vue 3</span>
              </div> -->
              <div class="setting-row">
                <span class="setting-label">GitHub</span>
                <a class="setting-link" href="https://github.com/Cuixiaoboo/Gnothi" target="_blank"
                  >github.com/Cuixiaoboo/Gnothi</a
                >
              </div>
            </div>
          </div>

          <!-- 外观 -->
          <div v-if="activeSection === 'appearance'" class="content-section">
            <!-- <h3>外观</h3> -->
            <div class="settings-card">
              <div class="theme-options">
                <button
                  class="theme-option"
                  :class="{ active: currentTheme === 'dark' }"
                  @click="setTheme('dark')"
                >
                  <div class="theme-preview dark-preview">
                    <div class="preview-bar"></div>
                    <div class="preview-content">
                      <div class="preview-line"></div>
                      <div class="preview-line short"></div>
                    </div>
                  </div>
                  <span class="theme-name">深色</span>
                </button>
                <button
                  class="theme-option"
                  :class="{ active: currentTheme === 'gray' }"
                  @click="setTheme('gray')"
                >
                  <div class="theme-preview gray-preview">
                    <div class="preview-bar"></div>
                    <div class="preview-content">
                      <div class="preview-line"></div>
                      <div class="preview-line short"></div>
                    </div>
                  </div>
                  <span class="theme-name">青灰</span>
                </button>
                <button
                  class="theme-option"
                  :class="{ active: currentTheme === 'light' }"
                  @click="setTheme('light')"
                >
                  <div class="theme-preview light-preview">
                    <div class="preview-bar"></div>
                    <div class="preview-content">
                      <div class="preview-line"></div>
                      <div class="preview-line short"></div>
                    </div>
                  </div>
                  <span class="theme-name">浅色</span>
                </button>
                <button
                  class="theme-option"
                  :class="{ active: currentTheme === 'coral' }"
                  @click="setTheme('coral')"
                >
                  <div class="theme-preview coral-preview">
                    <div class="preview-bar"></div>
                    <div class="preview-content">
                      <div class="preview-line"></div>
                      <div class="preview-line short"></div>
                    </div>
                  </div>
                  <span class="theme-name">珊瑚</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 数据 -->
          <div v-if="activeSection === 'data'" class="content-section">
            <!-- <h3>数据</h3> -->
            <div class="settings-card">
              <div class="setting-row">
                <span class="setting-label">数据库路径</span>
                <span class="setting-value mono">./data/gnothi.db</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">日志路径</span>
                <span class="setting-value mono">./log/gnothi.log</span>
              </div>
            </div>
          </div>

          <!-- 工作时间 -->
          <div v-if="activeSection === 'worktime'" class="content-section">
            <!-- <h3>工作时间</h3> -->
            <div class="settings-card">
              <div class="setting-row">
                <span class="setting-label">下班时间</span>
                <div class="setting-control">
                  <TimePicker v-model="workEndTime" @update:modelValue="saveWorkEndTime" />
                </div>
              </div>
              <div class="setting-row">
                <span class="setting-label">说明</span>
                <span class="setting-value">设置后首页会显示下班倒计时</span>
              </div>
            </div>
          </div>

          <!-- 金句 -->
          <div v-if="activeSection === 'mottos'" class="content-section">
            <!-- <h3>金句</h3> -->
            <div class="settings-card">
              <div class="motto-add-row">
                <input
                  v-model="newMotto"
                  type="text"
                  placeholder="输入新的名言..."
                  class="motto-input"
                  @keyup.enter="addMotto"
                />
                <button class="motto-add-btn" @click="addMotto" :disabled="!newMotto.trim()">
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2.5"
                    stroke-linecap="round"
                  >
                    <line x1="12" y1="5" x2="12" y2="19" />
                    <line x1="5" y1="12" x2="19" y2="12" />
                  </svg>
                </button>
              </div>
              <div class="motto-list">
                <div class="motto-item" v-for="motto in mottos" :key="motto.id">
                  <div class="motto-content" v-if="editingId !== motto.id">{{ motto.content }}</div>
                  <input
                    v-else
                    v-model="editingContent"
                    class="motto-edit-input"
                    @keyup.enter="saveEdit(motto.id)"
                    @keyup.esc="cancelEdit"
                  />
                  <div class="motto-actions">
                    <button
                      v-if="editingId !== motto.id"
                      class="motto-action-btn"
                      @click="startEdit(motto)"
                      title="编辑"
                    >
                      <svg
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                      </svg>
                    </button>
                    <button
                      v-else
                      class="motto-action-btn save"
                      @click="saveEdit(motto.id)"
                      title="保存"
                    >
                      <svg
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2.5"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                    </button>
                    <button
                      class="motto-action-btn delete"
                      @click="deleteMotto(motto.id)"
                      title="删除"
                    >
                      <svg
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <polyline points="3 6 5 6 21 6" />
                        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
                      </svg>
                    </button>
                  </div>
                </div>
                <div class="motto-empty" v-if="mottos.length === 0">
                  <span>暂无名言，添加一条吧</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TimePicker from '../components/TimePicker.vue'
import { mottoApi } from '../api'

const activeSection = ref('about')
const currentTheme = ref('dark')
const workEndTime = ref('18:00')
const mottos = ref([])
const newMotto = ref('')
const editingId = ref(null)
const editingContent = ref('')

const sections = [
  { id: 'about', label: '关于' },
  { id: 'appearance', label: '外观' },
  { id: 'data', label: '数据' },
  { id: 'worktime', label: '工作时间' },
  { id: 'mottos', label: '金句' },
]

onMounted(async () => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    currentTheme.value = savedTheme
    applyTheme(savedTheme)
  }

  const savedTime = localStorage.getItem('workEndTime')
  if (savedTime) {
    workEndTime.value = savedTime
  }

  await loadMottos()
})

async function loadMottos() {
  try {
    mottos.value = await mottoApi.list()
  } catch (e) {
    console.error('加载名言失败:', e)
  }
}

async function addMotto() {
  if (!newMotto.value.trim()) return
  try {
    await mottoApi.create(newMotto.value.trim())
    newMotto.value = ''
    await loadMottos()
  } catch (e) {
    console.error('添加名言失败:', e)
  }
}

function startEdit(motto) {
  editingId.value = motto.id
  editingContent.value = motto.content
}

function cancelEdit() {
  editingId.value = null
  editingContent.value = ''
}

async function saveEdit(id) {
  if (!editingContent.value.trim()) return
  try {
    await mottoApi.update(id, editingContent.value.trim())
    editingId.value = null
    editingContent.value = ''
    await loadMottos()
  } catch (e) {
    console.error('更新名言失败:', e)
  }
}

async function deleteMotto(id) {
  try {
    await mottoApi.delete(id)
    await loadMottos()
  } catch (e) {
    console.error('删除名言失败:', e)
  }
}

function setTheme(theme) {
  currentTheme.value = theme
  localStorage.setItem('theme', theme)
  applyTheme(theme)
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme)
}

function saveWorkEndTime() {
  localStorage.setItem('workEndTime', workEndTime.value)
}
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
  flex-shrink: 0;
}

.page-title {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.page-body {
  flex: 1;
  overflow: hidden;
  padding: 20px 28px 28px;
}

.settings-layout {
  height: 100%;
  display: flex;
  gap: 16px;
}

/* ═══════════ Navigation ═══════════ */
.settings-nav {
  width: 180px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: var(--radius);
  border: none;
  background: transparent;
  color: var(--text-sec);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  text-align: left;
  transition: all 0.15s;
}

.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.nav-item.active {
  background: var(--accent-bg);
  color: var(--accent);
}

.nav-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.nav-label {
  white-space: nowrap;
}

/* ═══════════ Content ═══════════ */
.settings-content {
  flex: 1;
  overflow: auto;
  min-width: 0;
  border-left: 1px solid var(--border);
  padding-left: 16px;
}

.content-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.content-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
  flex-shrink: 0;
}

.settings-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: visible;
}

/* 金句卡片铺满 */
.content-section:has(.motto-add-row) {
  height: 100%;
}

.content-section:has(.motto-add-row) .settings-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}

.setting-row:last-child {
  border-bottom: none;
}

.setting-label {
  font-size: 14px;
  color: var(--text);
}

.setting-value {
  font-size: 13px;
  color: var(--text-muted);
}

.setting-value.mono {
  font-family: var(--mono);
  font-size: 12px;
}

.setting-link {
  font-size: 13px;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.15s;
}

.setting-link:hover {
  color: var(--accent);
  text-decoration: underline;
}

.setting-control {
  display: flex;
  align-items: center;
}

/* ═══════════ Theme ═══════════ */
.theme-options {
  display: flex;
  gap: 12px;
  padding: 16px;
}

.theme-option {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border-radius: var(--radius);
  border: 2px solid transparent;
  background: transparent;
  cursor: pointer;
  transition: all 0.15s;
}

.theme-option:hover {
  background: var(--bg-hover);
}

.theme-option.active {
  border-color: var(--accent);
  background: var(--accent-bg);
}

.theme-preview {
  width: 100%;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.dark-preview {
  background: #1a1a1f;
  border: 1px solid #2a2a32;
}

.gray-preview {
  background: #242a32;
  border: 1px solid #303842;
}

.light-preview {
  background: #ffffff;
  border: 1px solid #e0e0e0;
}

.preview-bar {
  height: 12px;
  background: #141418;
}

.gray-preview .preview-bar {
  background: #1e2228;
  border-bottom: 1px solid #303842;
}

.light-preview .preview-bar {
  background: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.preview-content {
  flex: 1;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.preview-line {
  height: 4px;
  border-radius: 2px;
  background: #2a2a32;
}

.gray-preview .preview-line {
  background: #303842;
}

.light-preview .preview-line {
  background: #e0e0e0;
}

.coral-preview {
  background: #FDF6EC;
  border: 1px solid #E0D5C5;
}

.coral-preview .preview-bar {
  background: #FCF1E4;
  border-bottom: 1px solid #E0D5C5;
}

.coral-preview .preview-line {
  background: #E0D5C5;
}

.preview-line.short {
  width: 60%;
}

.theme-name {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-sec);
}

/* ═══════════ Motto Management ═══════════ */
.motto-add-row {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}

.motto-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg);
  color: var(--text);
  font-size: 13px;
  outline: none;
}

.motto-input:focus {
  border-color: var(--accent);
}

.motto-input::placeholder {
  color: var(--text-muted);
}

.motto-add-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: var(--radius);
  background: var(--accent);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.motto-add-btn:hover:not(:disabled) {
  background: var(--accent-hover);
}

.motto-add-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.motto-list {
  flex: 1;
  overflow-y: auto;
}

.motto-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  border-bottom: 1px solid var(--border);
  gap: 12px;
}

.motto-item:last-child {
  border-bottom: none;
}

.motto-content {
  flex: 1;
  font-size: 13px;
  color: var(--text);
  line-height: 1.5;
}

.motto-edit-input {
  flex: 1;
  padding: 6px 10px;
  border: 1px solid var(--accent);
  border-radius: var(--radius);
  background: var(--bg);
  color: var(--text);
  font-size: 13px;
  outline: none;
}

.motto-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.motto-action-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: var(--radius);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.motto-action-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.motto-action-btn.save:hover {
  color: var(--green);
}

.motto-action-btn.delete:hover {
  color: var(--red);
  background: var(--red-bg);
}

.motto-empty {
  padding: 24px 16px;
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
}
</style>

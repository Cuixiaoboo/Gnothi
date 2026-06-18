<template>
  <div class="view-wrapper">
    <div class="page-header">
      <div class="page-title">设置</div>
    </div>
    <div class="page-body">
      <div class="settings-layout">
        <!-- 版本信息 -->
        <div class="settings-section">
          <div class="section-title">关于</div>
          <div class="settings-card">
            <div class="setting-row">
              <span class="setting-label">应用名称</span>
              <span class="setting-value">Gnothi&nbsp;(观己)</span>
            </div>
            <div class="setting-row">
              <span class="setting-label">版本号</span>
              <span class="setting-value">0.1.0</span>
            </div>
            <!-- <div class="setting-row">
              <span class="setting-label">技术栈</span>
              <span class="setting-value">Tauri 2 + Vue 3</span>
            </div> -->
          </div>
        </div>

        <!-- 皮肤选择 -->
        <div class="settings-section">
          <div class="section-title">外观</div>
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
            </div>
          </div>
        </div>

        <!-- 数据管理 -->
        <div class="settings-section">
          <div class="section-title">数据</div>
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
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentTheme = ref('dark')

onMounted(() => {
  // 从 localStorage 读取主题
  const saved = localStorage.getItem('theme')
  if (saved) {
    currentTheme.value = saved
    applyTheme(saved)
  }
})

function setTheme(theme) {
  currentTheme.value = theme
  localStorage.setItem('theme', theme)
  applyTheme(theme)
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme)
}

const themeNames = { dark: '深色', gray: '青灰', light: '浅色' }
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

.settings-layout {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.settings-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.settings-card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
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

.preview-line.short {
  width: 60%;
}

.theme-name {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-sec);
}
</style>

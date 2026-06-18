<template>
  <div class="titlebar" data-tauri-drag-region>
    <div class="titlebar-left">
      <!-- <span class="titlebar-icon">◆</span> -->
      <span class="titlebar-title">Gnothi</span>
    </div>
    <div class="titlebar-controls">
      <button class="tb-btn tb-min" @click="minimize" title="最小化">
        <svg width="12" height="12" viewBox="0 0 12 12">
          <line
            x1="2"
            y1="6"
            x2="10"
            y2="6"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
          />
        </svg>
      </button>
      <button class="tb-btn tb-max" @click="toggleMaximize" title="最大化">
        <svg
          v-if="!isMaximized"
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
          stroke="currentColor"
          stroke-width="1.2"
        >
          <rect x="1.5" y="1.5" width="9" height="9" rx="0.5" />
        </svg>
        <svg
          v-else
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
          stroke="currentColor"
          stroke-width="1.2"
        >
          <rect x="3" y="1" width="7.5" height="7.5" rx="0.5" />
          <path d="M1 4.5v6a1 1 0 001 1h6" />
        </svg>
      </button>
      <button class="tb-btn tb-close" @click="close" title="关闭">
        <svg width="12" height="12" viewBox="0 0 12 12">
          <line
            x1="2.5"
            y1="2.5"
            x2="9.5"
            y2="9.5"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
          />
          <line
            x1="9.5"
            y1="2.5"
            x2="2.5"
            y2="9.5"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getCurrentWindow } from '@tauri-apps/api/window'

const appWindow = getCurrentWindow()
const isMaximized = ref(false)

async function updateMaximizedState() {
  try {
    isMaximized.value = await appWindow.isMaximized()
  } catch (e) {}
}

async function minimize() {
  await appWindow.minimize()
}

async function toggleMaximize() {
  await appWindow.toggleMaximize()
  setTimeout(updateMaximizedState, 100)
}

async function close() {
  await appWindow.close()
}

onMounted(() => {
  updateMaximizedState()
  window.addEventListener('resize', updateMaximizedState)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateMaximizedState)
})
</script>

<style scoped>
.titlebar {
  align-items: center;
  height: 36px;
  background: var(--bg-sidebar);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  user-select: none;
  position: relative;
}

.titlebar-left {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  gap: 8px;
}

.titlebar-icon {
  color: var(--accent);
  font-size: 14px;
}

.titlebar-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-sec);
  letter-spacing: -0.3px;
}

.titlebar-controls {
  position: absolute;
  right: 0;
  display: flex;
  height: 100%;
}

.tb-btn {
  width: 46px;
  height: 100%;
  border: none;
  background: transparent;
  color: var(--text-sec);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.1s;
}

.tb-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.tb-close:hover {
  background: var(--red);
  color: #fff;
}
</style>

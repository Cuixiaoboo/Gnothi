<template>
  <aside class="sidebar" :class="{ collapsed }">
    <div class="sidebar-brand">
      <div class="brand-left">
        <img
          class="brand-icon"
          src="../../assets/k5vkm-g92oy-001.ico"
          alt="Gnothi"
          v-show="!collapsed"
        />
        <span class="brand-text" v-show="!collapsed">Gnothi</span>
      </div>
      <button
        class="collapse-btn"
        @click="collapsed = !collapsed"
        :title="collapsed ? '展开' : '收起'"
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
        >
          <polyline v-if="collapsed" points="9 18 15 12 9 6" />
          <polyline v-else points="15 18 9 12 15 6" />
        </svg>
      </button>
    </div>

    <div class="nav-list">
      <button
        v-for="item in navItems"
        :key="item.name"
        class="nav-btn"
        :class="{ active: page === item.name }"
        @click="$emit('navigate', item.name)"
        :title="item.label"
      >
        <component :is="item.icon" />
        <span class="nav-label" v-show="!collapsed">{{ item.label }}</span>
      </button>
    </div>

    <div class="sidebar-footer">
      <button
        class="nav-btn settings-btn"
        :class="{ active: page === 'settings' }"
        @click="$emit('navigate', 'settings')"
        title="设置"
      >
        <svg
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
        >
          <circle cx="12" cy="12" r="3" />
          <path
            d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"
          />
        </svg>
        <span class="nav-label" v-show="!collapsed">设置</span>
      </button>
      <!-- <span class="footer-version" v-show="!collapsed">v0.1.0</span>
      <button
        class="theme-toggle"
        @click="toggleTheme"
        :title="theme === 'dark' ? '切换青灰' : theme === 'gray' ? '切换浅色' : '切换深色'"
      >
        <svg
          v-if="theme === 'dark'"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
        >
          <circle cx="12" cy="12" r="5" />
          <line x1="12" y1="1" x2="12" y2="3" />
          <line x1="12" y1="21" x2="12" y2="23" />
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
          <line x1="1" y1="12" x2="3" y2="12" />
          <line x1="21" y1="12" x2="23" y2="12" />
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
        </svg>
        <svg
          v-else-if="theme === 'gray'"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
        >
          <circle cx="12" cy="12" r="5" />
          <line x1="12" y1="1" x2="12" y2="3" />
          <line x1="12" y1="21" x2="12" y2="23" />
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
          <line x1="1" y1="12" x2="3" y2="12" />
          <line x1="21" y1="12" x2="23" y2="12" />
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
        </svg>
        <svg
          v-else
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
        >
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      </button> -->
    </div>
  </aside>
</template>

<script setup>
import { ref, h } from 'vue'
import { useTheme } from '../composables/useTheme'

defineProps({
  page: { type: String, required: true },
})
defineEmits(['navigate'])

const { theme, toggleTheme } = useTheme()
const collapsed = ref(false)

const iconCalendar = {
  render() {
    return h(
      'svg',
      {
        viewBox: '0 0 24 24',
        fill: 'none',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
      },
      [
        h('rect', { x: 3, y: 4, width: 18, height: 18, rx: 2 }),
        h('line', { x1: 16, y1: 2, x2: 16, y2: 6 }),
        h('line', { x1: 8, y1: 2, x2: 8, y2: 6 }),
        h('line', { x1: 3, y1: 10, x2: 21, y2: 10 }),
      ],
    )
  },
}

const iconCheck = {
  render() {
    return h(
      'svg',
      {
        viewBox: '0 0 24 24',
        fill: 'none',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
      },
      [h('rect', { x: 3, y: 3, width: 18, height: 18, rx: 2 }), h('path', { d: 'M9 12l2 2 4-4' })],
    )
  },
}

const iconDoc = {
  render() {
    return h(
      'svg',
      {
        viewBox: '0 0 24 24',
        fill: 'none',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
      },
      [
        h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
        h('polyline', { points: '14 2 14 8 20 8' }),
        h('line', { x1: 16, y1: 13, x2: 8, y2: 13 }),
        h('line', { x1: 16, y1: 17, x2: 8, y2: 17 }),
      ],
    )
  },
}

const iconTools = {
  render() {
    return h(
      'svg',
      {
        viewBox: '0 0 24 24',
        fill: 'none',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
      },
      [
        h('path', { d: 'M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z' }),
      ],
    )
  },
}

const iconHome = {
  render() {
    return h(
      'svg',
      {
        viewBox: '0 0 24 24',
        fill: 'none',
        stroke: 'currentColor',
        'stroke-width': 2,
        'stroke-linecap': 'round',
      },
      [
        h('path', { d: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z' }),
        h('polyline', { points: '9 22 9 12 15 12 15 22' }),
      ],
    )
  },
}

const navItems = [
  { name: 'home', label: '首页', icon: iconHome },
  { name: 'report', label: '随手小记', icon: iconCalendar },
  { name: 'todo', label: '待办事项', icon: iconCheck },
  { name: 'notes', label: '个人笔记', icon: iconDoc },
  { name: 'tools', label: '工具箱', icon: iconTools },
]
</script>

<style scoped>
.brand-icon {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.sidebar {
  width: var(--sidebar-w);
  min-width: var(--sidebar-w);
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 20px 12px;
  gap: 4px;
  transition:
    width 0.3s ease,
    min-width 0.3s ease,
    padding 0.3s ease;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 64px;
  min-width: 64px;
  padding: 20px 10px;
}

.sidebar-brand {
  height: 32px;
  padding: 0 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar.collapsed .sidebar-brand {
  justify-content: center;
}

.brand-left {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
}

.brand-text {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: var(--text);
  white-space: nowrap;
}

.collapse-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius);
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.collapse-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-btn {
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
  width: 100%;
  height: 40px;
  overflow: hidden;
  transition:
    background 0.15s,
    color 0.15s;
}

.sidebar.collapsed .nav-btn {
  padding: 10px;
  justify-content: center;
}

.nav-label {
  white-space: nowrap;
}

.nav-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.nav-btn.active {
  background: var(--accent-bg);
  color: var(--accent);
}

.nav-btn svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.sidebar-footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 0;
}

.sidebar.collapsed .sidebar-footer {
  align-items: center;
}

.sidebar.collapsed .settings-btn {
  justify-content: center;
  padding: 10px;
}

.sidebar.collapsed .theme-toggle {
  margin: 0 auto;
}

.footer-version {
  font-size: 11px;
  color: var(--text-muted);
  white-space: nowrap;
}

.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--bg-surface);
  color: var(--text-sec);
  cursor: pointer;
  flex-shrink: 0;
  transition:
    background 0.15s,
    color 0.15s,
    border-color 0.15s;
}

.theme-toggle:hover {
  background: var(--bg-hover);
  color: var(--text);
  border-color: var(--border-light);
}

.theme-toggle svg {
  flex-shrink: 0;
}
</style>

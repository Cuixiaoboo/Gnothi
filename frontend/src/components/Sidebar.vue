<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <img class="brand-icon" src="../../assets/k5vkm-g92oy-001.ico" alt="Gnothi" />
      <span class="brand-text">&nbsp;观己</span>
    </div>

    <button
      v-for="item in navItems"
      :key="item.name"
      class="nav-btn"
      :class="{ active: page === item.name }"
      @click="$emit('navigate', item.name)"
    >
      <component :is="item.icon" />
      <span>{{ item.label }}</span>
    </button>

    <div class="sidebar-footer">
      <span class="footer-version">观己 v1.0.0</span>
      <button
        class="theme-toggle"
        @click="toggleTheme"
        :title="theme === 'dark' ? '切换亮色' : '切换暗色'"
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
      </button>
    </div>
  </aside>
</template>

<script setup>
import { h } from 'vue'
import { useTheme } from '../composables/useTheme'

defineProps({
  page: { type: String, required: true },
})
defineEmits(['navigate'])

const { theme, toggleTheme } = useTheme()

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
  { name: 'report', label: '每日日报', icon: iconCalendar },
  { name: 'todo', label: '待办事项', icon: iconCheck },
  { name: 'notes', label: '个人笔记', icon: iconDoc },
]
</script>

<style scoped>
.brand-icon {
  width: 32px;
  height: 32px;
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
}

.sidebar-brand {
  font-size: 18px;
  font-weight: 700;
  padding: 0 12px 20px;
  letter-spacing: -0.5px;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 8px;
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
  transition: all 0.15s;
  font-size: 14px;
  font-weight: 500;
  text-align: left;
  width: 100%;
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
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0 12px 0 12px;
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
  transition: all 0.15s;
  flex-shrink: 0;
  margin-left: auto;
}

.theme-toggle:hover {
  background: var(--bg-hover);
  color: var(--text);
  border-color: var(--border-light);
}

.theme-toggle svg {
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .sidebar {
    width: 56px;
    min-width: 56px;
    padding: 12px 6px;
  }

  .brand-text,
  .nav-btn span,
  .sidebar-footer {
    display: none;
  }

  .nav-btn {
    justify-content: center;
    padding: 10px;
  }
}
</style>

import { ref, watch } from 'vue'

const theme = ref(localStorage.getItem('theme') || 'dark')

function setTheme(t) {
  theme.value = t
  document.documentElement.setAttribute('data-theme', t)
  localStorage.setItem('theme', t)
}

function toggleTheme() {
  setTheme(theme.value === 'dark' ? 'light' : 'dark')
}

// 初始化
setTheme(theme.value)

export function useTheme() {
  return { theme, setTheme, toggleTheme }
}

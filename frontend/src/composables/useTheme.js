import { ref } from 'vue'

const theme = ref(localStorage.getItem('theme') || 'dark')

function setTheme(t) {
  theme.value = t
  document.documentElement.setAttribute('data-theme', t)
  localStorage.setItem('theme', t)
}

function toggleTheme() {
  const themes = ['dark', 'gray', 'light']
  const idx = themes.indexOf(theme.value)
  setTheme(themes[(idx + 1) % themes.length])
}

// 初始化
setTheme(theme.value)

export function useTheme() {
  return { theme, setTheme, toggleTheme }
}

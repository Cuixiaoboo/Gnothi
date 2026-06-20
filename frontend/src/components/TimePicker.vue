<template>
  <div class="time-picker" ref="pickerRef">
    <div class="time-display" @click="togglePicker">
      <span class="time-value">{{ displayTime }}</span>
      <span class="time-icon">🕐</span>
    </div>
    <div class="time-dropdown" v-if="isOpen">
      <div class="time-section">
        <div class="time-label">时</div>
        <div class="time-scroll">
          <div
            v-for="h in 24"
            :key="h"
            class="time-option"
            :class="{ active: selectedHour === h - 1 }"
            @click="selectHour(h - 1)"
          >
            {{ String(h - 1).padStart(2, '0') }}
          </div>
        </div>
      </div>
      <div class="time-divider">:</div>
      <div class="time-section">
        <div class="time-label">分</div>
        <div class="time-scroll">
          <div
            v-for="m in 60"
            :key="m"
            class="time-option"
            :class="{ active: selectedMinute === m - 1 }"
            @click="selectMinute(m - 1)"
          >
            {{ String(m - 1).padStart(2, '0') }}
          </div>
        </div>
      </div>
      <div class="time-actions">
        <button class="time-btn" @click="confirm" title="确定">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '18:00'
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)
const pickerRef = ref(null)

// 解析时间
const selectedHour = ref(18)
const selectedMinute = ref(0)

// 初始化
onMounted(() => {
  const [h, m] = props.modelValue.split(':').map(Number)
  selectedHour.value = h
  selectedMinute.value = m
})

// 监听外部变化
watch(() => props.modelValue, (newVal) => {
  const [h, m] = newVal.split(':').map(Number)
  selectedHour.value = h
  selectedMinute.value = m
})

// 显示时间
const displayTime = computed(() => {
  return `${String(selectedHour.value).padStart(2, '0')}:${String(selectedMinute.value).padStart(2, '0')}`
})

// 切换选择器
function togglePicker() {
  isOpen.value = !isOpen.value
}

// 选择小时
function selectHour(h) {
  selectedHour.value = h
}

// 选择分钟
function selectMinute(m) {
  selectedMinute.value = m
}

// 确认选择
function confirm() {
  emit('update:modelValue', displayTime.value)
  isOpen.value = false
}

// 点击外部关闭
function handleClickOutside(event) {
  if (pickerRef.value && !pickerRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.time-picker {
  position: relative;
}

.time-display {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg-surface-2);
  cursor: pointer;
  transition: all 0.2s;
  min-width: 100px;
}

.time-display:hover {
  border-color: var(--border-light);
}

.time-value {
  font-family: var(--mono);
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
}

.time-icon {
  font-size: 12px;
  opacity: 0.6;
}

.time-dropdown {
  position: absolute;
  bottom: calc(100% + 8px);
  right: 0;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 12px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  z-index: 100;
  animation: fadeIn 0.15s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.time-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.time-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.time-scroll {
  display: flex;
  flex-direction: column;
  height: 200px;
  overflow-y: auto;
  scrollbar-width: thin;
}

.time-scroll::-webkit-scrollbar {
  width: 4px;
}

.time-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.time-scroll::-webkit-scrollbar-thumb {
  background: var(--border);
  border-radius: 2px;
}

.time-option {
  padding: 6px 12px;
  font-family: var(--mono);
  font-size: 14px;
  color: var(--text-sec);
  cursor: pointer;
  border-radius: var(--radius);
  transition: all 0.15s;
  text-align: center;
  white-space: nowrap;
}

.time-option:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.time-option.active {
  background: var(--accent-bg);
  color: var(--accent);
  font-weight: 600;
}

.time-divider {
  font-family: var(--mono);
  font-size: 18px;
  font-weight: 600;
  color: var(--text-muted);
  padding-top: 28px;
}

.time-actions {
  display: flex;
  justify-content: center;
  padding-top: 12px;
  border-top: 1px solid var(--border);
  margin-top: 12px;
}

.time-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 20%;
  background: var(--accent);
  color: #fff;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.time-btn:hover {
  background: var(--accent-hover);
  transform: scale(1.1);
  box-shadow: 0 4px 12px var(--accent-bg);
}

.time-btn:active {
  transform: scale(1);
}
</style>

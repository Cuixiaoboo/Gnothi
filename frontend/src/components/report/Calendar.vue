<template>
  <div class="calendar">
    <div class="cal-header">
      <button class="cal-nav-btn" @click="prevMonth" title="上一月">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <polyline points="15 18 9 12 15 6" />
        </svg>
      </button>
      <select
        class="cal-select"
        :value="year"
        @change="$emit('changeYear', Number($event.target.value))"
      >
        <option v-for="y in yearRange" :key="y" :value="y">{{ y }}年</option>
      </select>
      <select
        class="cal-select"
        :value="month"
        @change="$emit('changeMonth', Number($event.target.value))"
      >
        <option v-for="m in 12" :key="m - 1" :value="m - 1">{{ m }}月</option>
      </select>
      <button class="cal-nav-btn" @click="nextMonth" title="下一月">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <polyline points="9 18 15 12 9 6" />
        </svg>
      </button>
    </div>
    <div class="cal-grid">
      <div class="cal-weekday" v-for="d in weekdays" :key="d">{{ d }}</div>
      <button
        v-for="(day, i) in days"
        :key="i"
        class="cal-day"
        :class="{
          'other-month': !day.currentMonth,
          today: day.isToday,
          selected: day.dateStr === selectedDate,
          'has-data': reportDates.has(day.dateStr),
        }"
        @click="$emit('select', day.dateStr)"
      >
        {{ day.day }}
      </button>
    </div>
    <button class="btn cal-today-btn" @click="$emit('goToday')">回到今天</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  selectedDate: String,
  year: Number,
  month: Number,
  days: Array,
  reportDates: { type: Set, default: () => new Set() },
})
const emit = defineEmits(['select', 'changeYear', 'changeMonth', 'goToday'])

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

const yearRange = computed(() => {
  const years = []
  for (let y = 2025; y <= 2035; y++) {
    years.push(y)
  }
  return years
})

function prevMonth() {
  if (props.month === 0) {
    emit('changeYear', props.year - 1)
    emit('changeMonth', 11)
  } else {
    emit('changeMonth', props.month - 1)
  }
}

function nextMonth() {
  if (props.month === 11) {
    emit('changeYear', props.year + 1)
    emit('changeMonth', 0)
  } else {
    emit('changeMonth', props.month + 1)
  }
}
</script>

<style scoped>
.calendar {
  width: 25%;
  flex-shrink: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.cal-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 12px;
}

.cal-nav-btn {
  width: 28px;
  height: 28px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-sec);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.15s;
}

.cal-nav-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
  border-color: var(--border-light);
}

.cal-select {
  flex: 1;
  min-width: 0;
  background: var(--bg-surface-2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 4px;
  border-radius: var(--radius);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  outline: none;
  text-align: center;
  appearance: none;
  -webkit-appearance: none;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cal-select:hover {
  border-color: var(--border-light);
}

.cal-select:focus {
  border-color: var(--accent);
}

.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  text-align: center;
}

.cal-weekday {
  font-size: 11px;
  color: var(--text-muted);
  padding: 4px 0;
  font-weight: 600;
  text-transform: uppercase;
}

.cal-day {
  padding: 6px 0;
  font-size: 13px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.1s;
  position: relative;
  border: none;
  background: transparent;
  color: var(--text-sec);
  font-family: var(--font);
}

.cal-day:hover {
  background: var(--bg-hover);
  color: var(--text);
}

.cal-day.today {
  color: var(--accent);
  font-weight: 700;
}

.cal-day.selected {
  background: var(--accent);
  color: #fff;
  font-weight: 700;
}

.cal-day.has-data::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--accent);
}

.cal-day.selected.has-data::after {
  background: #fff;
}

.cal-day.other-month {
  color: var(--text-muted);
  opacity: 0.4;
}

.cal-today-btn {
  margin-top: 12px;
  width: 100%;
}

@media (max-width: 768px) {
  .calendar {
    width: 100%;
  }
}
</style>

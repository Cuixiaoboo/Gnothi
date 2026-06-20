<template>
  <div class="view-wrapper">
    <div class="page-header">
      <div class="page-title">随手小记</div>
      <div class="save-indicator" :class="saveStatus">
        <template v-if="saveStatus === 'saving'">● 保存中...</template>
        <template v-else-if="saveStatus === 'saved'">✓ 已保存</template>
      </div>
    </div>
    <div class="page-body">
      <div class="report-layout">
        <Calendar
          :selected-date="selectedDate"
          :report-dates="reportDatesSet"
          @select="selectDate"
          @change-year="changeYear"
          @change-month="changeMonth"
          @go-today="goToday"
          :year="calYear"
          :month="calMonth"
          :days="calendarDays"
        />
        <ReportTable
          :date="selectedDate"
          :columns="columns"
          :rows="rows"
          @add-row="addRow"
          @remove-row="removeRow"
          @add-column="addColumn"
          @remove-column="removeColumn"
          @rename-column="renameColumn"
          @cell-input="onCellInput"
          @delete-report="deleteReport"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { reportApi } from '../api'
import { inject } from 'vue'
import Calendar from '../components/report/Calendar.vue'
import ReportTable from '../components/report/ReportTable.vue'

const showToast = inject('showToast')
const showConfirm = inject('showConfirm')

const today = new Date()
const selectedDate = ref(fmtDate(today))
const calYear = ref(today.getFullYear())
const calMonth = ref(today.getMonth())
const columns = ref([])
const rows = ref([])
const reportDatesSet = ref(new Set())
const saveStatus = ref('')
let saveTimer = null

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

function changeYear(y) {
  calYear.value = y
  // 自动选择该月的1号
  const dateStr = `${y}-${String(calMonth.value + 1).padStart(2, '0')}-01`
  selectDate(dateStr)
}

function changeMonth(m) {
  calMonth.value = m
  // 自动选择该月的1号
  const dateStr = `${calYear.value}-${String(m + 1).padStart(2, '0')}-01`
  selectDate(dateStr)
}

function goToday() {
  const now = new Date()
  calYear.value = now.getFullYear()
  calMonth.value = now.getMonth()
  selectDate(fmtDate(now))
}

async function loadReportDates() {
  try {
    const data = await reportApi.getDates()
    reportDatesSet.value = new Set(data)
  } catch (e) {
    console.error(e)
  }
}

async function loadReport(date) {
  try {
    const data = await reportApi.get(date)
    if (data.exists) {
      columns.value = data.columns || []
      rows.value = data.rows || []
    } else {
      // 新日报：初始化固定表头
      columns.value = [
        { key: 'content', label: '内容' },
        { key: 'status', label: '状态' },
        // { key: 'notes', label: '备注' },
      ]
      rows.value = []
    }
  } catch {
    columns.value = [
      { key: 'content', label: '内容' },
      { key: 'status', label: '状态' },
      // { key: 'notes', label: '备注' },
    ]
    rows.value = []
  }
}

function selectDate(dateStr) {
  selectedDate.value = dateStr
  loadReport(dateStr)
}

function addRow() {
  const row = {}
  columns.value.forEach((c) => {
    row[c.key] = ''
  })
  rows.value.push(row)
  saveReport()
}

function removeRow(index) {
  rows.value.splice(index, 1)
  saveReport()
}

function addColumn() {
  const key = 'col_' + Date.now()
  const label = '列' + (columns.value.length + 1)
  columns.value.push({ key, label })
  rows.value.forEach((r) => {
    r[key] = ''
  })
  saveReport()
}

function removeColumn(index) {
  const key = columns.value[index].key
  columns.value.splice(index, 1)
  rows.value.forEach((r) => {
    delete r[key]
  })
  saveReport()
}

function renameColumn(index, newLabel) {
  columns.value[index].label = newLabel
  saveReport()
}

function onCellInput(rowIdx, colKey, value) {
  if (!rows.value[rowIdx]) return
  rows.value[rowIdx][colKey] = value
  clearTimeout(saveTimer)
  saveTimer = setTimeout(() => saveReport(), 800)
}

async function saveReport() {
  clearTimeout(saveTimer)
  saveStatus.value = 'saving'
  try {
    await reportApi.save(selectedDate.value, { columns: columns.value, rows: rows.value })
    saveStatus.value = 'saved'
    reportDatesSet.value.add(selectedDate.value)
    setTimeout(() => {
      if (saveStatus.value === 'saved') saveStatus.value = ''
    }, 2000)
  } catch {
    saveStatus.value = ''
    showToast('保存失败', 'error')
  }
}

async function deleteReport() {
  const ok = await showConfirm(`确定删除 ${selectedDate.value} 的日报吗？`)
  if (!ok) return
  try {
    await reportApi.delete(selectedDate.value)
    columns.value = []
    rows.value = []
    reportDatesSet.value.delete(selectedDate.value)
    showToast('日报已删除')
  } catch {
    showToast('删除失败', 'error')
  }
}

onMounted(() => {
  loadReportDates()
  loadReport(selectedDate.value)
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

.report-layout {
  display: flex;
  gap: 20px;
  height: 100%;
}

.save-indicator {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-muted);
}

.save-indicator.saving {
  color: var(--yellow);
}

.save-indicator.saved {
  color: var(--green);
}

@media (max-width: 768px) {
  .report-layout {
    flex-direction: column;
  }
}
</style>

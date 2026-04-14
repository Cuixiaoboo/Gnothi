<template>
  <div class="report-table-area">
    <div class="table-toolbar">
      <button class="btn btn-primary btn-sm" @click="$emit('addRow')">
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        添加行
      </button>
      <button class="btn btn-sm" @click="$emit('addColumn')">
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        添加列
      </button>
      <div class="spacer"></div>
      <span class="date-label">{{ date }}</span>
    </div>
    <div class="table-wrapper">
      <table class="report-table" v-if="columns.length > 0">
        <thead>
          <tr>
            <th class="row-num"></th>
            <th v-for="(col, ci) in columns" :key="col.key">
              <div class="col-header">
                <input
                  class="col-label"
                  :value="col.label"
                  @change="$emit('renameColumn', ci, $event.target.value)"
                  @keydown.enter="$event.target.blur()"
                />
                <button class="col-delete" @click="$emit('removeColumn', ci)" title="删除列">
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>
            </th>
            <th class="row-delete"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, ri) in rows" :key="ri">
            <td class="row-num">{{ ri + 1 }}</td>
            <td v-for="col in columns" :key="col.key">
              <input
                :value="row[col.key] || ''"
                @input="$emit('cellInput', ri, col.key, $event.target.value)"
                @keydown.enter="$event.target.blur()"
              />
            </td>
            <td class="row-delete">
              <button class="btn-icon danger" @click="$emit('removeRow', ri)" title="删除行">
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
                  <path d="M10 11v6" />
                  <path d="M14 11v6" />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="empty" v-else>
        <div class="empty-icon">📋</div>
        <p>点击「添加行」和「添加列」开始编写日报</p>
      </div>
    </div>
    <div class="table-footer">
      <span class="footer-info">{{ rows.length }} 行 × {{ columns.length }} 列</span>
      <button
        class="btn btn-sm btn-danger"
        @click="$emit('deleteReport')"
        v-if="rows.length > 0 || columns.length > 0"
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
          <path d="M10 11v6" />
          <path d="M14 11v6" />
        </svg>
        删除日报
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  date: String,
  columns: Array,
  rows: Array,
})
defineEmits([
  'addRow',
  'removeRow',
  'addColumn',
  'removeColumn',
  'renameColumn',
  'cellInput',
  'deleteReport',
])
</script>

<style scoped>
.report-table-area {
  flex: 1;
  overflow: auto;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
}

.table-toolbar {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.table-toolbar .spacer {
  flex: 1;
}

.date-label {
  font-size: 12px;
  color: var(--text-muted);
}

.table-wrapper {
  flex: 1;
  overflow: auto;
}

.report-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.report-table th {
  background: var(--bg-surface-2);
  padding: 8px 12px;
  text-align: left;
  font-weight: 600;
  font-size: 12px;
  color: var(--text-sec);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
  position: sticky;
  top: 0;
  z-index: 1;
}

.col-header {
  display: flex;
  align-items: center;
  gap: 6px;
}

.col-label {
  background: transparent;
  border: none;
  color: var(--text-sec);
  font: inherit;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  width: 100%;
  outline: none;
  padding: 0;
}

.col-delete {
  opacity: 0;
  transition: opacity 0.15s;
  cursor: pointer;
  color: var(--text-muted);
  background: none;
  border: none;
  padding: 2px;
  display: flex;
  border-radius: 4px;
}

.report-table th:hover .col-delete {
  opacity: 1;
}

.col-delete:hover {
  color: var(--red);
}

.report-table td {
  padding: 0;
  border-bottom: 1px solid var(--border);
}

.report-table td input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 8px 12px;
  color: var(--text);
  outline: none;
  border-radius: 0;
}

.report-table td input:focus {
  background: var(--bg-hover);
  box-shadow: inset 0 0 0 2px var(--accent);
}

.report-table tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.row-num {
  width: 40px;
  text-align: center;
  color: var(--text-muted);
  font-family: var(--mono);
  font-size: 11px;
}

.row-delete {
  width: 36px;
  text-align: center;
}

.row-delete button {
  opacity: 0;
  transition: opacity 0.15s;
}

.report-table tr:hover .row-delete button {
  opacity: 1;
}

.table-footer {
  padding: 10px 16px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-info {
  font-size: 12px;
  color: var(--text-muted);
}

.btn-danger {
  background: var(--red-bg);
  color: var(--red);
  border-color: rgba(248, 113, 113, 0.3);
}

.btn-danger:hover {
  background: var(--red);
  color: #fff;
  border-color: var(--red);
}
</style>

<template>
  <div class="view-wrapper">
    <div class="page-header">
      <div class="page-title">个人笔记</div>
      <button class="btn btn-primary btn-sm" @click="addNote">
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
        新建笔记
      </button>
    </div>
    <div class="page-body">
      <div class="notes-layout">
        <NotesList
          :notes="filteredNotes"
          :selected-id="selectedId"
          :search="search"
          @select="selectedId = $event"
          @search="search = $event"
          @reorder="handleReorder"
        />
        <NoteEditor :note="currentNote" @update="updateField" @delete="deleteNote" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject, watch } from 'vue'
import { useRoute } from 'vue-router'
import { noteApi } from '../api'
import NotesList from '../components/notes/NotesList.vue'
import NoteEditor from '../components/notes/NoteEditor.vue'

const route = useRoute()
const showToast = inject('showToast')
const showConfirm = inject('showConfirm')

const notes = ref([])
const selectedId = ref(null)
const search = ref('')

const filteredNotes = computed(() => {
  if (!search.value.trim()) return notes.value
  const q = search.value.toLowerCase()
  return notes.value.filter(
    (n) => (n.title || '').toLowerCase().includes(q) || (n.content || '').toLowerCase().includes(q),
  )
})

const currentNote = computed(() => notes.value.find((n) => n.id === selectedId.value) || null)

async function loadNotes() {
  try {
    const data = await noteApi.list()
    notes.value = data
    // 如果路由参数中有 id，选中对应的笔记
    const noteId = Number(route.query.id)
    if (noteId && data.find((n) => n.id === noteId)) {
      selectedId.value = noteId
    } else if (data.length > 0) {
      selectedId.value = data[0].id
    }
  } catch (e) {
    console.error(e)
  }
}

// 监听路由参数变化
watch(
  () => route.query.id,
  (newId) => {
    const noteId = Number(newId)
    if (noteId && notes.value.find((n) => n.id === noteId)) {
      selectedId.value = noteId
    }
  },
)

async function addNote() {
  try {
    const data = await noteApi.create({ title: '新笔记' })
    notes.value.unshift(data)
    selectedId.value = data.id
    showToast('已创建笔记')
  } catch {
    showToast('创建失败', 'error')
  }
}

let updateTimer = null
async function updateField(field, value) {
  const idx = notes.value.findIndex((n) => n.id === selectedId.value)
  if (idx >= 0) notes.value[idx][field] = value
  clearTimeout(updateTimer)
  updateTimer = setTimeout(async () => {
    try {
      await noteApi.update(selectedId.value, { [field]: value })
    } catch {
      showToast('保存失败', 'error')
    }
  }, 600)
}

async function deleteNote(id) {
  const ok = await showConfirm('确定删除此笔记吗？')
  if (!ok) return
  try {
    await noteApi.delete(id)
    notes.value = notes.value.filter((n) => n.id !== id)
    if (selectedId.value === id) {
      selectedId.value = notes.value.length > 0 ? notes.value[0].id : null
    }
    showToast('已删除')
  } catch {
    showToast('删除失败', 'error')
  }
}

// 拖拽排序完成
async function handleReorder(orderedIds) {
  // 1. 本地立即按新顺序排列
  const idMap = new Map(notes.value.map((n) => [n.id, n]))
  notes.value = orderedIds.map((id) => idMap.get(id)).filter(Boolean)

  // 2. 持久化到后端（如果你的 API 支持批量排序）
  try {
    await noteApi.reorder(orderedIds)
  } catch {
    showToast('排序保存失败', 'error')
  }
}

onMounted(loadNotes)
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

.notes-layout {
  display: flex;
  gap: 16px;
  height: 100%;
}

@media (max-width: 768px) {
  .notes-layout {
    flex-direction: column;
  }
}
</style>

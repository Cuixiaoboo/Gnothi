<template>
  <div id="app-root">
    <TitleBar />
    <div class="app-body">
      <Sidebar :page="currentPage" @navigate="navigate" />
      <main class="main-content">
        <router-view />
      </main>
    </div>
    <Toast ref="toastRef" />
    <ConfirmDialog ref="confirmRef" />
  </div>
</template>

<script setup>
import { ref, computed, provide } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import TitleBar from './components/TitleBar.vue'
import Sidebar from './components/Sidebar.vue'
import Toast from './components/Toast.vue'
import ConfirmDialog from './components/ConfirmDialog.vue'

const router = useRouter()
const route = useRoute()
const toastRef = ref(null)
const confirmRef = ref(null)

const currentPage = computed(() => route.name || 'home')

function navigate(name) {
  router.push({ name })
}

function showToast(message, type = 'success') {
  toastRef.value?.show(message, type)
}

function showConfirm(message, icon) {
  return confirmRef.value?.show(message, icon)
}

provide('showToast', showToast)
provide('showConfirm', showConfirm)
</script>

<style scoped>
#app-root {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.app-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.main-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>

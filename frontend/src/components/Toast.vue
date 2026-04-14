<template>
  <Transition name="toast">
    <div v-if="visible" class="toast" :class="'toast-' + toastType">
      {{ message }}
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue'

const visible = ref(false)
const message = ref('')
const toastType = ref('success')
let timer = null

function show(msg, type = 'success') {
  clearTimeout(timer)
  message.value = msg
  toastType.value = type
  visible.value = true
  timer = setTimeout(() => {
    visible.value = false
  }, 2200)
}

defineExpose({ show })
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: var(--bg-surface-2);
  border: 1px solid var(--border-light);
  color: var(--text);
  padding: 10px 18px;
  border-radius: var(--radius);
  font-size: 13px;
  box-shadow: var(--shadow);
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 8px;
}

.toast-success {
  border-left: 3px solid var(--green);
}

.toast-error {
  border-left: 3px solid var(--red);
}

.toast-enter-active {
  animation: toastIn 0.3s ease;
}

.toast-leave-active {
  animation: toastOut 0.25s ease;
}

@keyframes toastIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes toastOut {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(12px);
  }
}
</style>

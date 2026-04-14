<template>
  <Teleport to="body">
    <Transition name="modal">
      <div class="modal-overlay" v-if="visible" @click.self="onCancel">
        <div class="modal-box">
          <!-- <div class="modal-icon">{{ icon }}</div> -->
          <div class="modal-message">{{ message }}</div>
          <div class="modal-actions">
            <button class="btn" @click="onCancel">取消</button>
            <button class="btn btn-danger" @click="onConfirm">确定</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const visible = ref(false)
const message = ref('')
// const icon = ref('⚠️')
let resolvePromise = null

function show(msg) {
  message.value = msg
//   icon.value = emoji
  visible.value = true
  return new Promise((resolve) => {
    resolvePromise = resolve
  })
}

function onConfirm() {
  visible.value = false
  resolvePromise?.(true)
}

function onCancel() {
  visible.value = false
  resolvePromise?.(false)
}

defineExpose({ show })
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

.modal-box {
  background: var(--bg-surface);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 28px 32px;
  min-width: 320px;
  max-width: 420px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5);
  text-align: center;
}

.modal-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.modal-message {
  font-size: 15px;
  color: var(--text);
  line-height: 1.6;
  margin-bottom: 24px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.modal-actions .btn {
  padding: 8px 20px;
}

.btn-danger {
  background: var(--red);
  color: #fff;
  border-color: var(--red);
}

.btn-danger:hover {
  background: #e05555;
  border-color: #e05555;
}

.modal-enter-active {
  animation: fadeIn 0.2s ease;
}

.modal-leave-active {
  animation: fadeOut 0.15s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
</style>

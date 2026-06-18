<template>
  <div class="view-wrapper">
    <div class="page-header">
      <div class="page-title">工具箱</div>
    </div>
    <div class="page-body">
      <div class="tools-layout">
        <!-- 工具导航 -->
        <div class="tools-nav">
          <button
            v-for="tool in tools"
            :key="tool.id"
            class="tool-nav-btn"
            :class="{ active: activeTool === tool.id }"
            @click="activeTool = tool.id"
          >
            <span class="tool-icon">{{ tool.icon }}</span>
            <span class="tool-name">{{ tool.name }}</span>
          </button>
        </div>

        <!-- 工具内容 -->
        <div class="tools-content">
          <JsonFormatter v-if="activeTool === 'json'" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import JsonFormatter from '../components/tools/JsonFormatter.vue'

const activeTool = ref('json')

const tools = [
  { id: 'json', name: 'JSON 格式化', icon: '{ }' },
  // 后续可以添加更多工具
  // { id: 'regex', name: '正则测试', icon: '.*' },
  // { id: 'timestamp', name: '时间戳转换', icon: '⏱' },
  // { id: 'base64', name: 'Base64 编解码', icon: 'B64' },
]
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

.tools-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tools-nav {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tool-nav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--bg-surface);
  color: var(--text-sec);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.15s;
}

.tool-nav-btn:hover {
  background: var(--bg-hover);
  color: var(--text);
  border-color: var(--border-light);
}

.tool-nav-btn.active {
  background: var(--accent-bg);
  color: var(--accent);
  border-color: var(--accent);
}

.tool-icon {
  font-family: var(--mono);
  font-weight: 700;
  font-size: 13px;
}

.tools-content {
  flex: 1;
  overflow: hidden;
}
</style>

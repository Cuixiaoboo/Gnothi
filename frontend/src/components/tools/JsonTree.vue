<template>
  <div class="json-tree">
    <template v-for="(item, index) in nodes" :key="index">
      <div class="json-line" :style="{ paddingLeft: item.depth * 20 + 'px' }">
        <!-- 展开/收缩按钮 -->
        <span 
          v-if="item.expandable" 
          class="json-toggle" 
          @click="toggleExpand(item.id)"
        >
          {{ expanded[item.id] ? '▼' : '▶' }}
        </span>
        <span v-else class="json-toggle-space"></span>
        
        <!-- 键名 -->
        <span v-if="item.key !== undefined" class="json-key">"{{ item.key }}"</span>
        <span v-if="item.key !== undefined" class="json-colon">: </span>
        
        <!-- 值 -->
        <template v-if="!item.expandable">
          <span :class="getValueClass(item.value)">{{ formatValue(item.value) }}</span>
        </template>
        <template v-else-if="!expanded[item.id]">
          <span class="json-bracket">{{ item.bracketOpen }}</span>
          <span class="json-ellipsis">...</span>
          <span class="json-bracket">{{ item.bracketClose }}</span>
        </template>
        <template v-else>
          <span class="json-bracket">{{ item.bracketOpen }}</span>
        </template>
        
        <!-- 逗号 -->
        <span v-if="item.comma" class="json-comma">,</span>
      </div>
      
      <!-- 收缩时的结束括号 -->
      <div 
        v-if="item.expandable && expanded[item.id]" 
        class="json-line" 
        :style="{ paddingLeft: item.depth * 20 + 'px' }"
      >
        <span class="json-toggle-space"></span>
        <span class="json-bracket">{{ item.bracketClose }}</span>
        <span v-if="item.comma" class="json-comma">,</span>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  data: {
    type: [Object, Array, String, Number, Boolean, null],
    default: null
  }
})

const expanded = ref({})

// 将 JSON 数据转换为扁平节点列表
const nodes = computed(() => {
  const result = []
  let id = 0
  
  function processNode(value, key, depth, isLast) {
    const nodeId = id++
    const isObject = typeof value === 'object' && value !== null && !Array.isArray(value)
    const isArray = Array.isArray(value)
    const expandable = isObject || isArray
    
    // 默认展开前3层
    if (expandable && depth < 3) {
      expanded.value[nodeId] = true
    }
    
    const item = {
      id: nodeId,
      key: key,
      depth: depth,
      expandable: expandable,
      value: expandable ? null : value,
      bracketOpen: isArray ? '[' : '{',
      bracketClose: isArray ? ']' : '}',
      comma: !isLast
    }
    
    result.push(item)
    
    if (expandable && expanded.value[nodeId]) {
      const entries = isObject ? Object.entries(value) : value.map((v, i) => [i, v])
      entries.forEach(([k, v], idx) => {
        processNode(v, isObject ? k : undefined, depth + 1, idx === entries.length - 1)
      })
    }
  }
  
  if (props.data !== null && props.data !== undefined) {
    processNode(props.data, undefined, 0, true)
  }
  
  return result
})

function toggleExpand(id) {
  expanded.value[id] = !expanded.value[id]
}

function getValueClass(value) {
  if (value === null) return 'json-null'
  if (typeof value === 'boolean') return 'json-boolean'
  if (typeof value === 'number') return 'json-number'
  if (typeof value === 'string') return 'json-string'
  return ''
}

function formatValue(value) {
  if (value === null) return 'null'
  if (typeof value === 'string') return `"${value}"`
  return String(value)
}
</script>

<style scoped>
.json-tree {
  font-family: var(--mono);
  font-size: 13px;
  line-height: 1.6;
  padding: 12px;
  overflow: auto;
}

.json-line {
  display: flex;
  align-items: baseline;
  padding: 1px 0;
}

.json-toggle {
  cursor: pointer;
  user-select: none;
  color: var(--text-muted);
  font-size: 10px;
  width: 16px;
  text-align: center;
  flex-shrink: 0;
}

.json-toggle:hover {
  color: var(--text);
}

.json-toggle-space {
  width: 16px;
  flex-shrink: 0;
}

.json-key {
  color: #e06c75;
}

.json-string {
  color: #98c379;
}

.json-number {
  color: #d19a66;
}

.json-boolean {
  color: #56b6c2;
}

.json-null {
  color: #c678dd;
}

.json-bracket {
  color: var(--text-muted);
}

.json-colon {
  color: var(--text-muted);
}

.json-comma {
  color: var(--text-muted);
}

.json-ellipsis {
  color: var(--text-muted);
  font-style: italic;
}
</style>

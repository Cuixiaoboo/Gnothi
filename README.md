# Gnothi（观己）

一个基于 Tauri 2 + Vue 3 的桌面工作助手，帮助你管理日常工作中的笔记、待办和日报。

## 功能特性

- 📒 **笔记管理**：创建、编辑、删除、拖拽排序
- ✅ **待办事项**：任务管理、优先级、完成状态
- 📅 **日报记录**：每日数据表格式记录，支持日历视图
- 🎨 **多主题支持**：深色、青灰、浅色三套主题
- 🖥️ **自定义标题栏**：支持窗口拖拽、最小化、最大化、关闭
- 📁 **侧边栏收起**：支持展开/收起，节省屏幕空间

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Rust + Tauri 2 |
| 前端 | Vue 3 + Vite + Vue Router |
| 数据库 | SQLite（通过 rusqlite） |
| 日志 | tauri-plugin-log |
| 状态管理 | Vue Composition API |

## 项目结构

```
Gnothi/
├── src-tauri/              # Rust 后端
│   ├── src/
│   │   └── main.rs         # 应用入口、数据库操作、Tauri 命令
│   ├── capabilities/       # 权限配置
│   ├── icons/              # 应用图标
│   ├── Cargo.toml          # Rust 依赖
│   └── tauri.conf.json     # Tauri 配置
├── frontend/               # Vue3 前端
│   ├── src/
│   │   ├── api/            # 调用 Tauri 命令
│   │   ├── components/     # 组件
│   │   ├── composables/    # 组合式函数（主题等）
│   │   ├── views/          # 页面视图
│   │   ├── router/         # 路由配置
│   │   └── styles/         # 全局样式
│   └── package.json
├── assets/                 # 静态资源
├── Cargo.toml              # Rust workspace 配置
├── package.json            # Tauri CLI
└── README.md
```

## 数据存储

应用使用相对路径存储数据，便于打包和迁移：

```
<应用运行目录>/
├── data/
│   └── gnothi.db           # SQLite 数据库
└── log/
    └── gnothi.log          # 应用日志（超过 10MB 自动清空）
```

## 快速开始

### 1. 安装依赖

```bash
# 前端依赖
cd frontend
npm install

# 回到根目录
cd ..

# 安装 Tauri CLI
npm install
```

### 2. 启动开发环境

```bash
npm run tauri dev
```

### 3. 打包桌面应用

```bash
npm run tauri build
```

打包产物位于 `src-tauri/target/release/bundle/`，包含：
- Windows: `.exe` 或 `.msi`（约 3-10MB）
- macOS: `.app` 或 `.dmg`
- Linux: `.deb` 或 `.AppImage`

## 开发命令

```bash
# 开发模式（热重载）
npm run tauri dev

# 仅前端开发
cd frontend && npm run dev

# 构建发布版
npm run tauri build

# 构建调试版
npm run tauri build --debug
```

## 窗口配置

- 窗口大小：1200 x 800（固定，不可调整）
- 无原生标题栏（使用自定义标题栏）
- 支持窗口拖拽
- 支持最小化、最大化、关闭

## 主题系统

应用内置三套主题，可通过侧边栏底部的主题按钮切换，或在设置页面选择：

| 主题 | 说明 |
|------|------|
| 深色 | 纯黑背景，适合夜间使用 |
| 青灰 | 偏蓝的深灰色，柔和不刺眼 |
| 浅色 | 纯白背景，适合白天使用 |

主题选择会保存到 localStorage，下次打开应用会自动应用。

## 数据模型

### 笔记（Note）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| title | TEXT | 笔记标题 |
| content | TEXT | 笔记内容 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |
| sort_order | INTEGER | 排序顺序 |

### 待办（Todo）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| title | TEXT | 任务标题 |
| status | TEXT | 状态（pending/in_progress/completed/hangup） |
| priority | TEXT | 优先级（high/medium/low） |
| due_date | TEXT | 截止日期 |
| notes | TEXT | 备注 |
| completed_at | TEXT | 完成时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 日报（DailyReport）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| date | TEXT | 日期（YYYY-MM-DD） |
| columns | TEXT | 表头配置（JSON） |
| rows | TEXT | 表格数据（JSON） |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

## 后续规划

- [ ] 笔记 Block 编辑器（标题、段落、代码块）
- [ ] 全局搜索
- [ ] 数据导入导出
- [ ] 系统托盘
- [ ] 工作计时与统计

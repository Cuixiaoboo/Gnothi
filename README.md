# Gnothi（观己）

一个基于 Tauri 2 + Vue 3 的桌面工作助手，帮助你管理日常工作中的笔记、待办和日报。

## 功能特性

### 核心功能
- 📒 **笔记管理**：创建、编辑、删除、拖拽排序，支持 Block 编辑器（标题、段落、代码块）
- ✅ **待办事项**：任务管理、优先级、完成状态
- 📅 **日报记录**：每日数据表格式记录，支持日历视图
- 🛠️ **工具箱**：JSON 格式化等实用工具

### 界面特性
- 🎨 **多主题支持**：深色、青灰、浅色三套主题
- 🖥️ **自定义标题栏**：支持窗口拖拽、最小化、最大化、关闭
- 📁 **侧边栏收起**：支持展开/收起，节省屏幕空间
- ⏰ **下班倒计时**：首页显示距离下班的时间

### 趣味功能
- 💬 **摸鱼名言**：首页底部随机显示摸鱼名言，支持增删改
- 📊 **仪表盘首页**：统计卡片 + 待办/笔记列表 + 下班倒计时

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Rust + Tauri 2 |
| 前端 | Vue 3 + Vite + Vue Router |
| 数据库 | SQLite（通过 rusqlite） |
| 编辑器 | Tiptap（Block 编辑器） |
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
│   │   │   ├── notes/      # 笔记相关组件（BlockEditor、NoteEditor）
│   │   │   ├── tools/      # 工具箱组件（JsonFormatter）
│   │   │   └── ...         # 其他组件
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
- 最小尺寸：800 x 600
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
| content | TEXT | 笔记内容（支持 JSON Block 格式或纯文本） |
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

### 名言（Motto）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| content | TEXT | 名言内容 |
| created_at | DATETIME | 创建时间 |

## 更新日志

### v0.2.0（当前版本）

#### 新增功能

**首页改造**
- 仪表盘风格布局：统计卡片 + 待办/笔记列表
- 下班倒计时：实时显示距离下班的时间
- 摸鱼名言：首页底部随机显示名言，支持刷新切换
- 快捷入口：快速访问日报、待办、笔记、工具箱

**工具箱**
- JSON 格式化：支持格式化、压缩、提取 JSON
- 支持从混合文本中提取 JSON 部分
- 输入内容本地存储，切换页面不丢失

**摸鱼名言系统**
- 数据库存储名言，支持增删改
- 设置页面侧边栏式管理界面
- 首页每天固定显示一条，支持随机刷新
- 首次启动自动插入 10 条默认名言

**下班倒计时**
- 设置页面可配置下班时间（默认 18:00）
- 自定义时间选择器组件
- 首页实时倒计时显示

**设置页面**
- 侧边栏式布局：关于、外观、数据、工作时间、摸鱼名言
- 主题切换（深色、青灰、浅色）
- 下班时间设置
- 名言管理（增删改）

**笔记 Block 编辑器**
- 基于 Tiptap 实现
- 支持标题（H1-H3）、段落、代码块
- 代码块支持语法高亮
- 兼容旧的纯文本笔记格式

**日志系统**
- 使用 tauri-plugin-log
- 日志文件存储在 `./log/gnothi.log`
- 超过 10MB 自动清空
- 使用本地时间

#### 界面优化

- 自定义标题栏：支持窗口拖拽、最小化、最大化、关闭
- 侧边栏收起/展开：节省屏幕空间
- 多主题支持：深色、青灰、浅色三套主题
- 响应式布局：适配不同屏幕尺寸
- 统一的 UI 风格：圆角、阴影、过渡动画

#### 技术改进

- Tauri 2 + Vue 3 架构
- SQLite 数据库存储
- 前端使用 Tiptap Block 编辑器
- 日志系统集成
- 权限配置（capabilities）

### v0.1.0

- 初始版本
- 基础功能：笔记、待办、日报
- Flask + PyWebview 架构（已迁移至 Tauri 2）

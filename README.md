# Gnothi

Gnothi 是一个基于 Flask + Vue3 的桌面/网页一体化知识管理与日常记录应用，支持笔记、待办、日报等功能，适合个人效率提升与知识沉淀。

## 项目结构

```
gnothi/
├── backend/      # Python Flask 后端，含 API、数据库、桌面端入口
├── frontend/     # Vue3 前端，支持网页与桌面端
├── assets/       # 资源文件
└── README.md     # 项目说明文档
```

## 项目截图
<img src="assets\image.png">

## 主要功能

- 📒 笔记管理：创建、编辑、删除、查询笔记
- ✅ 待办事项：任务管理、优先级、完成状态
- 📅 日报记录：每日数据表格式记录
- 🖥️ 桌面端：PyWebview 打包，原生窗口体验
- 🌐 网页端：Vite + Vue3 SPA，现代前端体验

## 技术栈

- 后端：Python 3, Flask, Flask-CORS, Flask-SQLAlchemy, SQLite
- 前端：Vue 3, Vite, Vue Router, Axios
- 桌面端：PyWebview
- 打包：PyInstaller

## 快速开始

### 1. 安装依赖

#### 后端依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 前端依赖

```bash
cd frontend
npm install
```

### 2. 启动开发环境

#### 启动后端 API

```bash
cd backend
python app.py
```

#### 启动前端

```bash
cd frontend
npm run dev
```

访问：http://localhost:5173

### 3. 启动桌面端

```bash
cd backend
python desktop.py
```

### 4. 打包桌面应用

```bash
cd backend
python build.py
```
- 项目采用免安装的方式打包，打包后的文件位于 `backend/dist/`，可直接将exe文件拖入任意目录运行。

## 数据库

- 默认使用 SQLite，数据库文件位于 `backend/gnothi.db` 或打包后同级目录下的 `gnothi_data/gnothi.db`。

## 目录说明

- `backend/app.py`：后端 API 启动入口
- `backend/desktop.py`：桌面端启动入口（内嵌 Flask + Webview）
- `backend/models/`：数据模型（笔记、待办、日报）
- `backend/routes/`：API 路由
- `frontend/`：Vue3 前端源码

## 依赖列表

### 后端

- flask==3.0.3
- flask-cors==5.0.0
- flask-sqlalchemy==3.1.1
- pywebview==6.2

### 前端

- vue ^3.5.31
- vue-router ^5.0.4
- axios ^1.15.0
- vite ^8.0.3
- vuedraggable ^4.1.0
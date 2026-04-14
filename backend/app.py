"""
gnothi 后端入口
启动方式: python app.py
"""

import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from routes import register_blueprints
from utils import setup_logging


def create_app():
    """
    应用工厂函数：创建并配置 Flask 应用实例
    """
    # 初始化 Flask 应用
    app = Flask(__name__)

    # 加载配置对象
    app.config.from_object(Config)

    # 启用跨域资源共享 (CORS)，允许前端跨域访问 API
    CORS(app)

    # 初始化日志
    logger = setup_logging(app)

    # 初始化数据库扩展，绑定到当前 app 实例
    db.init_app(app)

    # 注册所有蓝图（路由模块）
    register_blueprints(app)

    # --- 前端静态文件服务配置（适用于生产环境或单体部署）---
    # 构建前端 dist 目录的绝对路径
    frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

    # 如果前端构建产物存在，则配置静态文件服务
    if os.path.exists(frontend_dist):
        # 设置静态文件夹路径
        app.static_folder = frontend_dist

        @app.route("/")
        def index():
            """
            根路径：返回前端入口 HTML 文件
            """
            return send_from_directory(frontend_dist, "index.html")

        @app.route("/<path:path>")
        def static_files(path):
            """
            通配符路径：处理前端路由刷新及静态资源请求
            注意：这可能会拦截未匹配到后端 API 的所有请求
            """
            return send_from_directory(frontend_dist, path)

    # 在应用上下文中创建数据库表（如果不存在）
    with app.app_context():
        db.create_all()

    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)

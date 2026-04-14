"""
Gnothi 桌面应用入口
"""

import os
import sys
import threading
import time
import webview
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config
from models import db
from routes import register_blueprints
from utils import setup_logging


def get_base_path():
    if getattr(sys, "_MEIPASS", None):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def get_data_dir():
    if getattr(sys, "_MEIPASS", None):
        exe_dir = os.path.dirname(sys.executable)
        data_dir = os.path.join(exe_dir, "gnothi_data")
        os.makedirs(data_dir, exist_ok=True)
        return data_dir
    return os.path.dirname(os.path.abspath(__file__))


class WindowApi:
    """暴露给前端的窗口控制 API"""

    def __init__(self, window):
        self.window = window

    def minimize(self):
        self.window.minimize()

    def toggle_maximize(self):
        if self.window.get_state() == webview.FULLSCREEN:
            self.window.restore()
        elif self.window.get_state() == webview.MAXIMIZED:
            self.window.restore()
        else:
            self.window.maximize()

    def close(self):
        self.window.destroy()

    def is_maximized(self):
        return self.window.get_state() in (webview.MAXIMIZED, webview.FULLSCREEN)

    def move(self, x, y):
        """移动窗口（用于拖拽）"""
        self.window.move(x, y)


def create_desktop_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    data_dir = get_data_dir()
    db_path = os.path.join(data_dir, "gnothi.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    CORS(app)
    setup_logging(app)

    db.init_app(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    static_dir = os.path.join(get_base_path(), "frontend", "dist")

    @app.route("/")
    def index():
        return send_from_directory(static_dir, "index.html")

    @app.route("/<path:path>")
    def static_files(path):
        return send_from_directory(static_dir, path)

    return app


def start_flask(app):
    app.run(host="127.0.0.1", port=5173, debug=False, use_reloader=False)


def main():
    app = create_desktop_app()

    thread = threading.Thread(target=start_flask, args=(app,), daemon=True)
    thread.start()
    time.sleep(1)

    INIT_W, INIT_H = 1200, 800

    window = webview.create_window(
        title="Gnothi",
        url="http://127.0.0.1:5173",
        width=INIT_W,
        height=INIT_H,
        min_size=(800, 600),
        frameless=True,
        easy_drag=False,
    )

    is_max = [False]
    saved = {"x": 0, "y": 0, "w": INIT_W, "h": INIT_H}

    def minimize():
        window.minimize()

    def toggle_maximize():
        if is_max[0]:
            window.resize(saved["w"], saved["h"])
            window.move(saved["x"], saved["y"])
            is_max[0] = False
        else:
            saved["x"], saved["y"] = window.x, window.y
            saved["w"], saved["h"] = window.width, window.height
            screens = webview.screens
            if screens:
                s = screens[0]
                window.resize(s.width, s.height)
                window.move(s.x, s.y)
            is_max[0] = True

    def close():
        window.destroy()

    def is_maximized():
        return is_max[0]

    window.expose(minimize, toggle_maximize, close, is_maximized)

    webview.start()


if __name__ == "__main__":
    main()

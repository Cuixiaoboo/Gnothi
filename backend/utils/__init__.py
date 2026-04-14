import os
import sys
import logging
import traceback
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone, timedelta
from flask import request


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)


def format_datetime(dt):
    """将 datetime 对象格式化为 ISO 字符串"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt


def parse_date(date_str: str) -> datetime:
    """解析 YYYY-MM-DD 格式日期"""
    return datetime.strptime(date_str, "%Y-%m-%d")


def get_log_dir():
    """获取日志目录（支持打包后运行）"""
    if getattr(sys, "_MEIPASS", None):
        # 打包后：日志存放在 exe 同级目录
        exe_dir = os.path.dirname(sys.executable)
        log_dir = os.path.join(exe_dir, "log")
    else:
        # 开发模式：日志存放在 backend/log
        log_dir = os.path.join(os.path.dirname(__file__), "..", "log")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def setup_logging(app):
    """配置日志系统，输出到 log/gnothi.log"""

    # 日志目录（改动点）
    log_dir = get_log_dir()

    log_file = os.path.join(log_dir, "gnothi.log")

    # 日志格式
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)-7s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 文件处理器（最大 5MB，保留 5 个备份）
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)

    # 应用日志
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)

    # werkzeug 日志
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.handlers = []
    werkzeug_logger.addHandler(file_handler)
    werkzeug_logger.addHandler(console_handler)

    # ─── 请求日志中间件 ───
    @app.before_request
    def log_request_start():
        from flask import g

        g.request_start_time = utc_now()

    @app.after_request
    def log_request_end(response):
        from flask import g

        duration = (utc_now() - g.request_start_time).total_seconds() * 1000

        if response.status_code >= 400:
            app.logger.error(
                f"{request.method} {request.path} → {response.status_code} | "
                f"耗时 {duration:.0f}ms | "
                f"请求体: {request.get_data(as_text=True)[:500]}"
            )
        elif response.status_code >= 300:
            app.logger.warning(
                f"{request.method} {request.path} → {response.status_code} | "
                f"耗时 {duration:.0f}ms"
            )
        else:
            app.logger.debug(
                f"{request.method} {request.path} → {response.status_code} | "
                f"耗时 {duration:.0f}ms"
            )

        return response

    # ─── 全局异常捕获 ───
    @app.errorhandler(Exception)
    def handle_exception(e):
        # HTTP 异常（404、500 等）
        if hasattr(e, "code") and hasattr(e, "description"):
            code = e.code or 500
            desc = e.description
            app.logger.error(
                f"HTTP 异常 | {request.method} {request.path} → {code} | {desc}"
            )
            return {"error": desc, "code": code}, code

        # 未预期的异常
        tb = traceback.format_exc()
        app.logger.error(
            f"服务器异常 | {request.method} {request.path}\n"
            f"异常类型: {type(e).__name__}\n"
            f"异常信息: {str(e)}\n"
            f"请求体: {request.get_data(as_text=True)[:500]}\n"
            f"堆栈:\n{tb}"
        )
        return {"error": f"{type(e).__name__}: {str(e)}"}, 500

    # ─── 数据库异常 ───
    @app.errorhandler(404)
    def handle_404(e):
        app.logger.warning(f"404 | {request.method} {request.path}")
        return {"error": "资源不存在", "code": 404}, 404

    app.logger.info("=" * 50)
    app.logger.info("Gnothi 日志系统已初始化")
    app.logger.info(f"日志文件: {log_file}")
    app.logger.info("=" * 50)

    return app.logger

import os
import sys


def get_base_dir():
    """获取基础目录（支持打包后运行）"""
    if getattr(sys, '_MEIPASS', None):
        exe_dir = os.path.dirname(sys.executable)
        data_dir = os.path.join(exe_dir, 'gnothi_data')
        os.makedirs(data_dir, exist_ok=True)
        return data_dir
    return os.path.abspath(os.path.dirname(__file__))


BASE_DIR = get_base_dir()


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'gnothi.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

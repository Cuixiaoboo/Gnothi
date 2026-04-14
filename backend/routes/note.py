from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify
from models import db, Note

# 创建笔记相关的蓝图，用于模块化路由管理
note_bp = Blueprint("note", __name__)


def utc_now():
    """返回不带时区的 UTC 时间（SQLite 兼容）"""
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)


@note_bp.route("", methods=["GET"])
def get_notes():
    """
    获取所有笔记列表
    按更新时间降序排列
    """
    # 查询所有笔记，并按 updated_at 字段降序排序
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    # 将笔记对象转换为字典并返回 JSON 响应
    return jsonify([n.to_dict() for n in notes])


@note_bp.route("/<int:nid>", methods=["GET"])
def get_note(nid):
    """
    获取单个笔记详情
    :param nid: 笔记ID
    """
    # 根据 ID 查询笔记，若不存在则返回 404
    n = Note.query.get_or_404(nid)
    return jsonify(n.to_dict())


@note_bp.route("", methods=["POST"])
def create_note():
    """
    创建新笔记
    """
    # 强制解析请求体中的 JSON 数据
    data = request.get_json(force=True)
    # 创建 Note 实例，设置默认标题和内容
    n = Note(title=data.get("title", "新笔记"), content=data.get("content", ""))
    # 添加到会话并提交到数据库
    db.session.add(n)
    db.session.commit()
    # 返回创建的笔记信息及 201 状态码
    return jsonify(n.to_dict()), 201


@note_bp.route("/<int:nid>", methods=["PUT"])
def update_note(nid):
    """
    更新指定笔记
    :param nid: 笔记ID
    """
    # 查询需更新的笔记，若不存在则返回 404
    n = Note.query.get_or_404(nid)
    # 解析请求数据
    data = request.get_json(force=True)

    # 仅当字段存在于请求数据中时才进行更新
    if "title" in data:
        n.title = data["title"]
    if "content" in data:
        n.content = data["content"]

    # 手动更新最后修改时间
    n.updated_at = utc_now()
    # 提交更改
    db.session.commit()
    return jsonify(n.to_dict())


@note_bp.route("/<int:nid>", methods=["DELETE"])
def delete_note(nid):
    """
    删除指定笔记
    :param nid: 笔记ID
    """
    # 查询需删除的笔记，若不存在则返回 404
    n = Note.query.get_or_404(nid)
    # 从会话中删除并提交
    db.session.delete(n)
    db.session.commit()
    # 返回成功标识
    return jsonify({"ok": True})

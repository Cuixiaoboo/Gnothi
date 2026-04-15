from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify
from models import db, Note

note_bp = Blueprint("note", __name__)


def utc_now():
    """返回不带时区的 UTC 时间（SQLite 兼容）"""
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)


@note_bp.route("", methods=["GET"])
def get_notes():
    """
    获取所有笔记列表
    按 sort_order 升序排列（用户拖拽定义的顺序）
    """
    notes = Note.query.order_by(Note.sort_order.asc(), Note.updated_at.desc()).all()
    return jsonify([n.to_dict() for n in notes])


@note_bp.route("/<int:nid>", methods=["GET"])
def get_note(nid):
    n = Note.query.get_or_404(nid)
    return jsonify(n.to_dict())


@note_bp.route("", methods=["POST"])
def create_note():
    """
    创建新笔记
    新笔记排在最前面（sort_order = 当前最小值 - 1）
    """
    data = request.get_json(force=True)

    # 查找当前最小的 sort_order，新笔记排到最前
    min_order = db.session.query(db.func.min(Note.sort_order)).scalar()
    new_order = (min_order or 0) - 1

    n = Note(
        title=data.get("title", "新笔记"),
        content=data.get("content", ""),
        sort_order=new_order,
    )
    db.session.add(n)
    db.session.commit()
    return jsonify(n.to_dict()), 201


@note_bp.route("/<int:nid>", methods=["PUT"])
def update_note(nid):
    n = Note.query.get_or_404(nid)
    data = request.get_json(force=True)

    if "title" in data:
        n.title = data["title"]
    if "content" in data:
        n.content = data["content"]

    n.updated_at = utc_now()
    db.session.commit()
    return jsonify(n.to_dict())


@note_bp.route("/<int:nid>", methods=["DELETE"])
def delete_note(nid):
    n = Note.query.get_or_404(nid)
    db.session.delete(n)
    db.session.commit()
    return jsonify({"ok": True})


@note_bp.route("/reorder", methods=["PUT"])
def reorder_notes():
    """
    批量更新笔记排序
    请求体: { "ids": [3, 1, 5, 2, 4] }
    按 ids 数组的顺序依次赋值 sort_order（0, 1, 2, ...）
    """
    data = request.get_json(force=True)
    ids = data.get("ids", [])

    if not ids:
        return jsonify({"error": "ids 不能为空"}), 400

    # 按数组顺序给每个笔记赋值 sort_order
    for index, note_id in enumerate(ids):
        Note.query.filter_by(id=note_id).update({"sort_order": index})

    db.session.commit()
    return jsonify({"ok": True})

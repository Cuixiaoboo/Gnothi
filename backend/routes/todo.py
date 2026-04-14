from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify, current_app
from models import db, Todo

todo_bp = Blueprint("todo", __name__)


def utc_now():
    """返回不带时区的 UTC 时间（SQLite 兼容）"""
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)


@todo_bp.route("", methods=["GET"])
def get_todos():
    status = request.args.get("status")
    q = Todo.query
    if status and status != "all":
        q = q.filter_by(status=status)
    todos = q.order_by(Todo.created_at.desc()).all()
    return jsonify([t.to_dict() for t in todos])


@todo_bp.route("", methods=["POST"])
def create_todo():
    data = request.get_json(force=True)
    now = utc_now()
    t = Todo(
        title=data.get("title", ""),
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium"),
        due_date=data.get("due_date", ""),
        notes=data.get("notes", ""),
        completed_at="",
        created_at=now,
        updated_at=now,
    )
    db.session.add(t)
    db.session.commit()
    current_app.logger.info(f"创建待办: [{t.id}] {t.title}")
    return jsonify(t.to_dict()), 201


@todo_bp.route("/<int:tid>", methods=["PUT"])
def update_todo(tid):
    t = Todo.query.get_or_404(tid)
    data = request.get_json(force=True)
    changes = []
    for key in ["title", "status", "priority", "due_date", "notes"]:
        if key in data:
            old = getattr(t, key)
            new = data[key]
            if old != new:
                changes.append(f"{key}: '{old}' → '{new}'")
            setattr(t, key, data[key])
    if data.get("status") == "completed" and not t.completed_at:
        t.completed_at = utc_now().isoformat()
    if data.get("status") in ("hangup","pending", "in_progress"):
        t.completed_at = ""
    t.updated_at = utc_now()
    db.session.commit()

    if changes:
        current_app.logger.info(f"更新待办 [{tid}]: {', '.join(changes)}")
    return jsonify(t.to_dict())


@todo_bp.route("/<int:tid>", methods=["DELETE"])
def delete_todo(tid):
    t = Todo.query.get_or_404(tid)
    title = t.title
    db.session.delete(t)
    db.session.commit()
    current_app.logger.info(f"删除待办: [{tid}] {title}")
    return jsonify({"ok": True})

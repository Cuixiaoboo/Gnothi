from datetime import datetime
from . import db


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(20), default="pending")
    priority = db.Column(db.String(10), default="medium")
    due_date = db.Column(db.String(10), default="")
    notes = db.Column(db.Text, default="")
    completed_at = db.Column(db.String(30), default="")
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "notes": self.notes,
            "completed_at": self.completed_at,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

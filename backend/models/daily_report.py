from datetime import datetime
from . import db


class DailyReport(db.Model):
    __tablename__ = "daily_reports"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), unique=True, nullable=False, index=True)
    columns = db.Column(db.Text, default="[]")
    rows = db.Column(db.Text, default="[]")
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def to_dict(self):
        import json
        return {
            "date": self.date,
            "columns": json.loads(self.columns),
            "rows": json.loads(self.rows),
            "exists": True,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

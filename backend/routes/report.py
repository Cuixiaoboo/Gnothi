import json
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify
from models import db, DailyReport

report_bp = Blueprint("report", __name__)


def utc_now():
    """返回不带时区的 UTC 时间（SQLite 兼容）"""
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)


@report_bp.route("/dates", methods=["GET"])
def report_dates():
    """所有有日报的日期列表（日历标记用）"""
    rows = DailyReport.query.with_entities(DailyReport.date).all()
    return jsonify([r[0] for r in rows])


@report_bp.route("/<date>", methods=["GET"])
def get_report(date):
    r = DailyReport.query.filter_by(date=date).first()
    if not r:
        return jsonify({"date": date, "columns": [], "rows": [], "exists": False})
    return jsonify(r.to_dict())


@report_bp.route("/<date>", methods=["PUT"])
def save_report(date):
    data = request.get_json(force=True)
    r = DailyReport.query.filter_by(date=date).first()
    if not r:
        r = DailyReport(date=date)
        db.session.add(r)
    r.columns = json.dumps(data.get("columns", []), ensure_ascii=False)
    r.rows = json.dumps(data.get("rows", []), ensure_ascii=False)
    r.updated_at = utc_now()
    db.session.commit()
    return jsonify({"ok": True, "date": date})


@report_bp.route("/<date>", methods=["DELETE"])
def delete_report(date):
    r = DailyReport.query.filter_by(date=date).first()
    if r:
        db.session.delete(r)
        db.session.commit()
    return jsonify({"ok": True})

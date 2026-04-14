from .report import report_bp
from .todo import todo_bp
from .note import note_bp


def register_blueprints(app):
    app.register_blueprint(report_bp, url_prefix="/api/reports")
    app.register_blueprint(todo_bp, url_prefix="/api/todos")
    app.register_blueprint(note_bp, url_prefix="/api/notes")

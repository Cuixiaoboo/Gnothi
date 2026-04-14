from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .daily_report import DailyReport
from .todo import Todo
from .note import Note

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Хеш пароля
    salt = db.Column(db.String(16), nullable=False)  # Соль
    name = db.Column(db.String(100), nullable=False)


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    team_leader_id = db.Column(db.Integer, nullable=False)
    work_size = db.Column(db.Integer, nullable=False)
    collaborators = db.Column(db.String(500), nullable=False)
    is_job_finished = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

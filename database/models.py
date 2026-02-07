from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(300),
        nullable=False
    )


class LoginLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    ip_address = db.Column(db.String(100))

    user_agent = db.Column(db.String(300))

    status = db.Column(db.String(20))

    login_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
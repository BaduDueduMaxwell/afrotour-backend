from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from afrotour import db
from datetime import datetime


class User(db.Model):
    """
    Model for user in the Afrotour app.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, email, password, created_at=None, is_admin=False):
        """
        Initializes new user instance with username, email, password.
        """
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.created_at = created_at or datetime.utcnow()
        self.is_admin = is_admin

    def verify_password(self, password):
        """
        Verifies the user's password.
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Converts the User instance to a dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at,
        }

from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) 
    ideas = db.relationship('Idea', backref='author', lazy=True)  # Relationship with Idea

    def check_password(self, password):
        return check_password_hash(self.password, password) 

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    encrypted_content = db.Column(db.Text, nullable=False)  # For encrypted ideas
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for idea creation

from app import db
from werkzeug.security import generate_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def create_user(cls, username, email):
        user = cls(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def username_exists(cls, username):
        return cls.query.filter_by(username=username).first() is not None
    
    @classmethod
    def email_exists(cls, email):
        return cls.query.filter_by(email=email).first() is not None

from datetime import datetime, timedelta
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Password reset fields
    reset_token = db.Column(db.String(255), unique=True, nullable=True, index=True)
    reset_token_expires_at = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_token(self) -> str:
        """Generate a secure reset token and set expiration."""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires_at = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        return self.reset_token
    
    def validate_reset_token(self, token: str) -> bool:
        """Check if the reset token is valid and not expired."""
        if not self.reset_token or self.reset_token != token:
            return False
        
        if not self.reset_token_expires_at or self.reset_token_expires_at < datetime.utcnow():
            return False
        
        return True
    
    def clear_reset_token(self) -> None:
        """Clear the reset token after successful use."""
        self.reset_token = None
        self.reset_token_expires_at = None
        db.session.commit()
    
    def to_dict(self) -> dict:
        """Return user data as dictionary, excluding sensitive information."""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

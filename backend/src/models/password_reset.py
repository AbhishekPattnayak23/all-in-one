from datetime import datetime, timedelta
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

from ..database import Base

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="password_reset_tokens")
    
    @classmethod
    def create(cls, user_id: str, duration_hours: int = 24):
        return cls(
            user_id=user_id,
            token=str(uuid4()),
            expires_at=datetime.utcnow() + timedelta(hours=duration_hours)
        )
    
    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_used(self):
        return self.used is not None
    
    def mark_used(self):
        self.used = datetime.utcnow()

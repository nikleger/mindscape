from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, String, Integer, JSON
from sqlalchemy.orm import relationship

from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # MFA fields
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String, nullable=True)
    
    # Profile fields
    full_name = Column(String(255), nullable=True)
    preferences = Column(JSON, nullable=True, default=dict)
    
    # Relationships
    mind_maps = relationship("MindMap", back_populates="owner", cascade="all, delete-orphan")
    collaborations = relationship("Collaboration", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    @property
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return True
    
    @property
    def display_name(self) -> str:
        """Get user's display name."""
        return self.full_name or self.email.split('@')[0]
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        if self.is_superuser:
            return True
        # TODO: Implement role-based permissions
        return False 
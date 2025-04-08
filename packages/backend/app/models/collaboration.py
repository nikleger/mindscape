from sqlalchemy import Column, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum
from app.models.base import Base

class CollaborationRole(PyEnum):
    """Collaboration role enum."""
    VIEWER = "viewer"
    EDITOR = "editor"
    ADMIN = "admin"

class Collaboration(Base):
    """Collaboration model for managing mind map sharing."""
    
    # Core fields
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    mind_map_id = Column(UUID, ForeignKey("mind_map.id"), nullable=False)
    role = Column(Enum(CollaborationRole), default=CollaborationRole.VIEWER, nullable=False)
    
    # Additional permissions
    can_edit = Column(Boolean, default=False, nullable=False)
    can_share = Column(Boolean, default=False, nullable=False)
    can_delete = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="collaborations")
    mind_map = relationship("MindMap", back_populates="collaborations")
    
    def __repr__(self) -> str:
        return f"<Collaboration {self.user_id} on {self.mind_map_id}>"
    
    @property
    def is_admin(self) -> bool:
        """Check if collaboration has admin role."""
        return self.role == CollaborationRole.ADMIN
    
    def update_role(self, new_role: CollaborationRole) -> None:
        """Update collaboration role and associated permissions."""
        self.role = new_role
        if new_role == CollaborationRole.ADMIN:
            self.can_edit = True
            self.can_share = True
            self.can_delete = True
        elif new_role == CollaborationRole.EDITOR:
            self.can_edit = True
            self.can_share = False
            self.can_delete = False
        else:  # VIEWER
            self.can_edit = False
            self.can_share = False
            self.can_delete = False 
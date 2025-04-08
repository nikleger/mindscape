from sqlalchemy import Column, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Template(Base):
    """Template model for reusable mind map structures."""
    
    # Core fields
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(String(100), nullable=True)
    
    # Template content
    structure = Column(JSON, nullable=False, default=dict)
    default_styles = Column(JSON, nullable=True, default=dict)
    
    # Metadata
    is_public = Column(Boolean, default=False, nullable=False)
    creator_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    metadata = Column(JSON, nullable=True, default=dict)
    
    # Relationships
    creator = relationship("User", back_populates="templates")
    mind_maps = relationship("MindMap", back_populates="template")
    
    def __repr__(self) -> str:
        return f"<Template {self.title}>"
    
    @property
    def usage_count(self) -> int:
        """Get number of mind maps using this template."""
        return len(self.mind_maps)
    
    def can_user_access(self, user_id: UUID) -> bool:
        """Check if user can access this template."""
        return self.is_public or str(self.creator_id) == str(user_id)
    
    def can_user_edit(self, user_id: UUID) -> bool:
        """Check if user can edit this template."""
        return str(self.creator_id) == str(user_id)
    
    def get_initial_structure(self) -> dict:
        """Get the initial structure for a new mind map."""
        return {
            "nodes": self.structure.get("nodes", []),
            "styles": self.default_styles or {},
            "metadata": {
                "template_id": str(self.id),
                "template_version": self.metadata.get("version", "1.0")
            }
        } 
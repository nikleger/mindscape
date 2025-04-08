from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, ForeignKey, String, Table, JSON, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from .base import Base, TimestampedBase

# Association table for mind map collaborators
mind_map_collaborators = Table(
    'mind_map_collaborators',
    Base.metadata,
    Column('mind_map_id', PGUUID(as_uuid=True), ForeignKey('mind_maps.id'), primary_key=True),
    Column('user_id', PGUUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
)

class MindMapStatus(PyEnum):
    """Mind map status enum."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class MindMapBase(BaseModel):
    """Base Pydantic model for mind maps."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class MindMapCreate(MindMapBase):
    """Pydantic model for mind map creation."""
    template_id: Optional[UUID] = None

class MindMapUpdate(MindMapBase):
    """Pydantic model for mind map updates."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None

class MindMap(Base):
    """Mind map model."""
    
    # Core fields
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(MindMapStatus), default=MindMapStatus.DRAFT, nullable=False)
    
    # Ownership and template
    owner_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    template_id = Column(PGUUID(as_uuid=True), ForeignKey("templates.id"), nullable=True)
    
    # Content and metadata
    content = Column(JSON, nullable=False, default=dict)
    metadata = Column(JSON, nullable=True, default=dict)
    
    # Relationships
    owner = relationship("UserModel", back_populates="mind_maps")
    template = relationship("TemplateModel", back_populates="mind_maps")
    nodes = relationship("NodeModel", back_populates="mind_map", cascade="all, delete-orphan")
    collaborations = relationship("CollaborationModel", back_populates="mind_map", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<MindMap {self.title}>"
    
    @property
    def is_published(self) -> bool:
        """Check if mind map is published."""
        return self.status == MindMapStatus.PUBLISHED
    
    @property
    def collaborator_count(self) -> int:
        """Get number of collaborators."""
        return len(self.collaborations)
    
    def can_user_access(self, user_id: UUID) -> bool:
        """Check if user can access this mind map."""
        if str(self.owner_id) == str(user_id):
            return True
        return any(c.user_id == user_id for c in self.collaborations)
    
    def can_user_edit(self, user_id: UUID) -> bool:
        """Check if user can edit this mind map."""
        if str(self.owner_id) == str(user_id):
            return True
        return any(
            c.user_id == user_id and c.can_edit 
            for c in self.collaborations
        )

class MindMapModel(Base, TimestampedBase):
    """SQLAlchemy model for mind maps."""
    __tablename__ = 'mind_maps'

    id = Column(PGUUID(as_uuid=True), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(PGUUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    template_id = Column(PGUUID(as_uuid=True), ForeignKey('templates.id'), nullable=True)

    # Relationships
    owner = relationship("UserModel", back_populates="mind_maps")
    template = relationship("TemplateModel", back_populates="mind_maps")
    nodes = relationship("NodeModel", back_populates="mind_map", cascade="all, delete-orphan")
    collaborators = relationship(
        "UserModel",
        secondary=mind_map_collaborators,
        back_populates="collaborated_mind_maps"
    )

class NodeBase(BaseModel):
    """Base Pydantic model for nodes."""
    content: str = Field(..., min_length=1)
    position: Dict[str, float] = Field(..., description="Node position {x: float, y: float}")
    style: Optional[Dict[str, Any]] = None

class NodeCreate(NodeBase):
    """Pydantic model for node creation."""
    parent_id: Optional[UUID] = None

class NodeUpdate(NodeBase):
    """Pydantic model for node updates."""
    content: Optional[str] = Field(None, min_length=1)
    position: Optional[Dict[str, float]] = None
    style: Optional[Dict[str, Any]] = None
    parent_id: Optional[UUID] = None

class Node(NodeBase):
    """Pydantic model for node responses."""
    id: UUID
    mind_map_id: UUID
    parent_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NodeModel(Base, TimestampedBase):
    """SQLAlchemy model for mind map nodes."""
    __tablename__ = 'nodes'

    id = Column(PGUUID(as_uuid=True), primary_key=True)
    content = Column(String, nullable=False)
    position = Column(JSON, nullable=False)
    style = Column(JSON)
    parent_id = Column(PGUUID(as_uuid=True), ForeignKey('nodes.id'), nullable=True)
    mind_map_id = Column(PGUUID(as_uuid=True), ForeignKey('mind_maps.id'), nullable=False)
    
    # Relationships
    mind_map = relationship("MindMapModel", back_populates="nodes")
    parent = relationship("NodeModel", remote_side=[id], backref="children")
    
    def __repr__(self) -> str:
        return f"<Node {self.content[:20]}...>" 
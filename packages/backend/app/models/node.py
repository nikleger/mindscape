from sqlalchemy import Column, String, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Node(Base):
    """Node model for representing elements in a mind map."""
    
    # Core fields
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=True)
    node_type = Column(String(50), nullable=False, default="text")
    
    # Position and hierarchy
    x_position = Column(Integer, nullable=False, default=0)
    y_position = Column(Integer, nullable=False, default=0)
    parent_id = Column(UUID, ForeignKey("node.id"), nullable=True)
    mind_map_id = Column(UUID, ForeignKey("mind_map.id"), nullable=False)
    
    # Styling and metadata
    style = Column(JSON, nullable=True, default=dict)
    metadata = Column(JSON, nullable=True, default=dict)
    
    # Relationships
    mind_map = relationship("MindMap", back_populates="nodes")
    parent = relationship("Node", remote_side="Node.id", backref="children")
    
    def __repr__(self) -> str:
        return f"<Node {self.title}>"
    
    @property
    def depth(self) -> int:
        """Calculate the depth of this node in the tree."""
        depth = 0
        current = self
        while current.parent_id is not None:
            depth += 1
            current = current.parent
        return depth
    
    def get_subtree(self) -> list["Node"]:
        """Get all nodes in the subtree (including this node)."""
        nodes = [self]
        for child in self.children:
            nodes.extend(child.get_subtree())
        return nodes
    
    def move(self, x: int, y: int) -> None:
        """Move node to new position."""
        self.x_position = x
        self.y_position = y
    
    def update_style(self, new_style: dict) -> None:
        """Update node style."""
        if self.style is None:
            self.style = {}
        self.style.update(new_style) 
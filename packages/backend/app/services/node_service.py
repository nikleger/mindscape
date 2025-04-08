from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import get_db
from ..models.mind_map import NodeModel, Node, NodeCreate, NodeUpdate, MindMapModel
from ..models.user import User

class NodeService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create_node(
        self,
        mind_map_id: UUID,
        data: NodeCreate,
        current_user: User
    ) -> Node:
        """Create a new node in a mind map."""
        # Verify mind map access
        query = select(MindMapModel).where(MindMapModel.id == mind_map_id)
        result = await self.db.execute(query)
        mind_map = result.scalar_one_or_none()

        if not mind_map:
            raise HTTPException(status_code=404, detail="Mind map not found")

        if mind_map.owner_id != current_user.id and current_user.id not in [c.id for c in mind_map.collaborators]:
            raise HTTPException(status_code=403, detail="Access denied")

        # If parent_id is provided, verify it exists in the same mind map
        if data.parent_id:
            parent_query = select(NodeModel).where(
                (NodeModel.id == data.parent_id) & 
                (NodeModel.mind_map_id == mind_map_id)
            )
            parent_result = await self.db.execute(parent_query)
            if not parent_result.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Parent node not found")

        # Create the node
        node = NodeModel(
            id=uuid4(),
            content=data.content,
            position=data.position,
            style=data.style,
            parent_id=data.parent_id,
            mind_map_id=mind_map_id
        )

        self.db.add(node)
        await self.db.commit()
        await self.db.refresh(node)

        return Node.from_orm(node)

    async def get_nodes(
        self,
        mind_map_id: UUID,
        current_user: User
    ) -> List[Node]:
        """Get all nodes in a mind map."""
        # Verify mind map access
        query = select(MindMapModel).where(MindMapModel.id == mind_map_id)
        result = await self.db.execute(query)
        mind_map = result.scalar_one_or_none()

        if not mind_map:
            raise HTTPException(status_code=404, detail="Mind map not found")

        if mind_map.owner_id != current_user.id and current_user.id not in [c.id for c in mind_map.collaborators]:
            raise HTTPException(status_code=403, detail="Access denied")

        # Get all nodes
        nodes_query = select(NodeModel).where(NodeModel.mind_map_id == mind_map_id)
        nodes_result = await self.db.execute(nodes_query)
        nodes = nodes_result.scalars().all()

        return [Node.from_orm(node) for node in nodes]

    async def update_node(
        self,
        node_id: UUID,
        data: NodeUpdate,
        current_user: User
    ) -> Optional[Node]:
        """Update a node if the user has access to its mind map."""
        # Get the node and its mind map
        query = (
            select(NodeModel)
            .join(MindMapModel)
            .where(NodeModel.id == node_id)
        )
        result = await self.db.execute(query)
        node = result.scalar_one_or_none()

        if not node:
            return None

        # Verify access
        mind_map = node.mind_map
        if mind_map.owner_id != current_user.id and current_user.id not in [c.id for c in mind_map.collaborators]:
            raise HTTPException(status_code=403, detail="Access denied")

        # If changing parent, verify new parent exists in same mind map
        if data.parent_id and data.parent_id != node.parent_id:
            parent_query = select(NodeModel).where(
                (NodeModel.id == data.parent_id) & 
                (NodeModel.mind_map_id == mind_map.id)
            )
            parent_result = await self.db.execute(parent_query)
            if not parent_result.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Parent node not found")

        # Update fields
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(node, key, value)

        await self.db.commit()
        await self.db.refresh(node)

        return Node.from_orm(node)

    async def delete_node(
        self,
        node_id: UUID,
        current_user: User
    ) -> bool:
        """Delete a node if the user has access to its mind map."""
        # Get the node and its mind map
        query = (
            select(NodeModel)
            .join(MindMapModel)
            .where(NodeModel.id == node_id)
        )
        result = await self.db.execute(query)
        node = result.scalar_one_or_none()

        if not node:
            return False

        # Verify access
        mind_map = node.mind_map
        if mind_map.owner_id != current_user.id and current_user.id not in [c.id for c in mind_map.collaborators]:
            raise HTTPException(status_code=403, detail="Access denied")

        # Delete the node (cascade will handle children)
        await self.db.delete(node)
        await self.db.commit()

        return True 
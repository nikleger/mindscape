from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.database import get_db
from ..models.mind_map import MindMap, MindMapCreate, MindMapUpdate, MindMapModel
from ..models.user import User, UserModel

class MindMapService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create_mind_map(self, data: MindMapCreate, current_user: User) -> MindMap:
        """Create a new mind map."""
        mind_map = MindMapModel(
            id=uuid4(),
            title=data.title,
            description=data.description,
            owner_id=current_user.id,
            template_id=data.template_id
        )
        
        self.db.add(mind_map)
        await self.db.commit()
        await self.db.refresh(mind_map)
        
        return MindMap.from_orm(mind_map)

    async def list_mind_maps(self, current_user: User) -> List[MindMap]:
        """List all mind maps accessible to the user."""
        query = (
            select(MindMapModel)
            .where(
                (MindMapModel.owner_id == current_user.id) |
                (MindMapModel.id.in_(
                    select(mind_map_collaborators.c.mind_map_id)
                    .where(mind_map_collaborators.c.user_id == current_user.id)
                ))
            )
        )
        
        result = await self.db.execute(query)
        mind_maps = result.scalars().all()
        
        return [MindMap.from_orm(mm) for mm in mind_maps]

    async def get_mind_map(self, mind_map_id: UUID, current_user: User) -> Optional[MindMap]:
        """Get a specific mind map if the user has access."""
        query = (
            select(MindMapModel)
            .where(
                (MindMapModel.id == mind_map_id) &
                (
                    (MindMapModel.owner_id == current_user.id) |
                    (MindMapModel.id.in_(
                        select(mind_map_collaborators.c.mind_map_id)
                        .where(mind_map_collaborators.c.user_id == current_user.id)
                    ))
                )
            )
        )
        
        result = await self.db.execute(query)
        mind_map = result.scalar_one_or_none()
        
        if mind_map:
            return MindMap.from_orm(mind_map)
        return None

    async def update_mind_map(
        self,
        mind_map_id: UUID,
        data: MindMapUpdate,
        current_user: User
    ) -> Optional[MindMap]:
        """Update a mind map if the user has permission."""
        mind_map = await self.get_mind_map(mind_map_id, current_user)
        if not mind_map:
            return None
            
        # Only owner can update title and description
        if mind_map.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Only the owner can update mind map details"
            )
        
        update_data = data.dict(exclude_unset=True)
        if not update_data:
            return mind_map
            
        query = (
            select(MindMapModel)
            .where(MindMapModel.id == mind_map_id)
        )
        
        result = await self.db.execute(query)
        db_mind_map = result.scalar_one_or_none()
        
        for key, value in update_data.items():
            setattr(db_mind_map, key, value)
            
        await self.db.commit()
        await self.db.refresh(db_mind_map)
        
        return MindMap.from_orm(db_mind_map)

    async def delete_mind_map(self, mind_map_id: UUID, current_user: User) -> bool:
        """Delete a mind map if the user is the owner."""
        mind_map = await self.get_mind_map(mind_map_id, current_user)
        if not mind_map:
            return False
            
        if mind_map.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Only the owner can delete the mind map"
            )
            
        query = (
            select(MindMapModel)
            .where(MindMapModel.id == mind_map_id)
        )
        
        result = await self.db.execute(query)
        db_mind_map = result.scalar_one_or_none()
        
        await self.db.delete(db_mind_map)
        await self.db.commit()
        
        return True 
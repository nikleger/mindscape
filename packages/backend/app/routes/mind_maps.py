from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID

from ..models.mind_map import MindMap, MindMapCreate, MindMapUpdate
from ..services.mind_map_service import MindMapService
from ..core.auth import get_current_user
from ..models.user import User

router = APIRouter(
    prefix="/api/v1/mind-maps",
    tags=["mind-maps"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=MindMap)
async def create_mind_map(
    data: MindMapCreate,
    current_user: User = Depends(get_current_user),
    service: MindMapService = Depends()
) -> MindMap:
    """
    Create a new mind map.
    
    This endpoint allows users to create a new mind map with optional template.
    The mind map will be owned by the authenticated user.
    """
    return await service.create_mind_map(data, current_user)

@router.get("/", response_model=List[MindMap])
async def list_mind_maps(
    current_user: User = Depends(get_current_user),
    service: MindMapService = Depends()
) -> List[MindMap]:
    """
    List all mind maps accessible to the current user.
    
    This includes mind maps owned by the user and those shared with them.
    """
    return await service.list_mind_maps(current_user)

@router.get("/{mind_map_id}", response_model=MindMap)
async def get_mind_map(
    mind_map_id: UUID,
    current_user: User = Depends(get_current_user),
    service: MindMapService = Depends()
) -> MindMap:
    """
    Get a specific mind map by ID.
    
    The user must have access to the requested mind map.
    """
    mind_map = await service.get_mind_map(mind_map_id, current_user)
    if not mind_map:
        raise HTTPException(status_code=404, detail="Mind map not found")
    return mind_map

@router.put("/{mind_map_id}", response_model=MindMap)
async def update_mind_map(
    mind_map_id: UUID,
    data: MindMapUpdate,
    current_user: User = Depends(get_current_user),
    service: MindMapService = Depends()
) -> MindMap:
    """
    Update a specific mind map.
    
    The user must be the owner of the mind map or have edit permissions.
    """
    mind_map = await service.update_mind_map(mind_map_id, data, current_user)
    if not mind_map:
        raise HTTPException(status_code=404, detail="Mind map not found")
    return mind_map

@router.delete("/{mind_map_id}")
async def delete_mind_map(
    mind_map_id: UUID,
    current_user: User = Depends(get_current_user),
    service: MindMapService = Depends()
) -> None:
    """
    Delete a specific mind map.
    
    The user must be the owner of the mind map.
    """
    success = await service.delete_mind_map(mind_map_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Mind map not found") 
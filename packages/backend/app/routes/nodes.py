from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID

from ..models.mind_map import Node, NodeCreate, NodeUpdate
from ..services.node_service import NodeService
from ..core.auth import get_current_user
from ..models.user import User

router = APIRouter(
    prefix="/api/v1/mind-maps/{mind_map_id}/nodes",
    tags=["nodes"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Node)
async def create_node(
    mind_map_id: UUID,
    data: NodeCreate,
    current_user: User = Depends(get_current_user),
    service: NodeService = Depends()
) -> Node:
    """
    Create a new node in a mind map.
    
    The user must have access to the mind map.
    """
    return await service.create_node(mind_map_id, data, current_user)

@router.get("/", response_model=List[Node])
async def list_nodes(
    mind_map_id: UUID,
    current_user: User = Depends(get_current_user),
    service: NodeService = Depends()
) -> List[Node]:
    """
    List all nodes in a mind map.
    
    The user must have access to the mind map.
    """
    return await service.get_nodes(mind_map_id, current_user)

@router.put("/{node_id}", response_model=Node)
async def update_node(
    mind_map_id: UUID,  # Used for route organization
    node_id: UUID,
    data: NodeUpdate,
    current_user: User = Depends(get_current_user),
    service: NodeService = Depends()
) -> Node:
    """
    Update a specific node.
    
    The user must have access to the mind map containing the node.
    """
    node = await service.update_node(node_id, data, current_user)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@router.delete("/{node_id}")
async def delete_node(
    mind_map_id: UUID,  # Used for route organization
    node_id: UUID,
    current_user: User = Depends(get_current_user),
    service: NodeService = Depends()
) -> None:
    """
    Delete a specific node.
    
    The user must have access to the mind map containing the node.
    All child nodes will also be deleted.
    """
    success = await service.delete_node(node_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Node not found") 
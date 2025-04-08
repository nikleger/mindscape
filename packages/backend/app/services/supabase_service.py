from typing import List, Optional, Dict, Any
from uuid import UUID
from app.core.supabase_config import SupabaseClient

class SupabaseService:
    """Service for handling Supabase operations."""
    
    def __init__(self):
        self.client = SupabaseClient.get_client()
    
    async def create_mind_map(self, title: str, owner_id: UUID, template_id: Optional[UUID] = None) -> Dict[str, Any]:
        """Create a new mind map."""
        data = {
            'title': title,
            'owner_id': str(owner_id),
            'template_id': str(template_id) if template_id else None
        }
        
        result = self.client.table('mind_maps').insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_mind_map(self, mind_map_id: UUID) -> Optional[Dict[str, Any]]:
        """Get mind map by ID."""
        result = self.client.table('mind_maps').select('*').eq('id', str(mind_map_id)).execute()
        return result.data[0] if result.data else None
    
    async def update_mind_map(self, mind_map_id: UUID, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update mind map."""
        result = self.client.table('mind_maps').update(data).eq('id', str(mind_map_id)).execute()
        return result.data[0] if result.data else None
    
    async def delete_mind_map(self, mind_map_id: UUID) -> bool:
        """Delete mind map."""
        result = self.client.table('mind_maps').delete().eq('id', str(mind_map_id)).execute()
        return bool(result.data)
    
    async def create_node(self, mind_map_id: UUID, content: str, position: Dict[str, float], style: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a new node."""
        data = {
            'mind_map_id': str(mind_map_id),
            'content': content,
            'position': position,
            'style': style
        }
        
        result = self.client.table('nodes').insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_nodes(self, mind_map_id: UUID) -> List[Dict[str, Any]]:
        """Get all nodes for a mind map."""
        result = self.client.table('nodes').select('*').eq('mind_map_id', str(mind_map_id)).execute()
        return result.data if result.data else []
    
    async def update_node(self, node_id: UUID, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update node."""
        result = self.client.table('nodes').update(data).eq('id', str(node_id)).execute()
        return result.data[0] if result.data else None
    
    async def delete_node(self, node_id: UUID) -> bool:
        """Delete node."""
        result = self.client.table('nodes').delete().eq('id', str(node_id)).execute()
        return bool(result.data)
    
    async def add_collaboration(self, mind_map_id: UUID, user_id: UUID, permission: str) -> Dict[str, Any]:
        """Add a collaboration."""
        data = {
            'mind_map_id': str(mind_map_id),
            'user_id': str(user_id),
            'permission': permission
        }
        
        result = self.client.table('collaborations').insert(data).execute()
        return result.data[0] if result.data else None
    
    async def get_collaborators(self, mind_map_id: UUID) -> List[Dict[str, Any]]:
        """Get all collaborators for a mind map."""
        result = self.client.table('collaborations').select(
            'collaborations.permission',
            'users.id',
            'users.email',
            'users.name'
        ).eq('mind_map_id', str(mind_map_id)).join(
            'users',
            'collaborations.user_id',
            'users.id'
        ).execute()
        return result.data if result.data else []
    
    async def setup_realtime_subscription(self, mind_map_id: UUID, callback: callable):
        """Set up real-time subscription for mind map changes."""
        return self.client.table('nodes').on(
            'postgres_changes',
            event='*',
            schema='public',
            filter=f"mind_map_id=eq.{str(mind_map_id)}"
        ).subscribe(callback)
    
    async def remove_realtime_subscription(self, subscription):
        """Remove real-time subscription."""
        await self.client.remove_subscription(subscription) 
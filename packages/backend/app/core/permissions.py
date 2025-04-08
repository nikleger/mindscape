from enum import Enum
from typing import List, Optional

from fastapi import Depends, HTTPException, Request, status
from pydantic import BaseModel

from app.core.security import get_current_user
from app.core.audit import AuditAction, AuditEvent, log_audit_event

class Permission(str, Enum):
    READ_MIND_MAPS = "read:mind_maps"
    WRITE_MIND_MAPS = "write:mind_maps"
    DELETE_MIND_MAPS = "delete:mind_maps"
    MANAGE_TEAMS = "manage:teams"
    ADMIN = "*"

class Role(BaseModel):
    name: str
    permissions: List[Permission]
    inherits: Optional[List[str]] = None

# Role definitions as per Security Strategy
ROLES = {
    "admin": Role(
        name="admin",
        permissions=[Permission.ADMIN],
    ),
    "manager": Role(
        name="manager",
        permissions=[
            Permission.READ_MIND_MAPS,
            Permission.WRITE_MIND_MAPS,
            Permission.MANAGE_TEAMS,
        ],
        inherits=["user"],
    ),
    "user": Role(
        name="user",
        permissions=[
            Permission.READ_MIND_MAPS,
            Permission.WRITE_MIND_MAPS,
        ],
    ),
}

def get_role_permissions(role_name: str) -> List[Permission]:
    """Get all permissions for a role, including inherited ones."""
    if role_name not in ROLES:
        return []
    
    role = ROLES[role_name]
    permissions = set(role.permissions)
    
    if role.inherits:
        for inherited_role in role.inherits:
            permissions.update(get_role_permissions(inherited_role))
    
    return list(permissions)

def requires_permission(required_permission: Permission):
    """Decorator to check if user has required permission."""
    async def permission_dependency(
        request: Request,
        token_data = Depends(get_current_user)
    ):
        if not token_data.scopes:
            await log_audit_event(
                request,
                AuditEvent(
                    action=AuditAction.PERMISSION_CHECK,
                    user_id=token_data.sub,
                    status="failed",
                    details={
                        "required_permission": required_permission,
                        "reason": "No scopes found"
                    }
                )
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
            
        # Admin has all permissions
        if Permission.ADMIN in token_data.scopes:
            await log_audit_event(
                request,
                AuditEvent(
                    action=AuditAction.PERMISSION_CHECK,
                    user_id=token_data.sub,
                    status="success",
                    details={
                        "required_permission": required_permission,
                        "reason": "Admin access"
                    }
                )
            )
            return token_data
            
        if required_permission not in token_data.scopes:
            await log_audit_event(
                request,
                AuditEvent(
                    action=AuditAction.PERMISSION_CHECK,
                    user_id=token_data.sub,
                    status="failed",
                    details={
                        "required_permission": required_permission,
                        "available_permissions": token_data.scopes
                    }
                )
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission {required_permission} required"
            )
        
        await log_audit_event(
            request,
            AuditEvent(
                action=AuditAction.PERMISSION_CHECK,
                user_id=token_data.sub,
                status="success",
                details={
                    "required_permission": required_permission
                }
            )
        )
        return token_data
    
    return permission_dependency

def requires_role(required_role: str):
    """Decorator to check if user has required role."""
    required_permissions = get_role_permissions(required_role)
    
    async def role_dependency(
        request: Request,
        token_data = Depends(get_current_user)
    ):
        if not token_data.scopes:
            await log_audit_event(
                request,
                AuditEvent(
                    action=AuditAction.PERMISSION_CHECK,
                    user_id=token_data.sub,
                    status="failed",
                    details={
                        "required_role": required_role,
                        "reason": "No scopes found"
                    }
                )
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
            
        # Admin role has all permissions
        if Permission.ADMIN in token_data.scopes:
            await log_audit_event(
                request,
                AuditEvent(
                    action=AuditAction.PERMISSION_CHECK,
                    user_id=token_data.sub,
                    status="success",
                    details={
                        "required_role": required_role,
                        "reason": "Admin access"
                    }
                )
            )
            return token_data
            
        # Check if user has all required permissions
        missing_permissions = [
            perm for perm in required_permissions
            if perm not in token_data.scopes
        ]
        
        if missing_permissions:
            await log_audit_event(
                request,
                AuditEvent(
                    action=AuditAction.PERMISSION_CHECK,
                    user_id=token_data.sub,
                    status="failed",
                    details={
                        "required_role": required_role,
                        "missing_permissions": missing_permissions,
                        "available_permissions": token_data.scopes
                    }
                )
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role} required"
            )
        
        await log_audit_event(
            request,
            AuditEvent(
                action=AuditAction.PERMISSION_CHECK,
                user_id=token_data.sub,
                status="success",
                details={
                    "required_role": required_role
                }
            )
        )
        return token_data
    
    return role_dependency 
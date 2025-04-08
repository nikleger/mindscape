from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import Request
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum as SQLAEnum, ForeignKey, String, JSON
from sqlalchemy.dialects.postgresql import INET, UUID as PGUUID

from app.db.base_class import Base
from app.core.config import settings

class AuditAction(str, Enum):
    # Authentication events
    LOGIN_ATTEMPT = "login_attempt"
    PASSWORD_CHANGE = "password_change"
    MFA_EVENT = "mfa_event"
    
    # Authorization events
    PERMISSION_CHECK = "permission_check"
    ROLE_CHANGE = "role_change"
    
    # Data access events
    READ_SENSITIVE_DATA = "read_sensitive_data"
    MODIFY_SENSITIVE_DATA = "modify_sensitive_data"
    
    # Admin actions
    ADMIN_ACTION = "admin_action"
    API_KEY_USAGE = "api_key_usage"
    SYSTEM_CONFIG_CHANGE = "system_config_change"

class AuditLog(Base):
    """Audit log model for security events."""
    __tablename__ = "audit_logs"
    __table_args__ = {"schema": "security"}
    
    id = Column(PGUUID, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(PGUUID, ForeignKey("users.id"), nullable=True)
    action = Column(SQLAEnum(AuditAction), nullable=False)
    resource_type = Column(String, nullable=True)
    resource_id = Column(PGUUID, nullable=True)
    changes = Column(JSON, nullable=True)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(String, nullable=True)
    status = Column(String, nullable=True)
    details = Column(JSON, nullable=True)

class AuditEvent(BaseModel):
    """Audit event data model."""
    action: AuditAction
    user_id: Optional[UUID]
    resource_type: Optional[str]
    resource_id: Optional[UUID]
    changes: Optional[Dict[str, Any]]
    status: Optional[str]
    details: Optional[Dict[str, Any]]

async def log_audit_event(
    request: Request,
    event: AuditEvent,
) -> None:
    """
    Log an audit event to the database.
    
    Args:
        request: The FastAPI request object
        event: The audit event to log
    """
    audit_log = AuditLog(
        user_id=event.user_id,
        action=event.action,
        resource_type=event.resource_type,
        resource_id=event.resource_id,
        changes=event.changes,
        status=event.status,
        details=event.details,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    # TODO: Add to database session and commit
    # This will be implemented when we set up the database session management

async def audit_log_middleware(request: Request, call_next):
    """Middleware to automatically log certain HTTP requests."""
    response = await call_next(request)
    
    # Only log requests to API endpoints
    if not request.url.path.startswith("/api/"):
        return response
    
    # Create audit event for sensitive operations
    if request.method in ["POST", "PUT", "DELETE"]:
        event = AuditEvent(
            action=AuditAction.MODIFY_SENSITIVE_DATA,
            resource_type=request.url.path.split("/")[-2],  # Get resource type from URL
            status=str(response.status_code),
            details={
                "method": request.method,
                "path": request.url.path,
            }
        )
        await log_audit_event(request, event)
    
    return response 
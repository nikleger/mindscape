from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

# API Models
class User(BaseModel):
    id: UUID
    email: str
    name: str
    created_at: datetime
    updated_at: datetime

class MindMap(BaseModel):
    id: UUID
    title: str
    owner_id: UUID
    template_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

class Node(BaseModel):
    id: UUID
    mind_map_id: UUID
    content: str
    position: dict
    style: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

class Edge(BaseModel):
    id: UUID
    source_id: UUID
    target_id: UUID
    style: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

class Template(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    nodes: List[dict]
    edges: List[dict]
    created_at: datetime
    updated_at: datetime

# API Documentation
def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Mindscape API",
        version="1.0.0",
        description="""
        Enterprise Mind Mapping Platform API
        
        ## Authentication
        - JWT Bearer token required for all endpoints
        - Token format: `Authorization: Bearer <token>`
        
        ## Rate Limiting
        - 100 requests per minute per IP
        - 5 requests per minute for login endpoints
        
        ## Error Codes
        - 400: Bad Request
        - 401: Unauthorized
        - 403: Forbidden
        - 404: Not Found
        - 429: Too Many Requests
        - 500: Internal Server Error
        """,
        routes=app.routes,
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Add global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]

    # Add tags
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "User authentication and authorization endpoints",
        },
        {
            "name": "Mind Maps",
            "description": "Mind map management endpoints",
        },
        {
            "name": "Nodes",
            "description": "Mind map node management endpoints",
        },
        {
            "name": "Edges",
            "description": "Mind map edge management endpoints",
        },
        {
            "name": "Templates",
            "description": "Mind map template management endpoints",
        },
        {
            "name": "Users",
            "description": "User management endpoints",
        },
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema 
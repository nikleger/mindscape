from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """Response schema for access token."""
    access_token: str
    token_type: str
    refresh_token: str

class TokenPayload(BaseModel):
    """Schema for token data."""
    sub: str
    exp: datetime
    iat: datetime
    type: str = "access"

class RefreshTokenPayload(BaseModel):
    """Schema for refresh token data."""
    sub: str
    exp: datetime
    iat: datetime
    type: str = "refresh"

class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int 
from pydantic import BaseModel, Field

class MFAVerifyRequest(BaseModel):
    """Request schema for MFA token verification."""
    token: str = Field(..., min_length=6, max_length=6, description="6-digit MFA token")

class MFASetupResponse(BaseModel):
    """Response schema for MFA setup."""
    qr_code: str = Field(..., description="Base64 encoded QR code for MFA setup")
    backup_codes: list[str] = Field(..., description="List of one-time backup codes") 
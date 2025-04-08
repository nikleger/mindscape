from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.mfa import MFAManager, MFARequired, InvalidMFAToken
from app.core.security import get_current_user
from app.core.audit import AuditAction, log_audit_event
from app.db.session import get_db
from app.models.user import User
from app.schemas.mfa import MFASetupResponse, MFAVerifyRequest

router = APIRouter()
mfa_manager = MFAManager()

@router.post("/setup", response_model=MFASetupResponse)
async def setup_mfa(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> MFASetupResponse:
    """
    Set up MFA for the current user.
    Returns a QR code and backup codes.
    """
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled"
        )
    
    # Generate new TOTP secret
    secret = mfa_manager.generate_secret()
    qr_code = mfa_manager.generate_qr_code(current_user.email, secret)
    
    # Generate backup codes
    backup_codes = [secrets.token_urlsafe(16)[:10] for _ in range(10)]
    
    # Update user
    current_user.mfa_secret = secret
    current_user.mfa_backup_codes = backup_codes
    db.commit()
    
    # Log MFA setup
    await log_audit_event(
        action=AuditAction.MFA_EVENT,
        user_id=current_user.id,
        details={"event": "setup"}
    )
    
    return MFASetupResponse(
        qr_code=qr_code,
        backup_codes=backup_codes
    )

@router.post("/verify")
async def verify_mfa(
    verify_request: MFAVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Verify MFA token and enable MFA for the user.
    """
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled"
        )
    
    if not current_user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA setup not initiated"
        )
    
    # Verify token
    if not mfa_manager.verify_totp(current_user.mfa_secret, verify_request.token):
        raise InvalidMFAToken("Invalid MFA token")
    
    # Enable MFA
    current_user.mfa_enabled = True
    db.commit()
    
    # Log MFA verification
    await log_audit_event(
        action=AuditAction.MFA_EVENT,
        user_id=current_user.id,
        details={"event": "enabled"}
    )
    
    return {"message": "MFA enabled successfully"}

@router.post("/disable")
async def disable_mfa(
    verify_request: MFAVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Disable MFA for the user.
    Requires current MFA token for verification.
    """
    if not current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled"
        )
    
    # Verify token
    if not mfa_manager.verify_totp(current_user.mfa_secret, verify_request.token):
        raise InvalidMFAToken("Invalid MFA token")
    
    # Disable MFA
    current_user.mfa_enabled = False
    current_user.mfa_secret = None
    current_user.mfa_backup_codes = None
    db.commit()
    
    # Log MFA disable
    await log_audit_event(
        action=AuditAction.MFA_EVENT,
        user_id=current_user.id,
        details={"event": "disabled"}
    )
    
    return {"message": "MFA disabled successfully"} 
from fastapi import APIRouter
from app.api.v1.endpoints import auth, mfa

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(mfa.router, prefix="/mfa", tags=["multi-factor authentication"]) 
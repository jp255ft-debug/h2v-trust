"""
Authentication routes: login and token management.
"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models.auth import LoginRequest, TokenResponse
from services.auth_service import authenticate_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT token.
    
    Accepts email and password, returns a Bearer token with 1-hour expiration.
    The token contains user_id, tenant_id, and role claims.
    """
    return authenticate_user(db, login_data.email, login_data.password)

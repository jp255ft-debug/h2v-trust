"""
Pydantic models for authentication (login, JWT tokens).
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    """Login request with email and password."""
    email: str
    password: str


class UserInfo(BaseModel):
    """User info returned with token."""
    id: str
    email: str
    full_name: str
    role: str
    tenant_id: Optional[str] = None
    tenant_name: Optional[str] = None


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    user: UserInfo


class TokenData(BaseModel):
    """Decoded JWT token payload."""
    user_id: str
    tenant_id: str
    role: str
    exp: Optional[int] = None

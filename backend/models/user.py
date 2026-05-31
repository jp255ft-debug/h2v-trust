"""
Pydantic models for User management.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: str
    full_name: str


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str


class UserResponse(UserBase):
    """Schema for user API response."""
    id: str
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserTenantCreate(BaseModel):
    """Schema for inviting a user to a tenant."""
    email: str
    full_name: Optional[str] = None
    role: str = "operator"  # admin, operator, auditor


class UserTenantResponse(BaseModel):
    """Schema for user-tenant association response."""
    id: str
    user_id: str
    tenant_id: str
    role: str
    is_primary: bool
    user: Optional[UserResponse] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserTenantListResponse(BaseModel):
    """Schema for listing users of a tenant."""
    users: list[UserTenantResponse]
    total: int

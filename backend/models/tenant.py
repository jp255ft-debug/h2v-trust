"""
Pydantic models for Tenant management.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TenantBase(BaseModel):
    """Base tenant schema."""
    name: str
    slug: str
    contact_email: Optional[str] = None


class TenantCreate(TenantBase):
    """Schema for creating a new tenant."""
    pass


class TenantUpdate(BaseModel):
    """Schema for updating a tenant."""
    name: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[str] = None
    contact_email: Optional[str] = None


class TenantResponse(TenantBase):
    """Schema for tenant API response."""
    id: str
    status: str
    api_key: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TenantListResponse(BaseModel):
    """Schema for listing tenants."""
    tenants: list[TenantResponse]
    total: int

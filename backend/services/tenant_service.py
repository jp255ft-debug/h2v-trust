"""
Tenant management service for CRUD operations.
"""

import logging
import hashlib
from typing import Optional
from sqlalchemy.orm import Session

from db.models import Tenant, User, UserTenant
from api.dependencies.jwt_auth import generate_api_key
from models.tenant import TenantCreate, TenantUpdate, TenantResponse

logger = logging.getLogger(__name__)


def _hash_api_key(api_key: str) -> str:
    """Hash an API key for storage."""
    return hashlib.sha256(api_key.encode()).hexdigest()


def list_tenants(db: Session) -> list[Tenant]:
    """List all tenants."""
    return db.query(Tenant).order_by(Tenant.created_at.desc()).all()


def get_tenant(db: Session, tenant_id: str) -> Optional[Tenant]:
    """Get a tenant by ID."""
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()


def get_tenant_by_slug(db: Session, slug: str) -> Optional[Tenant]:
    """Get a tenant by slug."""
    return db.query(Tenant).filter(Tenant.slug == slug).first()


def create_tenant(db: Session, tenant_data: TenantCreate) -> TenantResponse:
    """
    Create a new tenant with a generated API key.
    
    Returns:
        TenantResponse with the generated API key (shown only once).
    """
    from fastapi import HTTPException, status
    
    # Check for duplicate slug
    existing = get_tenant_by_slug(db, tenant_data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tenant with slug '{tenant_data.slug}' already exists",
        )
    
    # Generate API key
    api_key = generate_api_key()
    api_key_hash = _hash_api_key(api_key)
    
    tenant = Tenant(
        name=tenant_data.name,
        slug=tenant_data.slug,
        api_key_hash=api_key_hash,
        status="active",
        contact_email=tenant_data.contact_email,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    logger.info(f"Tenant created: name={tenant.name}, slug={tenant.slug}, id={tenant.id}")
    
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        slug=tenant.slug,
        status=tenant.status,
        contact_email=tenant.contact_email,
        api_key=api_key,  # Shown only once
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )


def update_tenant(
    db: Session,
    tenant_id: str,
    tenant_data: TenantUpdate,
) -> Optional[Tenant]:
    """Update a tenant's fields."""
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        return None
    
    update_data = tenant_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tenant, field, value)
    
    db.commit()
    db.refresh(tenant)
    logger.info(f"Tenant updated: id={tenant_id}, fields={list(update_data.keys())}")
    return tenant


def get_tenant_user_count(db: Session, tenant_id: str) -> int:
    """Get the number of active users in a tenant."""
    return (
        db.query(UserTenant)
        .filter(UserTenant.tenant_id == tenant_id)
        .count()
    )

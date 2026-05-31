"""
User management service for tenant user operations.
"""

import logging
from typing import Optional
from sqlalchemy.orm import Session

from db.models import User, Tenant, UserTenant
from models.user import UserTenantCreate, UserTenantResponse, UserResponse
from services.auth_service import get_or_create_user

logger = logging.getLogger(__name__)


def list_tenant_users(db: Session, tenant_id: str) -> list[UserTenant]:
    """List all users associated with a tenant."""
    return (
        db.query(UserTenant)
        .filter(UserTenant.tenant_id == tenant_id)
        .order_by(UserTenant.created_at.desc())
        .all()
    )


def invite_user_to_tenant(
    db: Session,
    tenant_id: str,
    invite_data: UserTenantCreate,
) -> UserTenant:
    """
    Invite a user to a tenant.
    
    If the user doesn't exist, creates a new user with a temporary password.
    If the user is already in the tenant, updates their role.
    """
    from fastapi import HTTPException, status
    
    # Verify tenant exists
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    
    # Get or create user
    full_name = invite_data.full_name or invite_data.email.split("@")[0]
    user = get_or_create_user(db, invite_data.email, full_name)
    
    # Check if user is already in this tenant
    existing = (
        db.query(UserTenant)
        .filter(
            UserTenant.user_id == user.id,
            UserTenant.tenant_id == tenant_id,
        )
        .first()
    )
    
    if existing:
        # Update role if different
        if existing.role != invite_data.role:
            existing.role = invite_data.role
            db.commit()
            db.refresh(existing)
            logger.info(
                f"User role updated: user={user.email}, "
                f"tenant={tenant_id}, role={invite_data.role}"
            )
        return existing
    
    # Create association
    user_tenant = UserTenant(
        user_id=user.id,
        tenant_id=tenant_id,
        role=invite_data.role,
        is_primary=False,
    )
    db.add(user_tenant)
    db.commit()
    db.refresh(user_tenant)
    
    logger.info(
        f"User invited: user={user.email}, "
        f"tenant={tenant_id}, role={invite_data.role}"
    )
    
    return user_tenant


def remove_user_from_tenant(
    db: Session,
    tenant_id: str,
    user_id: str,
) -> bool:
    """Remove a user from a tenant."""
    from fastapi import HTTPException, status
    
    user_tenant = (
        db.query(UserTenant)
        .filter(
            UserTenant.user_id == user_id,
            UserTenant.tenant_id == tenant_id,
        )
        .first()
    )
    
    if not user_tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in this tenant",
        )
    
    db.delete(user_tenant)
    db.commit()
    logger.info(f"User removed from tenant: user={user_id}, tenant={tenant_id}")
    return True


def get_user_tenant_role(db: Session, user_id: str, tenant_id: str) -> Optional[str]:
    """Get a user's role in a specific tenant."""
    user_tenant = (
        db.query(UserTenant)
        .filter(
            UserTenant.user_id == user_id,
            UserTenant.tenant_id == tenant_id,
        )
        .first()
    )
    return user_tenant.role if user_tenant else None

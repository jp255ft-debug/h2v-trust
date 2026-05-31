"""
Admin routes for tenant and user management.
"""

import logging
from datetime import date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Tenant, User, UserTenant, AuditLog
from api.dependencies.jwt_auth import get_current_user, require_role
from models.tenant import TenantCreate, TenantUpdate, TenantResponse, TenantListResponse
from models.user import UserTenantCreate, UserTenantResponse, UserTenantListResponse, UserResponse
from services.tenant_service import (
    list_tenants,
    get_tenant,
    create_tenant,
    update_tenant,
    get_tenant_user_count,
)
from services.user_service import (
    list_tenant_users,
    invite_user_to_tenant,
    remove_user_from_tenant,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


# ─── Tenant Management ───────────────────────────────────────────────


@router.get("/tenants", response_model=TenantListResponse)
async def admin_list_tenants(
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """List all tenants. Admin only."""
    tenants = list_tenants(db)
    tenant_responses = []
    for t in tenants:
        user_count = get_tenant_user_count(db, t.id)
        tr = TenantResponse(
            id=t.id,
            name=t.name,
            slug=t.slug,
            status=t.status,
            contact_email=t.contact_email,
            created_at=t.created_at,
            updated_at=t.updated_at,
        )
        tenant_responses.append(tr)
    
    return TenantListResponse(
        tenants=tenant_responses,
        total=len(tenant_responses),
    )


@router.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_tenant(
    tenant_data: TenantCreate,
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """Create a new tenant with generated API key. Admin only."""
    return create_tenant(db, tenant_data)


@router.get("/tenants/{tenant_id}", response_model=TenantResponse)
async def admin_get_tenant(
    tenant_id: str,
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """Get tenant details. Admin only."""
    tenant = get_tenant(db, tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        slug=tenant.slug,
        status=tenant.status,
        contact_email=tenant.contact_email,
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )


@router.patch("/tenants/{tenant_id}", response_model=TenantResponse)
async def admin_update_tenant(
    tenant_id: str,
    tenant_data: TenantUpdate,
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """Update tenant status or details. Admin only."""
    tenant = update_tenant(db, tenant_id, tenant_data)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return TenantResponse(
        id=tenant.id,
        name=tenant.name,
        slug=tenant.slug,
        status=tenant.status,
        contact_email=tenant.contact_email,
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )


# ─── User Management per Tenant ──────────────────────────────────────


@router.get("/tenants/{tenant_id}/users", response_model=UserTenantListResponse)
async def admin_list_users(
    tenant_id: str,
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """List users of a tenant. Admin only."""
    user_tenants = list_tenant_users(db, tenant_id)
    responses = []
    for ut in user_tenants:
        user = db.query(User).filter(User.id == ut.user_id).first()
        user_resp = UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
        ) if user else None
        responses.append(UserTenantResponse(
            id=ut.id,
            user_id=ut.user_id,
            tenant_id=ut.tenant_id,
            role=ut.role,
            is_primary=ut.is_primary,
            user=user_resp,
            created_at=ut.created_at,
        ))
    return UserTenantListResponse(users=responses, total=len(responses))


@router.post("/tenants/{tenant_id}/users", status_code=status.HTTP_201_CREATED)
async def admin_invite_user(
    tenant_id: str,
    invite_data: UserTenantCreate,
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """Invite a user to a tenant. Admin only."""
    user_tenant = invite_user_to_tenant(db, tenant_id, invite_data)
    user = db.query(User).filter(User.id == user_tenant.user_id).first()
    return {
        "message": f"User {user.email} invited to tenant",
        "user_id": user.id,
        "tenant_id": tenant_id,
        "role": user_tenant.role,
    }


@router.delete("/tenants/{tenant_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_remove_user(
    tenant_id: str,
    user_id: str,
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """Remove a user from a tenant. Admin only."""
    remove_user_from_tenant(db, tenant_id, user_id)


# ─── Audit Logs ──────────────────────────────────────────────────────


@router.get("/audit-logs")
async def admin_list_audit_logs(
    tenant_id: Optional[str] = Query(None, description="Filter by tenant ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action type"),
    date_from: Optional[date] = Query(None, description="Filter logs from this date (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Filter logs up to this date (YYYY-MM-DD)"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    page: Optional[int] = Query(None, ge=1, description="Page number (alternative to offset)"),
    page_size: Optional[int] = Query(None, ge=1, le=500, description="Page size (alternative to limit)"),
    current_user: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """List audit logs with optional filters. Admin only.
    
    Supports both offset/limit and page/page_size pagination.
    """
    query = db.query(AuditLog)
    
    if tenant_id:
        query = query.filter(AuditLog.tenant_id == tenant_id)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    
    # Filtro por período
    if date_from:
        query = query.filter(AuditLog.created_at >= date_from)
    if date_to:
        # Inclui o dia inteiro: data_fim 2026-05-11 → created_at < 2026-05-12
        query = query.filter(AuditLog.created_at < date_to + timedelta(days=1))
    
    total = query.count()
    
    # Suporta page/page_size como alternativa a offset/limit
    if page is not None and page_size is not None:
        effective_offset = (page - 1) * page_size
        effective_limit = page_size
    else:
        effective_offset = offset
        effective_limit = limit
    
    logs = (
        query
        .order_by(AuditLog.created_at.desc())
        .offset(effective_offset)
        .limit(effective_limit)
        .all()
    )
    
    # Mapear tenant_name para cada log
    tenant_cache = {}
    log_dicts = []
    for log in logs:
        tenant_name = None
        if log.tenant_id:
            if log.tenant_id not in tenant_cache:
                tenant = db.query(Tenant).filter(Tenant.id == log.tenant_id).first()
                tenant_cache[log.tenant_id] = tenant.name if tenant else None
            tenant_name = tenant_cache[log.tenant_id]
        log_dicts.append(log.to_dict(tenant_name=tenant_name))
    
    return {
        "logs": log_dicts,
        "total": total,
        "page": page or (offset // limit + 1 if limit > 0 else 1),
        "page_size": page_size or limit,
    }

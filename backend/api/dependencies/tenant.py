"""
Tenant isolation dependency with role-based access control.

Two dependency functions are provided:
- get_tenant_id: For read/list operations. Returns None for auditors (cross-tenant),
  or the tenant_id string for operators (single-tenant).
- require_tenant_id: For write/create operations. Returns tenant_id for operators,
  raises 403 for auditors.

The tenant_id is derived from the authenticated user (via get_current_user),
which supports JWT Bearer tokens first, with API Key fallback.
The X-Tenant-Id header from the client is IGNORED for authorization purposes.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from api.dependencies.jwt_auth import get_current_user


async def get_tenant_id(current_user: dict = Depends(get_current_user)) -> Optional[str]:
    """
    Extract tenant_id for READ operations.

    - Operators (role="operator"): Returns their own tenant_id.
      Services MUST filter queries by this tenant_id.
    - Auditors (role="auditor"): Returns None.
      Services MUST NOT filter by tenant_id (cross-tenant access).
    - Admins (role="admin"): Returns None (cross-tenant access).

    Args:
        current_user: Dict with "user_id", "tenant_id", "role", "auth_method"
                      from get_current_user (jwt_auth.py).

    Returns:
        The tenant_id string, or None for auditors/admins (cross-tenant access).
    """
    role = current_user.get("role", "auditor")
    if role in ("auditor", "admin"):
        return None  # Cross-tenant access: no tenant filter
    return current_user.get("tenant_id")


async def require_tenant_id(current_user: dict = Depends(get_current_user)) -> str:
    """
    Extract tenant_id for WRITE operations.

    - Operators (role="operator"): Returns their own tenant_id.
    - Auditors (role="auditor"): Raises 403 Forbidden.
      Auditors cannot create or modify data.
    - Admins (role="admin"): Returns their tenant_id.

    Args:
        current_user: Dict with "user_id", "tenant_id", "role", "auth_method"
                      from get_current_user (jwt_auth.py).

    Returns:
        The tenant_id string.

    Raises:
        HTTPException 403: If the caller is an auditor.
    """
    role = current_user.get("role", "auditor")
    if role == "auditor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Auditores não podem criar ou modificar dados"
        )
    return current_user.get("tenant_id")

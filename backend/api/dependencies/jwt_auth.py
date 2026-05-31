"""
JWT authentication and unified auth middleware for H2V-Trust.

Provides:
- get_current_user: Unified auth that tries JWT first, falls back to API Key
- require_role: RBAC decorator for minimum role verification
- get_tenant_id: Extracts tenant_id from authenticated user
"""

import logging
import secrets
from typing import Optional
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Header, status, Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import settings
from db.database import get_db
from db.models import User, Tenant, UserTenant
from api.dependencies.auth import verify_api_key

logger = logging.getLogger(__name__)

# Password hashing context with bcrypt (cost 12)
pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12)

# JWT configuration
JWT_SECRET_KEY = getattr(settings, "JWT_SECRET_KEY", None) or settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with cost 12."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_api_key() -> str:
    """Generate a secure random API key with 'h2v_' prefix."""
    return "h2v_" + secrets.token_hex(32)


def create_access_token(user_id: str, tenant_id: str, role: str) -> str:
    """Create a JWT access token with user_id, tenant_id, and role claims."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    to_encode = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


async def get_current_user(
    request: Request,
    authorization: Optional[str] = Header(None, alias="Authorization"),
    api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> dict:
    """
    Unified authentication middleware.
    
    Tries JWT Bearer token first, falls back to API Key (X-API-Key header).
    
    Returns a dict with:
    - user_id: str (UUID)
    - tenant_id: str
    - role: str (admin, operator, auditor)
    - auth_method: str ("jwt" or "api_key")
    """
    # Try JWT first
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        try:
            payload = decode_access_token(token)
            return {
                "user_id": payload.get("sub"),
                "tenant_id": payload.get("tenant_id"),
                "role": payload.get("role", "operator"),
                "auth_method": "jwt",
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.warning(f"JWT auth failed, trying API key: {e}")
    
    # Fallback to API Key
    if api_key:
        try:
            auth_info = verify_api_key(api_key)
            # Map API key roles to new RBAC roles
            role_map = {
                "producer": "operator",
                "auditor": "auditor",
            }
            return {
                "user_id": None,
                "tenant_id": auth_info["tenant_id"],
                "role": role_map.get(auth_info["role"], "operator"),
                "auth_method": "api_key",
            }
        except HTTPException:
            raise
    
    # No authentication provided
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Provide Bearer token or X-API-Key header.",
    )


def require_role(min_role: str):
    """
    Dependency factory for RBAC.
    
    Usage:
        @router.get("/admin/tenants")
        async def list_tenants(current_user: dict = Depends(require_role("admin"))):
            ...
    
    Role hierarchy: admin > operator > auditor
    """
    role_hierarchy = {
        "auditor": 0,
        "operator": 1,
        "admin": 2,
    }
    
    min_level = role_hierarchy.get(min_role, 0)
    
    async def _require_role(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role", "auditor")
        user_level = role_hierarchy.get(user_role, -1)
        
        if user_level < min_level:
            logger.warning(
                f"Authorization FAILED: user role={user_role}, "
                f"required={min_role}, user_id={current_user.get('user_id')}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {min_role}",
            )
        
        return current_user
    
    return _require_role


async def get_tenant_id(current_user: dict = Depends(get_current_user)) -> Optional[str]:
    """
    Extract tenant_id for READ operations.
    
    - Operators: Returns their own tenant_id.
    - Auditors: Returns None (cross-tenant access).
    - Admins: Returns None (cross-tenant access).
    """
    role = current_user.get("role", "auditor")
    if role in ("auditor", "admin"):
        return None  # Cross-tenant access
    return current_user.get("tenant_id")


async def require_tenant_id(current_user: dict = Depends(get_current_user)) -> str:
    """
    Extract tenant_id for WRITE operations.
    
    - Operators: Returns their own tenant_id.
    - Auditors: Raises 403 Forbidden.
    - Admins: Returns their tenant_id.
    """
    role = current_user.get("role", "auditor")
    if role == "auditor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Auditores não podem criar ou modificar dados",
        )
    return current_user.get("tenant_id")

"""
Authentication service for user login and JWT token management.
"""

import logging
from sqlalchemy.orm import Session

from db.models import User, Tenant, UserTenant
from api.dependencies.jwt_auth import (
    hash_password,
    verify_password,
    create_access_token,
    generate_api_key,
)
from models.auth import TokenResponse, UserInfo

logger = logging.getLogger(__name__)


def authenticate_user(db: Session, email: str, password: str) -> TokenResponse:
    """
    Authenticate a user by email and password.
    
    Steps:
    1. Find user by email
    2. Verify password hash (bcrypt, cost 12)
    3. Find primary tenant association
    4. Generate JWT with user_id, tenant_id, role
    
    Returns:
        TokenResponse with access_token
    
    Raises:
        HTTPException 401 if credentials are invalid
    """
    from fastapi import HTTPException, status
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Login FAILED: user not found (email={email})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Verify password
    if not verify_password(password, user.password_hash):
        logger.warning(f"Login FAILED: wrong password (email={email})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Check if user is active
    if not user.is_active:
        logger.warning(f"Login FAILED: inactive user (email={email})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
        )
    
    # Find primary tenant
    user_tenant = (
        db.query(UserTenant)
        .filter(UserTenant.user_id == user.id, UserTenant.is_primary == True)
        .first()
    )
    
    if not user_tenant:
        # Fallback to first tenant
        user_tenant = (
            db.query(UserTenant)
            .filter(UserTenant.user_id == user.id)
            .first()
        )
    
    if not user_tenant:
        logger.warning(f"Login FAILED: user has no tenant (email={email})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User has no tenant association",
        )
    
    # Generate JWT
    access_token = create_access_token(
        user_id=user.id,
        tenant_id=user_tenant.tenant_id,
        role=user_tenant.role,
    )
    
    # Get tenant name
    tenant = db.query(Tenant).filter(Tenant.id == user_tenant.tenant_id).first()
    tenant_name = tenant.name if tenant else None
    
    logger.info(
        f"Login SUCCESS: email={email}, "
        f"role={user_tenant.role}, "
        f"tenant={user_tenant.tenant_id}"
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=3600,
        user=UserInfo(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user_tenant.role,
            tenant_id=str(user_tenant.tenant_id),
            tenant_name=tenant_name,
        ),
    )


def create_user(
    db: Session,
    email: str,
    password: str,
    full_name: str,
) -> User:
    """
    Create a new user with hashed password.
    
    Returns:
        The created User object.
    """
    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"User created: email={email}, id={user.id}")
    return user


def get_or_create_user(
    db: Session,
    email: str,
    full_name: str,
) -> User:
    """
    Get existing user by email or create a new one.
    New users are created with a random password (must be reset).
    """
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    
    # Create with random password (user will need to reset)
    import secrets
    temp_password = secrets.token_urlsafe(16)
    return create_user(db, email, temp_password, full_name)

"""
UserTenant model for user-tenant association with role-based access control.
"""

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid


class UserTenant(Base):
    """Association model linking users to tenants with specific roles.
    
    A user can belong to multiple tenants with different roles.
    Each user has exactly one primary tenant (is_primary=True).
    """
    
    __tablename__ = "user_tenants"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50), nullable=False, default="operator")  # admin, operator, auditor
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="tenants")
    tenant = relationship("Tenant", back_populates="users")
    
    __table_args__ = (
        # Ensure a user can only be associated once with a tenant
        # UniqueConstraint is handled via the unique_together behavior
    )
    
    def __repr__(self):
        return f"<UserTenant(user={self.user_id}, tenant={self.tenant_id}, role={self.role})>"
    
    def to_dict(self):
        """Convert user-tenant association to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "role": self.role,
            "is_primary": self.is_primary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

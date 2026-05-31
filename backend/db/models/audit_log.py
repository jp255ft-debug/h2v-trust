"""
AuditLog model for tracking all system operations and compliance events.
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, JSON
from sqlalchemy.sql import func
from ..database import Base


class AuditLog(Base):
    """Model for audit trail of all system operations."""
    
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(50), nullable=True, index=True)
    entity_id = Column(String(100), nullable=True, index=True)
    actor = Column(String(100), nullable=True)
    user_id = Column(String(36), nullable=True, index=True)
    tenant_id = Column(String(36), nullable=True, index=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, entity={self.entity_type}:{self.entity_id})>"
    
    def to_dict(self, tenant_name: str = None):
        """Convert audit log to dictionary.
        
        Args:
            tenant_name: Optional tenant name for display.
        """
        return {
            "id": str(self.id),
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "actor": self.actor,
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "tenant_name": tenant_name,
            "details": self.details,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            # Campos compatíveis com o frontend admin
            "user_email": self.actor or "",
            "resource": self.entity_type or "",
            "resource_id": self.entity_id,
        }

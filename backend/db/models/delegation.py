"""
Delegation model for CBAM delegated declarant management.
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.sql import func
from ..database import Base


class Delegation(Base):
    """Model for CBAM delegation authorizations."""
    
    __tablename__ = "delegations"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tenant_id = Column(String(100), nullable=False, index=True, default="default")
    delegation_id = Column(String(100), unique=True, nullable=False, index=True)
    producer_id = Column(String(100), nullable=False, index=True)
    producer_wallet = Column(String(100), nullable=True)
    declarant_address = Column(String(100), nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="active")  # active, revoked, expired
    blockchain_tx_hash = Column(String(66), nullable=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Delegation(id={self.delegation_id}, producer={self.producer_id}, status={self.status})>"
    
    def to_dict(self):
        """Convert delegation to dictionary."""
        return {
            "id": self.delegation_id,
            "producer_id": self.producer_id,
            "producer_wallet": self.producer_wallet,
            "declarant_address": self.declarant_address,
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "status": self.status,
            "blockchain_tx_hash": self.blockchain_tx_hash,
            "revoked_at": self.revoked_at.isoformat() if self.revoked_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

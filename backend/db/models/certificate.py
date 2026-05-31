"""
Certificate model for blockchain-based hydrogen certificates.
"""

from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Certificate(Base):
    """Model for blockchain-based hydrogen certificates (SBT tokens).
    
    token_id uses BigInteger to accommodate uint256 values from the blockchain.
    batch_id is NOT unique - a batch may have multiple certificates over time
    (renewal, reissuance). Uniqueness of token_id is guaranteed by the blockchain.
    """
    
    __tablename__ = "certificates"
    
    id = Column(String(36), primary_key=True, index=True)
    tenant_id = Column(String(100), nullable=False, index=True, default="default")
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False, index=True)
    token_id = Column(BigInteger, nullable=False, index=True)
    blockchain_tx_hash = Column(String(66), nullable=False)
    qr_code_data = Column(Text, nullable=True)
    is_consumed = Column(Boolean, default=False)
    consumed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    batch = relationship("Batch", back_populates="certificate")
    
    def __repr__(self):
        return f"<Certificate(id={self.id}, batch={self.batch_id}, token={self.token_id})>"
    
    def to_dict(self):
        """Convert certificate to dictionary for API response."""
        return {
            "id": self.id,
            "batch_id": self.batch_id,
            "token_id": self.token_id,
            "blockchain_tx_hash": self.blockchain_tx_hash,
            "qr_code_data": self.qr_code_data,
            "is_consumed": self.is_consumed,
            "consumed_at": self.consumed_at.isoformat() if self.consumed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

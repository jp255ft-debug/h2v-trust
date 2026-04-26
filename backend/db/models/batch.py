"""
Batch model for hydrogen production batch tracking.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Batch(Base):
    """Model for hydrogen production batches."""
    
    __tablename__ = "batches"
    
    id = Column(String(36), primary_key=True, index=True)
    telemetry_id = Column(Integer, ForeignKey("telemetry_records.id"), nullable=True)
    producer_wallet = Column(String(100), nullable=True, index=True)
    producer_id = Column(String(100), nullable=True, index=True)
    facility_id = Column(String(100), nullable=True)
    production_location = Column(String(200), nullable=True)
    size_kg = Column(Float, nullable=False, default=1000.0)
    is_compliant = Column(Boolean, default=False)
    blockchain_status = Column(String(20), nullable=True, default=None)  # None=not_attempted, "pending", "confirmed", "failed"
    compliance_report = Column(JSON, nullable=True)
    batch_hash = Column(String(100), nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    telemetry = relationship("TelemetryRecord", back_populates="batch")
    certificate = relationship("Certificate", back_populates="batch", uselist=False)
    
    def __repr__(self):
        return f"<Batch(id={self.id}, size={self.size_kg}kg, compliant={self.is_compliant})>"
    
    def to_dict(self):
        """Convert batch to dictionary for API response."""
        return {
            "id": self.id,
            "telemetry_id": self.telemetry_id,
            "producer_wallet": self.producer_wallet,
            "producer_id": self.producer_id,
            "facility_id": self.facility_id,
            "production_location": self.production_location,
            "size_kg": self.size_kg,
            "is_compliant": self.is_compliant,
            "compliance_report": self.compliance_report,
            "batch_hash": self.batch_hash,
            "telemetry": self.telemetry.to_dict() if self.telemetry else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

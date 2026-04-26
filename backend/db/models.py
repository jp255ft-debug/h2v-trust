from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class TelemetryRecord(Base):
    """Raw telemetry data from IoT sensors."""
    __tablename__ = "telemetry_records"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    energy_source = Column(String)  # wind, solar, diesel
    power_generated_mwh = Column(Float)
    ghg_emissions_kgCO2_per_kgH2 = Column(Float)
    water_consumption_liters = Column(Float)
    water_source = Column(String)  # desalination, surface_water
    batch_id = Column(String, ForeignKey("batches.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    batch = relationship("Batch", back_populates="telemetry_records")


class Batch(Base):
    """Batch of hydrogen production."""
    __tablename__ = "batches"

    id = Column(String, primary_key=True, index=True)
    producer_id = Column(String, index=True)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True), nullable=True)
    total_hydrogen_kg = Column(Float)
    avg_ghg_emissions_kgCO2_per_kgH2 = Column(Float)
    total_ghg_emissions_tCO2e = Column(Float)
    water_source = Column(String)
    energy_source_mix = Column(JSON)  # {"wind": 0.7, "solar": 0.3}
    compliance_status = Column(String)  # compliant, non_compliant, pending
    compliance_reason = Column(Text, nullable=True)
    certificate_token_id = Column(String, nullable=True)
    certificate_tx_hash = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    telemetry_records = relationship("TelemetryRecord", back_populates="batch")
    certificates = relationship("Certificate", back_populates="batch")
    audit_logs = relationship("AuditLog", back_populates="batch")


class Certificate(Base):
    """Blockchain certificate (SBT) for a batch."""
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(String, unique=True, index=True)
    batch_id = Column(String, ForeignKey("batches.id"))
    producer_id = Column(String, index=True)
    metadata_uri = Column(String)  # IPFS URI
    metadata = Column(JSON)  # On-chain metadata
    tx_hash = Column(String)
    block_number = Column(Integer)
    is_consumed = Column(Boolean, default=False)
    consumed_at = Column(DateTime(timezone=True), nullable=True)
    consumed_by = Column(String, nullable=True)  # Importer ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    batch = relationship("Batch", back_populates="certificates")


class AuditLog(Base):
    """Audit trail for compliance verification."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, ForeignKey("batches.id"))
    auditor_id = Column(String, index=True)
    action = Column(String)  # verify, reject, comment
    details = Column(Text)
    evidence_uri = Column(String, nullable=True)  # IPFS URI for evidence
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    batch = relationship("Batch", back_populates="audit_logs")


class Delegation(Base):
    """Delegated CBAM declarant authorization."""
    __tablename__ = "delegations"

    id = Column(Integer, primary_key=True, index=True)
    producer_id = Column(String, index=True)
    declarant_id = Column(String, index=True)
    authorization_hash = Column(String, unique=True)
    valid_from = Column(DateTime(timezone=True))
    valid_until = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
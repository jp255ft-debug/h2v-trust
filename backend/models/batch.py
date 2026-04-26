"""
Pydantic models for batch data validation and serialization.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any


class BatchBase(BaseModel):
    """Base model for batch data."""
    telemetry_id: int
    producer_wallet: Optional[str] = None
    producer_id: Optional[str] = None
    facility_id: Optional[str] = None
    production_location: Optional[str] = None
    size_kg: float = Field(ge=0, default=1000.0)
    is_compliant: bool = False
    compliance_report: Optional[Dict[str, Any]] = None
    batch_hash: Optional[str] = None


class BatchCreate(BatchBase):
    """Model for creating a new batch."""
    pass


class BatchUpdate(BaseModel):
    """Model for updating an existing batch."""
    telemetry_id: Optional[int] = None
    producer_wallet: Optional[str] = None
    producer_id: Optional[str] = None
    facility_id: Optional[str] = None
    production_location: Optional[str] = None
    size_kg: Optional[float] = Field(ge=0, default=None)
    is_compliant: Optional[bool] = None
    compliance_report: Optional[Dict[str, Any]] = None
    batch_hash: Optional[str] = None


class BatchResponse(BatchBase):
    """Model for batch API responses."""
    id: str
    telemetry: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class BatchListResponse(BaseModel):
    """Model for batch list API responses."""
    batches: list[BatchResponse]
    total: int


class BatchComplianceCheck(BaseModel):
    """Model for batch compliance check request."""
    batch_id: str
    ghg_emissions_kgCO2_per_kgH2: float
    water_consumption_liters: float
    water_source: str
    energy_source: str
    h2_kg: float


class BatchComplianceResponse(BaseModel):
    """Model for batch compliance check response."""
    batch_id: str
    is_compliant: bool
    ghg_emissions: float
    water_consumption: float
    energy_source: str
    compliance_details: Dict[str, Any]
    generated_at: str


class TelemetryData(BaseModel):
    """Model for telemetry data associated with a batch."""
    id: int
    sensor_id: str
    timestamp: Optional[datetime] = None
    energy_source: str
    power_generated_mwh: float
    ghg_emissions: float
    water_consumption_liters: float
    water_source: Optional[str] = None

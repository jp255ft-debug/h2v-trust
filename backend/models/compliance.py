"""
Pydantic models for compliance data validation and serialization.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any, List


class ComplianceBase(BaseModel):
    """Base model for compliance data."""
    batch_id: str
    is_compliant: bool = False
    checks: Dict[str, Any] = {}
    violations: List[str] = []


class ComplianceCreate(ComplianceBase):
    """Model for creating a new compliance record."""
    pass


class ComplianceUpdate(BaseModel):
    """Model for updating an existing compliance record."""
    is_compliant: Optional[bool] = None
    checks: Optional[Dict[str, Any]] = None
    violations: Optional[List[str]] = None


class ComplianceResponse(ComplianceBase):
    """Model for compliance API responses."""
    id: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ComplianceCheckRequest(BaseModel):
    """Model for compliance check request."""
    batch_id: str
    ghg_emissions_kgCO2_per_kgH2: float = Field(ge=0)
    water_consumption_liters: float = Field(ge=0)
    water_source: str
    energy_source: str
    h2_kg: float = Field(ge=0, default=1000.0)


class ComplianceCheckResponse(BaseModel):
    """Model for compliance check response."""
    is_compliant: bool
    checks: Dict[str, Any]
    violations: List[str] = []
    cbam_report: Optional[Dict[str, Any]] = None


class CBAMReportRequest(BaseModel):
    """Model for CBAM report request."""
    batch_id: str
    ghg_emissions_kgCO2_per_kgH2: float = Field(ge=0)
    h2_kg: float = Field(ge=0, default=1000.0)


class CBAMReportResponse(BaseModel):
    """Model for CBAM report response."""
    batch_id: str
    declared_emissions_tco2: float
    saved_emissions_vs_grey: float
    certificate_eligible: bool
    generated_at: str


class ComplianceStats(BaseModel):
    """Model for compliance statistics."""
    total_batches: int
    compliant_batches: int
    non_compliant_batches: int
    compliance_rate: float


class ComplianceListResponse(BaseModel):
    """Model for compliance list response."""
    records: list[ComplianceResponse]
    total: int


class ComplianceValidateRequest(BaseModel):
    """Model for compliance validation request."""
    batch_id: str
    validator_wallet: str = Field(..., min_length=10)


class ComplianceReportResponse(BaseModel):
    """Model for compliance report response."""
    batch_id: str
    is_compliant: bool
    ghg_emissions: float
    water_consumption: float
    energy_source: str
    compliance_details: Dict[str, Any]
    generated_at: datetime = Field(default_factory=datetime.utcnow)

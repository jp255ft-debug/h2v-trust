"""
Pydantic models for certificate data validation and serialization.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class CertificateBase(BaseModel):
    """Base model for certificate data."""
    batch_id: str
    token_id: int
    blockchain_tx_hash: str
    qr_code_data: Optional[str] = None


class CertificateCreate(CertificateBase):
    """Model for creating a new certificate."""
    pass


class CertificateUpdate(BaseModel):
    """Model for updating an existing certificate."""
    is_consumed: Optional[bool] = None
    consumed_at: Optional[datetime] = None


class CertificateResponse(CertificateBase):
    """Model for certificate API responses."""
    id: str
    is_consumed: bool = False
    consumed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CertificateConsumeRequest(BaseModel):
    """Model for certificate consumption request."""
    consumer_wallet: str = Field(..., min_length=10)
    purpose: str = Field(default="cbam_surrender")


class CertificateConsumeResponse(BaseModel):
    """Model for certificate consumption response."""
    certificate_id: str
    status: str
    tx_hash: Optional[str] = None
    message: str = "Certificate consumed successfully"


class CertificateVerifyRequest(BaseModel):
    """Model for certificate verification request."""
    certificate_id: str
    batch_id: Optional[str] = None


class CertificateVerifyResponse(BaseModel):
    """Model for certificate verification response."""
    is_valid: bool
    token_id: int
    batch_id: Optional[str] = None
    producer: Optional[str] = None
    emissions_data: Optional[dict] = None
    is_consumed: bool = False
    blockchain_verified: bool = False


class CertificateListResponse(BaseModel):
    """Model for certificate list response."""
    certificates: list[CertificateResponse]
    total: int


class CertificateMintRequest(BaseModel):
    """Model for certificate minting request."""
    batch_id: str
    recipient_wallet: str = Field(..., min_length=10)


class CertificateMintResponse(BaseModel):
    """Model for certificate minting response."""
    certificate_id: str
    tx_hash: str
    token_id: int
    status: str = "minted"

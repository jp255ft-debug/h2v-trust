"""
Pydantic models for delegation data validation and serialization.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class DelegationBase(BaseModel):
    """Base model for delegation data."""
    producer_id: str
    declarant_address: str
    valid_until: Optional[str] = None
    status: str = "active"


class DelegationCreate(DelegationBase):
    """Model for creating a new delegation."""
    pass


class DelegationUpdate(BaseModel):
    """Model for updating an existing delegation."""
    status: Optional[str] = None
    valid_until: Optional[str] = None
    revoked_at: Optional[str] = None


class DelegationResponse(DelegationBase):
    """Model for delegation API responses."""
    id: str
    producer_wallet: Optional[str] = None
    blockchain_tx_hash: Optional[str] = None
    revoked_at: Optional[str] = None
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DelegationVerifyRequest(BaseModel):
    """Model for delegation verification request."""
    producer_id: str
    declarant_address: str


class DelegationVerifyResponse(BaseModel):
    """Model for delegation verification response."""
    is_valid: bool
    producer_id: str
    declarant_address: str
    valid_until: Optional[str] = None
    message: str = ""


class DelegationBlockchainRequest(BaseModel):
    """Model for blockchain delegation request."""
    producer_id: str
    declarant_address: str
    valid_until: str


class DelegationBlockchainResponse(BaseModel):
    """Model for blockchain delegation response."""
    success: bool
    tx_hash: Optional[str] = None
    message: str = ""


class DelegationListResponse(BaseModel):
    """Model for delegation list response."""
    delegations: list[DelegationResponse]
    total: int


class DelegationStats(BaseModel):
    """Model for delegation statistics."""
    total_delegations: int
    active_delegations: int
    revoked_delegations: int


class DelegationSearchRequest(BaseModel):
    """Model for delegation search request."""
    producer_id: Optional[str] = None
    declarant_address: Optional[str] = None
    status: Optional[str] = None


class DelegationExpirationNotification(BaseModel):
    """Model for delegation expiration notification."""
    delegation_id: str
    producer_id: str
    declarant_address: str
    valid_until: str
    days_until_expiry: int


class DelegationCreateRequest(BaseModel):
    """Model for creating a new delegation (alternative)."""
    producer_id: str = Field(..., min_length=1)
    declarant_address: str = Field(..., min_length=10)
    valid_until: str  # ISO date string


class DelegationStatusResponse(BaseModel):
    """Model for delegation status response."""
    producer_id: str
    has_active_delegation: bool
    declarant_address: Optional[str] = None
    valid_until: Optional[str] = None
    created_at: Optional[str] = None


class DelegationRevokeRequest(BaseModel):
    """Model for revoking a delegation."""
    producer_id: str = Field(..., min_length=1)


class DelegationRevokeResponse(BaseModel):
    """Model for delegation revoke response."""
    producer_id: str
    status: str = "revoked"
    revoked_at: str
    message: str = "Delegation revoked successfully"

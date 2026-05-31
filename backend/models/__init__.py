"""
Pydantic models for H2V-Trust API.
"""

from .batch import (
    BatchBase,
    BatchCreate,
    BatchResponse,
    BatchUpdate,
    BatchListResponse,
    BatchComplianceCheck,
    BatchComplianceResponse,
    TelemetryData
)

from .certificate import (
    CertificateBase,
    CertificateCreate,
    CertificateResponse,
    CertificateUpdate,
    CertificateConsumeRequest,
    CertificateConsumeResponse,
    CertificateVerifyRequest,
    CertificateVerifyResponse,
    CertificateListResponse,
    CertificateMintRequest,
    CertificateMintResponse
)

from .compliance import (
    ComplianceBase,
    ComplianceCreate,
    ComplianceResponse,
    ComplianceUpdate,
    ComplianceCheckRequest,
    ComplianceCheckResponse,
    CBAMReportRequest,
    CBAMReportResponse,
    ComplianceStats,
    ComplianceListResponse
)

from .delegation import (
    DelegationBase,
    DelegationCreate,
    DelegationResponse,
    DelegationUpdate,
    DelegationVerifyRequest,
    DelegationVerifyResponse,
    DelegationBlockchainRequest,
    DelegationBlockchainResponse,
    DelegationListResponse,
    DelegationStats,
    DelegationSearchRequest,
    DelegationExpirationNotification
)

from .auth import (
    LoginRequest,
    TokenResponse,
    TokenData,
)

from .tenant import (
    TenantBase,
    TenantCreate,
    TenantUpdate,
    TenantResponse,
    TenantListResponse,
)

from .user import (
    UserBase,
    UserCreate,
    UserResponse,
    UserTenantCreate,
    UserTenantResponse,
    UserTenantListResponse,
)

# Re-export commonly used models
__all__ = [
    # Batch models
    "BatchBase",
    "BatchCreate",
    "BatchResponse",
    "BatchUpdate",
    "BatchListResponse",
    "BatchComplianceCheck",
    "BatchComplianceResponse",
    "TelemetryData",
    
    # Certificate models
    "CertificateBase",
    "CertificateCreate",
    "CertificateResponse",
    "CertificateUpdate",
    "CertificateConsumeRequest",
    "CertificateConsumeResponse",
    "CertificateVerifyRequest",
    "CertificateVerifyResponse",
    "CertificateListResponse",
    "CertificateMintRequest",
    "CertificateMintResponse",
    
    # Compliance models
    "ComplianceBase",
    "ComplianceCreate",
    "ComplianceResponse",
    "ComplianceUpdate",
    "ComplianceCheckRequest",
    "ComplianceCheckResponse",
    "CBAMReportRequest",
    "CBAMReportResponse",
    "ComplianceStats",
    "ComplianceListResponse",
    
    # Delegation models
    "DelegationBase",
    "DelegationCreate",
    "DelegationResponse",
    "DelegationUpdate",
    "DelegationVerifyRequest",
    "DelegationVerifyResponse",
    "DelegationBlockchainRequest",
    "DelegationBlockchainResponse",
    "DelegationListResponse",
    "DelegationStats",
    "DelegationSearchRequest",
    "DelegationExpirationNotification",
    
    # Auth models
    "LoginRequest",
    "TokenResponse",
    "TokenData",
    
    # Tenant models
    "TenantBase",
    "TenantCreate",
    "TenantUpdate",
    "TenantResponse",
    "TenantListResponse",
    
    # User models
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserTenantCreate",
    "UserTenantResponse",
    "UserTenantListResponse",
]

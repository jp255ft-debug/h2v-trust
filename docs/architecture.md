# H2V-Trust Architecture

## Overview

H2V-Trust is a comprehensive platform for verifying, certifying, and tracking green hydrogen production with CBAM (Carbon Border Adjustment Mechanism) compliance. The system integrates IoT telemetry, blockchain certification, satellite monitoring, and compliance verification.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │Dashboard │ │ Producer │ │ Auditor  │ │ Certificates │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
┌──────────────────────▼──────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │  Routes  │ │ Services │ │  Core    │ │  Blockchain  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ PostgreSQL │ │ Blockchain │ │  Oracle    │
│  Database  │ │ (Polygon)  │ │ (Satellite)│
└────────────┘ └────────────┘ └────────────┘
```

## Components

### Frontend (Next.js)
- **Dashboard**: Real-time monitoring of production metrics, compliance status, and certificates
- **Producer Portal**: Batch management, delegation, and certificate issuance
- **Auditor Portal**: Batch verification, compliance checking, and certificate validation
- **Shared Components**: Error boundaries, loading states, QR codes, and UI components

### Backend (FastAPI)
- **API Routes**: RESTful endpoints for batches, certificates, compliance, delegation, telemetry, and reports
- **Services**: Business logic for certificate management, delegation, reporting, and exporting
- **Core**: Compliance checking, emissions calculation, water compliance, and delegation management
- **Blockchain**: Web3 client, minting service, contract ABI, and verification
- **Oracle**: Satellite monitoring and task automation

### Database (PostgreSQL)
- **Models**: Telemetry records, audit logs, delegations, batches, and certificates
- **Relationships**: Batches linked to telemetry data, certificates linked to batches

### Smart Contracts (Solidity)
- **GreenHydrogenSBT**: Soulbound token for green hydrogen certificates
- **BatchRegistry**: On-chain batch registration and tracking
- **ComplianceVerifier**: Decentralized compliance verification
- **DelegationManager**: CBAM delegation management

## Data Flow

1. **Telemetry Ingestion**: IoT sensors send production data via API
2. **Batch Creation**: Producers create batches from telemetry data
3. **Compliance Check**: System validates GHG emissions, water usage, and energy source
4. **Certificate Minting**: Compliant batches receive blockchain certificates
5. **Verification**: Auditors verify batches and certificates on-chain
6. **CBAM Reporting**: Automated CBAM report generation for EU compliance

## Security

- API rate limiting for DDoS protection
- Blockchain-based certificate immutability
- Wallet-based authentication for sensitive operations
- Input validation and sanitization
- CORS configuration for frontend access

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

## Authentication & Authorization

### Overview

The H2V-Trust platform implements a **dual authentication system** supporting both modern JWT-based authentication and legacy API Key authentication, with automatic fallback.

### Authentication Flows

```
┌─────────────────────────────────────────────────────────────────┐
│                    Authentication Flow                            │
│                                                                   │
│  ┌──────────┐     ┌──────────────────┐     ┌─────────────────┐  │
│  │  Client   │────▶│  get_current_user │────▶│  JWT Decode     │  │
│  │  Request  │     │  (Dependency)     │     │  (python-jose)  │  │
│  └──────────┘     └────────┬─────────┘     └────────┬────────┘  │
│                            │                        │           │
│                            ▼                        ▼           │
│                    ┌──────────────┐        ┌──────────────┐     │
│                    │ Has Bearer   │ YES ──▶│ Decode JWT   │     │
│                    │ Token?       │        │ Validate sig │     │
│                    └──────┬───────┘        └──────┬───────┘     │
│                           │ NO                    │             │
│                           ▼                       ▼             │
│                    ┌──────────────┐        ┌──────────────┐     │
│                    │ Has X-API-Key │ YES ──▶│ Lookup API   │     │
│                    │ Header?      │        │ Key in DB    │     │
│                    └──────┬───────┘        └──────┬───────┘     │
│                           │ NO                    │             │
│                           ▼                       ▼             │
│                    ┌──────────────┐        ┌──────────────┐     │
│                    │ 401          │        │ Map to User  │     │
│                    │ Unauthorized │        │ & Tenant     │     │
│                    └──────────────┘        └──────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

#### 1. JWT Authentication (Primary)

- **Endpoint:** `POST /api/v1/auth/login`
- **Payload:** `{"email": "...", "password": "..."}`
- **Response:** `{"access_token": "<JWT>", "token_type": "bearer"}`
- **Token lifetime:** 60 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Algorithm:** HS256 with secret key from `JWT_SECRET_KEY` env var
- **Password hashing:** bcrypt with cost factor 12 (via `passlib`)
- **Header format:** `Authorization: Bearer <token>`

**JWT Payload Structure:**
```json
{
  "sub": "<user_uuid>",
  "email": "user@example.com",
  "role": "admin|operator|auditor",
  "tenant_id": "<tenant_uuid_or_null>",
  "exp": 1715000000,
  "iat": 1714996400
}
```

#### 2. API Key Authentication (Legacy)

- **Header:** `X-API-Key: <api_key>`
- **Lookup:** API key is hashed and compared against `Tenant.api_key_hash` in the database
- **Role mapping:** `producer` → `operator`, `auditor` → `auditor`
- **Status:** Maintained for backward compatibility with existing frontend integrations

#### 3. Dual Fallback (`get_current_user`)

The `get_current_user` dependency in `backend/api/dependencies/jwt_auth.py` implements the fallback logic:

```python
async def get_current_user(
    authorization: str | None = Header(None, alias="Authorization"),
    x_api_key: str | None = Header(None, alias="X-API-Key"),
    db: AsyncSession = Depends(get_db)
) -> UserContext:
    # 1. Try JWT Bearer token first
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
        payload = decode_access_token(token)
        return await get_user_from_payload(payload, db)
    
    # 2. Fallback to API Key
    if x_api_key:
        return await get_user_from_api_key(x_api_key, db)
    
    # 3. No valid auth
    raise HTTPException(status_code=401, detail="Not authenticated")
```

### Role-Based Access Control (RBAC)

#### Role Hierarchy

| Role | Level | Description |
|------|-------|-------------|
| `admin` | 2 | Full system access, tenant CRUD, user management, audit logs |
| `operator` | 1 | Access to own tenant data, create batches and certificates |
| `auditor` | 0 | Cross-tenant read-only access, batch verification |

#### Permission Enforcement

```python
# Require minimum role level
require_role("admin")     # Only admins
require_role("operator")  # Admins and operators
require_role("auditor")   # All authenticated users
```

**Implementation:** `backend/api/dependencies/jwt_auth.py` — `require_role(min_role)` is a **synchronous factory** that returns a dependency function:

```python
def require_role(min_role: str):
    """Factory that returns a FastAPI dependency."""
    role_levels = {"auditor": 0, "operator": 1, "admin": 2}
    min_level = role_levels.get(min_role, 0)
    
    async def role_checker(current_user: UserContext = Depends(get_current_user)):
        user_level = role_levels.get(current_user.role, -1)
        if user_level < min_level:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    
    return role_checker
```

### Multi-Tenant Isolation

#### Tenant Model

Each tenant represents an organization (e.g., a hydrogen producer). The `Tenant` model stores:

- `id` (UUID, primary key)
- `name` (e.g., "Produtor Alfa Ltda")
- `slug` (e.g., "produtor-alfa")
- `api_key_hash` (bcrypt hash of the API key)
- `status` (active / inactive)
- `contact_email`

#### User-Tenant Association

Users are associated with tenants via the `UserTenant` join table:

```python
class UserTenant(Base):
    __tablename__ = "user_tenants"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey("tenants.id"), primary_key=True)
    role: Mapped[str]  # admin, operator, auditor
    is_primary: Mapped[bool]  # Primary tenant association
```

#### Data Isolation Functions

```python
# Returns tenant_id from JWT or API Key lookup
# Returns None for auditors/admins (cross-tenant access)
get_tenant_id(current_user: UserContext) -> UUID | None

# Requires a specific tenant context
# Raises 403 for auditors (no tenant context)
require_tenant_id(current_user: UserContext) -> UUID
```

#### Isolation Behavior by Role

| Role | `get_tenant_id()` | `require_tenant_id()` | Data Scope |
|------|-------------------|----------------------|------------|
| `admin` | `None` | `None` (bypass) | All tenants |
| `operator` | `tenant_id` | `tenant_id` | Own tenant only |
| `auditor` | `None` | Raises 403 | All tenants (read-only) |

#### Query Filtering Example

```python
# In batch_service.py
async def list_batches(
    tenant_id: UUID | None = Depends(get_tenant_id),
    ...
):
    query = select(BatchORM)
    if tenant_id is not None:  # Filter for operators
        query = query.where(BatchORM.tenant_id == tenant_id)
    # If tenant_id is None (admin/auditor), return all batches
    result = await db.execute(query)
    return result.scalars().all()
```

### Admin Routes

All admin routes are under `/api/v1/admin/*` and protected with `require_role("admin")`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/admin/tenants` | List all tenants |
| `POST` | `/api/v1/admin/tenants` | Create a new tenant |
| `GET` | `/api/v1/admin/tenants/{id}` | Get tenant details |
| `PATCH` | `/api/v1/admin/tenants/{id}` | Update tenant |
| `GET` | `/api/v1/admin/tenants/{id}/users` | List tenant users |
| `POST` | `/api/v1/admin/tenants/{id}/users` | Invite user to tenant |
| `DELETE` | `/api/v1/admin/tenants/{id}/users/{uid}` | Remove user from tenant |
| `GET` | `/api/v1/admin/audit-logs` | List audit logs |

### Test Credentials

| User | Email | Password | Role | Tenant |
|------|-------|----------|------|--------|
| Admin | admin@h2v-trust.com | admin123 | admin | Default Platform |
| Operator | operator@produtor-alfa.com | operator123 | operator | Produtor Alfa Ltda |
| Auditor | auditor@h2v-trust.com | auditor123 | auditor | Cross-tenant |

### Security Audit Results (5/11/2026)

| # | Finding | Severity | Status |
|---|---------|----------|--------|
| 1 | `certificates.py` filter `tenant_id == None` returned no results for auditors | 🔴 Medium | ✅ Fixed |
| 2 | Legacy routes (`/batches`, `/certificates`) use API Key only, no JWT | 🟡 Low | ⏳ Backlog |
| 3 | API Key → JWT fallback maps without DB tenant validation | 🟡 Low | ⏳ Backlog |
| 4 | Admin routes protected with `require_role("admin")` | ✅ OK | Verified |

### Additional Security Measures

- API rate limiting for DDoS protection
- Blockchain-based certificate immutability
- Wallet-based authentication for sensitive operations
- Input validation and sanitization
- CORS configuration for frontend access

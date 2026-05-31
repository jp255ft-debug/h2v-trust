"""
Authentication and tenant isolation via API key → tenant binding.

Each API key is mapped to a role and tenant. This ensures that:
- The tenant identity is derived from a server-validated credential
- Clients cannot impersonate other tenants by manipulating headers
- The X-Tenant-Id header from the client is IGNORED for authorization
- Auditors have cross-tenant read access (role="auditor")
- Producers have single-tenant access (role="producer")
"""

import logging
from fastapi import HTTPException, Header, status
from config import settings

logger = logging.getLogger(__name__)

# Mapeamento de API keys para {role, tenant_id}.
# Em produção, isso viria de um banco de dados ou serviço de auth.
# Formato: { "api_key": {"role": str, "tenant_id": str} }
# Roles disponíveis: "producer" (acesso ao próprio tenant), "auditor" (cross-tenant)
TENANT_API_KEYS: dict[str, dict] = {
    # Chave padrão de desenvolvimento → tenant "default"
    settings.SECRET_KEY: {"role": "producer", "tenant_id": "default"},
    # Chaves específicas por tenant (para testes de isolamento)
    "key-produtor-alfa-123": {"role": "producer", "tenant_id": "produtor-alfa"},
    "key-produtor-beta-456": {"role": "producer", "tenant_id": "produtor-beta"},
    # Chave de auditor: acesso cross-tenant (NÃO filtra por tenant_id)
    "key-auditor-global-789": {"role": "auditor", "tenant_id": "auditor"},
}


def verify_api_key(api_key: str = Header(..., alias="X-API-Key")) -> dict:
    """
    Verify API key and return the associated role and tenant_id.

    The tenant_id is derived from the API key, NOT from any client-supplied header.
    This prevents tenant impersonation attacks.

    Args:
        api_key: The API key from the X-API-Key header.

    Returns:
        A dict with "role" (str) and "tenant_id" (str).

    Raises:
        HTTPException 401: If the API key is invalid.
    """
    info = TENANT_API_KEYS.get(api_key)
    if not info:
        logger.warning(
            "Authentication FAILED: invalid API key "
            f"(masked: {api_key[:8] if len(api_key) >= 8 else '****'}...)"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    logger.info(
        f"Authentication SUCCESS: role={info['role']}, "
        f"tenant={info['tenant_id']} "
        f"(key masked: {api_key[:8]}...)"
    )
    return info

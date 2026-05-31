import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.dependencies.tenant import get_tenant_id
from services.delegation_service import DelegationService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/delegation", tags=["delegation"])


@router.post("/authorize")
async def delegate_cbam_declarant(
    producer_id: str = Query(..., description="ID do produtor"),
    declarant_wallet: str = Query(..., description="Carteira do declarante (0x...)"),
    valid_until: str = Query(None, description="Data de validade (ISO 8601)"),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
):
    """Autorizar um declarante CBAM."""
    service = DelegationService(db)
    delegation = await service.create_delegation(producer_id, declarant_wallet, valid_until, tenant_id=tenant_id)
    return delegation


@router.get("/status/{producer_id}")
async def get_delegation_status(
    producer_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
):
    """Listar todas as delegações de um produtor."""
    service = DelegationService(db)
    delegations = service.get_delegations(producer_id, tenant_id=tenant_id)
    return delegations


@router.post("/revoke")
async def revoke_delegation(
    producer_id: str = Query(..., description="ID do produtor"),
    declarant_wallet: str = Query(None, description="Carteira do declarante (opcional)"),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
):
    """Revogar delegação(ões) de um produtor."""
    service = DelegationService(db)
    result = await service.revoke_delegation(producer_id, declarant_wallet, tenant_id=tenant_id)
    return result

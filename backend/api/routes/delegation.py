import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies.auth import verify_api_key
from api.dependencies.db import get_db
from services.delegation_service import DelegationService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/delegation", tags=["delegation"])


@router.post("/authorize")
async def delegate_cbam_declarant(
    producer_id: str,
    declarant_address: str,
    valid_until: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    service = DelegationService(db)
    delegation = await service.create_delegation(producer_id, declarant_address, valid_until)
    return delegation


@router.get("/status/{producer_id}")
async def get_delegation_status(
    producer_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    service = DelegationService(db)
    status = service.get_active_delegation(producer_id)
    return status


@router.post("/revoke")
async def revoke_delegation(
    producer_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    service = DelegationService(db)
    result = await service.revoke_delegation(producer_id)
    return result

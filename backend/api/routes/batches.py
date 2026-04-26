import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.dependencies.auth import verify_api_key
from api.dependencies.db import get_db
from services.batch_service import BatchService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/batches", tags=["batches"])


@router.get("")
async def list_batches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    producer_id: str = Query(None),
    compliant_only: bool = Query(False),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    service = BatchService(db)
    batches = service.get_batches(skip, limit, producer_id, compliant_only)
    return {"batches": batches, "total": len(batches)}


@router.get("/{batch_id}")
async def get_batch(
    batch_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    service = BatchService(db)
    batch = service.get_batch_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch


@router.get("/{batch_id}/compliance")
async def get_batch_compliance(
    batch_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    service = BatchService(db)
    compliance = service.get_compliance_report(batch_id)
    if not compliance:
        raise HTTPException(status_code=404, detail="Compliance report not found")
    return compliance

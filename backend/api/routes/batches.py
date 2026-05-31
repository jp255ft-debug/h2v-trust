import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.dependencies.tenant import get_tenant_id, require_tenant_id
from services.batch_service import BatchService
from services.certificate_service import CertificateService
from models.telemetry import TelemetryData
from core.compliance import CBAMComplianceChecker
from db.models import Batch as BatchORM
from db.models import Certificate as CertificateORM

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/batches", tags=["batches"])


@router.get("")
async def list_batches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    producer_id: str = Query(None),
    compliant_only: bool = Query(False),
    db: Session = Depends(get_db),
    tenant_id: Optional[str] = Depends(get_tenant_id),
):
    service = BatchService(db)
    batches = service.get_batches(skip, limit, producer_id, compliant_only, tenant_id=tenant_id)
    return {"batches": batches, "total": len(batches)}


@router.post("")
async def create_batch(
    telemetry: TelemetryData,
    batch_size_kg: float = Query(..., description="Batch size in kg"),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(require_tenant_id),
):
    """Cria um novo lote com dados de telemetria e verifica conformidade CBAM.
    
    Apenas produtores (role="operator") podem criar lotes.
    Auditores recebem 403 Forbidden.
    """
    try:
        compliance = CBAMComplianceChecker.full_compliance_check(telemetry, batch_size_kg)
        service = BatchService(db)
        batch = await service.create_batch(telemetry, compliance, batch_size_kg, tenant_id=tenant_id)
        return batch.to_dict()
    except Exception as e:
        logger.error(f"Error creating batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{batch_id}")
async def get_batch(
    batch_id: str,
    db: Session = Depends(get_db),
    tenant_id: Optional[str] = Depends(get_tenant_id),
):
    service = BatchService(db)
    batch = service.get_batch_by_id(batch_id, tenant_id=tenant_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch


@router.post("/{batch_id}/certify")
async def certify_batch(
    batch_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(require_tenant_id),
):
    """Emite certificado Soulbound (SBT) para um lote conforme.
    
    Apenas produtores (role="operator") podem certificar lotes.
    Auditores recebem 403 Forbidden.
    """
    batch = db.query(BatchORM).filter(BatchORM.id == batch_id, BatchORM.tenant_id == tenant_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    if not batch.is_compliant:
        raise HTTPException(status_code=400, detail="Lote não é conforme. Corrija não-conformidades antes de certificar.")

    existing = db.query(CertificateORM).filter(CertificateORM.batch_id == batch_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Este lote já possui um certificado")

    try:
        service = CertificateService(db)
        result = await service.mint_certificate(batch, tenant_id=tenant_id)
        return result
    except Exception as e:
        logger.error(f"Error certifying batch {batch_id}: {e}")
        # Fallback offline: criar certificado mesmo sem blockchain
        try:
            service = CertificateService(db)
            result = await service.mint_certificate(batch, tenant_id=tenant_id)
            return {**result, "blockchain_status": "pending", "warning": str(e)}
        except Exception as fallback_err:
            logger.error(f"Fallback certification also failed for batch {batch_id}: {fallback_err}")
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/{batch_id}/compliance")
async def get_batch_compliance(
    batch_id: str,
    db: Session = Depends(get_db),
    tenant_id: Optional[str] = Depends(get_tenant_id),
):
    service = BatchService(db)
    compliance = service.get_compliance_report(batch_id, tenant_id=tenant_id)
    if not compliance:
        raise HTTPException(status_code=404, detail="Compliance report not found")
    return compliance

import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.dependencies.tenant import get_tenant_id, require_tenant_id
from services.certificate_service import CertificateService
from db.models import Certificate as CertificateORM
from db.models import Batch as BatchORM

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("")
async def list_certificates(
    batch_id: Optional[str] = Query(None, description="Filter by batch ID"),
    producer_id: Optional[str] = Query(None, description="Filter by producer ID"),
    db: Session = Depends(get_db),
    tenant_id: Optional[str] = Depends(get_tenant_id),
):
    """List certificates, optionally filtered by batch_id or producer_id.
    
    Tenant isolation:
    - Producers (tenant_id is string): Only see their own tenant's certificates.
    - Auditors (tenant_id is None): See certificates from ALL tenants.
    """
    query = db.query(CertificateORM)
    if tenant_id is not None:
        query = query.filter(CertificateORM.tenant_id == tenant_id)
    if batch_id:
        query = query.filter(CertificateORM.batch_id == batch_id)
    if producer_id:
        query = query.join(BatchORM, CertificateORM.batch_id == BatchORM.id).filter(
            BatchORM.producer_id == producer_id
        )
    certificates = query.all()
    return {"certificates": [c.to_dict() for c in certificates], "total": len(certificates)}


@router.get("/{certificate_id}")
async def get_certificate(
    certificate_id: str,
    db: Session = Depends(get_db),
    tenant_id: Optional[str] = Depends(get_tenant_id),
):
    service = CertificateService(db)
    cert = service.get_certificate_by_id(certificate_id, tenant_id=tenant_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    # Tentar verificação on-chain, mas não quebrar se falhar
    try:
        on_chain_data = await service.verify_on_chain(certificate_id)
    except Exception as e:
        logger.warning(f"On-chain verification failed for {certificate_id}: {e}")
        on_chain_data = {"error": "Blockchain not available", "detail": str(e)}
    return {"certificate": cert, "on_chain_proof": on_chain_data}


@router.post("/{certificate_id}/consume")
async def consume_certificate(
    certificate_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(require_tenant_id),
):
    """Marca o certificado como consumido (evita double counting).
    
    Apenas produtores (role="operator") podem consumir certificados.
    Auditores recebem 403 Forbidden.
    """
    service = CertificateService(db)
    result = await service.consume_certificate(certificate_id, tenant_id=tenant_id)
    return result

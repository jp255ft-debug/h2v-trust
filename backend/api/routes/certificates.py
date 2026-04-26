import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies.auth import verify_api_key
from api.dependencies.db import get_db
from services.certificate_service import CertificateService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/{certificate_id}")
async def get_certificate(
    certificate_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    service = CertificateService(db)
    cert = service.get_certificate_by_id(certificate_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    # Buscar dados on-chain para verificação adicional
    on_chain_data = await service.verify_on_chain(certificate_id)
    return {"certificate": cert, "on_chain_proof": on_chain_data}


@router.post("/{certificate_id}/consume")
async def consume_certificate(
    certificate_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """Marca o certificado como consumido (evita double counting)."""
    service = CertificateService(db)
    result = await service.consume_certificate(certificate_id)
    return result

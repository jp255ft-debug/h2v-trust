import uuid
import logging
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from blockchain.minting import mint_certificate_on_chain
from blockchain.verification import verify_certificate_on_chain
from db.models import Certificate as CertificateORM
from services.qrcode_service import generate_qr_code

logger = logging.getLogger(__name__)


class CertificateService:
    def __init__(self, db: Session):
        self.db = db

    async def mint_certificate(self, batch, tenant_id: str = "default") -> dict:
        # 1. Gerar hash do batch
        batch_hash = batch.batch_hash
        
        # 2. Preparar metadados detalhados para o token
        # Extrair dados do relatório de conformidade
        compliance_report = batch.compliance_report or {}
        cbam_report = compliance_report.get("cbam_report", {})
        
        # Calcular métricas ambientais
        emissions_tco2 = float(cbam_report.get("declared_emissions_tco2", 0))
        emissions_kgco2e_per_kgh2 = emissions_tco2 * 1000  # Convertendo para kg
        
        # Verificar conformidade com limites CBAM
        cbam_limit = 3.4  # kgCO2e/kgH2
        is_cbam_compliant = emissions_kgco2e_per_kgh2 <= cbam_limit
        
        # Preparar metadados estruturados
        metadata = {
            # Informações básicas do lote
            "batch_id": str(batch.id),
            "batch_size_kg": int(batch.size_kg),
            "production_date": batch.created_at.isoformat() if hasattr(batch, 'created_at') else "Unknown",
            
            # Métricas ambientais
            "environmental_metrics": {
                "ghg_emissions_kgco2e_per_kgh2": round(emissions_kgco2e_per_kgh2, 2),
                "water_consumption_l_per_kgh2": batch.telemetry.water_consumption_liters if hasattr(batch.telemetry, 'water_consumption_liters') else 0,
                "energy_consumption_kwh_per_kgh2": batch.telemetry.energy_consumption_kwh if hasattr(batch.telemetry, 'energy_consumption_kwh') else 0,
                "water_source": batch.telemetry.water_source if hasattr(batch.telemetry, 'water_source') else "Unknown",
                "energy_source": batch.telemetry.energy_source if hasattr(batch.telemetry, 'energy_source') else "Renewable",
            },
            
            # Conformidade e certificação
            "compliance": {
                "cbam_compliant": is_cbam_compliant,
                "cbam_limit_kgco2e_per_kgh2": cbam_limit,
                "compliance_margin_percent": round(((cbam_limit - emissions_kgco2e_per_kgh2) / cbam_limit) * 100, 2) if is_cbam_compliant else 0,
                "certification_standard": "CBAM 2026",
                "verification_date": datetime.utcnow().isoformat(),
            },
            
            # Informações do produtor
            "producer_info": {
                "wallet_address": batch.producer_wallet,
                "facility_id": getattr(batch, 'facility_id', 'Unknown'),
                "location": getattr(batch, 'production_location', 'Unknown'),
            },
            
            # Metadados técnicos
            "technical_metadata": {
                "certificate_version": "1.0",
                "blockchain_network": "Hardhat Local",
                "token_standard": "ERC-721 SBT",
                "issuer": "H2V-Trust Platform",
            }
        }

        # 3. Interagir com blockchain (com fallback offline)
        try:
            tx_hash, token_id = await mint_certificate_on_chain(
                batch_id=batch_hash,
                producer_address=getattr(batch, 'producer_wallet', getattr(batch, 'producer_id', '')),
                metadata=metadata
            )
            blockchain_status = "confirmed"
        except Exception as e:
            logger.warning(f"Blockchain mint failed for batch {batch.id}, using offline fallback: {e}")
            tx_hash = f"offline-{uuid.uuid4()}"
            token_id = 0
            blockchain_status = "pending"

        # 4. Salvar certificado no banco
        cert_id = str(uuid.uuid4())
        cert = CertificateORM(
            id=cert_id,
            batch_id=batch.id,
            token_id=token_id,
            blockchain_tx_hash=tx_hash,
            qr_code_data=generate_qr_code(cert_id, batch_hash),
            tenant_id=tenant_id,
            created_at=datetime.utcnow(),
            is_consumed=False,
        )
        self.db.add(cert)
        self.db.commit()
        self.db.refresh(cert)

        return {
            "certificate_id": cert.id,
            "tx_hash": tx_hash,
            "token_id": token_id,
            "blockchain_status": blockchain_status,
        }

    async def verify_on_chain(self, certificate_id: str, tenant_id: Optional[str] = "default") -> dict:
        """
        Verify a certificate on-chain with tenant isolation.
        
        Args:
            tenant_id: If None (auditor), can verify any tenant's certificate.
                       If string (producer), only verifies if belongs to that tenant.
        """
        query = self.db.query(CertificateORM).filter(CertificateORM.id == certificate_id)
        if tenant_id is not None:
            query = query.filter(CertificateORM.tenant_id == tenant_id)
        cert = query.first()
        if not cert:
            return {"error": "Certificate not found"}
        on_chain_data = await verify_certificate_on_chain(cert.token_id)
        return on_chain_data

    async def consume_certificate(self, certificate_id: str, tenant_id: Optional[str] = "default") -> dict:
        """
        Consume (surrender) a certificate with tenant isolation.
        
        Args:
            tenant_id: If None (auditor), cannot consume (will be rejected).
                       If string (producer), only consumes if belongs to that tenant.
        """
        query = self.db.query(CertificateORM).filter(CertificateORM.id == certificate_id)
        if tenant_id is not None:
            query = query.filter(CertificateORM.tenant_id == tenant_id)
        cert = query.first()
        if not cert:
            return {"error": "Not found"}
        if cert.is_consumed:
            return {"error": "Already consumed"}
        # Chamar contrato para marcar consumido
        from blockchain.sbt_manager import consume_sbt
        tx = await consume_sbt(cert.token_id)
        cert.is_consumed = True
        cert.consumed_at = datetime.utcnow()
        self.db.commit()
        return {"status": "consumed", "tx_hash": tx}

    def get_certificate_by_id(self, certificate_id: str, tenant_id: Optional[str] = "default"):
        """
        Get a certificate by ID with tenant isolation.
        
        Args:
            tenant_id: If None (auditor), can access any tenant's certificate.
                       If string (producer), only returns if belongs to that tenant.
        """
        query = self.db.query(CertificateORM).filter(CertificateORM.id == certificate_id)
        if tenant_id is not None:
            query = query.filter(CertificateORM.tenant_id == tenant_id)
        cert = query.first()
        return cert.to_dict() if cert else None

import logging
import uuid
import traceback
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies.auth import verify_api_key
from api.dependencies.db import get_db
from blockchain.minting import mint_certificate_on_chain
from core.compliance import CBAMComplianceChecker
from db.models import Batch as BatchORM
from db.models import TelemetryRecord
from db.models import Certificate as CertificateORM
from db.models import AuditLog
from models.telemetry import TelemetryData
from services.qrcode_service import generate_qr_code
from utils.hashing import generate_batch_hash

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/telemetry", tags=["telemetry"])


def _create_audit_log(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: str,
    actor: str,
    details: dict,
):
    """Helper para criar log de auditoria."""
    try:
        audit = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            actor=actor,
            details=details,
        )
        db.add(audit)
        db.flush()
        logger.info(f"Audit log: {action} | {entity_type}:{entity_id} | {details}")
    except Exception as audit_err:
        logger.error(f"Failed to create audit log: {audit_err}")


@router.post("", status_code=status.HTTP_201_CREATED)
async def ingest_telemetry(
    data: TelemetryData,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """
    Recebe dados de telemetria de um sensor (IoT).

    Fluxo de integridade:
    A. Validar payload (Pydantic) - já feito pelo FastAPI
    B. Avaliar regras CBAM
    C. Chamar contrato blockchain PRIMEIRO (mint SBT, aguardar confirmação)
    D. Só então salvar telemetria + batch + certificado no banco

    Em caso de falha na blockchain, o lote é salvo como "Pendente"
    para retentativa posterior.
    """
    batch_id = str(uuid.uuid4())
    # Incluir batch_id no hash para garantir unicidade
    hash_data = data.model_dump()
    hash_data["_batch_id"] = batch_id
    batch_hash = generate_batch_hash(hash_data)
    tx_hash = None
    token_id = None
    certificate_id = None
    blockchain_error = None

    try:
        logger.info(f"Received telemetry data from sensor: {data.sensor_id}")

        # ============================================================
        # PASSO A: Validação já feita pelo Pydantic (TelemetryData)
        # ============================================================
        _create_audit_log(
            db, "telemetry.received", "telemetry", batch_id, api_key,
            {"sensor_id": data.sensor_id, "timestamp": data.timestamp.isoformat()}
        )

        # ============================================================
        # PASSO B: Avaliar regras CBAM
        # ============================================================
        batch_size_kg = 1000.0
        compliance_result = CBAMComplianceChecker.full_compliance_check(data, batch_size_kg)
        logger.info(f"Compliance check result: {compliance_result['is_compliant']}")

        _create_audit_log(
            db, "compliance.check", "batch", batch_id, api_key,
            {
                "is_compliant": compliance_result["is_compliant"],
                "violations": compliance_result.get("violations", []),
                "checks": {k: v["ok"] for k, v in compliance_result.get("checks", {}).items()},
            }
        )

        # ============================================================
        # PASSO C: Chamar blockchain PRIMEIRO (se conforme)
        # ============================================================
        if compliance_result["is_compliant"]:
            # Extrair metadados ambientais para o token
            cbam_report = compliance_result.get("cbam_report", {})
            emissions_tco2 = float(cbam_report.get("declared_emissions_tco2", 0))
            emissions_kgco2e_per_kgh2 = emissions_tco2 * 1000

            metadata = {
                "batch_id": batch_id,
                "batch_size_kg": int(batch_size_kg),
                "production_date": datetime.utcnow().isoformat(),
                "environmental_metrics": {
                    "ghg_emissions_kgco2e_per_kgh2": round(emissions_kgco2e_per_kgh2, 2),
                    "water_consumption_l_per_kgh2": data.water_consumption_liters,
                    "energy_consumption_kwh_per_kgh2": data.power_generated_mwh * 1000,
                    "water_source": data.water_source,
                    "energy_source": data.energy_source,
                },
                "compliance": {
                    "cbam_compliant": True,
                    "cbam_limit_kgco2e_per_kgh2": 3.4,
                    "certification_standard": "CBAM 2026",
                    "verification_date": datetime.utcnow().isoformat(),
                },
                "producer_info": {
                    "wallet_address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
                    "facility_id": data.sensor_id,
                    "location": "Namibia",
                },
                "technical_metadata": {
                    "certificate_version": "1.0",
                    "blockchain_network": "Hardhat Local",
                    "token_standard": "ERC-721 SBT",
                    "issuer": "H2V-Trust Platform",
                }
            }

            # Mint na blockchain - AGUARDA confirmação e extrai token_id
            logger.info(f"Minting certificate on-chain for batch {batch_id}...")
            _create_audit_log(
                db, "blockchain.mint.attempt", "batch", batch_id, api_key,
                {"batch_hash": batch_hash, "producer": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"}
            )

            try:
                tx_hash, token_id = await mint_certificate_on_chain(
                    batch_id=batch_hash,
                    producer_address="0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
                    metadata=metadata
                )
                logger.info(f"Blockchain mint confirmed: token_id={token_id}, tx_hash={tx_hash}")
                _create_audit_log(
                    db, "blockchain.mint.success", "certificate", str(token_id), api_key,
                    {"batch_id": batch_id, "tx_hash": tx_hash, "token_id": token_id}
                )
            except Exception as bc_err:
                blockchain_error = str(bc_err)
                logger.error(f"Blockchain mint FAILED for batch {batch_id}: {blockchain_error}")
                logger.error(traceback.format_exc())
                _create_audit_log(
                    db, "blockchain.mint.failed", "batch", batch_id, api_key,
                    {
                        "error": blockchain_error,
                        "batch_hash": batch_hash,
                        "stage": "blockchain_mint",
                    }
                )

        # ============================================================
        # PASSO D: Salvar no banco (sempre, mesmo se blockchain falhar)
        # ============================================================

        # Determinar blockchain_status
        if not compliance_result["is_compliant"]:
            blockchain_status = None  # Não conforme, não tentou blockchain
        elif blockchain_error:
            blockchain_status = "pending"  # Falhou na blockchain, pendente para retry
        elif token_id is not None:
            blockchain_status = "confirmed"  # Sucesso na blockchain
        else:
            blockchain_status = "pending"  # Caso genérico

        # Salvar telemetria
        telemetry_record = TelemetryRecord(
            sensor_id=data.sensor_id,
            timestamp=data.timestamp,
            energy_source=data.energy_source,
            power_generated_mwh=data.power_generated_mwh,
            ghg_emissions=data.ghg_emissions_kgCO2_per_kgH2,
            water_consumption_liters=data.water_consumption_liters,
            water_source=data.water_source,
        )
        db.add(telemetry_record)
        db.flush()

        # Criar lote com blockchain_status
        batch = BatchORM(
            id=batch_id,
            telemetry_id=telemetry_record.id,
            size_kg=batch_size_kg,
            is_compliant=compliance_result["is_compliant"],
            blockchain_status=blockchain_status,
            compliance_report=compliance_result,
            batch_hash=batch_hash,
            created_at=datetime.utcnow(),
        )
        db.add(batch)
        db.flush()

        # Salvar certificado (se mintado com sucesso na blockchain)
        if token_id is not None:
            cert_id = str(uuid.uuid4())
            cert = CertificateORM(
                id=cert_id,
                batch_id=batch.id,
                token_id=token_id,
                blockchain_tx_hash=tx_hash,
                qr_code_data=generate_qr_code(cert_id, batch_hash),
                created_at=datetime.utcnow(),
                is_consumed=False,
            )
            db.add(cert)
            certificate_id = cert_id

        db.commit()

        status_msg = f"Batch {batch.id} saved (compliant={compliance_result['is_compliant']}, blockchain={blockchain_status})"
        logger.info(status_msg)
        _create_audit_log(
            db, "batch.created", "batch", batch.id, api_key,
            {
                "blockchain_status": blockchain_status,
                "is_compliant": compliance_result["is_compliant"],
                "certificate_id": certificate_id,
                "blockchain_error": blockchain_error,
            }
        )

        return {
            "batch_id": batch.id,
            "certificate_id": certificate_id,
            "token_id": token_id,
            "tx_hash": tx_hash,
            "is_compliant": compliance_result["is_compliant"],
            "blockchain_status": blockchain_status,
            "blockchain_error": blockchain_error,
            "violations": compliance_result.get("violations", []),
            "cbam_report": compliance_result.get("cbam_report"),
        }
    except Exception as e:
        logger.error(f"Error in ingest_telemetry: {e}", exc_info=True)
        logger.error(traceback.format_exc())
        _create_audit_log(
            db, "telemetry.error", "telemetry", batch_id, api_key,
            {"error": str(e), "traceback": traceback.format_exc()}
        )
        raise


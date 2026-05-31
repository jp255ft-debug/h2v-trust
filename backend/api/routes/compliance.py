import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.dependencies.tenant import get_tenant_id
from core.compliance import CBAMComplianceChecker
from services.batch_service import BatchService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.get("/check/{batch_id}")
async def check_batch_compliance(
    batch_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
):
    """
    Reavalia compliance de um lote específico.
    Produtores: só podem verificar seus próprios lotes.
    Auditores: podem verificar qualquer lote (cross-tenant).
    """
    service = BatchService(db)
    batch = service.get_batch_by_id(batch_id, tenant_id=tenant_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Reavalia compliance (útil para auditoria)
    # batch é um dicionário (to_dict()), precisamos criar TelemetryData
    from models.telemetry import TelemetryData
    from datetime import datetime, timezone
    
    if not batch.get("telemetry"):
        raise HTTPException(status_code=400, detail="Batch has no telemetry data")
    
    telemetry_data = batch["telemetry"]
    # Converter timestamp string para datetime se necessário
    timestamp = telemetry_data.get("timestamp")
    if timestamp and isinstance(timestamp, str):
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            timestamp = datetime.now(timezone.utc)
    else:
        timestamp = datetime.now(timezone.utc)
    
    telemetry = TelemetryData(
        sensor_id=telemetry_data.get("sensor_id", "unknown"),
        timestamp=timestamp,
        energy_source=telemetry_data.get("energy_source", "unknown"),
        power_generated_mwh=0.0,  # Não disponível no batch.to_dict()
        ghg_emissions_kgCO2_per_kgH2=telemetry_data.get("ghg_emissions", 0.0),
        water_consumption_liters=telemetry_data.get("water_consumption_liters", 0.0),
        water_source=telemetry_data.get("water_source", "unknown"),
    )
    
    compliance = CBAMComplianceChecker.full_compliance_check(telemetry, batch["size_kg"])
    return compliance


@router.post("/validate")
async def validate_against_cbam(
    emissions_kgco2_per_kgh2: float,
    energy_source: str,
    water_source: str,
    water_liters_per_kg: float,
    tenant_id: str = Depends(get_tenant_id),
):
    """Endpoint simples para testar conformidade sem criar lote."""
    from models.telemetry import TelemetryData
    from datetime import datetime, timezone

    mock_telemetry = TelemetryData(
        sensor_id="test",
        timestamp=datetime.now(timezone.utc),
        energy_source=energy_source,
        power_generated_mwh=0,
        ghg_emissions_kgCO2_per_kgH2=emissions_kgco2_per_kgh2,
        water_consumption_liters=water_liters_per_kg,
        water_source=water_source,
    )
    result = CBAMComplianceChecker.full_compliance_check(mock_telemetry, h2_kg=1.0)
    return result

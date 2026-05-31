import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session, joinedload

from db.models import Batch as BatchORM
from db.models import TelemetryRecord
from models.telemetry import TelemetryData
from utils.hashing import generate_batch_hash


class BatchService:
    def __init__(self, db: Session):
        self.db = db

    async def create_batch(self, telemetry: TelemetryData, compliance: Dict, batch_size_kg: float, tenant_id: str = "default") -> BatchORM:
        batch_id = str(uuid.uuid4())
        batch_hash = generate_batch_hash(telemetry.dict())

        # Salvar telemetria
        telemetry_record = TelemetryRecord(
            sensor_id=telemetry.sensor_id,
            timestamp=telemetry.timestamp,
            energy_source=telemetry.energy_source,
            power_generated_mwh=telemetry.power_generated_mwh,
            ghg_emissions=telemetry.ghg_emissions_kgCO2_per_kgH2,
            water_consumption_liters=telemetry.water_consumption_liters,
            water_source=telemetry.water_source,
        )
        self.db.add(telemetry_record)
        self.db.flush()

        # Criar lote
        batch = BatchORM(
            id=batch_id,
            telemetry_id=telemetry_record.id,
            size_kg=batch_size_kg,
            is_compliant=compliance["is_compliant"],
            compliance_report=compliance,
            batch_hash=batch_hash,
            tenant_id=tenant_id,
            created_at=datetime.utcnow(),
        )
        self.db.add(batch)
        self.db.commit()
        self.db.refresh(batch)
        return batch

    def get_batches(self, skip: int, limit: int, producer_id: Optional[str], compliant_only: bool, tenant_id: Optional[str] = "default") -> List[Dict]:
        """
        List batches with optional tenant isolation.
        
        Args:
            tenant_id: If None (auditor), returns batches from ALL tenants.
                       If string (producer), returns only that tenant's batches.
        """
        query = self.db.query(BatchORM).options(joinedload(BatchORM.telemetry))
        
        # Apenas filtra por tenant se tenant_id não for None (auditor vê tudo)
        if tenant_id is not None:
            query = query.filter(BatchORM.tenant_id == tenant_id)
        
        if producer_id:
            query = query.filter(BatchORM.producer_id == producer_id)
        if compliant_only:
            query = query.filter(BatchORM.is_compliant == True)
        batches = query.offset(skip).limit(limit).all()
        return [b.to_dict() for b in batches]

    def get_batch_by_id(self, batch_id: str, tenant_id: Optional[str] = "default") -> Optional[Dict]:
        """
        Get a single batch by ID with tenant isolation.
        
        Args:
            tenant_id: If None (auditor), can access any tenant's batch.
                       If string (producer), only returns if batch belongs to that tenant.
        """
        query = self.db.query(BatchORM).options(joinedload(BatchORM.telemetry)).filter(
            BatchORM.id == batch_id
        )
        
        # Apenas filtra por tenant se tenant_id não for None
        if tenant_id is not None:
            query = query.filter(BatchORM.tenant_id == tenant_id)
        
        batch = query.first()
        return batch.to_dict() if batch else None

    def get_compliance_report(self, batch_id: str, tenant_id: Optional[str] = "default") -> Optional[Dict]:
        """
        Get compliance report for a batch with tenant isolation.
        
        Args:
            tenant_id: If None (auditor), can access any tenant's report.
                       If string (producer), only returns if batch belongs to that tenant.
        """
        query = self.db.query(BatchORM).filter(BatchORM.id == batch_id)
        
        # Apenas filtra por tenant se tenant_id não for None
        if tenant_id is not None:
            query = query.filter(BatchORM.tenant_id == tenant_id)
        
        batch = query.first()
        return batch.compliance_report if batch else None

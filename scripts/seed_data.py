#!/usr/bin/env python3
"""
Seed database with test data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.db.database import SessionLocal, engine, Base
from backend.db.models import TelemetryRecord, Batch, Certificate, Delegation, AuditLog

def seed_database():
    """Seed the database with test data."""
    print("Seeding database with test data...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Certificate).delete()
        db.query(Batch).delete()
        db.query(TelemetryRecord).delete()
        db.query(Delegation).delete()
        db.query(AuditLog).delete()
        db.commit()
        
        # Create telemetry records
        telemetry1 = TelemetryRecord(
            sensor_id="sensor_001",
            timestamp=datetime.utcnow() - timedelta(days=2),
            energy_source="solar",
            power_generated_mwh=10.5,
            ghg_emissions=2.8,
            water_consumption_liters=1500,
            water_source="recycled"
        )
        
        telemetry2 = TelemetryRecord(
            sensor_id="sensor_002",
            timestamp=datetime.utcnow() - timedelta(days=1),
            energy_source="wind",
            power_generated_mwh=8.2,
            ghg_emissions=1.5,
            water_consumption_liters=1200,
            water_source="desalinated"
        )
        
        telemetry3 = TelemetryRecord(
            sensor_id="sensor_003",
            timestamp=datetime.utcnow(),
            energy_source="hydro",
            power_generated_mwh=15.0,
            ghg_emissions=0.8,
            water_consumption_liters=1800,
            water_source="river"
        )
        
        db.add_all([telemetry1, telemetry2, telemetry3])
        db.flush()
        
        # Create batches
        batch1 = Batch(
            id="batch_001",
            telemetry_id=telemetry1.id,
            size_kg=1000.0,
            is_compliant=True,
            compliance_report={
                "is_compliant": True,
                "ghg_emissions_tco2_per_th2": 2.8,
                "water_consumption_m3_per_kg": 1.5,
                "energy_source_score": 95,
                "certification_standard": "CBAM",
                "verification_date": (datetime.utcnow() - timedelta(days=1)).isoformat()
            },
            batch_hash="abc123",
            producer_wallet="0x1234567890123456789012345678901234567890"
        )
        
        batch2 = Batch(
            id="batch_002",
            telemetry_id=telemetry2.id,
            size_kg=800.0,
            is_compliant=True,
            compliance_report={
                "is_compliant": True,
                "ghg_emissions_tco2_per_th2": 1.5,
                "water_consumption_m3_per_kg": 1.2,
                "energy_source_score": 98,
                "certification_standard": "CBAM",
                "verification_date": datetime.utcnow().isoformat()
            },
            batch_hash="def456",
            producer_wallet="0x2345678901234567890123456789012345678901"
        )
        
        batch3 = Batch(
            id="batch_003",
            telemetry_id=telemetry3.id,
            size_kg=1200.0,
            is_compliant=False,
            compliance_report={
                "is_compliant": False,
                "ghg_emissions_tco2_per_th2": 4.2,
                "water_consumption_m3_per_kg": 2.1,
                "energy_source_score": 65,
                "certification_standard": "CBAM",
                "verification_date": datetime.utcnow().isoformat(),
                "non_compliance_reason": "GHG emissions exceed CBAM limit"
            },
            batch_hash="ghi789",
            producer_wallet="0x3456789012345678901234567890123456789012"
        )
        
        db.add_all([batch1, batch2, batch3])
        db.flush()
        
        # Create certificates
        certificate1 = Certificate(
            id="cert_001",
            batch_id=batch1.id,
            token_id=1,
            blockchain_tx_hash="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            qr_code_data="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            is_consumed=False,
            consumed_at=None
        )
        
        certificate2 = Certificate(
            id="cert_002",
            batch_id=batch2.id,
            token_id=2,
            blockchain_tx_hash="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            qr_code_data="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            is_consumed=False,
            consumed_at=None
        )
        
        db.add_all([certificate1, certificate2])
        
        # Create delegations
        delegation1 = Delegation(
            producer_id="producer_001",
            declarant_address="0x4567890123456789012345678901234567890123",
            valid_until=datetime.utcnow() + timedelta(days=30),
            is_active=True
        )
        
        delegation2 = Delegation(
            producer_id="producer_002",
            declarant_address="0x5678901234567890123456789012345678901234",
            valid_until=datetime.utcnow() + timedelta(days=60),
            is_active=True
        )
        
        db.add_all([delegation1, delegation2])
        
        # Create audit logs
        audit_log1 = AuditLog(
            batch_id="batch_001",
            action="batch_created",
            actor="0x1234567890123456789012345678901234567890",
            details={"size_kg": 1000.0, "compliant": True}
        )
        
        audit_log2 = AuditLog(
            batch_id="batch_001",
            action="certificate_minted",
            actor="system",
            details={"token_id": 1, "batch_id": "batch_001"}
        )
        
        db.add_all([audit_log1, audit_log2])
        
        db.commit()
        print("Database seeded successfully!")
        print(f"Created: 3 telemetry records, 3 batches, 2 certificates, 2 delegations, 2 audit logs")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
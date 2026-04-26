import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models.telemetry import TelemetryData
from backend.core.compliance import CBAMComplianceChecker
from backend.services.batch_service import BatchService
from backend.services.certificate_service import CertificateService

async def test_full_flow():
    print("Testing full H2V-Trust flow (simulating API)...")
    print("=" * 60)
    
    # Create database session
    DATABASE_URL = "sqlite:///./h2v_trust.db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Create telemetry data (same as API would receive)
        telemetry_data = TelemetryData(
            sensor_id="test_sensor_api",
            timestamp=datetime.now().isoformat() + "Z",
            energy_source="wind",
            power_generated_mwh=12.5,
            ghg_emissions_kgCO2_per_kgH2=2.8,
            water_consumption_liters=150,
            water_source="desalination"
        )
        
        print("1. Telemetry data created")
        
        # 2. Check compliance (same as API)
        batch_size_kg = 1000.0
        compliance_result = CBAMComplianceChecker.full_compliance_check(telemetry_data, batch_size_kg)
        
        print(f"2. Compliance check: {compliance_result['is_compliant']}")
        
        # 3. Create batch (simulating BatchService)
        print("3. Creating batch...")
        batch_service = BatchService(db)
        
        try:
            batch = await batch_service.create_batch(
                telemetry=telemetry_data,
                compliance=compliance_result,
                batch_size_kg=batch_size_kg
            )
            print(f"   Batch created with ID: {batch.id}")
            
            # 4. If compliant, mint certificate
            if compliance_result["is_compliant"]:
                print("4. Minting certificate...")
                cert_service = CertificateService(db)
                
                try:
                    mint_result = await cert_service.mint_certificate(batch)
                    print(f"   Certificate minted!")
                    print(f"   Token ID: {mint_result.get('token_id')}")
                    print(f"   Transaction hash: {mint_result.get('tx_hash')}")
                    print(f"   Certificate ID: {mint_result.get('certificate_id')}")
                except Exception as e:
                    print(f"   ERROR minting certificate: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("4. Not compliant, skipping certificate minting")
                
        except Exception as e:
            print(f"   ERROR creating batch: {e}")
            import traceback
            traceback.print_exc()
            
    finally:
        db.close()
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_full_flow())
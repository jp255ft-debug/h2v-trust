#!/usr/bin/env python3
"""Test the ReportService fix."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models.batch import Batch
from backend.services.report_service import ReportService

def test_report_service():
    """Test the ReportService with the fixed line."""
    print("Testing ReportService with fixed line 22...")
    
    # Create in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    db = Session()
    
    # Create tables
    from backend.db.database import Base
    Base.metadata.create_all(engine)
    
    # Create test batches with different compliance_report scenarios
    test_batches = [
        # Batch 1: Normal compliance report
        Batch(
            id="batch_001",
            producer_wallet="0x123...",
            size_kg=1000.0,
            is_compliant=True,
            compliance_report={
                "cbam_report": {
                    "declared_emissions_tco2": 2.8
                }
            },
            created_at=datetime(2026, 1, 15)
        ),
        # Batch 2: Empty compliance report
        Batch(
            id="batch_002",
            producer_wallet="0x123...",
            size_kg=1500.0,
            is_compliant=False,
            compliance_report={},
            created_at=datetime(2026, 2, 20)
        ),
        # Batch 3: None compliance report (should work with fix)
        Batch(
            id="batch_003",
            producer_wallet="0x123...",
            size_kg=800.0,
            is_compliant=True,
            compliance_report=None,
            created_at=datetime(2026, 3, 10)
        ),
        # Batch 4: Compliance report without cbam_report key
        Batch(
            id="batch_004",
            producer_wallet="0x123...",
            size_kg=1200.0,
            is_compliant=True,
            compliance_report={"other_data": "value"},
            created_at=datetime(2026, 4, 5)
        ),
    ]
    
    # Add batches to session
    for batch in test_batches:
        db.add(batch)
    db.commit()
    
    # Test ReportService
    report_service = ReportService(db)
    
    try:
        report = report_service.generate_cbam_report(2026)
        print(f"[SUCCESS] Report generated successfully!")
        print(f"  Total H2 kg: {report['total_hydrogen_kg']}")
        print(f"  Total emissions tCO2: {report['total_emissions_tco2e']}")
        print(f"  Average emissions per kg: {report['average_emissions_per_kg']:.2f} gCO2/kgH2")
        print(f"  Compliance rate: {report['compliance_rate']:.1%}")
        
        # Verify calculations
        expected_total_h2 = 1000 + 1500 + 800 + 1200  # 4500 kg
        expected_emissions = 2.8  # Only batch_001 has emissions data
        
        if report['total_hydrogen_kg'] == expected_total_h2:
            print(f"[OK] Total H2 calculation correct: {expected_total_h2} kg")
        else:
            print(f"[ERROR] Total H2 calculation wrong: expected {expected_total_h2}, got {report['total_hydrogen_kg']}")
            
        if abs(report['total_emissions_tco2e'] - expected_emissions) < 0.01:
            print(f"[OK] Total emissions calculation correct: {expected_emissions} tCO2")
        else:
            print(f"[ERROR] Total emissions calculation wrong: expected {expected_emissions}, got {report['total_emissions_tco2e']}")
            
        return True
        
    except Exception as e:
        print(f"[ERROR] Report generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_report_service()
    sys.exit(0 if success else 1)
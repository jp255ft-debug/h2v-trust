import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.models.telemetry import TelemetryData
    from pydantic import ValidationError
    
    # Test the telemetry data model
    test_data = {
        "sensor_id": "test_sensor",
        "timestamp": "2026-04-22T10:00:00Z",
        "energy_source": "wind",
        "power_generated_mwh": 12.5,
        "ghg_emissions_kgCO2_per_kgH2": 2.8,
        "water_consumption_liters": 150,
        "water_source": "desalination"
    }
    
    print("Testing TelemetryData model...")
    print(f"Test data: {test_data}")
    
    try:
        telemetry = TelemetryData(**test_data)
        print("SUCCESS: Model validation successful!")
        print(f"Telemetry object created")
        print(f"Dict: {telemetry.model_dump()}")
    except ValidationError as e:
        print(f"ERROR: Validation error: {e}")
        print(f"Errors: {e.errors()}")
except ImportError as e:
    print(f"ERROR: Could not import TelemetryData: {e}")
    import traceback
    traceback.print_exc()
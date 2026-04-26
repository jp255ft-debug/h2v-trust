import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core.compliance import CBAMComplianceChecker
from backend.models.telemetry import TelemetryData

# Create telemetry data
data = TelemetryData(
    sensor_id="electrolyzer_01",
    timestamp="2026-04-22T19:10:30Z",
    energy_source="wind",
    power_generated_mwh=12.5,
    ghg_emissions_kgCO2_per_kgH2=2.8,
    water_consumption_liters=150,
    water_source="desalination"
)

print("Testing compliance checker...")
try:
    result = CBAMComplianceChecker.full_compliance_check(data, 1000.0)
    print(f"Compliance result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
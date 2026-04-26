import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from backend.models.telemetry import TelemetryData
from backend.core.compliance import CBAMComplianceChecker

# Test the full flow
print("Testing H2V-Trust flow...")
print("=" * 60)

# 1. Create telemetry data
telemetry_data = TelemetryData(
    sensor_id="test_sensor_01",
    timestamp=datetime.now().isoformat() + "Z",
    energy_source="wind",
    power_generated_mwh=12.5,
    ghg_emissions_kgCO2_per_kgH2=2.8,
    water_consumption_liters=150,
    water_source="desalination"
)

print("1. Telemetry data created:")
print(f"   Sensor ID: {telemetry_data.sensor_id}")
print(f"   Energy source: {telemetry_data.energy_source}")
print(f"   Emissions: {telemetry_data.ghg_emissions_kgCO2_per_kgH2} kgCO2/kgH2")
print(f"   Water consumption: {telemetry_data.water_consumption_liters} L")

# 2. Check compliance
print("\n2. Checking CBAM compliance...")
batch_size_kg = 1000.0
compliance_result = CBAMComplianceChecker.full_compliance_check(telemetry_data, batch_size_kg)

print(f"   Is compliant: {compliance_result['is_compliant']}")
print(f"   Checks:")
for check_name, check_result in compliance_result['checks'].items():
    print(f"     - {check_name}: {check_result['ok']} - {check_result['message']}")

if compliance_result['violations']:
    print(f"   Violations: {compliance_result['violations']}")

if compliance_result['cbam_report']:
    print(f"   CBAM Report: {compliance_result['cbam_report']}")

# 3. Test with non-compliant data
print("\n3. Testing with non-compliant data (high emissions)...")
non_compliant_data = TelemetryData(
    sensor_id="test_sensor_02",
    timestamp=datetime.now().isoformat() + "Z",
    energy_source="coal",
    power_generated_mwh=12.5,
    ghg_emissions_kgCO2_per_kgH2=10.5,  # Above limit
    water_consumption_liters=150,
    water_source="desalination"
)

non_compliant_result = CBAMComplianceChecker.full_compliance_check(non_compliant_data, batch_size_kg)
print(f"   Is compliant: {non_compliant_result['is_compliant']}")
print(f"   Violations: {non_compliant_result['violations']}")

print("\n" + "=" * 60)
print("Flow test completed successfully!")
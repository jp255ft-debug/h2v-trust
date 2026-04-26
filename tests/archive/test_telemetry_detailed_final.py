import requests
import json
from datetime import datetime
import traceback

print("Testing telemetry endpoint in detail...")
print("=" * 60)

# Base URL
BASE_URL = "http://localhost:8000"
API_KEY = "test-secret-key-for-local-development-12345"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# Test telemetry endpoint
telemetry_data = {
    "sensor_id": "test_sensor_detailed_final",
    "timestamp": datetime.now().isoformat() + "Z",
    "energy_source": "wind",
    "power_generated_mwh": 12.5,
    "ghg_emissions_kgCO2_per_kgH2": 2.8,
    "water_consumption_liters": 150,
    "water_source": "desalination"
}

print(f"Sending telemetry data: {json.dumps(telemetry_data, indent=2)}")

try:
    response = requests.post(
        f"{BASE_URL}/api/v1/telemetry",
        json=telemetry_data,
        headers=headers,
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"Response: {response.json()}")
        print("[OK] Telemetry endpoint working!")
    elif response.status_code == 500:
        print(f"Response text: {response.text}")
        print("\n[ERROR] Server error details:")
        try:
            error_json = response.json()
            print(f"Error JSON: {json.dumps(error_json, indent=2)}")
        except:
            print("Could not parse error as JSON")
    else:
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"[ERROR] Exception: {e}")
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test completed!")
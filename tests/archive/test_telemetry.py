import requests
import json

url = "http://localhost:8000/api/v1/telemetry"
headers = {
    "X-API-Key": "test-secret-key-for-local-development-12345",
    "Content-Type": "application/json"
}
data = {
    "sensor_id": "electrolyzer_01",
    "timestamp": "2026-04-22T19:06:30Z",
    "energy_source": "wind",
    "power_generated_mwh": 12.5,
    "ghg_emissions_kgCO2_per_kgH2": 2.8,
    "water_consumption_liters": 150,
    "water_source": "desalination"
}

print("Testing telemetry endpoint...")
try:
    response = requests.post(url, headers=headers, json=data, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
import requests
import json
from datetime import datetime

print("Testing H2V-Trust API endpoints...")
print("=" * 60)

# Base URL
BASE_URL = "http://localhost:8000"
API_KEY = "test-secret-key-for-local-development-12345"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# 1. Test health endpoint
print("1. Testing health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print("   [OK] Health check passed")
except Exception as e:
    print(f"   [ERROR] Health check failed: {e}")

# 2. Test telemetry endpoint
print("\n2. Testing telemetry endpoint...")
telemetry_data = {
    "sensor_id": "test_sensor_final_2",
    "timestamp": datetime.now().isoformat() + "Z",
    "energy_source": "wind",
    "power_generated_mwh": 12.5,
    "ghg_emissions_kgCO2_per_kgH2": 2.8,
    "water_consumption_liters": 150,
    "water_source": "desalination"
}

print(f"   Sending telemetry data...")

try:
    response = requests.post(
        f"{BASE_URL}/api/v1/telemetry",
        json=telemetry_data,
        headers=headers,
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
        print("   [OK] Telemetry endpoint working!")
    elif response.status_code == 500:
        print(f"   [ERROR] Server error: {response.text}")
        print("   Note: This might be due to duplicate token_id in mock mode")
    else:
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   [ERROR] Error: {e}")

# 3. Test batches endpoint
print("\n3. Testing batches endpoint...")
try:
    response = requests.get(
        f"{BASE_URL}/api/v1/batches",
        headers=headers,
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        batches = response.json()
        print(f"   Found {len(batches)} batches")
        if batches:
            print(f"   First batch ID: {batches[0].get('id', 'N/A')}")
        print("   [OK] Batches endpoint working!")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   [ERROR] Error: {e}")

# 4. Test certificates endpoint
print("\n4. Testing certificates endpoint...")
try:
    response = requests.get(
        f"{BASE_URL}/api/v1/certificates",
        headers=headers,
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        certificates = response.json()
        print(f"   Found {len(certificates)} certificates")
        if certificates:
            print(f"   First certificate ID: {certificates[0].get('id', 'N/A')}")
        print("   [OK] Certificates endpoint working!")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   [ERROR] Error: {e}")

print("\n" + "=" * 60)
print("API test completed!")
import requests
import json
import traceback

def test_telemetry():
    url = "http://localhost:8000/api/v1/telemetry"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "test-secret-key-for-local-development-12345"
    }
    
    data = {
        "sensor_id": "test_sensor",
        "timestamp": "2026-04-22T10:00:00Z",
        "energy_source": "wind",
        "power_generated_mwh": 12.5,
        "ghg_emissions_kgCO2_per_kgH2": 2.8,
        "water_consumption_liters": 150,
        "water_source": "desalination"
    }
    
    print("Testing telemetry endpoint...")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"\nStatus code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            print("\n✅ Telemetry endpoint working!")
        else:
            print(f"Response text: {response.text}")
            
            # Try to parse as JSON
            try:
                error_json = response.json()
                print(f"Error JSON: {json.dumps(error_json, indent=2)}")
            except:
                pass
                
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        traceback.print_exc()

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"\nHealth check: {response.status_code} - {response.text}")
    except:
        print("\nHealth endpoint not available")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing H2V-Trust API")
    print("=" * 60)
    
    test_health()
    test_telemetry()
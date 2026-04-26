import asyncio
import httpx
import os

async def test_connection():
    API_URL = os.getenv("API_BASE_URL", "http://localhost:8002") + "/api/v1/telemetry"
    API_KEY = os.getenv("H2V_API_KEY", "test-secret-key-for-local-development-12345")
    
    print(f"Testing connection to: {API_URL}")
    print(f"Using API key: {API_KEY[:10]}...")
    
    # Test data matching the TelemetryData model
    payload = {
        "sensor_id": "test_sensor",
        "timestamp": "2026-04-19T10:00:00Z",
        "energy_source": "wind",
        "power_generated_mwh": 10.5,
        "ghg_emissions_kgCO2_per_kgH2": 2.5,
        "water_consumption_liters": 150,
        "water_source": "desalination"
    }
    
    headers = {"X-API-Key": API_KEY}
    
    try:
        async with httpx.AsyncClient() as client:
            print("Sending request...")
            response = await client.post(API_URL, json=payload, headers=headers, timeout=10.0)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
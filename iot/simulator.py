import asyncio
import random
import httpx
from datetime import datetime, timezone
import yaml
from pathlib import Path
import os

CONFIG_PATH = Path(__file__).parent / "config.yaml"
# Configurable API URL via environment variable
API_URL = os.getenv("API_BASE_URL", "http://localhost:8000") + "/api/v1/telemetry"
# Em produção, definir H2V_API_KEY no ambiente
API_KEY = os.getenv("H2V_API_KEY", "")

async def send_telemetry(sensor_config):
    async with httpx.AsyncClient() as client:
        while True:
            # Simulate reading
            payload = {
                "sensor_id": sensor_config["id"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "energy_source": sensor_config["energy_source"],
                "power_generated_mwh": round(random.uniform(5, 20), 2),
                "ghg_emissions_kgCO2_per_kgH2": round(random.uniform(2.0, 4.0), 2),
                "water_consumption_liters": round(random.uniform(100, 300), 2),
                "water_source": random.choice(["desalination", "surface_water"]),
            }
            # Enforce compliance for valid ones
            if sensor_config.get("force_compliant", False):
                payload["ghg_emissions_kgCO2_per_kgH2"] = round(random.uniform(2.0, 3.3), 2)

            headers = {"X-API-Key": API_KEY}
            try:
                response = await client.post(API_URL, json=payload, headers=headers)
                print(f"[{sensor_config['id']}] Status: {response.status_code} - {response.json().get('batch_id', 'N/A')}")
            except Exception as e:
                print(f"Error: {e}")

            await asyncio.sleep(sensor_config.get("interval_seconds", 10))

async def main():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    tasks = [send_telemetry(sensor) for sensor in config["sensors"]]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
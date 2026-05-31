"""Probe script to discover API behavior."""
import sys
sys.path.insert(0, "/app")
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Login
r = client.post("/api/v1/auth/login", json={
    "email": "operator@produtor-alfa.com",
    "password": "H2v@Trust!2026"
})
print("Login:", r.status_code)
data = r.json()
token = data["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Create batch
r = client.post("/api/v1/batches?batch_size_kg=1000", json={
    "sensor_id": "probe_test",
    "timestamp": "2026-05-18T10:00:00Z",
    "energy_source": "solar",
    "power_generated_mwh": 100.0,
    "ghg_emissions_kgCO2_per_kgH2": 2.5,
    "water_consumption_liters": 10.0,
    "water_source": "desalination"
}, headers=headers)
print("Create batch:", r.status_code)
print("Response keys:", list(r.json().keys()))
print("Response:", r.json())
batch_id = r.json()["id"]

# Certify
r = client.post(f"/api/v1/batches/{batch_id}/certify", headers=headers)
print("\nCertify:", r.status_code)
print("Response:", r.json())
cert_data = r.json()
cert_id = cert_data.get("certificate_id", "")

# Get certificate
r = client.get(f"/api/v1/certificates/{cert_id}", headers=headers)
print("\nGet cert:", r.status_code)
print("Response:", r.json())

# Consume
r = client.post(f"/api/v1/certificates/{cert_id}/consume", headers=headers)
print("\nConsume:", r.status_code)
print("Response:", r.json())

# Double consume
r = client.post(f"/api/v1/certificates/{cert_id}/consume", headers=headers)
print("\nDouble consume:", r.status_code)
print("Response:", r.json())

# Non-compliant batch
r = client.post("/api/v1/batches?batch_size_kg=1000", json={
    "sensor_id": "probe_noncompliant",
    "timestamp": "2026-05-18T10:00:00Z",
    "energy_source": "diesel",
    "power_generated_mwh": 100.0,
    "ghg_emissions_kgCO2_per_kgH2": 5.0,
    "water_consumption_liters": 10.0,
    "water_source": "desalination"
}, headers=headers)
print("\nNon-compliant batch:", r.status_code)
print("Response:", r.json())

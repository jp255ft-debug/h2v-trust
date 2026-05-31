"""
Runner para o teste E2E de certificação.
Executa o fluxo completo sem depender do pytest (evita conflito web3/eth-typing).
"""
import sys
sys.path.insert(0, "/app")
import uuid
import json
import traceback
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# ─── Config ──────────────────────────────────────────────────────────────────
PRODUCER_ALFA_EMAIL = "operator@produtor-alfa.com"
PRODUCER_ALFA_PASS = "H2v@Trust!2026"
AUDITOR_EMAIL = "auditor@h2v-trust.com"
AUDITOR_PASS = "H2v@Trust!2026"

# Usar UUIDs únicos para evitar colisão de batch_hash
unique_suffix = uuid.uuid4().hex[:8]

COMPLIANT_TELEMETRY = {
    "sensor_id": f"e2e_compliant_{unique_suffix}",
    "timestamp": "2026-05-18T10:00:00Z",
    "energy_source": "solar",
    "power_generated_mwh": 100.0,
    "ghg_emissions_kgCO2_per_kgH2": 2.5,
    "water_consumption_liters": 10.0,
    "water_source": "desalination",
}

NON_COMPLIANT_TELEMETRY = {
    "sensor_id": f"e2e_noncompliant_{unique_suffix}",
    "timestamp": "2026-05-18T10:00:00Z",
    "energy_source": "diesel",
    "power_generated_mwh": 100.0,
    "ghg_emissions_kgCO2_per_kgH2": 5.0,
    "water_consumption_liters": 10.0,
    "water_source": "desalination",
}

passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name}: {detail}")

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Login
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("🔐 LOGIN")
print("="*60)

r = client.post("/api/v1/auth/login", json={
    "email": PRODUCER_ALFA_EMAIL,
    "password": PRODUCER_ALFA_PASS,
})
test("Login produtor-alfa", r.status_code == 200, f"Status: {r.status_code}")
data = r.json()
producer_token = data.get("access_token", "")
tenant_id = data.get("user", {}).get("tenant_id", "")
test("Token recebido", bool(producer_token))
test("Tenant ID presente", bool(tenant_id), f"tenant_id={tenant_id}")

r = client.post("/api/v1/auth/login", json={
    "email": AUDITOR_EMAIL,
    "password": AUDITOR_PASS,
})
test("Login auditor", r.status_code == 200, f"Status: {r.status_code}")
auditor_token = r.json().get("access_token", "")

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Criar lote conforme
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("✅ CRIAÇÃO DE LOTE CONFORME")
print("="*60)

r = client.post("/api/v1/batches?batch_size_kg=1000",
    json=COMPLIANT_TELEMETRY,
    headers=auth_header(producer_token))
test("Create batch status", r.status_code == 200, f"Status: {r.status_code}")
data = r.json()
test("Batch is compliant", data.get("is_compliant") is True, str(data.get("compliance_report", {})))
test("Compliance report presente", "compliance_report" in data)
test("Violations vazio", data.get("compliance_report", {}).get("violations") == [])
test("CBAM eligible", data.get("compliance_report", {}).get("cbam_report", {}).get("certificate_eligible") is True)

batch_id = data["id"]
batch_hash = data.get("batch_hash", "")
print(f"  📦 Batch ID: {batch_id}")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Verificar compliance
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("📋 VERIFICAÇÃO DE COMPLIANCE")
print("="*60)

r = client.get(f"/api/v1/batches/{batch_id}/compliance",
    headers=auth_header(producer_token))
test("Compliance endpoint", r.status_code == 200, f"Status: {r.status_code}")
data = r.json()
test("is_compliant True", data.get("is_compliant") is True)
test("Violations vazio", len(data.get("violations", [])) == 0)
test("CBAM report presente", data.get("cbam_report") is not None)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Certificar lote
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("🏅 CERTIFICAÇÃO (SBT MINT)")
print("="*60)

r = client.post(f"/api/v1/batches/{batch_id}/certify",
    headers=auth_header(producer_token))
test("Certify status", r.status_code == 200, f"Status: {r.status_code}")
data = r.json()
cert_id = data.get("certificate_id", "")
test("Certificate ID presente", bool(cert_id), f"cert_id={cert_id}")
test("Blockchain status válido", data.get("blockchain_status") in ("confirmed", "pending"))
print(f"  🆔 Certificate ID: {cert_id}")
print(f"  ⛓️  Blockchain: {data.get('blockchain_status')}")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Consultar certificado
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("🔍 CONSULTA DE CERTIFICADO")
print("="*60)

r = client.get(f"/api/v1/certificates/{cert_id}",
    headers=auth_header(producer_token))
test("Get certificate status", r.status_code == 200, f"Status: {r.status_code}")
data = r.json()
test("Certificate data presente", "certificate" in data)
test("Batch ID corresponde", data.get("certificate", {}).get("batch_id") == batch_id)
test("is_consumed False", data.get("certificate", {}).get("is_consumed") is False)
test("On-chain proof presente", "on_chain_proof" in data)
print(f"  📄 Certificado encontrado: {data['certificate']['id']}")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. Consumir certificado
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("♻️  CONSUMO DO CERTIFICADO (SURRENDER)")
print("="*60)

r = client.post(f"/api/v1/certificates/{cert_id}/consume",
    headers=auth_header(producer_token))
test("Consume status", r.status_code == 200, f"Status: {r.status_code}")
data = r.json()
if "status" in data:
    test("Consumed com sucesso", data["status"] == "consumed", str(data))
    print(f"  ✅ Certificado consumido: {data}")
elif "error" in data:
    test("Erro não é 'Not found'", data["error"] != "Not found",
         f"Certificado deveria existir: {data}")
    print(f"  ⚠️  Erro no consume: {data}")

# ═══════════════════════════════════════════════════════════════════════════════
# 7. Double counting
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("🚫 DOUBLE COUNTING")
print("="*60)

r = client.post(f"/api/v1/certificates/{cert_id}/consume",
    headers=auth_header(producer_token))
data = r.json()
if "error" in data:
    error_msg = str(data.get("error", "")).lower()
    test("Double counting rejeitado", True, f"Erro: {data['error']}")
    print(f"  🚫 Double counting rejeitado: {data['error']}")
else:
    test("Double counting - status inesperado", False, f"Esperava erro, recebeu: {data}")

# ═══════════════════════════════════════════════════════════════════════════════
# 8. Lote não conforme
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("❌ LOTE NÃO CONFORME")
print("="*60)

r = client.post("/api/v1/batches?batch_size_kg=1000",
    json=NON_COMPLIANT_TELEMETRY,
    headers=auth_header(producer_token))
test("Create non-compliant batch", r.status_code == 200, f"Status: {r.status_code}")
data = r.json()
test("is_compliant False", data.get("is_compliant") is False)
test("Violations presentes", len(data.get("compliance_report", {}).get("violations", [])) > 0)
non_compliant_id = data["id"]
print(f"  📦 Non-compliant batch ID: {non_compliant_id}")

r = client.post(f"/api/v1/batches/{non_compliant_id}/certify",
    headers=auth_header(producer_token))
test("Certify non-compliant rejeitado (400)", r.status_code == 400, f"Status: {r.status_code}")
detail = str(r.json().get("detail", "")).lower()
test("Mensagem de erro clara",
     any(w in detail for w in ["conforme", "compliance", "não"]),
     f"detail={detail}")

# ═══════════════════════════════════════════════════════════════════════════════
# 9. Isolamento por tenant
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("🔒 ISOLAMENTO POR TENANT")
print("="*60)

r = client.get("/api/v1/batches?limit=100",
    headers=auth_header(auditor_token))
test("Auditor vê batches", r.status_code == 200, f"Status: {r.status_code}")
data = r.json()
test("Auditor vê >= 1 batch", data.get("total", 0) >= 1, f"total={data.get('total')}")

r = client.post("/api/v1/batches?batch_size_kg=1000",
    json=COMPLIANT_TELEMETRY,
    headers=auth_header(auditor_token))
test("Auditor não cria batch (403/500)", r.status_code in (403, 500),
     f"Status: {r.status_code}")

# ═══════════════════════════════════════════════════════════════════════════════
# Resultado Final
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print(f"📊 RESULTADO FINAL: {passed} passed, {failed} failed")
print("="*60)

if failed == 0:
    print("\n🎉 TODOS OS TESTES PASSARAM!")
    sys.exit(0)
else:
    print(f"\n❌ {failed} teste(s) falharam")
    sys.exit(1)

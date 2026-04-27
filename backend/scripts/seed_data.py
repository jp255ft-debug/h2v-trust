import sys
sys.path.insert(0, '/app')
from db.database import SessionLocal
from db.models import Batch, Certificate
import uuid
from datetime import datetime, timedelta

db = SessionLocal()

PRODUCER_WALLET = "0x1234567890abcdef1234567890abcdef12345678"
PRODUCER_ID = "12345678-1234-1234-1234-123456789abc"
FACILITY_ID = "FAC-001"
LOCATION = "Cedro, Ceará, Brasil"

print("🌱 Inserindo lotes de demonstração...")
batch_ids = []
for i in range(5):
    batch = Batch(
        id=str(uuid.uuid4()),
        producer_wallet=PRODUCER_WALLET,
        producer_id=PRODUCER_ID,
        facility_id=FACILITY_ID,
        production_location=LOCATION,
        size_kg=round(100 + i * 25, 2),
        is_compliant=True,
        blockchain_status="confirmed" if i < 3 else "pending",
        compliance_report={"standard": "CBAM", "score": 95.0 + i},
        batch_hash=f"0x{uuid.uuid4().hex[:64]}",
        created_at=datetime.utcnow() - timedelta(days=i)
    )
    db.add(batch)
    db.flush()
    batch_ids.append(batch.id)
    print(f"   Lote {i+1}: {batch.size_kg} kg de H₂ ({batch.blockchain_status})")

# Criar certificados para os lotes confirmados (3 primeiros)
print("📜 Emitindo certificados...")
for i, bid in enumerate(batch_ids[:3]):
    cert = Certificate(
        id=str(uuid.uuid4()),
        batch_id=bid,
        token_id=int(1000 + i),   # BIGINT
        blockchain_tx_hash=f"0x{uuid.uuid4().hex[:64]}",
        qr_code_data=f"https://h2v-trust.com/cert/{bid[:8]}",
        is_consumed=False,
        created_at=datetime.utcnow()
    )
    db.add(cert)
    print(f"   Certificado emitido para lote {bid[:8]}...")

db.commit()
print("✅ Seed concluído! 5 lotes e 3 certificados criados.")
db.close()

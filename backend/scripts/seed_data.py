"""
⚠️ DEPRECATED — Use scripts/seed_demo_data.py em vez deste.

Script de seed para popular o banco com dados realistas de produção de H₂ verde.
Gera lotes com telemetria, certificados e dados de conformidade CBAM.

ATENÇÃO: Este script NÃO cria tenant_id nos registros, sendo incompatível com
o modelo multi-tenant atual. Mantido apenas para referência histórica.
"""

import sys
sys.path.insert(0, '/app')
from db.database import SessionLocal
from db.models import Batch, Certificate, TelemetryRecord
import uuid
from datetime import datetime, timedelta
import random

db = SessionLocal()

PRODUCER_WALLET = "0x1234567890abcdef1234567890abcdef12345678"
PRODUCER_ID = "12345678-1234-1234-1234-123456789abc"
FACILITY_ID = "FAC-001"
LOCATION = "Cedro, Ceará, Brasil"

# Limpar dados existentes para evitar duplicatas
print("🧹 Limpando dados existentes...")
db.query(Certificate).delete()
db.query(Batch).delete()
db.query(TelemetryRecord).delete()
db.commit()

print("🌱 Inserindo lotes de demonstração com telemetria...")
batch_ids = []
now = datetime.utcnow()

# Gerar 20 lotes espalhados nos últimos 6 meses
for i in range(20):
    dias_atras = random.randint(0, 180)
    created_at = now - timedelta(days=dias_atras, hours=random.randint(0, 23))

    # Tamanho do lote: entre 80 e 250 kg
    size_kg = round(random.uniform(80, 250), 2)

    # Emissões GHG: entre 1.5 e 4.5 kgCO₂e/kgH₂ (limite CBAM: 3.4)
    ghg_emissions = round(random.uniform(1.5, 4.5), 2)
    is_compliant_ghg = ghg_emissions <= 3.4

    # Consumo de água: entre 8 e 20 L/kgH₂ (limite recomendado: 15)
    water_consumption = round(random.uniform(8, 20), 1)
    is_compliant_water = water_consumption <= 15

    # Conformidade geral
    is_compliant = is_compliant_ghg and is_compliant_water

    # Status blockchain (mais realista: confirmado se conforme)
    blockchain_status = "confirmed" if is_compliant else "pending"

    # Score de compliance
    if is_compliant:
        score = round(random.uniform(85, 100), 1)
    else:
        score = round(random.uniform(40, 79), 1)

    # 1. Criar telemetria primeiro (Batch tem FK telemetry_id)
    telemetry = TelemetryRecord(
        sensor_id="sensor_prod_001",
        timestamp=created_at,
        energy_source="wind",
        power_generated_mwh=round(size_kg / 100 * random.uniform(0.8, 1.2), 2),
        ghg_emissions=ghg_emissions,
        water_consumption_liters=water_consumption,
        water_source="desalination"
    )
    db.add(telemetry)
    db.flush()  # Para obter o ID auto-increment

    # 2. Criar batch com referência à telemetria
    batch = Batch(
        id=str(uuid.uuid4()),
        telemetry_id=telemetry.id,
        producer_wallet=PRODUCER_WALLET,
        producer_id=PRODUCER_ID,
        facility_id=FACILITY_ID,
        production_location=LOCATION,
        size_kg=size_kg,
        is_compliant=is_compliant,
        blockchain_status=blockchain_status,
        compliance_report={
            "standard": "CBAM",
            "score": score,
            "ghg_emissions": ghg_emissions,
            "ghg_limit": 3.4,
            "ghg_compliant": is_compliant_ghg,
            "water_consumption": water_consumption,
            "water_limit": 15,
            "water_compliant": is_compliant_water,
            "energy_source": "wind",
            "water_source": "desalination"
        },
        batch_hash=f"0x{uuid.uuid4().hex[:64]}",
        created_at=created_at
    )
    db.add(batch)
    db.flush()
    batch_ids.append(batch.id)

    status_icon = "✅" if is_compliant else "⚠️"
    print(f"   Lote {i+1:2d}: {size_kg:6.1f} kg | GHG={ghg_emissions:4.2f} | Água={water_consumption:4.1f} | {status_icon} {'CONFORME' if is_compliant else 'NÃO CONFORME'}")

# Criar certificados para os lotes conformes
print("\n📜 Emitindo certificados para lotes conformes...")
cert_count = 0
for bid in batch_ids:
    batch = db.query(Batch).filter(Batch.id == bid).first()
    if batch and batch.is_compliant:
        cert = Certificate(
            id=str(uuid.uuid4()),
            batch_id=bid,
            token_id=int(1000 + cert_count),
            blockchain_tx_hash=f"0x{uuid.uuid4().hex[:64]}",
            qr_code_data=f"https://h2v-trust.com/cert/{bid[:8]}",
            is_consumed=False,
            created_at=batch.created_at
        )
        db.add(cert)
        cert_count += 1
        print(f"   Certificado #{1000 + cert_count - 1} emitido para lote {bid[:8]}...")

db.commit()

# Estatísticas finais
total_lotes = len(batch_ids)
conformes = db.query(Batch).filter(Batch.is_compliant == True).count()
nao_conformes = total_lotes - conformes
total_certificados = cert_count

print(f"\n{'='*50}")
print(f"✅ SEED CONCLUÍDO!")
print(f"{'='*50}")
print(f"   Total de lotes:       {total_lotes}")
print(f"   Conformes:            {conformes}")
print(f"   Não conformes:        {nao_conformes}")
print(f"   Taxa de conformidade: {conformes/total_lotes*100:.1f}%")
print(f"   Certificados emitidos:{total_certificados}")
print(f"{'='*50}")

db.close()

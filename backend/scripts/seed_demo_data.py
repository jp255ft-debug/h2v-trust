"""
Script de seed de dados realistas para demonstração comercial.
Gera dados limpos e coerentes para os 3 perfis (admin, operator, auditor).

Uso:
    docker compose exec backend python scripts/seed_demo_data.py
"""
import sys
sys.path.insert(0, '/app')

import uuid
import hashlib
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy import text

from db.database import SessionLocal
from db.models import (
    Tenant, User, UserTenant,
    TelemetryRecord, Batch, Certificate, Delegation, AuditLog
)
from api.dependencies.jwt_auth import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Constantes ──────────────────────────────────────────────────────────────

CBAM_GHG_LIMIT = 3.4  # kgCO2e/kgH2
WATER_LIMIT = 15.0     # L/kgH2

LOCATION_PECEM = "Hub de Hidrogênio Verde do Pecém, Ceará, Brasil"
LOCATION_CAMACARI = "Complexo Industrial de Camaçari, Bahia, Brasil"

PRODUCER_ALFA_WALLET = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
PRODUCER_BETA_WALLET = "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"

# ─── Dados dos lotes do Produtor Alfa ────────────────────────────────────────

ALFA_BATCHES = [
    # (size_kg, ghg_emissions, water_consumption, energy_source, water_source, days_ago, compliant)
    (1000, 1.8, 10.2, "solar", "desalination", 180, True),
    (1000, 2.1, 11.5, "solar", "desalination", 165, True),
    (1000, 1.5, 9.8,  "wind",  "recycled",     150, True),
    (1000, 2.3, 12.1, "solar", "desalination", 135, True),
    (1000, 1.9, 10.8, "wind",  "recycled",     120, True),
    (1000, 2.5, 13.2, "solar", "desalination", 105, True),
    (1000, 1.7, 9.5,  "solar", "recycled",      90, True),
    (1000, 2.0, 11.0, "wind",  "desalination",  75, True),
    (1000, 2.2, 12.5, "solar", "desalination",  60, True),
    (1000, 1.6, 10.0, "wind",  "recycled",      45, True),
    # 2 não-compliant
    (1000, 3.8, 14.5, "solar", "desalination",  30, False),  # GHG acima do limite
    (1000, 2.8, 18.2, "wind",  "desalination",  15, False),  # Água acima do limite
]

# ─── Dados dos lotes do Produtor Beta ────────────────────────────────────────

BETA_BATCHES = [
    (1000, 2.0, 11.0, "solar", "desalination", 160, True),
    (1000, 2.4, 12.8, "wind",  "desalination", 130, True),
    (1000, 1.9, 10.5, "solar", "recycled",     100, True),
    (1000, 3.6, 13.0, "solar", "desalination",  70, False),  # GHG acima do limite
    (1000, 2.6, 17.5, "wind",  "desalination",  40, False),  # Água acima do limite
]


def make_batch_hash():
    """Generate a realistic batch hash."""
    return "0x" + hashlib.sha256(uuid.uuid4().bytes).hexdigest()


def make_tx_hash():
    """Generate a realistic blockchain transaction hash."""
    return "0x" + hashlib.sha256(uuid.uuid4().bytes).hexdigest()


def create_telemetry(db, size_kg, ghg, water, energy, water_source, ts):
    """Create a telemetry record and return it."""
    telemetry = TelemetryRecord(
        sensor_id=f"sensor_{energy}_{ts.strftime('%Y%m')}",
        timestamp=ts,
        energy_source=energy,
        power_generated_mwh=round(size_kg / 100 * 1.1, 2),
        ghg_emissions=ghg,
        water_consumption_liters=water,
        water_source=water_source,
    )
    db.add(telemetry)
    db.flush()
    return telemetry


def create_batch(db, tenant_id, telemetry_id, producer_wallet, location,
                 size_kg, ghg, water, energy, water_source, ts, compliant):
    """Create a batch record and return it."""
    is_ghg_ok = ghg <= CBAM_GHG_LIMIT
    is_water_ok = water <= WATER_LIMIT
    score = round(95 - (ghg - 1.5) * 10 - (water - 9) * 2, 1) if compliant else \
            round(40 + (3.4 - min(ghg, 3.4)) * 10 + (WATER_LIMIT - min(water, WATER_LIMIT)) * 2, 1)
    score = max(0, min(100, score))

    batch = Batch(
        id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        telemetry_id=telemetry_id,
        producer_wallet=producer_wallet,
        producer_id=tenant_id,
        facility_id="FAC-001",
        production_location=location,
        size_kg=size_kg,
        is_compliant=compliant,
        blockchain_status="confirmed",
        compliance_report={
            "standard": "CBAM",
            "score": score,
            "ghg_emissions": ghg,
            "ghg_limit": CBAM_GHG_LIMIT,
            "ghg_compliant": is_ghg_ok,
            "water_consumption": water,
            "water_limit": WATER_LIMIT,
            "water_compliant": is_water_ok,
            "energy_source": energy,
            "water_source": water_source,
            "is_compliant": compliant,
            "checks": {
                "ghg": {"ok": is_ghg_ok, "message": f"Emissions {'OK' if is_ghg_ok else 'EXCEEDED'}: {ghg} <= {CBAM_GHG_LIMIT} kgCO2e/kgH2"},
                "water": {"ok": is_water_ok, "message": f"Water compliance {'OK' if is_water_ok else 'EXCEEDED'} (source: {water_source}, intensity: {water} L/kg)"},
                "energy": {"ok": True, "message": f"Renewable energy source: {energy}"},
                "additionality": {"ok": True, "message": "Additionality satisfied (dedicated renewable plant)"},
            },
            "violations": [] if compliant else [
                {"type": "ghg", "message": f"GHG emissions {ghg} exceed limit {CBAM_GHG_LIMIT}"} if not is_ghg_ok else None,
                {"type": "water", "message": f"Water consumption {water} exceeds limit {WATER_LIMIT}"} if not is_water_ok else None,
            ],
            "cbam_report": {
                "declared_emissions_tco2": ghg,
                "saved_emissions_vs_grey": round(10 - ghg, 1),
                "certificate_eligible": compliant,
            },
        },
        batch_hash=make_batch_hash(),
        created_at=ts,
    )
    db.add(batch)
    db.flush()
    return batch


def create_certificate(db, batch, token_id, consumed=False):
    """Create a certificate for a batch."""
    cert = Certificate(
        id=str(uuid.uuid4()),
        tenant_id=batch.tenant_id,
        batch_id=batch.id,
        token_id=token_id,
        blockchain_tx_hash=make_tx_hash(),
        qr_code_data=f"https://h2v-trust.com/cert/{batch.id[:8]}",
        is_consumed=consumed,
        consumed_at=batch.created_at + timedelta(days=30) if consumed else None,
        created_at=batch.created_at,
    )
    db.add(cert)
    return cert


def create_delegation(db, tenant_id, delegation_id, producer_wallet,
                      declarant_address, valid_until, status="active"):
    """Create a delegation record."""
    delegation = Delegation(
        tenant_id=tenant_id,
        delegation_id=delegation_id,
        producer_id=tenant_id,
        producer_wallet=producer_wallet,
        declarant_address=declarant_address,
        valid_until=valid_until,
        status=status,
        blockchain_tx_hash=make_tx_hash(),
    )
    db.add(delegation)
    return delegation


def create_audit_log(db, action, entity_type, entity_id, actor, tenant_id,
                     user_id=None, details=None):
    """Create an audit log entry."""
    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor=actor,
        user_id=user_id,
        tenant_id=tenant_id,
        details=details or {},
    )
    db.add(log)
    return log


def seed():
    """Main seed function."""
    db = SessionLocal()
    now = datetime.now(timezone.utc)

    try:
        print("=" * 70)
        print("🌱 SEED DE DADOS DE DEMONSTRAÇÃO - H2V-Trust")
        print("=" * 70)

        # ─── Buscar tenants e usuários ──────────────────────────────
        alfa_tenant = db.query(Tenant).filter(Tenant.slug == "produtor-alfa").first()
        beta_tenant = db.query(Tenant).filter(Tenant.slug == "produtor-beta").first()
        default_tenant = db.query(Tenant).filter(Tenant.slug == "default").first()

        admin_user = db.query(User).filter(User.email == "admin@h2v-trust.com").first()
        operator_user = db.query(User).filter(User.email == "operator@produtor-alfa.com").first()
        auditor_user = db.query(User).filter(User.email == "auditor@h2v-trust.com").first()

        if not all([alfa_tenant, beta_tenant, default_tenant, admin_user, operator_user, auditor_user]):
            print("❌ Erro: Tenants/usuários não encontrados. Execute seed_users_tenants.py primeiro.")
            return

        print(f"\n📋 Tenants encontrados:")
        print(f"   • Produtor Alfa: {alfa_tenant.id}")
        print(f"   • Produtor Beta: {beta_tenant.id}")
        print(f"   • Default:       {default_tenant.id}")

        # ─── Atualizar senhas ───────────────────────────────────────
        print("\n🔑 Atualizando senhas...")
        new_password = hash_password("H2v@Trust!2026")
        for user in [admin_user, operator_user, auditor_user]:
            user.password_hash = new_password
        db.flush()
        print("   Senhas atualizadas para: H2v@Trust!2026")

        # ─── Gerar lotes do Produtor Alfa ───────────────────────────
        print(f"\n📦 Gerando lotes para Produtor Alfa ({len(ALFA_BATCHES)} lotes)...")
        alfa_batches = []
        token_counter = 1001

        for i, (size, ghg, water, energy, wsource, days, compliant) in enumerate(ALFA_BATCHES):
            ts = now - timedelta(days=days, hours=i * 2)
            telemetry = create_telemetry(db, size, ghg, water, energy, wsource, ts)
            batch = create_batch(db, alfa_tenant.id, telemetry.id, PRODUCER_ALFA_WALLET,
                                 LOCATION_PECEM, size, ghg, water, energy, wsource, ts, compliant)
            alfa_batches.append(batch)

            # Criar certificado apenas para lotes compliant
            if compliant:
                consumed = i < 3  # Primeiros 3 certificados consumidos
                create_certificate(db, batch, token_counter, consumed=consumed)
                token_counter += 1

            status = "✅" if compliant else "⚠️"
            print(f"   Lote {i+1:2d}: {size:5.0f}kg | GHG={ghg:.1f} | Água={water:.1f} | {energy:5s} | {status}")

        # ─── Gerar lotes do Produtor Beta ───────────────────────────
        print(f"\n📦 Gerando lotes para Produtor Beta ({len(BETA_BATCHES)} lotes)...")
        beta_batches = []

        for i, (size, ghg, water, energy, wsource, days, compliant) in enumerate(BETA_BATCHES):
            ts = now - timedelta(days=days, hours=i * 3)
            telemetry = create_telemetry(db, size, ghg, water, energy, wsource, ts)
            batch = create_batch(db, beta_tenant.id, telemetry.id, PRODUCER_BETA_WALLET,
                                 LOCATION_CAMACARI, size, ghg, water, energy, wsource, ts, compliant)
            beta_batches.append(batch)

            if compliant:
                create_certificate(db, batch, token_counter)
                token_counter += 1

            status = "✅" if compliant else "⚠️"
            print(f"   Lote {i+1:2d}: {size:5.0f}kg | GHG={ghg:.1f} | Água={water:.1f} | {energy:5s} | {status}")

        # ─── Gerar delegações CBAM ──────────────────────────────────
        print("\n📜 Gerando delegações CBAM...")
        delegations_data = [
            ("del-alfa-eu-001", alfa_tenant.id, PRODUCER_ALFA_WALLET,
             "0xE11BA2b4D45Eaed5996Cd40D3B99F1A5c5C8b3fB",
             now + timedelta(days=365), "active"),
            ("del-alfa-eu-002", alfa_tenant.id, PRODUCER_ALFA_WALLET,
             "0xdD2FD4581271e230360230F9337D5c0430Bf44C0",
             now + timedelta(days=180), "active"),
        ]

        for del_id, tenant_id, wallet, declarant, valid, status in delegations_data:
            create_delegation(db, tenant_id, del_id, wallet, declarant, valid, status)
            print(f"   Delegação {del_id}: {declarant[:20]}... → válida até {valid.strftime('%d/%m/%Y')}")

        # ─── Gerar logs de auditoria ────────────────────────────────
        print("\n📋 Gerando logs de auditoria...")
        audit_events = []

        # Eventos do Produtor Alfa
        for batch in alfa_batches:
            audit_events.append(("batch.created", "batch", batch.id, "operator@produtor-alfa.com",
                                 alfa_tenant.id, operator_user.id, {"size_kg": batch.size_kg}))
            audit_events.append(("compliance.check", "batch", batch.id, "operator@produtor-alfa.com",
                                 alfa_tenant.id, operator_user.id,
                                 {"is_compliant": batch.is_compliant, "score": batch.compliance_report.get("score")}))
            if batch.is_compliant:
                audit_events.append(("certificate.minted", "certificate", batch.id,
                                     "operator@produtor-alfa.com", alfa_tenant.id, operator_user.id,
                                     {"token_id": token_counter - 1}))

        # Eventos do Produtor Beta
        for batch in beta_batches:
            audit_events.append(("batch.created", "batch", batch.id, "operator@produtor-beta.com",
                                 beta_tenant.id, None, {"size_kg": batch.size_kg}))
            audit_events.append(("compliance.check", "batch", batch.id, "operator@produtor-beta.com",
                                 beta_tenant.id, None,
                                 {"is_compliant": batch.is_compliant}))

        # Eventos de delegação
        audit_events.append(("delegation.created", "delegation", "del-alfa-eu-001",
                             "operator@produtor-alfa.com", alfa_tenant.id, operator_user.id, {}))
        audit_events.append(("delegation.created", "delegation", "del-alfa-eu-002",
                             "operator@produtor-alfa.com", alfa_tenant.id, operator_user.id, {}))

        # Eventos de login
        audit_events.append(("user.login", "user", admin_user.id, "admin@h2v-trust.com",
                             default_tenant.id, admin_user.id, {}))
        audit_events.append(("user.login", "user", operator_user.id, "operator@produtor-alfa.com",
                             alfa_tenant.id, operator_user.id, {}))
        audit_events.append(("user.login", "user", auditor_user.id, "auditor@h2v-trust.com",
                             default_tenant.id, auditor_user.id, {}))

        for action, entity_type, entity_id, actor, tenant_id, user_id, details in audit_events:
            create_audit_log(db, action, entity_type, entity_id, actor, tenant_id, user_id, details)

        print(f"   {len(audit_events)} eventos de auditoria gerados")

        # ─── Commit final ───────────────────────────────────────────
        db.commit()

        # ─── Estatísticas ───────────────────────────────────────────
        total_batches = db.query(Batch).count()
        total_certificates = db.query(Certificate).count()
        total_delegations = db.query(Delegation).count()
        total_audit = db.query(AuditLog).count()
        total_telemetry = db.query(TelemetryRecord).count()

        alfa_compliant = db.query(Batch).filter(
            Batch.tenant_id == alfa_tenant.id, Batch.is_compliant == True
        ).count()
        beta_compliant = db.query(Batch).filter(
            Batch.tenant_id == beta_tenant.id, Batch.is_compliant == True
        ).count()

        print("\n" + "=" * 70)
        print("✅ SEED DE DEMONSTRAÇÃO CONCLUÍDO!")
        print("=" * 70)
        print(f"\n📊 ESTATÍSTICAS FINAIS:")
        print(f"   Lotes totais:           {total_batches}")
        print(f"     → Produtor Alfa:      {len(ALFA_BATCHES)} ({alfa_compliant} compliant, {len(ALFA_BATCHES) - alfa_compliant} não-compliant)")
        print(f"     → Produtor Beta:      {len(BETA_BATCHES)} ({beta_compliant} compliant, {len(BETA_BATCHES) - beta_compliant} não-compliant)")
        print(f"   Certificados emitidos:  {total_certificates}")
        print(f"   Delegações CBAM:        {total_delegations}")
        print(f"   Logs de auditoria:      {total_audit}")
        print(f"   Registros de telemetria:{total_telemetry}")
        print(f"\n🔑 Credenciais atualizadas:")
        print(f"   Admin:    admin@h2v-trust.com / H2v@Trust!2026")
        print(f"   Operator: operator@produtor-alfa.com / H2v@Trust!2026")
        print(f"   Auditor:  auditor@h2v-trust.com / H2v@Trust!2026")
        print("=" * 70)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro durante seed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()

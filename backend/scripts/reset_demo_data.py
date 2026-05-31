"""
Script de limpeza do banco de dados para demonstração.
Remove dados de batches, certificates, delegations, telemetry_records e audit_logs.
Preserva tenants, users, user_tenants e alembic_version.

Uso:
    docker compose exec backend python scripts/reset_demo_data.py
"""
import sys
sys.path.insert(0, '/app')

from db.database import SessionLocal
from db.models import AuditLog, Certificate, Delegation, Batch, TelemetryRecord
from sqlalchemy import text

db = SessionLocal()

try:
    print("=" * 60)
    print("🧹 LIMPEZA DE DADOS DE DEMONSTRAÇÃO")
    print("=" * 60)

    # Ordem importa por causa das FKs
    print("\n1. Removendo AuditLogs...")
    count = db.query(AuditLog).delete()
    print(f"   → {count} registros removidos")

    print("2. Removendo Certificates...")
    count = db.query(Certificate).delete()
    print(f"   → {count} registros removidos")

    print("3. Removendo Delegations...")
    count = db.query(Delegation).delete()
    print(f"   → {count} registros removidos")

    print("4. Removendo Batches...")
    count = db.query(Batch).delete()
    print(f"   → {count} registros removidos")

    print("5. Removendo TelemetryRecords...")
    count = db.query(TelemetryRecord).delete()
    print(f"   → {count} registros removidos")

    db.commit()

    # Verificar o que sobrou
    print("\n" + "=" * 60)
    print("📊 VERIFICAÇÃO PÓS-LIMPEZA")
    print("=" * 60)

    tables = db.execute(
        text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
    ).fetchall()

    for t in tables:
        tn = t[0]
        count = db.execute(text(f'SELECT COUNT(*) FROM "{tn}"')).scalar()
        print(f"   {tn}: {count} registros")

    print("\n✅ Limpeza concluída com sucesso!")
    print("   Tenants, usuários e associações preservados.")

except Exception as e:
    db.rollback()
    print(f"\n❌ Erro durante limpeza: {e}")
    raise
finally:
    db.close()

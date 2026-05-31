"""
Relatório simples do banco de dados H2V-Trust.
"""
import sys
sys.path.insert(0, '/app')

from db.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

# 1. Listar tabelas e colunas
tables = db.execute(
    text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
).fetchall()

print("=" * 80)
print("RELATORIO DO BANCO DE DADOS - H2V-Trust")
print("=" * 80)
print(f"\nTABELAS ENCONTRADAS: {len(tables)}")

for t in tables:
    tn = t[0]
    count = db.execute(text(f'SELECT COUNT(*) FROM "{tn}"')).scalar()
    cols = db.execute(
        text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{tn}' ORDER BY ordinal_position")
    ).fetchall()
    col_names = [c[0] for c in cols]
    print(f"\n--- {tn}: {count} registros ---")
    print(f"  Colunas: {', '.join(col_names)}")

# 2. Dados detalhados
print("\n" + "=" * 80)
print("DADOS DETALHADOS")
print("=" * 80)

# Tenants
try:
    rows = db.execute(text("SELECT * FROM tenants")).fetchall()
    if rows:
        cols = [c[0] for c in db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'tenants' ORDER BY ordinal_position")).fetchall()]
        print(f"\n--- TENANTS ({len(rows)}) ---")
        for r in rows:
            for i, c in enumerate(cols):
                print(f"  {c}: {r[i]}")
            print()
except Exception as e:
    print(f"  Erro tenants: {e}")

# Users
try:
    rows = db.execute(text("SELECT * FROM users")).fetchall()
    if rows:
        cols = [c[0] for c in db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'users' ORDER BY ordinal_position")).fetchall()]
        print(f"--- USERS ({len(rows)}) ---")
        for r in rows:
            for i, c in enumerate(cols):
                print(f"  {c}: {r[i]}")
            print()
except Exception as e:
    print(f"  Erro users: {e}")

# Batches
try:
    rows = db.execute(text("SELECT * FROM batches ORDER BY created_at")).fetchall()
    if rows:
        cols = [c[0] for c in db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'batches' ORDER BY ordinal_position")).fetchall()]
        print(f"--- BATCHES ({len(rows)}) ---")
        for r in rows:
            for i, c in enumerate(cols):
                print(f"  {c}: {r[i]}")
            print()
except Exception as e:
    print(f"  Erro batches: {e}")

# Certificates
try:
    rows = db.execute(text("SELECT * FROM certificates ORDER BY created_at")).fetchall()
    if rows:
        cols = [c[0] for c in db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'certificates' ORDER BY ordinal_position")).fetchall()]
        print(f"--- CERTIFICATES ({len(rows)}) ---")
        for r in rows:
            for i, c in enumerate(cols):
                print(f"  {c}: {r[i]}")
            print()
except Exception as e:
    print(f"  Erro certificates: {e}")

# Delegations
try:
    rows = db.execute(text("SELECT * FROM delegations ORDER BY created_at")).fetchall()
    if rows:
        cols = [c[0] for c in db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'delegations' ORDER BY ordinal_position")).fetchall()]
        print(f"--- DELEGATIONS ({len(rows)}) ---")
        for r in rows:
            for i, c in enumerate(cols):
                print(f"  {c}: {r[i]}")
            print()
except Exception as e:
    print(f"  Erro delegations: {e}")

# Audit Logs
try:
    count = db.execute(text("SELECT COUNT(*) FROM audit_logs")).scalar()
    print(f"--- AUDIT_LOGS: {count} registros ---")
    if count > 0:
        rows = db.execute(text("SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 5")).fetchall()
        cols = [c[0] for c in db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'audit_logs' ORDER BY ordinal_position")).fetchall()]
        for r in rows:
            for i, c in enumerate(cols):
                print(f"  {c}: {r[i]}")
            print()
except Exception as e:
    print(f"  Erro audit_logs: {e}")

# Telemetry Records
try:
    count = db.execute(text("SELECT COUNT(*) FROM telemetry_records")).scalar()
    print(f"--- TELEMETRY_RECORDS: {count} registros ---")
    if count > 0:
        rows = db.execute(text("SELECT * FROM telemetry_records ORDER BY recorded_at DESC LIMIT 3")).fetchall()
        cols = [c[0] for c in db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'telemetry_records' ORDER BY ordinal_position")).fetchall()]
        for r in rows:
            for i, c in enumerate(cols):
                print(f"  {c}: {r[i]}")
            print()
except Exception as e:
    print(f"  Erro telemetry_records: {e}")

# UserTenants
try:
    rows = db.execute(text("SELECT * FROM user_tenants")).fetchall()
    if rows:
        cols = [c[0] for c in db.execute(text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'user_tenants' ORDER BY ordinal_position")).fetchall()]
        print(f"--- USER_TENANTS ({len(rows)}) ---")
        for r in rows:
            for i, c in enumerate(cols):
                print(f"  {c}: {r[i]}")
            print()
except Exception as e:
    print(f"  Erro user_tenants: {e}")

db.close()
print("=" * 80)
print("FIM DO RELATORIO")
print("=" * 80)

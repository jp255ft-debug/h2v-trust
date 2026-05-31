"""
Relatório completo do banco de dados H2V-Trust.
Gera um resumo de todas as tabelas e seus registros.
"""
import sys
import os

# Adicionar /app ao path (dentro do container Docker)
sys.path.insert(0, '/app')

from db.database import SessionLocal
from sqlalchemy import text


def gerar_relatorio():
    """Gera relatório completo do banco de dados."""
    db = SessionLocal()
    
    try:
        # 1. Listar tabelas
        tables = db.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        ).fetchall()
        
        linhas = []
        linhas.append("=" * 80)
        linhas.append("RELATÓRIO DO BANCO DE DADOS - H2V-Trust")
        linhas.append("=" * 80)
        linhas.append(f"\n📋 TABELAS ENCONTRADAS: {len(tables)}")
        
        for t in tables:
            tn = t[0]
            count = db.execute(text(f'SELECT COUNT(*) FROM "{tn}"')).scalar()
            linhas.append(f"   - {tn}: {count} registros")
        
        # 2. Tenants
        tenants = db.execute(
            text("SELECT id, name, slug, is_active FROM tenants")
        ).fetchall()
        linhas.append(f"\n🏢 TENANTS ({len(tenants)})")
        for t in tenants:
            linhas.append(f"   ID: {t[0]}")
            linhas.append(f"   Nome: {t[1]}")
            linhas.append(f"   Slug: {t[2]}")
            linhas.append(f"   Ativo: {t[3]}")
            linhas.append("")
        
        # 3. Users
        users = db.execute(
            text("SELECT id, email, full_name, role, is_active FROM users")
        ).fetchall()
        linhas.append(f"👤 USERS ({len(users)})")
        for u in users:
            linhas.append(f"   ID: {u[0]}")
            linhas.append(f"   Email: {u[1]}")
            linhas.append(f"   Nome: {u[2]}")
            linhas.append(f"   Role: {u[3]}")
            linhas.append(f"   Ativo: {u[4]}")
            linhas.append("")
        
        # 4. UserTenants
        ut = db.execute(
            text("SELECT user_id, tenant_id, role FROM user_tenants")
        ).fetchall()
        linhas.append(f"🔗 USER_TENANTS ({len(ut)})")
        for u in ut:
            linhas.append(f"   User: {u[0][:8]}... -> Tenant: {u[1][:8]}... (role: {u[2]})")
        linhas.append("")
        
        # 5. Batches
        batches = db.execute(
            text("SELECT id, batch_id, producer_id, status, is_compliant, total_emissions, total_water, created_at FROM batches ORDER BY created_at")
        ).fetchall()
        linhas.append(f"📦 BATCHES ({len(batches)})")
        for b in batches:
            linhas.append(f"   ID: {b[0]}")
            linhas.append(f"   Batch ID: {b[1]}")
            linhas.append(f"   Producer: {b[2][:8]}...")
            linhas.append(f"   Status: {b[3]}")
            linhas.append(f"   Compliant: {b[4]}")
            linhas.append(f"   Emissões: {b[5]} kgCO2")
            linhas.append(f"   Água: {b[6]} L")
            linhas.append(f"   Criado: {b[7]}")
            linhas.append("")
        
        # 6. Certificates
        certs = db.execute(
            text("SELECT id, certificate_id, batch_id, status, blockchain_tx_hash, created_at FROM certificates ORDER BY created_at")
        ).fetchall()
        linhas.append(f"📜 CERTIFICATES ({len(certs)})")
        for c in certs:
            linhas.append(f"   ID: {c[0]}")
            linhas.append(f"   Certificate ID: {c[1]}")
            linhas.append(f"   Batch: {c[2][:8]}...")
            linhas.append(f"   Status: {c[3]}")
            linhas.append(f"   TX Hash: {c[4]}")
            linhas.append(f"   Criado: {c[5]}")
            linhas.append("")
        
        # 7. Delegations
        delegs = db.execute(
            text("SELECT id, producer_id, declarant_wallet, status, valid_until, created_at FROM delegations ORDER BY created_at")
        ).fetchall()
        linhas.append(f"📄 DELEGATIONS ({len(delegs)})")
        for d in delegs:
            linhas.append(f"   ID: {d[0]}")
            linhas.append(f"   Producer: {d[1][:8]}...")
            linhas.append(f"   Declarant: {d[2]}")
            linhas.append(f"   Status: {d[3]}")
            linhas.append(f"   Válido até: {d[4]}")
            linhas.append(f"   Criado: {d[5]}")
            linhas.append("")
        
        # 8. Audit Logs
        audit_count = db.execute(text("SELECT COUNT(*) FROM audit_logs")).scalar()
        linhas.append(f"📋 AUDIT_LOGS ({audit_count} registros)")
        if audit_count > 0:
            recent = db.execute(
                text("SELECT id, user_id, action, resource, details, created_at FROM audit_logs ORDER BY created_at DESC LIMIT 5")
            ).fetchall()
            for a in recent:
                linhas.append(f"   #{a[0]} User:{str(a[1])[:8]} Action:{a[2]} Resource:{a[3]} Data:{a[5]}")
        linhas.append("")
        
        # 9. Telemetry Records
        tele_count = db.execute(text("SELECT COUNT(*) FROM telemetry_records")).scalar()
        linhas.append(f"📡 TELEMETRY_RECORDS ({tele_count} registros)")
        if tele_count > 0:
            tele_sample = db.execute(
                text("SELECT id, batch_id, ghg_emissions, water_consumption_liters, energy_source, recorded_at FROM telemetry_records ORDER BY recorded_at DESC LIMIT 3")
            ).fetchall()
            for t in tele_sample:
                linhas.append(f"   ID: {t[0]} Batch:{str(t[1])[:8]} GHG:{t[2]} Água:{t[3]} Fonte:{t[4]} Data:{t[5]}")
        
        linhas.append("\n" + "=" * 80)
        linhas.append("FIM DO RELATÓRIO")
        linhas.append("=" * 80)
        
        return "\n".join(linhas)
    
    finally:
        db.close()


if __name__ == "__main__":
    print(gerar_relatorio())

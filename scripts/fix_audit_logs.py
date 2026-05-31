"""Fix audit_logs table - add missing user_id and tenant_id columns."""
import sys
sys.path.insert(0, '/app')

from db.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text(
        "SELECT column_name FROM information_schema.columns WHERE table_name='audit_logs' ORDER BY ordinal_position"
    )).fetchall()
    print('Colunas atuais em audit_logs:', [r[0] for r in result], flush=True)
    
    has_user_id = any(r[0] == 'user_id' for r in result)
    if not has_user_id:
        print('Adicionando colunas faltantes...', flush=True)
        conn.execute(text('ALTER TABLE audit_logs ADD COLUMN user_id VARCHAR(36)'))
        conn.execute(text('ALTER TABLE audit_logs ADD COLUMN tenant_id VARCHAR(36)'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS ix_audit_logs_user_id ON audit_logs(user_id)'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS ix_audit_logs_tenant_id ON audit_logs(tenant_id)'))
        conn.commit()
        print('Colunas adicionadas com sucesso!', flush=True)
    else:
        print('Colunas já existem.', flush=True)

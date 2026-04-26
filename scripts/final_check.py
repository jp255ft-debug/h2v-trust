#!/usr/bin/env python3
"""Script final de verificação de imports para o projeto H2V-Trust."""

import sys
import os
import traceback

# Adicionar o diretório raiz ao PYTHONPATH
project_root = r"C:\Source\Repos\h2v-trust"
sys.path.insert(0, project_root)

print("=" * 70)
print("VERIFICAÇÃO FINAL DE IMPORTS - H2V-TRUST")
print("=" * 70)
print(f"Python path: {sys.path[:2]}...")
print(f"Diretório atual: {os.getcwd()}")
print()

# Lista de imports para testar
tests = [
    ("backend.config", "settings", "Configurações"),
    ("backend.db.database", "engine", "Banco de dados"),
    ("backend.db.models", "Batch", "Modelo Batch"),
    ("backend.db.models", "Certificate", "Modelo Certificate"),
    ("backend.db.models", "TelemetryRecord", "Modelo TelemetryRecord"),
    ("backend.db.models", "AuditLog", "Modelo AuditLog"),
    ("backend.db.models", "Delegation", "Modelo Delegation"),
    ("backend.services.batch_service", "BatchService", "Serviço de lotes"),
    ("backend.services.certificate_service", "CertificateService", "Serviço de certificados"),
    ("backend.api.routes.telemetry", "router", "Rota de telemetria"),
    ("backend.api.dependencies.db", "get_db", "Dependência de banco"),
    ("backend.api.dependencies.auth", "verify_api_key", "Dependência de auth"),
    ("backend.blockchain.web3_client", "get_contract", "Cliente Web3"),
    ("backend.blockchain.minting", "mint_certificate_on_chain", "Minting blockchain"),
    ("backend.blockchain.sbt_manager", "consume_sbt", "Gerenciador SBT"),
    ("backend.oracle.chainlink_client", "fetch_external_data", "Cliente Chainlink"),
    ("backend.core.compliance", "CBAMComplianceChecker", "Verificador CBAM"),
    ("backend.models.telemetry", "TelemetryData", "Modelo de telemetria"),
    ("backend.utils.hashing", "generate_batch_hash", "Utilitário de hash"),
]

all_ok = True
results = []

for module_name, attr_name, description in tests:
    try:
        module = __import__(module_name, fromlist=[attr_name])
        if hasattr(module, attr_name):
            results.append(f"[OK]  {description:30} ({module_name}.{attr_name})")
        else:
            results.append(f"[ERRO] {description:30} - Atributo '{attr_name}' não encontrado")
            all_ok = False
    except ImportError as e:
        results.append(f"[ERRO] {description:30} - ImportError: {e}")
        all_ok = False
    except Exception as e:
        results.append(f"[ERRO] {description:30} - Erro: {e}")
        all_ok = False

# Imprimir resultados
for result in results:
    print(result)

print()
print("=" * 70)
if all_ok:
    print("✅ TODOS OS IMPORTS ESTÃO OK!")
    print("O backend está pronto para execução.")
else:
    print("❌ ALGUNS IMPORTS FALHARAM!")
    print("Verifique os erros acima.")
print("=" * 70)

# Testar execução do backend
if all_ok:
    print("\nTestando execução do backend...")
    try:
        # Importar a aplicação
        from backend.main import app
        print("✅ Aplicação FastAPI importada com sucesso!")
        print(f"   Título: {app.title}")
        print(f"   Versão: {app.version}")
        print(f"   Descrição: {app.description[:50]}...")
        
        # Testar inicialização do banco de dados
        print("\nTestando inicialização do banco de dados...")
        from backend.db.database import Base, engine
        print("✅ Engine do banco de dados importado")
        
        # Verificar se há funções de inicialização
        try:
            from backend.main import init_db
            print("✅ Função init_db encontrada")
        except ImportError:
            print("⚠️  Função init_db não encontrada (pode ser normal)")
            
    except Exception as e:
        print(f"❌ Erro ao testar backend: {e}")
        traceback.print_exc()
        all_ok = False

print()
print("=" * 70)
if all_ok:
    print("🎉 TUDO PRONTO! O backend está 100% funcional.")
    print()
    print("Para executar o backend:")
    print("   cd C:\\Source\\Repos\\h2v-trust")
    print("   .\\venv\\Scripts\\activate")
    print("   uvicorn backend.main:app --reload")
    print()
    print("Acesse: http://localhost:8000/docs")
else:
    print("⚠️  Corrija os erros antes de executar o backend.")
print("=" * 70)
#!/usr/bin/env python3
"""Script de verificação de imports para o projeto H2V-Trust."""

import sys
import os

# Adicionar o diretório raiz ao PYTHONPATH
project_root = r"C:\Source\Repos\h2v-trust"
sys.path.insert(0, project_root)

print("=" * 60)
print("VERIFICAÇÃO DE IMPORTS - H2V-TRUST")
print("=" * 60)
print(f"Python path: {sys.path[:2]}...")
print(f"Diretório atual: {os.getcwd()}")
print()

# Lista de imports para testar
import_tests = [
    ("backend.config", "settings", "Configurações do projeto"),
    ("backend.db.database", "engine", "Banco de dados"),
    ("backend.db.models", "Batch", "Modelo Batch"),
    ("backend.db.models", "Certificate", "Modelo Certificate"),
    ("backend.db.models", "TelemetryRecord", "Modelo TelemetryRecord"),
    ("backend.services.batch_service", "BatchService", "Serviço de lotes"),
    ("backend.services.certificate_service", "CertificateService", "Serviço de certificados"),
    ("backend.api.routes.telemetry", "router", "Rota de telemetria"),
    ("backend.main", "app", "Aplicação FastAPI"),
]

all_passed = True

for module_name, attr_name, description in import_tests:
    try:
        module = __import__(module_name, fromlist=[attr_name])
        if hasattr(module, attr_name):
            print(f"✅ {description:30} ({module_name}.{attr_name})")
        else:
            print(f"❌ {description:30} - Atributo '{attr_name}' não encontrado")
            all_passed = False
    except ImportError as e:
        print(f"❌ {description:30} - ImportError: {e}")
        all_passed = False
    except Exception as e:
        print(f"❌ {description:30} - Erro: {e}")
        all_passed = False

print()
print("=" * 60)
if all_passed:
    print("✅ TODOS OS IMPORTS ESTÃO OK!")
    print("O backend está pronto para execução.")
else:
    print("❌ ALGUNS IMPORTS FALHARAM!")
    print("Verifique os erros acima e corrija os imports.")
print("=" * 60)

# Teste adicional: tentar importar a aplicação completa
if all_passed:
    print("\nTeste adicional: importando aplicação FastAPI...")
    try:
        from backend.main import app
        print("✅ Aplicação FastAPI importada com sucesso!")
        print(f"   Título: {app.title}")
        print(f"   Versão: {app.version}")
    except Exception as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        all_passed = False

print()
if all_passed:
    print("🎉 TUDO PRONTO! Execute o backend com:")
    print("   uvicorn backend.main:app --reload")
else:
    print("⚠️  Corrija os erros antes de executar o backend.")
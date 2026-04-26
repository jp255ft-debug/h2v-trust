#!/usr/bin/env python3
"""Script simples de verificação de imports."""

import sys
import os

# Adicionar o diretório raiz ao PYTHONPATH
project_root = r"C:\Source\Repos\h2v-trust"
sys.path.insert(0, project_root)

print("=" * 60)
print("VERIFICACAO DE IMPORTS - H2V-TRUST")
print("=" * 60)
print(f"Python path: {sys.path[:2]}...")
print(f"Diretorio atual: {os.getcwd()}")
print()

# Testar imports básicos
tests = [
    ("backend.config", "settings"),
    ("backend.db.database", "engine"),
    ("backend.db.models", "Batch"),
    ("backend.db.models", "Certificate"),
    ("backend.db.models", "TelemetryRecord"),
    ("backend.services.batch_service", "BatchService"),
    ("backend.services.certificate_service", "CertificateService"),
    ("backend.api.routes.telemetry", "router"),
    ("backend.main", "app"),
]

all_ok = True

for module_name, attr_name in tests:
    try:
        module = __import__(module_name, fromlist=[attr_name])
        if hasattr(module, attr_name):
            print(f"[OK]  {module_name}.{attr_name}")
        else:
            print(f"[ERRO] {module_name}.{attr_name} - atributo nao encontrado")
            all_ok = False
    except ImportError as e:
        print(f"[ERRO] {module_name}.{attr_name} - ImportError: {e}")
        all_ok = False
    except Exception as e:
        print(f"[ERRO] {module_name}.{attr_name} - Erro: {e}")
        all_ok = False

print()
print("=" * 60)
if all_ok:
    print("TODOS OS IMPORTS ESTAO OK!")
    print("O backend esta pronto para execucao.")
else:
    print("ALGUNS IMPORTS FALHARAM!")
    print("Verifique os erros acima.")
print("=" * 60)

# Testar execução do backend
if all_ok:
    print("\nTestando execucao do backend...")
    try:
        exec(open("C:\\Source\\Repos\\h2v-trust\\backend\\main.py").read())
        print("Backend executado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar backend: {e}")
        all_ok = False
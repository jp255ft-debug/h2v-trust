#!/usr/bin/env python3
"""Teste simples de imports sem Unicode."""

import sys
import os

# Adicionar o diretório raiz ao PYTHONPATH
project_root = r"C:\Source\Repos\h2v-trust"
sys.path.insert(0, project_root)

print("Testando imports basicos...")

# Testar imports essenciais
tests = [
    ("backend.config", "settings"),
    ("backend.db.database", "engine"),
    ("backend.db.models", "TelemetryRecord"),
    ("backend.db.models", "Batch"),
    ("backend.db.models", "Certificate"),
    ("backend.services.batch_service", "BatchService"),
    ("backend.services.certificate_service", "CertificateService"),
    ("backend.api.routes.telemetry", "router"),
    ("backend.main", "app"),
]

for module_name, attr_name in tests:
    try:
        module = __import__(module_name, fromlist=[attr_name])
        if hasattr(module, attr_name):
            print(f"OK  {module_name}.{attr_name}")
        else:
            print(f"ERR {module_name}.{attr_name} - atributo nao encontrado")
    except ImportError as e:
        print(f"ERR {module_name}.{attr_name} - ImportError: {e}")
    except Exception as e:
        print(f"ERR {module_name}.{attr_name} - Erro: {e}")

print("\nTestando execucao do backend...")
try:
    from backend.main import app
    print(f"OK  Aplicacao FastAPI: {app.title}")
    print(f"   Descricao: {app.description[:60]}...")
    
    # Testar se as rotas estao registradas
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    print(f"OK  {len(routes)} rotas registradas")
    for route in routes[:5]:
        print(f"   - {route}")
    if len(routes) > 5:
        print(f"   ... e mais {len(routes) - 5} rotas")
        
except Exception as e:
    print(f"ERR Erro ao testar backend: {e}")
    import traceback
    traceback.print_exc()

print("\nTESTE CONCLUIDO!")
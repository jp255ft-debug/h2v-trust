#!/usr/bin/env python3
"""Auditoria do estado atual do projeto h2v-trust"""
import os
import sys
import subprocess

ROOT = os.getcwd()

def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check_file(path):
    full = os.path.join(ROOT, path)
    exists = os.path.exists(full)
    size = os.path.getsize(full) if exists else 0
    status = "OK" if exists else "FALTA"
    return f"  [{status}] {path} ({size} bytes)"

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return r.stdout.strip() or r.stderr.strip()
    except:
        return "ERRO"

section("1. ESTRUTURA DO PROJETO")
print(f"  Diretório raiz: {ROOT}")
print(f"  Python: {sys.version}")

section("2. ARQUIVOS CRÍTICOS")
critical = [
    "package.json", "frontend/package.json", "frontend/next.config.js",
    "backend/main.py", "backend/config.py", "backend/requirements.txt",
    "docker-compose.yml", "alembic.ini", ".env", ".env.example",
    "frontend/tailwind.config.js", "frontend/postcss.config.js",
    "frontend/tsconfig.json", "frontend/Dockerfile", "backend/Dockerfile",
]
for f in critical:
    print(check_file(f))

section("3. DEPENDÊNCIAS (node_modules)")
nm_root = os.path.exists(os.path.join(ROOT, "node_modules"))
nm_front = os.path.exists(os.path.join(ROOT, "frontend", "node_modules"))
print(f"  node_modules (raiz): {'EXISTE' if nm_root else 'NÃO EXISTE'}")
print(f"  node_modules (frontend): {'EXISTE' if nm_front else 'NÃO EXISTE'}")

if nm_root:
    next_pkg = os.path.join(ROOT, "node_modules", "next", "package.json")
    if os.path.exists(next_pkg):
        ver = run(f'node -e "console.log(require(\\\"{next_pkg.replace(chr(92), chr(92)*2)}\\\").version)"')
        print(f"  Next.js versão: {ver}")

section("4. PÁGINAS FRONTEND (frontend/app/)")
app_dir = os.path.join(ROOT, "frontend", "app")
if os.path.exists(app_dir):
    pages = []
    for root, dirs, files in os.walk(app_dir):
        for f in files:
            if f.endswith(".tsx") or f.endswith(".ts"):
                rel = os.path.relpath(os.path.join(root, f), ROOT)
                pages.append(rel)
    for p in sorted(pages):
        print(f"  {p}")
    print(f"  Total: {len(pages)} páginas/componentes")

section("5. COMPONENTES UI (frontend/src/)")
src_dir = os.path.join(ROOT, "frontend", "src")
if os.path.exists(src_dir):
    comps = []
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith(".tsx") or f.endswith(".ts"):
                rel = os.path.relpath(os.path.join(root, f), ROOT)
                comps.append(rel)
    for c in sorted(comps):
        print(f"  {c}")
    print(f"  Total: {len(comps)} componentes/hooks/lib")

section("6. BACKEND PYTHON")
backend_dir = os.path.join(ROOT, "backend")
if os.path.exists(backend_dir):
    py_files = []
    for root, dirs, files in os.walk(backend_dir):
        for f in files:
            if f.endswith(".py"):
                rel = os.path.relpath(os.path.join(root, f), ROOT)
                py_files.append(rel)
    for p in sorted(py_files):
        print(f"  {p}")
    print(f"  Total: {len(py_files)} arquivos Python")

section("7. TESTES")
test_root = [f for f in os.listdir(ROOT) if f.startswith("test_") and f.endswith(".py")]
test_dir = []
tests_path = os.path.join(ROOT, "tests")
if os.path.exists(tests_path):
    test_dir = [f"tests/{f}" for f in os.listdir(tests_path) if f.endswith(".py")]
print(f"  Testes na raiz: {len(test_root)}")
print(f"  Testes em tests/: {len(test_dir)}")
for t in sorted(test_root):
    print(f"    {t}")
for t in sorted(test_dir):
    print(f"    {t}")

section("8. CONTRATOS SMART")
contracts_dir = os.path.join(ROOT, "contracts", "contracts")
if os.path.exists(contracts_dir):
    sol_files = [f for f in os.listdir(contracts_dir) if f.endswith(".sol")]
    print(f"  Contratos Solidity: {len(sol_files)}")
    for s in sorted(sol_files):
        print(f"    contracts/contracts/{s}")

section("9. DOCUMENTAÇÃO")
docs_dir = os.path.join(ROOT, "docs")
if os.path.exists(docs_dir):
    md_files = [f for f in os.listdir(docs_dir) if f.endswith(".md")]
    print(f"  Documentos: {len(md_files)}")
    for d in sorted(md_files):
        print(f"    docs/{d}")

section("10. PROCESSOS RODANDO")
proc_node = run('tasklist /fi "imagename eq node.exe" 2>&1 | find /c "node.exe"')
proc_python = run('tasklist /fi "imagename eq python.exe" 2>&1 | find /c "python.exe"')
print(f"  Node.js rodando: {proc_node} instância(s)")
print(f"  Python rodando: {proc_python} instância(s)")

section("11. ARQUIVOS GRANDES (>100KB)")
for root, dirs, files in os.walk(ROOT):
    # Pular node_modules e .git
    if "node_modules" in root or ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        fp = os.path.join(root, f)
        try:
            size = os.path.getsize(fp)
            if size > 100 * 1024:
                rel = os.path.relpath(fp, ROOT)
                print(f"  {rel} ({size/1024:.0f} KB)")
        except:
            pass

section("12. ARQUIVOS VAZIOS (0 bytes)")
empty = []
for root, dirs, files in os.walk(ROOT):
    if "node_modules" in root or ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        fp = os.path.join(root, f)
        try:
            if os.path.getsize(fp) == 0:
                rel = os.path.relpath(fp, ROOT)
                empty.append(rel)
        except:
            pass
if empty:
    print(f"  {len(empty)} arquivos vazios encontrados:")
    for e in sorted(empty):
        print(f"    {e}")
else:
    print("  Nenhum arquivo vazio encontrado!")

print(f"\n{'='*60}")
print("  AUDITORIA CONCLUÍDA")
print(f"{'='*60}")

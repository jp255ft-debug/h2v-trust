#!/usr/bin/env python3
"""
Auditoria de Seguranca de Codigo
Busca: secrets hardcoded, URLs internas Docker, fallbacks inseguros
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivos e diretorios para ignorar
IGNORE_DIRS = {
    'node_modules', '.git', '__pycache__', '.next', 'venv', '.venv',
    'env', '.env', 'dist', 'build', 'cache', '.cache', 'target',
    'alembic/versions', 'monitoring', 'iot/data', 'docs/audits',
    'contracts/node_modules', 'contracts/artifacts', 'contracts/cache',
    'frontend/.next', 'frontend/node_modules',
}
IGNORE_FILES = {
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', '.gitkeep',
}

def should_ignore(path: Path) -> bool:
    """Verifica se o arquivo/diretorio deve ser ignorado."""
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
    if path.suffix in {'.pyc', '.pyo', '.so', '.dll', '.dylib', '.png', '.jpg', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot'}:
        return True
    if path.name in IGNORE_FILES:
        return True
    return False

def find_files():
    """Encontra todos os arquivos relevantes para auditoria."""
    files = []
    for ext in ['.py', '.ts', '.tsx', '.js', '.jsx', '.json', '.yaml', '.yml', '.sh', '.bat', '.conf', '.cfg']:
        for f in BASE_DIR.rglob(f'*{ext}'):
            if not should_ignore(f):
                files.append(f)
    # Arquivos .env (sem extensao ou com sufixo)
    for f in BASE_DIR.rglob('.env*'):
        if not should_ignore(f) and f.is_file():
            files.append(f)
    return sorted(set(files))

# ============================================================
# REGRAS DE AUDITORIA
# ============================================================

SECRET_PATTERNS = [
    # Private keys hex (64 chars)
    (r'0x[a-fA-F0-9]{64}', 'PRIVATE_KEY_HEX', 'Chave privada Ethereum (64 hex chars)'),
    # Private keys PEM
    (r'-----BEGIN (RSA|EC|PRIVATE) KEY-----', 'PRIVATE_KEY_PEM', 'Chave privada PEM'),
    # JWT / API secrets
    (r'["\']?(?:secret_key|api_key|api_secret|jwt_secret|jwt_key|auth_token|access_token|refresh_token|password|passwd)["\']?\s*[:=]\s*["\'][^"\'\\\s]{8,}["\']', 'HARDCODED_SECRET', 'Secret/Key hardcoded no codigo'),
    # Enderecos de contrato (0x + 40 hex)
    (r'0x[a-fA-F0-9]{40}', 'CONTRACT_ADDRESS', 'Endereco de contrato/carteira'),
    # Tokens JWT
    (r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}', 'JWT_TOKEN', 'Token JWT hardcoded'),
]

DOCKER_URL_PATTERNS = [
    # URLs internas do Docker no frontend
    (r'backend:\d+', 'DOCKER_INTERNAL_URL', 'URL interna do servico Docker (backend:porta)'),
    (r'http://(?:backend|redis|timescaledb|hardhat)[:\s]', 'DOCKER_SERVICE_URL', 'URL de servico Docker interno'),
]

FALLBACK_PATTERNS = [
    # Fallbacks com localhost
    (r'\|\|\s*["\']https?://localhost', 'FALLBACK_LOCALHOST', 'Fallback para localhost (nao funciona em producao)'),
    (r'\|\|\s*["\']test-', 'FALLBACK_TEST', 'Fallback para valor de teste'),
    (r'=\s*["\']https?://localhost', 'DEFAULT_LOCALHOST', 'Valor default apontando para localhost'),
    # os.getenv sem fallback ou com fallback inseguro
    (r'os\.getenv\(["\'](\w+)["\'],\s*["\'](?!$)["\']', 'GETENV_EMPTY_FALLBACK', 'os.getenv com fallback vazio'),
    (r'os\.environ\.get\(["\'](\w+)["\'],\s*["\'](?!$)["\']', 'ENVIRON_EMPTY_FALLBACK', 'os.environ.get com fallback vazio'),
    # process.env sem fallback ou com fallback inseguro
    (r'process\.env\.(\w+)\s*\|\|\s*["\']https?://localhost', 'PROCESS_ENV_FALLBACK_LOCALHOST', 'process.env com fallback localhost'),
    (r'process\.env\.(\w+)\s*\|\|\s*["\']test-', 'PROCESS_ENV_FALLBACK_TEST', 'process.env com fallback test'),
]

def audit_file(filepath: Path) -> list:
    """Audita um unico arquivo e retorna lista de achados."""
    findings = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return findings
    
    lines = content.split('\n')
    rel_path = filepath.relative_to(BASE_DIR)
    
    for line_num, line in enumerate(lines, 1):
        # Secrets
        for pattern, finding_type, description in SECRET_PATTERNS:
            for match in re.finditer(pattern, line):
                value = match.group()
                if finding_type == 'CONTRACT_ADDRESS' and len(value) != 42:
                    continue
                if finding_type == 'PRIVATE_KEY_HEX':
                    if value.startswith('0x0000') or value == '0x' + '0' * 64:
                        continue
                findings.append({
                    'file': str(rel_path),
                    'line': line_num,
                    'type': finding_type,
                    'severity': 'CRITICAL' if finding_type in ('PRIVATE_KEY_HEX', 'PRIVATE_KEY_PEM', 'HARDCODED_SECRET') else 'HIGH',
                    'description': description,
                    'match': line.strip()[:120],
                    'value': value[:50],
                })
        
        # Docker URLs (apenas no frontend)
        if 'frontend' in str(rel_path):
            for pattern, finding_type, description in DOCKER_URL_PATTERNS:
                for match in re.finditer(pattern, line):
                    if 'next.config.js' in str(rel_path) and 'rewrites' in content:
                        continue
                    findings.append({
                        'file': str(rel_path),
                        'line': line_num,
                        'type': finding_type,
                        'severity': 'HIGH',
                        'description': description,
                        'match': line.strip()[:120],
                        'value': match.group()[:50],
                    })
        
        # Fallbacks
        for pattern, finding_type, description in FALLBACK_PATTERNS:
            for match in re.finditer(pattern, line):
                findings.append({
                    'file': str(rel_path),
                    'line': line_num,
                    'type': finding_type,
                    'severity': 'MEDIUM' if 'localhost' in finding_type else 'HIGH',
                    'description': description,
                    'match': line.strip()[:120],
                    'value': match.group()[:80],
                })
    
    return findings

def main():
    print("=" * 70)
    print("AUDITORIA DE SEGURANCA DE CODIGO - H2V-Trust")
    print("=" * 70)
    
    files = find_files()
    print(f"\n Escaneando {len(files)} arquivos...\n")
    
    all_findings = []
    for f in files:
        findings = audit_file(f)
        all_findings.extend(findings)
    
    # Agrupar por severidade
    by_severity = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
    for finding in all_findings:
        sev = finding['severity']
        if sev in by_severity:
            by_severity[sev].append(finding)
    
    # Relatorio
    print(f"\n{'='*70}")
    print(f"RESUMO: {len(all_findings)} achados")
    print(f"{'='*70}")
    for sev, items in by_severity.items():
        print(f"  {sev}: {len(items)}")
    
    print(f"\n{'='*70}")
    print("DETALHAMENTO")
    print(f"{'='*70}")
    
    for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        items = by_severity[sev]
        if not items:
            continue
        print(f"\n{'-'*70}")
        print(f" {sev} - {len(items)} ocorrencia(s)")
        print(f"{'-'*70}")
        
        for item in items:
            print(f"\n  Arquivo: {item['file']}:{item['line']}")
            print(f"     Tipo: {item['type']}")
            print(f"     Descricao: {item['description']}")
            print(f"     Codigo: {item['match']}")
            if item['value']:
                print(f"     Valor: {item['value']}")
    
    # Salvar JSON
    output = {
        'summary': {sev: len(items) for sev, items in by_severity.items()},
        'total': len(all_findings),
        'findings': all_findings,
    }
    output_path = BASE_DIR / 'audit_secrets_result.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n{'='*70}")
    print(f"Relatorio salvo em: {output_path}")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()

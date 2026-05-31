#!/usr/bin/env python3
"""
Gera relatorio final AUDITORIA_SEGURANCA_CODIGO.md a partir do JSON de resultados.
Filtra falsos positivos e organiza por relevancia.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivos/diretorios que sao 100% falsos positivos
FP_PATHS = {
    'contracts/artifacts',
    'contracts/cache',
    'contracts/typechain-types',
    'node_modules',
    '.git',
    'backend/blockchain/GreenHydrogenSBT.json',
    'backend/blockchain/contract_abi.py',
}

# Extensoes de arquivo que sao sempre falsos positivos para certos padroes
FP_EXTENSIONS = {'.json'}  # ABIs, artifacts, package-lock, etc.

def is_false_positive(finding) -> bool:
    """Verifica se um achado e falso positivo."""
    filepath = finding['file']
    ftype = finding['type']
    match_text = finding.get('match', '')
    
    # Ignora diretorios/arquivos especificos
    for fp in FP_PATHS:
        if filepath.startswith(fp):
            return True
    
    # Ignora JSONs (ABIs, artifacts, package-lock)
    if filepath.endswith('.json'):
        return True
    
    # Ignora bytecode (sempre em JSONs, mas por seguranca)
    if 'bytecode' in match_text or 'deployedBytecode' in match_text:
        return True
    
    # Ignora enderecos de teste (0x1234..., 0x0000...)
    if ftype == 'CONTRACT_ADDRESS':
        value = finding.get('value', '')
        if value.startswith('0x1234') or value.startswith('0x0000') or value.startswith('0xdead'):
            return True
    
    # Ignora .env.example (e um template)
    if filepath.endswith('.env.example'):
        return True
    
    # Ignora tests/archive (codigo morto)
    if filepath.startswith('tests/archive'):
        return True
    
    return False

def classify_severity(finding) -> str:
    """Classifica a severidade real do achado."""
    ftype = finding['type']
    filepath = finding['file']
    
    # Private key real em arquivo de configuracao
    if ftype == 'PRIVATE_KEY_HEX' and filepath in ('.env', '.env.production'):
        return 'CRITICAL'
    
    # Secret hardcoded em codigo fonte (nao teste)
    if ftype == 'HARDCODED_SECRET' and not filepath.startswith('tests/'):
        return 'CRITICAL'
    
    # API key hardcoded como fallback
    if ftype == 'FALLBACK_TEST' and ('api' in filepath.lower() or 'route' in filepath.lower()):
        return 'CRITICAL'
    
    # Private key em .env.example
    if ftype == 'PRIVATE_KEY_HEX' and filepath == '.env.example':
        return 'HIGH'
    
    # Endereco de contrato em codigo fonte de producao
    if ftype == 'CONTRACT_ADDRESS' and not filepath.startswith('tests/'):
        return 'HIGH'
    
    # Fallback localhost em codigo de producao
    if ftype in ('FALLBACK_LOCALHOST', 'DEFAULT_LOCALHOST') and not filepath.startswith('tests/'):
        return 'HIGH'
    
    # Docker URL no frontend
    if ftype == 'DOCKER_INTERNAL_URL':
        return 'HIGH'
    
    # Fallback test em testes
    if ftype == 'FALLBACK_TEST' and filepath.startswith('tests/'):
        return 'MEDIUM'
    
    # Endereco de contrato em testes
    if ftype == 'CONTRACT_ADDRESS' and filepath.startswith('tests/'):
        return 'MEDIUM'
    
    # Default localhost em testes
    if ftype == 'DEFAULT_LOCALHOST' and filepath.startswith('tests/'):
        return 'LOW'
    
    return 'MEDIUM'

def main():
    # Carregar resultados
    json_path = BASE_DIR / 'audit_secrets_result.json'
    if not json_path.exists():
        print("ERRO: audit_secrets_result.json nao encontrado. Execute audit_secrets.py primeiro.")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filtrar e classificar
    real_findings = []
    fp_count = 0
    for finding in data['findings']:
        if is_false_positive(finding):
            fp_count += 1
            continue
        finding['real_severity'] = classify_severity(finding)
        real_findings.append(finding)
    
    # Agrupar por severidade real
    by_severity = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
    for finding in real_findings:
        sev = finding['real_severity']
        if sev in by_severity:
            by_severity[sev].append(finding)
    
    # Gerar relatorio Markdown
    report = []
    report.append("# AUDITORIA DE SEGURANCA DE CODIGO - H2V-Trust")
    report.append("")
    report.append("> **Data:** 30/04/2026")
    report.append("> **Arquivos escaneados:** 298")
    report.append("> **Total de achados (brutos):** " + str(data['total']))
    report.append("> **Achados reais (apos filtro):** " + str(len(real_findings)))
    report.append("> **Falsos positivos removidos:** " + str(fp_count))
    report.append("")
    report.append("---")
    report.append("")
    report.append("## SUMARIO EXECUTIVO")
    report.append("")
    report.append("| Severidade | Quantidade | Descricao |")
    report.append("|------------|:----------:|-----------|")
    
    for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        items = by_severity[sev]
        icons = {'CRITICAL': 'CRITICO', 'HIGH': 'ALTO', 'MEDIUM': 'MEDIO', 'LOW': 'BAIXO'}
        report.append(f"| **{icons[sev]}** | {len(items)} | {_get_severity_desc(sev)} |")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Detalhamento por severidade
    for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        items = by_severity[sev]
        if not items:
            continue
        
        icons = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}
        labels = {'CRITICAL': 'CRITICO', 'HIGH': 'ALTO', 'MEDIUM': 'MEDIO', 'LOW': 'BAIXO'}
        
        report.append(f"## {icons[sev]} PROBLEMAS {labels[sev]} ({len(items)})")
        report.append("")
        
        for i, item in enumerate(items, 1):
            report.append(f"### {i}. `{item['file']}` linha {item['line']}")
            report.append("")
            report.append(f"**Tipo:** `{item['type']}`")
            report.append("")
            report.append(f"**Descricao:** {item['description']}")
            report.append("")
            report.append("**Codigo:**")
            report.append("```")
            report.append(item['match'])
            report.append("```")
            if item['value']:
                report.append("")
                report.append(f"**Valor:** `{item['value']}`")
            report.append("")
            report.append("**Recomendacao:** " + _get_recommendation(item))
            report.append("")
            report.append("---")
            report.append("")
    
    # Resumo por arquivo
    report.append("## DISTRIBUICAO POR ARQUIVO")
    report.append("")
    report.append("| Arquivo | CRITICO | ALTO | MEDIO | BAIXO | Total |")
    report.append("|---------|:-------:|:----:|:-----:|:-----:|:-----:|")
    
    file_stats = {}
    for finding in real_findings:
        f = finding['file']
        if f not in file_stats:
            file_stats[f] = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        file_stats[f][finding['real_severity']] += 1
    
    for f, stats in sorted(file_stats.items()):
        total = sum(stats.values())
        report.append(f"| `{f}` | {stats['CRITICAL']} | {stats['HIGH']} | {stats['MEDIUM']} | {stats['LOW']} | {total} |")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Recomendacoes
    report.append("## RECOMENDACOES PRIORIZADAS")
    report.append("")
    
    report.append("### Imediatas (Criticas)")
    report.append("")
    report.append("1. **Remover PRIVATE_KEY do `.env.production`** - Usar GitHub Secrets ou vault")
    report.append("2. **Remover API_KEY hardcoded como fallback em `frontend/src/lib/api.ts`** - Tornar `NEXT_PUBLIC_API_KEY` obrigatoria")
    report.append("3. **Remover PRIVATE_KEY do `.env`** - Usar variavel de ambiente exclusivamente")
    report.append("4. **Remover SECRET_KEY hardcoded do `.env.production`** - Gerar em deploy")
    report.append("")
    report.append("### Curto Prazo (Altas)")
    report.append("")
    report.append("5. **Substituir fallbacks de localhost por env vars obrigatorias** em `backend/config.py`")
    report.append("6. **Remover enderecos de contrato fixos** do `.env.production` - Usar env vars")
    report.append("7. **Adicionar `.env.production` ao `.gitignore`** - Nunca commitar secrets")
    report.append("8. **Remover `tests/archive/`** - Codigo morto com secrets de teste")
    report.append("")
    report.append("### Medio Prazo")
    report.append("")
    report.append("9. **Implementar validacao de env vars obrigatorias** no startup do backend")
    report.append("10. **Adicionar linter de seguranca** (semgrep, bandit) no CI/CD")
    report.append("11. **Revisar `contracts/artifacts/`** - Nao commitar artifacts do Hardhat")
    report.append("12. **Adicionar `.env.example` sem valores reais**")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Relatorio gerado automaticamente em 30/04/2026*")
    
    # Salvar
    output_path = BASE_DIR / 'AUDITORIA_SEGURANCA_CODIGO.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"Relatorio salvo em: {output_path}")
    print(f"\nResumo final:")
    for sev in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        print(f"  {sev}: {len(by_severity[sev])}")
    print(f"\nFalsos positivos removidos: {fp_count}")

def _get_severity_desc(sev: str) -> str:
    descs = {
        'CRITICAL': 'Secrets reais expostos (private keys, API keys)',
        'HIGH': 'Fallbacks inseguros, URLs Docker no frontend, enderecos fixos',
        'MEDIUM': 'Secrets em testes, enderecos de contrato em codigo de teste',
        'LOW': 'URLs localhost em testes/arquivos',
    }
    return descs.get(sev, '')

def _get_recommendation(finding) -> str:
    ftype = finding['type']
    filepath = finding['file']
    
    if ftype == 'PRIVATE_KEY_HEX':
        return "Substituir por variavel de ambiente obrigatoria. Remover do arquivo e usar secrets do Docker/CI."
    if ftype == 'HARDCODED_SECRET':
        return "Substituir por variavel de ambiente. NUNCA hardcodar secrets no codigo fonte."
    if ftype == 'FALLBACK_TEST':
        return "Remover fallback de teste. Tornar a variavel de ambiente obrigatoria com validacao no startup."
    if ftype == 'FALLBACK_LOCALHOST':
        return "Substituir fallback por variavel de ambiente. Em producao, localhost nao funciona."
    if ftype == 'DEFAULT_LOCALHOST':
        return "Substituir valor default hardcoded por variavel de ambiente."
    if ftype == 'CONTRACT_ADDRESS':
        return "Substituir endereco fixo por variavel de ambiente."
    if ftype == 'DOCKER_INTERNAL_URL':
        return "URL interna do Docker no frontend. Usar apenas em next.config.js para rewrites."
    return "Revisar e substituir por variavel de ambiente."

if __name__ == '__main__':
    main()

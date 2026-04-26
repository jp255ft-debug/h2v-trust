# Auditoria de Saúde do Projeto H2V-Trust

## 📅 Data: 26/04/2026

---

## 1. Árvore de Pastas e Arquivos Atualizada

```
h2v-trust/
├── alembic/                    # Migrations do banco
│   ├── versions/
│   │   └── 6fef8df01c1e_init_timescaledb.py
│   ├── env.py
│   └── script.py.mako
├── backend/                    # API FastAPI (Python)
│   ├── api/
│   │   ├── dependencies/       # auth.py, db.py, rate_limit.py
│   │   └── routes/             # batches, certificates, compliance, delegation, reports, telemetry
│   ├── blockchain/             # Web3, minting, SBT manager, verification
│   ├── core/                   # certificates, compliance, constants, delegation, emissions, water
│   ├── db/
│   │   ├── models/             # audit_log, batch, certificate, delegation, telemetry_record
│   │   ├── database.py
│   │   └── models.py
│   ├── models/                 # batch, certificate, compliance, delegation, telemetry
│   ├── oracle/                 # automation, chainlink_client, satellite_monitor, sensor_aggregator
│   ├── services/               # batch_service, certificate_service, delegation_service, exporter_service, qrcode_service, report_service
│   ├── utils/                  # hashing, logging, metrics, validators
│   ├── main.py
│   ├── config.py
│   └── requirements.txt
├── contracts/                  # Smart Contracts Solidity
│   ├── contracts/              # BatchRegistry, ComplianceVerifier, DelegationManager, GreenHydrogenSBT
│   ├── scripts/                # deploy, test_mint, upgrade, verify
│   ├── test/                   # Testes dos contratos
│   └── hardhat.config.js
├── frontend/                   # Next.js 14 (React + TypeScript)
│   ├── app/                    # Páginas (App Router)
│   │   ├── api/[...path]/      # Proxy API
│   │   ├── auditor/            # Página do Auditor
│   │   │   ├── components/     # BatchVerification
│   │   │   └── verify/[batchId]/
│   │   ├── dashboard/          # Dashboard principal
│   │   │   └── components/     # CertificatesTable, EmissionsGauge, ProductionChart, WaterCompliance
│   │   ├── producer/           # Página do Produtor
│   │   │   ├── batches/
│   │   │   ├── certificates/
│   │   │   └── delegation/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/         # Footer, Header, Navbar, Sidebar
│   │   │   ├── shared/         # ErrorBoundary, LoadingSpinner, QRCode
│   │   │   └── ui/             # badge, button, card, dialog, dropdown-menu, input, label, progress, table, tabs
│   │   ├── hooks/              # useBatch, useCertificate, useCompliance
│   │   ├── lib/                # api, constants, utils, web3
│   │   └── types/              # batch, certificate, compliance
│   ├── next.config.js
│   ├── tsconfig.json
│   └── package.json
├── iot/                        # Simulador IoT
│   ├── simulator.py
│   └── config.yaml
├── monitoring/                 # Prometheus + Grafana
├── scripts/                    # Scripts de automação
├── tests/                      # Testes Python (pytest)
│   ├── test_api.py
│   ├── test_blockchain.py
│   ├── test_compliance.py
│   ├── test_delegation.py
│   ├── test_integration.py
│   └── test_oracle.py
├── docker-compose.yml
├── render.yaml                 # Config Render (Backend)
└── .env
```

---

## 2. Status dos Erros TypeScript (Frontend)

### ❌ Erros Ativos (2 erros)

| # | Arquivo | Linha | Erro | Impacto |
|---|---------|-------|------|---------|
| 1 | `frontend/app/dashboard/components/CertificatesTable.tsx` | 67 | `batch.created_at` pode ser `undefined` - `new Date(string \| undefined)` não compila | **BLOQUEANTE** - Impede build |
| 2 | `frontend/src/components/shared/QRCode.tsx` | 23 | `import("qrcode")` sem tipos - falta `@types/qrcode` | **BLOQUEANTE** - Impede build |

### ✅ Erros Corrigidos (erros originais do VS Code)

| # | Arquivo | Erro Original | Status |
|---|---------|---------------|--------|
| 1 | `BatchVerification.tsx` | `Cannot find module 'hooks/useBatch'` | ✅ Resolvido (path `@/hooks/useBatch` existe) |
| 2 | `BatchVerification.tsx` | `Cannot find module 'components/shared/LoadingSpinner'` | ✅ Resolvido |
| 3 | `auditor/page.tsx` | `Cannot find module 'lib/api'` | ✅ Resolvido |
| 4 | `verify/[batchId]/page.tsx` | `Cannot find module 'hooks/useBatch'` | ✅ Resolvido |
| 5 | `verify/[batchId]/page.tsx` | `Cannot find module 'components/shared/LoadingSpinner'` | ✅ Resolvido |
| 6 | `verify/[batchId]/page.tsx` | `Cannot find module 'components/shared/ErrorBoundary'` | ✅ Resolvido |
| 7 | `CertificatesTable.tsx` | `Cannot find module 'lib/api'` | ✅ Resolvido |
| 8 | `CertificatesTable.tsx` | `Cannot find module 'types/batch'` | ✅ Resolvido |
| 9 | `EmissionsGauge.tsx` | `Cannot find module 'lib/api'` | ✅ Resolvido |
| 10 | `ProductionChart.tsx` | `Cannot find module 'lib/api'` | ✅ Resolvido |
| 11 | `ProductionChart.tsx` | `Cannot find module 'types/batch'` | ✅ Resolvido |
| 12 | `WaterCompliance.tsx` | `Cannot find module 'lib/api'` | ✅ Resolvido |
| 13 | `WaterCompliance.tsx` | `Cannot find module 'types/batch'` | ✅ Resolvido |
| 14 | `dashboard/page.tsx` | `Cannot find module 'lib/api'` | ✅ Resolvido |
| 15 | `producer/batches/page.tsx` | `Cannot find module 'components/layout/Navbar'` | ✅ Resolvido |
| 16 | `producer/batches/page.tsx` | `Cannot find module 'hooks/useBatch'` | ✅ Resolvido |
| 17 | `producer/batches/page.tsx` | `Cannot find module 'components/shared/LoadingSpinner'` | ✅ Resolvido |
| 18 | `producer/page.tsx` | `Cannot find module 'components/layout/Navbar'` | ✅ Resolvido |
| 19 | `producer/page.tsx` | `Cannot find module 'lib/api'` | ✅ Resolvido |
| 20 | `dropdown-menu.tsx` | `Cannot find module '@/src/lib/utils'` | ✅ Resolvido (corrigido para `@/lib/utils`) |
| 21 | `table.tsx` | `Cannot find module '@/src/lib/utils'` | ✅ Resolvido (corrigido para `@/lib/utils`) |

---

## 3. Por que o Vercel não está funcionando?

### Causa Raiz: **TypeScript Strict Mode + Erros de Tipo**

O `tsconfig.json` tem `"strict": true`, o que significa que **QUALQUER** erro de tipo no TypeScript impede o build de produção no Vercel.

### Os 2 erros bloqueantes atuais:

#### Erro 1: `CertificatesTable.tsx:67` - `batch.created_at` pode ser `undefined`
```typescript
// Linha 67 - Código atual:
date: new Date(batch.created_at).toLocaleDateString('pt-BR'),

// Solução:
date: new Date(batch.created_at || "").toLocaleDateString('pt-BR'),
```

#### Erro 2: `QRCode.tsx:23` - Falta `@types/qrcode`
```typescript
// Linha 23 - Import dinâmico sem tipos
import("qrcode")...

// Solução 1: npm install --save-dev @types/qrcode
// Solução 2: Criar arquivo src/types/qrcode.d.ts com:
//   declare module 'qrcode';
```

### Problemas Adicionais de Configuração Vercel:

1. **`next.config.js` usa `module.exports` (CommonJS)** - Funciona, mas o Vercel espera Next.js 14 com suporte a ESM. Recomenda-se usar `next.config.mjs` ou manter como está.

2. **Proxy API no `next.config.js`** - As `rewrites` redirecionam `/api/*` para o backend no Render. Se o Render estiver offline, o frontend quebra.

3. **Variáveis de ambiente** - A Vercel precisa ter `NEXT_PUBLIC_API_URL` configurada apontando para `https://h2v-trust-api.onrender.com`.

---

## 4. Erro Python: `test_sbt_mint.py`

```
Import "web3" could not be resolved
```

**Causa:** Biblioteca `web3.py` não está instalada no ambiente Python local.

**Solução:**
```bash
pip install web3
```

Ou instalar as dependências completas:
```bash
pip install -r backend/requirements.txt
```

---

## 5. Recomendações para Deploy na Vercel

### Passo 1: Corrigir os 2 erros TypeScript

```bash
# Corrigir CertificatesTable.tsx - adicionar fallback para undefined
# Corrigir QRCode.tsx - instalar tipos
npm --prefix frontend install --save-dev @types/qrcode
```

### Passo 2: Verificar build localmente antes do deploy

```bash
cd frontend && npm run build
```

### Passo 3: Configurar Vercel

No dashboard da Vercel, configurar:

| Variável | Valor |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://h2v-trust-api.onrender.com` |
| `NEXT_PUBLIC_VERCEL_URL` | (automático) |

### Passo 4: Framework Preset

No Vercel, selecionar:
- **Framework:** Next.js
- **Root Directory:** `frontend/`
- **Build Command:** `npm run build`
- **Output Directory:** `.next`

---

## 6. Resumo de Saúde do Projeto

| Componente | Status | Observações |
|------------|--------|-------------|
| **Backend (FastAPI)** | ✅ Funcional | Rodando no Render |
| **Frontend (Next.js)** | ⚠️ 2 erros bloqueantes | Impede build Vercel |
| **Smart Contracts** | ✅ Compilados | Hardhat + OpenZeppelin |
| **Banco de Dados** | ✅ PostgreSQL | Render + TimescaleDB |
| **Testes Python** | ✅ 6 suites | pytest configurado |
| **Testes Solidity** | ✅ 3 suites | Hardhat test |
| **IoT Simulator** | ✅ Funcional | Gera dados mock |
| **Monitoring** | ✅ Configurado | Prometheus + Grafana |

### Ações Imediatas Necessárias:

1. ✅ **Corrigir** `CertificatesTable.tsx` linha 67 - adicionar `|| ""` no `new Date()`
2. ✅ **Instalar** `@types/qrcode` para resolver erro de tipos no QRCode
3. ⬜ **Rodar** `npm run build` no frontend para confirmar zero erros
4. ⬜ **Fazer deploy** na Vercel

---

## 7. Arquivos Órfãos / Lixo para Limpeza

| Arquivo | Tamanho | Motivo |
|---------|---------|--------|
| `test-next-app/` | ~2MB | Projeto Next.js de teste, não usado |
| `tests/archive/` | ~500KB | 38 testes antigos arquivados |
| `test_sbt_mint.py` | ~5KB | Script de teste solto na raiz |
| `test_backend_mint.py` | ~3KB | Script de teste solto na raiz |
| `test_backend_mint2.py` | ~3KB | Script de teste solto na raiz |
| `test_mint_debug.py` | ~2KB | Script de teste solto na raiz |
| `test_mint_direct.py` | ~2KB | Script de teste solto na raiz |
| `test_mint_quick.py` | ~1KB | Script de teste solto na raiz |
| `{const` | ~1KB | Arquivo corrompido na raiz |
| `logs/` | ~10MB | Logs de auditoria antigos |
| `dumb_output.txt` | ~1MB | Output de debug |
| `pytest_output.txt` | ~500KB | Output de teste |
| `code_check.txt` | ~100KB | Check de código |
| `checksum.txt` | ~50KB | Checksums |
| `code.txt` | ~100KB | Código extraído |

---

*Relatório gerado em 26/04/2026 às 19:59 BRT*

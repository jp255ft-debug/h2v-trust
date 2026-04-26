# AUDITORIA COMPLETA DO PROJETO H2V-TRUST

## 📋 Sumário

1. [Estrutura de Diretórios](#1-estrutura-de-diretórios)
2. [Backend (FastAPI)](#2-backend-fastapi)
3. [Frontend (Next.js)](#3-frontend-nextjs)
4. [Contratos Solidity (Blockchain)](#4-contratos-solidity-blockchain)
5. [Infraestrutura (Docker)](#5-infraestrutura-docker)
6. [IoT / Simulador](#6-iot--simulador)
7. [Testes](#7-testes)
8. [Documentação](#8-documentação)
9. [Funcionalidades Completas](#9-funcionalidades-completas)

---

## 1. ESTRUTURA DE DIRETÓRIOS

```
h2v-trust/
├── alembic/                    # Migrations do banco de dados
│   └── versions/               # Versão inicial TimescaleDB
├── backend/                    # API FastAPI (Python)
│   ├── api/
│   │   ├── dependencies/       # Auth, DB, Rate Limit
│   │   └── routes/             # 6 módulos de rotas
│   ├── blockchain/             # Web3, Minting, SBT Manager
│   ├── core/                   # Lógica de negócio (CBAM, emissões, água)
│   ├── db/
│   │   └── models/             # ORM: Batch, Certificate, Telemetry, etc.
│   ├── models/                 # Pydantic schemas
│   ├── oracle/                 # Chainlink, satélite, sensores
│   ├── services/               # Batch, Certificate, Delegation, Report, QRCode
│   └── utils/                  # Hashing, logging, métricas, validadores
├── contracts/                  # Smart Contracts Solidity (Hardhat)
│   ├── contracts/              # 4 contratos + interfaces
│   ├── scripts/                # Deploy, upgrade, verify
│   └── test/                   # Testes JS dos contratos
├── docs/
│   └── audits/                 # Relatórios de auditoria anteriores
├── frontend/                   # Next.js 14 (TypeScript)
│   ├── app/
│   │   ├── api/[...path]/      # Proxy API
│   │   ├── auditor/            # Portal do Auditor
│   │   ├── dashboard/          # Dashboard principal
│   │   ├── producer/           # Portal do Produtor
│   │   └── ...                 # Páginas de teste/debug
│   └── src/
│       ├── components/         # UI (shadcn) + Layout + Shared
│       ├── hooks/              # useBatch, useCertificate, useCompliance
│       ├── lib/                # API client, Web3, constants
│       └── types/              # TypeScript types
├── iot/                        # Simulador IoT
├── monitoring/                 # Prometheus + Grafana
├── scripts/                    # Scripts utilitários
├── tests/                      # Testes Python (pytest)
│   └── archive/                # Testes antigos arquivados
└── docker-compose.yml          # Orquestração completa
```

---

## 2. BACKEND (FASTAPI)

### 2.1 Rotas da API (`/api/v1`)

| Rota | Método | Descrição |
|------|--------|-----------|
| **Telemetria** | | |
| `POST /telemetry` | POST | Ingestão de dados IoT + mint blockchain + compliance CBAM |
| **Batches** | | |
| `GET /batches` | GET | Listar lotes (com filtros: producer_id, compliant_only) |
| `GET /batches/{id}` | GET | Detalhes de um lote |
| `GET /batches/{id}/compliance` | GET | Relatório de compliance do lote |
| **Certificados** | | |
| `GET /certificates/{id}` | GET | Certificado + prova on-chain |
| `POST /certificates/{id}/consume` | POST | Consumir certificado (anti-double-counting) |
| **Compliance** | | |
| `GET /compliance/check/{batch_id}` | GET | Reavaliar compliance de lote |
| `POST /compliance/validate` | POST | Validar parâmetros contra CBAM |
| **Delegação** | | |
| `POST /delegation/authorize` | POST | Autorizar declarante CBAM |
| `GET /delegation/status/{producer_id}` | GET | Status da delegação |
| `POST /delegation/revoke` | POST | Revogar delegação |
| **Relatórios** | | |
| `GET /reports/cbam/{year}` | GET | Relatório CBAM anual |
| `GET /reports/cbam/{year}/download` | GET | Download (JSON/CSV) |
| **Health** | | |
| `GET /health` | GET | Health check |

### 2.2 Fluxo Principal (Ingestão de Telemetria)

```
Sensor IoT → POST /telemetry
  ├── A. Validar payload (Pydantic)
  ├── B. Avaliar regras CBAM (limite 3.4 kgCO₂e/kgH₂)
  ├── C. Se conforme → Mint SBT na blockchain (Hardhat)
  │     ├── Sucesso → token_id + tx_hash
  │     └── Falha → blockchain_status = "pending" (retry)
  └── D. Salvar no banco:
        ├── TelemetryRecord
        ├── Batch (com blockchain_status)
        └── Certificate (se mintado)
```

### 2.3 Módulos Core

| Módulo | Arquivo | Função |
|--------|---------|--------|
| **CBAM Compliance** | `core/compliance.py` | Verifica GHG < 3.4, fonte energia, água |
| **Emissões** | `core/emissions.py` | Cálculo de emissões GHG |
| **Água** | `core/water.py` | Verificação consumo hídrico |
| **Certificados** | `core/certificates.py` | Lógica de certificação |
| **Delegação** | `core/delegation.py` | Delegação CBAM |
| **Constantes** | `core/constants.py` | Limites e thresholds |

### 2.4 Blockchain Integration

| Arquivo | Função |
|---------|--------|
| `web3_client.py` | Conexão Web3 com Hardhat/Polygon |
| `minting.py` | Mint de SBTs na blockchain |
| `sbt_manager.py` | Gerenciamento de tokens SBT |
| `verification.py` | Verificação on-chain |
| `contract_abi.py` | ABIs dos contratos |

### 2.5 Oracle / IoT

| Arquivo | Função |
|---------|--------|
| `satellite_monitor.py` | Monitoramento via satélite |
| `sensor_aggregator.py` | Agregação de dados de sensores |
| `chainlink_client.py` | Integração Chainlink |
| `automation.py` | Automação de processos |

### 2.6 Serviços

| Serviço | Função |
|---------|--------|
| `batch_service.py` | CRUD de lotes |
| `certificate_service.py` | Gerenciamento de certificados + verificação on-chain |
| `delegation_service.py` | Delegação CBAM |
| `report_service.py` | Relatórios CBAM (JSON/CSV) |
| `qrcode_service.py` | Geração de QR Codes |
| `exporter_service.py` | Exportação de dados |

### 2.7 Dependências

- **Auth**: `X-API-Key` header
- **DB**: SQLAlchemy + TimescaleDB (ou SQLite para dev)
- **Rate Limit**: 1000 req/s configurável

---

## 3. FRONTEND (NEXT.JS 14)

### 3.1 Páginas

| Rota | Página | Descrição |
|------|--------|-----------|
| `/` | Landing | Página inicial com 3 cards (Blockchain, CBAM, Rastreabilidade) |
| `/dashboard` | Dashboard | Métricas, gráficos, tabela de certificados, status do sistema |
| `/auditor` | Auditor | Pesquisa de certificados, métricas de auditoria |
| `/auditor/verify/[batchId]` | Verificação | Verificação detalhada de lote |
| `/producer` | Produtor | Gestão de produção, lotes, certificados |
| `/producer/batches` | Lotes | Lista de lotes do produtor |
| `/producer/certificates` | Certificados | Certificados do produtor |
| `/producer/delegation` | Delegação | Gerenciar delegação CBAM |
| `/api/[...path]` | Proxy | Proxy para backend API |

### 3.2 Componentes

| Componente | Tipo | Descrição |
|------------|------|-----------|
| **Layout** | | |
| `Navbar` | Layout | Navegação principal |
| `Header` | Layout | Cabeçalho |
| `Footer` | Layout | Rodapé |
| `Sidebar` | Layout | Barra lateral |
| **Shared** | | |
| `ErrorBoundary` | Shared | Tratamento de erros |
| `LoadingSpinner` | Shared | Indicador de carregamento |
| `QRCode` | Shared | Gerador de QR Code |
| **UI (shadcn)** | | |
| `Button`, `Badge`, `Card` | UI | Componentes base |
| `Dialog`, `Tabs`, `Table` | UI | Componentes interativos |
| `Input`, `Label`, `Progress` | UI | Formulários |
| `DropdownMenu` | UI | Menus |
| **Dashboard** | | |
| `ProductionChart` | Dashboard | Gráfico de produção (Recharts) |
| `EmissionsGauge` | Dashboard | Medidor de emissões |
| `CertificatesTable` | Dashboard | Tabela de certificados |
| `WaterCompliance` | Dashboard | Conformidade hídrica |
| **Auditor** | | |
| `BatchVerification` | Auditor | Verificação de lote |
| `BlockchainProof` | Auditor | Prova blockchain |
| `ComplianceReport` | Auditor | Relatório de compliance |

### 3.3 Hooks

| Hook | Função |
|------|--------|
| `useBatch` | Operações com lotes |
| `useCertificate` | Operações com certificados |
| `useCompliance` | Verificações de compliance |

### 3.4 API Client (`lib/api.ts`)

| Função | Endpoint |
|--------|----------|
| `fetchHealth()` | `GET /health` |
| `fetchStats()` | Calculado de batches |
| `fetchBatches()` | `GET /batches` |
| `fetchBatch()` | `GET /batches/{id}` |
| `fetchBatchCompliance()` | `GET /batches/{id}/compliance` |
| `fetchCertificate()` | `GET /certificates/{id}` |
| `consumeCertificate()` | `POST /certificates/{id}/consume` |
| `checkCompliance()` | `GET /compliance/check/{batch_id}` |
| `authorizeDelegation()` | `POST /delegation/authorize` |
| `fetchDelegationStatus()` | `GET /delegation/status/{producer_id}` |
| `revokeDelegation()` | `POST /delegation/revoke` |
| `fetchCBAMReport()` | `GET /reports/cbam/{year}` |
| `sendTelemetry()` | `POST /telemetry` |

### 3.5 Dependências Principais

- **Next.js 14.2.3** + TypeScript
- **Tailwind CSS** + shadcn/ui
- **Recharts** (gráficos)
- **ethers** + **wagmi** + **viem** (Web3)
- **lucide-react** (ícones)
- **qrcode.react** (QR Code)

---

## 4. CONTRATOS SOLIDITY (BLOCKCHAIN)

### 4.1 Contratos

| Contrato | Descrição |
|----------|-----------|
| **GreenHydrogenSBT.sol** | Token Soulbound (ERC-721 não transferível) para certificados de H₂ verde |
| **BatchRegistry.sol** | Registro de lotes de produção na blockchain |
| **ComplianceVerifier.sol** | Verificação de conformidade CBAM on-chain |
| **DelegationManager.sol** | Gerenciamento de delegação de declarantes CBAM |

### 4.2 Interfaces

| Interface | Descrição |
|-----------|-----------|
| `IGreenHydrogenSBT` | Mint, burn, verificar SBT |
| `IBatchRegistry` | Registrar, consultar lotes |
| `IComplianceVerifier` | Verificar conformidade |
| `IDelegationManager` | Autorizar, revogar delegação |
| `IBasicGreenHydrogenSBT` | Versão simplificada |
| `IBasicBatchRegistry` | Versão simplificada |
| `IBasicComplianceVerifier` | Versão simplificada |

### 4.3 Testes

| Arquivo | Descrição |
|---------|-----------|
| `GreenHydrogenSBT.test.js` | Testes do token SBT |
| `BatchRegistry.test.js` | Testes do registro de lotes |
| `ComplianceVerifier.test.js` | Testes de verificação |
| `integration.test.js` | Testes de integração |

### 4.4 Scripts

| Script | Descrição |
|--------|-----------|
| `deploy.js` | Deploy dos contratos |
| `upgrade.js` | Upgrade de contratos |
| `verify.js` | Verificação no Etherscan |

---

## 5. INFRAESTRUTURA (DOCKER)

### 5.1 Serviços (`docker-compose.yml`)

| Serviço | Imagem | Porta | Função |
|---------|--------|-------|--------|
| **timescaledb** | timescale/timescaledb:latest-pg16 | 5432 | Banco de dados séries temporais |
| **redis** | redis:7-alpine | 6379 | Cache/filas |
| **hardhat** | node:18-alpine | 8545 | Blockchain local Ethereum |
| **backend** | Dockerfile (./backend) | 8000 | API FastAPI |
| **frontend** | Dockerfile (./frontend) | 3000 | Next.js |

### 5.2 Dockerfiles

- **backend/Dockerfile**: Python com dependências FastAPI
- **frontend/Dockerfile**: Node.js com Next.js

### 5.3 Monitoramento

| Recurso | Descrição |
|---------|-----------|
| `prometheus.yml` | Config Prometheus |
| `grafana/dashboards/h2v_trust.json` | Dashboard Grafana |
| `alerts/alert_rules.yml` | Regras de alerta |

---

## 6. IoT / SIMULADOR

| Arquivo | Descrição |
|---------|-----------|
| `iot/simulator.py` | Simulador de sensores IoT |
| `iot/config.yaml` | Configuração do simulador |
| `iot/data/sample_readings.json` | Leituras de exemplo |
| `iot/scripts/generate_mock_data.py` | Geração de dados mock |

---

## 7. TESTES

### 7.1 Testes Ativos (pytest)

| Arquivo | Descrição |
|---------|-----------|
| `tests/test_api.py` | Testes de API |
| `tests/test_blockchain.py` | Testes de blockchain |
| `tests/test_compliance.py` | Testes de compliance CBAM |
| `tests/test_delegation.py` | Testes de delegação |
| `tests/test_integration.py` | Testes de integração |
| `tests/test_oracle.py` | Testes de oracle |
| `tests/conftest.py` | Fixtures compartilhadas |

### 7.2 Testes Arquivados (39 scripts)

Testes históricos movidos para `tests/archive/`:
- Testes de API (simples, detalhados, finais)
- Testes de blockchain (minting, conexão)
- Testes de fluxo completo
- Testes de telemetria
- Testes de modelo
- Testes de relatório

---

## 8. DOCUMENTAÇÃO

| Documento | Descrição |
|-----------|-----------|
| `docs/architecture.md` | Arquitetura do sistema |
| `docs/api_reference.md` | Referência da API |
| `docs/cbam_compliance.md` | Guia de compliance CBAM |
| `docs/delegation_guide.md` | Guia de delegação |
| `docs/deployment.md` | Guia de deploy |
| `docs/namibia_reference.md` | Referência Namíbia |
| `docs/api_proxy_guide.md` | Guia do proxy API |
| `docs/audits/*` | Relatórios de auditoria anteriores |

---

## 9. FUNCIONALIDADES COMPLETAS

### ✅ Funcionalidades Implementadas

| # | Funcionalidade | Status | Componentes |
|---|---------------|--------|-------------|
| 1 | **Landing Page** | ✅ | Frontend: `/` |
| 2 | **Dashboard com Métricas** | ✅ | Frontend: `/dashboard` + 4 componentes |
| 3 | **Portal do Auditor** | ✅ | Frontend: `/auditor` + verificação |
| 4 | **Portal do Produtor** | ✅ | Frontend: `/producer` + lotes + certificados + delegação |
| 5 | **Ingestão de Telemetria IoT** | ✅ | Backend: `POST /telemetry` |
| 6 | **Verificação CBAM** | ✅ | Backend: `core/compliance.py` (limite 3.4) |
| 7 | **Mint de SBT na Blockchain** | ✅ | Backend: `blockchain/minting.py` |
| 8 | **Certificados com Prova On-Chain** | ✅ | Backend: `GET /certificates/{id}` |
| 9 | **Anti-Double-Counting** | ✅ | Backend: `POST /certificates/{id}/consume` |
| 10 | **Delegação CBAM** | ✅ | Backend: 3 endpoints + `DelegationManager.sol` |
| 11 | **Relatórios CBAM Anuais** | ✅ | Backend: `GET /reports/cbam/{year}` (JSON/CSV) |
| 12 | **QR Code em Certificados** | ✅ | Backend: `qrcode_service.py` |
| 13 | **Audit Log** | ✅ | Backend: `AuditLog` model |
| 14 | **Rate Limiting** | ✅ | Backend: `dependencies/rate_limit.py` |
| 15 | **Autenticação via API Key** | ✅ | Backend: `dependencies/auth.py` |
| 16 | **Proxy API Frontend** | ✅ | Frontend: `app/api/[...path]/route.ts` |
| 17 | **Simulador IoT** | ✅ | `iot/simulator.py` |
| 18 | **Oracle / Satélite** | ✅ | Backend: `oracle/` |
| 19 | **Monitoramento Prometheus/Grafana** | ✅ | `monitoring/` |
| 20 | **Migrations TimescaleDB** | ✅ | `alembic/` |
| 21 | **Docker Compose Completo** | ✅ | 5 serviços |
| 22 | **Contratos Solidity (4)** | ✅ | SBT + Batch + Compliance + Delegation |
| 23 | **Testes Python (6 suites)** | ✅ | `tests/` |
| 24 | **Testes JS Contratos (4 suites)** | ✅ | `contracts/test/` |
| 25 | **Gráficos Recharts** | ✅ | Dashboard + Produtor |
| 26 | **UI shadcn** | ✅ | 10 componentes base |
| 27 | **Web3 Integration (wagmi/ethers)** | ✅ | `lib/web3.ts` |
| 28 | **Hooks React** | ✅ | useBatch, useCertificate, useCompliance |
| 29 | **Error Boundary** | ✅ | `components/shared/ErrorBoundary.tsx` |
| 30 | **Loading States** | ✅ | `components/shared/LoadingSpinner.tsx` |

### 🔧 Próximos Passos Recomendados

1. **Iniciar Backend**: `cd backend && uvicorn main:app --reload`
2. **Iniciar Blockchain**: `cd contracts && npx hardhat node`
3. **Fazer deploy dos contratos**: `npx hardhat run scripts/deploy.js --network localhost`
4. **Testar integração completa**: Frontend + Backend + Blockchain
5. **Configurar banco PostgreSQL/TimescaleDB** (ou usar SQLite para dev)
6. **Rodar testes**: `pytest tests/ -v`

---

*Auditoria gerada em 23/04/2026 às 20:57 BRT*

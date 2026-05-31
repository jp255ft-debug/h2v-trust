# 📋 Relatório Completo do Projeto H2V-Trust

## 🌿 Plataforma de Rastreabilidade Blockchain para Hidrogênio Verde

> **Data de atualização:** 27/04/2026
> **Versão:** MVP (Fase 1 Concluída)

---

## 1. ÁRVORE COMPLETA DO PROJETO

```
h2v-trust/
│
├── 📁 backend/                          # API FastAPI (Python 3.11+)
│   ├── main.py                          # Ponto de entrada da API
│   ├── config.py                        # Configurações centralizadas
│   ├── Dockerfile                       # Container da API (dev)
│   ├── Dockerfile.prod                  # Container da API (prod)
│   ├── requirements.txt                 # Dependências Python
│   ├── requirements.prod.txt            # Dependências produção
│   ├── requirements-minimal.txt         # Dependências mínimas
│   ├── requirements.dev.txt             # Dependências desenvolvimento
│   │
│   ├── 📁 api/                          # Rotas REST
│   │   ├── __init__.py
│   │   └── 📁 routes/
│   │       ├── __init__.py
│   │       ├── telemetry.py             # Ingestão de dados IoT
│   │       ├── batches.py               # Gerenciamento de lotes
│   │       ├── certificates.py          # Certificação de lotes
│   │       ├── compliance.py            # Verificação CBAM
│   │       ├── delegation.py            # Delegação CBAM
│   │       └── reports.py               # Relatórios CBAM
│   │   └── 📁 dependencies/
│   │       ├── __init__.py
│   │       ├── auth.py                  # Autenticação
│   │       ├── db.py                    # Dependência de banco
│   │       └── rate_limit.py            # Rate limiting
│   │
│   ├── 📁 core/                         # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── constants.py                 # Constantes CBAM 2026
│   │   ├── compliance.py                # Verificador de compliance
│   │   ├── emissions.py                 # Cálculo de emissões
│   │   ├── water.py                     # Conformidade hídrica
│   │   ├── certificates.py              # Geração de certificados
│   │   └── delegation.py                # Gestão de delegação
│   │
│   ├── 📁 blockchain/                   # Integração blockchain
│   │   ├── __init__.py
│   │   ├── web3_client.py               # Cliente Web3
│   │   ├── contract_abi.py              # ABIs dos contratos
│   │   ├── minting.py                   # Mint de SBTs
│   │   ├── sbt_manager.py               # Gerenciador SBT
│   │   ├── verification.py              # Verificação on-chain
│   │   └── GreenHydrogenSBT.json        # ABI do contrato
│   │
│   ├── 📁 oracle/                       # Oráculos e dados externos
│   │   ├── __init__.py
│   │   ├── satellite_monitor.py         # Monitoramento por satélite
│   │   ├── automation.py                # Automação de tarefas
│   │   ├── chainlink_client.py          # Cliente Chainlink
│   │   └── sensor_aggregator.py         # Agregador de sensores
│   │
│   ├── 📁 db/                           # Banco de dados
│   │   ├── __init__.py
│   │   ├── database.py                  # Conexão TimescaleDB
│   │   ├── models.py                    # Modelos ORM
│   │   └── 📁 models/
│   │       ├── __init__.py
│   │       ├── batch.py                 # Modelo de lote
│   │       ├── certificate.py           # Modelo de certificado
│   │       ├── telemetry_record.py      # Modelo de telemetria
│   │       ├── audit_log.py             # Log de auditoria
│   │       └── delegation.py            # Modelo de delegação
│   │
│   ├── 📁 models/                       # Modelos Pydantic
│   │   ├── __init__.py
│   │   ├── batch.py
│   │   ├── certificate.py
│   │   ├── compliance.py
│   │   ├── delegation.py
│   │   └── telemetry.py
│   │
│   ├── 📁 services/                     # Serviços de negócio
│   │   ├── __init__.py
│   │   ├── batch_service.py             # Serviço de lotes
│   │   ├── certificate_service.py       # Serviço de certificados
│   │   ├── delegation_service.py        # Serviço de delegação
│   │   ├── report_service.py            # Geração de relatórios
│   │   ├── exporter_service.py          # Exportação de dados
│   │   └── qrcode_service.py            # Geração de QR Codes
│   │
│   ├── 📁 utils/                        # Utilitários
│   │   ├── __init__.py
│   │   ├── hashing.py                   # Funções de hash
│   │   ├── logging.py                   # Configuração de logs
│   │   ├── metrics.py                   # Métricas Prometheus
│   │   └── validators.py               # Validadores
│   │
│   └── 📁 tests/                        # Testes do backend
│       └── __init__.py
│
├── 📁 contracts/                        # Smart Contracts Solidity
│   ├── hardhat.config.js                # Config Hardhat
│   ├── package.json                     # Dependências Node
│   ├── .env                             # Variáveis de ambiente
│   ├── .env.example                     # Exemplo de env
│   ├── check_balance.js                 # Script de consulta
│   │
│   ├── 📁 contracts/                    # Código fonte Solidity
│   │   ├── GreenHydrogenSBT.sol         # Token Soulbound (SBT)
│   │   ├── BatchRegistry.sol            # Registro de lotes
│   │   ├── ComplianceVerifier.sol       # Verificação on-chain
│   │   ├── DelegationManager.sol        # Gestão de delegação
│   │   ├── IBatchRegistry.sol           # Interface BatchRegistry
│   │   ├── IComplianceVerifier.sol      # Interface ComplianceVerifier
│   │   ├── IDelegationManager.sol       # Interface DelegationManager
│   │   ├── IGreenHydrogenSBT.sol        # Interface GreenHydrogenSBT
│   │   └── 📁 interfaces/               # Interfaces simplificadas
│   │       ├── IBasicBatchRegistry.sol
│   │       ├── IBasicComplianceVerifier.sol
│   │       └── IBasicGreenHydrogenSBT.sol
│   │
│   ├── 📁 scripts/                      # Scripts de deploy
│   │   ├── deploy.js                    # Deploy dos contratos
│   │   ├── test_mint.js                 # Teste de mint
│   │   ├── upgrade.js                   # Upgrade de contratos
│   │   └── verify.js                    # Verificação em explorer
│   │
│   ├── 📁 test/                         # Testes dos contratos
│   │   ├── GreenHydrogenSBT.test.js
│   │   ├── BatchRegistry.test.js
│   │   ├── ComplianceVerifier.test.js
│   │   └── integration.test.js
│   │
│   ├── 📁 artifacts/                    # Artefatos compilados
│   │   ├── 📁 contracts/                # ABIs e bytecodes
│   │   └── 📁 @openzeppelin/            # Dependências OpenZeppelin
│   │
│   └── 📁 cache/                        # Cache de compilação
│
├── 📁 frontend/                         # Next.js 14 + TypeScript
│   ├── next.config.js                   # Config Next.js
│   ├── package.json                     # Dependências
│   ├── tsconfig.json                    # Config TypeScript
│   ├── tailwind.config.js               # Config Tailwind
│   ├── postcss.config.js                # Config PostCSS
│   ├── Dockerfile                       # Container (dev)
│   ├── Dockerfile.prod                  # Container (prod)
│   ├── .env.local                       # Variáveis de ambiente
│   ├── .nvmrc                           # Versão Node
│   │
│   ├── 📁 app/                          # App Router (Next.js 14)
│   │   ├── layout.tsx                   # Layout principal
│   │   ├── page.tsx                     # Landing page
│   │   ├── globals.css                  # Estilos globais
│   │   │
│   │   ├── 📁 dashboard/                # Dashboard principal
│   │   │   ├── page.tsx                 # Dashboard com métricas
│   │   │   ├── page-simple.tsx          # Versão simplificada
│   │   │   ├── test-page.tsx            # Página de teste
│   │   │   └── 📁 components/
│   │   │       ├── ProductionChart.tsx   # Gráfico de produção
│   │   │       ├── EmissionsGauge.tsx    # Medidor de emissões
│   │   │       ├── CertificatesTable.tsx # Tabela de certificados
│   │   │       └── WaterCompliance.tsx   # Conformidade hídrica
│   │   │
│   │   ├── 📁 auditor/                  # Portal do Auditor
│   │   │   ├── page.tsx                 # Página principal
│   │   │   ├── page-backup.tsx          # Backup da página
│   │   │   ├── 📁 components/
│   │   │   │   └── BatchVerification.tsx # Verificação de lotes
│   │   │   └── 📁 verify/[batchId]/
│   │   │       └── page.tsx             # Verificação individual
│   │   │
│   │   ├── 📁 producer/                 # Portal do Produtor
│   │   │   ├── page.tsx                 # Página principal
│   │   │   ├── 📁 batches/
│   │   │   │   └── page.tsx             # Gerenciamento de lotes
│   │   │   ├── 📁 certificates/
│   │   │   │   └── page.tsx             # Certificados
│   │   │   └── 📁 delegation/
│   │   │       └── page.tsx             # Delegação CBAM
│   │   │
│   │   ├── 📁 api/                      # API Proxy
│   │   │   └── [...path]/route.ts       # Proxy para backend
│   │   │
│   │   ├── 📁 debug/
│   │   │   └── page.tsx                 # Página de debug
│   │   ├── 📁 test/
│   │   │   └── page.tsx                 # Página de teste
│   │   └── 📁 simple/
│   │       └── page.tsx                 # Página simples
│   │
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── 📁 layout/               # Componentes de layout
│   │   │   │   ├── Navbar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── Sidebar.tsx
│   │   │   ├── 📁 shared/               # Componentes compartilhados
│   │   │   │   ├── ErrorBoundary.tsx
│   │   │   │   ├── LoadingSpinner.tsx
│   │   │   │   └── QRCode.tsx
│   │   │   └── 📁 ui/                   # Componentes UI (shadcn)
│   │   │       ├── badge.tsx
│   │   │       ├── button.tsx
│   │   │       ├── card.tsx
│   │   │       ├── dialog.tsx
│   │   │       ├── dropdown-menu.tsx
│   │   │       ├── input.tsx
│   │   │       ├── label.tsx
│   │   │       ├── progress.tsx
│   │   │       ├── table.tsx
│   │   │       └── tabs.tsx
│   │   │
│   │   ├── 📁 hooks/                    # React Hooks
│   │   │   ├── index.ts
│   │   │   ├── useBatch.ts              # Hook de lotes
│   │   │   ├── useCertificate.ts        # Hook de certificados
│   │   │   ├── useCompliance.ts         # Hook de compliance
│   │   │   └── 📁 example/
│   │   │       └── HookExample.tsx
│   │   │
│   │   ├── 📁 lib/                      # Utilitários
│   │   │   ├── api.ts                   # Cliente API
│   │   │   ├── web3.ts                  # Conexão Web3
│   │   │   ├── constants.ts             # Constantes
│   │   │   └── utils.ts                 # Utilitários gerais
│   │   │
│   │   └── 📁 types/                    # Tipos TypeScript
│   │       ├── index.ts
│   │       ├── batch.ts
│   │       ├── certificate.ts
│   │       └── compliance.ts
│   │
│   └── 📁 tests/                        # Testes do frontend
│       └── __init__.py
│
├── 📁 iot/                              # Simulador IoT
│   ├── simulator.py                     # Simulador de sensores
│   ├── config.yaml                      # Configuração dos sensores
│   ├── __init__.py
│   ├── 📁 data/
│   │   └── sample_readings.json         # Leituras de exemplo
│   └── 📁 scripts/
│       └── generate_mock_data.py        # Geração de dados mock
│
├── 📁 monitoring/                       # Monitoramento
│   ├── prometheus.yml                   # Config Prometheus
│   ├── __init__.py
│   ├── 📁 alerts/
│   │   └── alert_rules.yml             # Regras de alerta
│   └── 📁 grafana/
│       ├── __init__.py
│       ├── 📁 dashboards/
│       │   └── h2v_trust.json          # Dashboard Grafana
│       └── 📁 datasources/
│           └── __init__.py
│
├── 📁 nginx/                            # Proxy reverso
│   ├── nginx.conf                       # Configuração Nginx
│   └── 📁 ssl/
│       └── .gitkeep                     # Certificados SSL
│
├── 📁 scripts/                          # Scripts utilitários
│   ├── __init__.py
│   ├── init_db.py                       # Inicialização do banco
│   ├── seed_data.py                     # Dados de exemplo
│   ├── deploy_contracts.sh              # Deploy de contratos
│   ├── generate_tree.py                 # Gerador de árvore
│   ├── create_cbam_report.py            # Relatório CBAM
│   ├── analyze_repo.py                  # Análise do repositório
│   ├── audit_state.py                   # Auditoria de estado
│   ├── check_imports.py                 # Verificação de imports
│   ├── final_check.py                   # Verificação final
│   ├── fix_imports.py                   # Correção de imports
│   ├── scan_repo.py                     # Escaneamento do repo
│   ├── simple_check.py                  # Verificação simples
│   ├── start_backend_test.py            # Início de teste backend
│   ├── test_compliance.py               # Teste de compliance
│   ├── dump_tree.py                     # Dump da árvore
│   └── count_stats.py                   # Estatísticas do projeto
│
├── 📁 tests/                            # Testes automatizados
│   ├── conftest.py                      # Configuração pytest
│   ├── test_api.py                      # Testes de API
│   ├── test_blockchain.py               # Testes blockchain
│   ├── test_compliance.py               # Testes compliance
│   ├── test_delegation.py               # Testes delegação
│   ├── test_integration.py              # Testes integração
│   ├── test_oracle.py                   # Testes oráculo
│   └── 📁 archive/                      # Testes arquivados
│       ├── test_account_balance.py
│       ├── test_api_clean.py
│       ├── test_api_detailed.py
│       ├── test_api_route.py
│       ├── test_api_simple.py
│       ├── test_backend.py
│       ├── test_batch_service.py
│       ├── test_blockchain_connection.py
│       ├── test_complete_flow.py
│       ├── test_db.py
│       ├── test_db_connection.py
│       ├── test_delegation_import.py
│       ├── test_direct_mock.py
│       ├── test_e2e.py
│       ├── test_e2e_simple.py
│       ├── test_fix_final.py
│       ├── test_flow.py
│       ├── test_flow_fixed.py
│       ├── test_import.py
│       ├── test_minting_direct.py
│       ├── test_minting_simple.py
│       ├── test_model.py
│       ├── test_model_simple.py
│       ├── test_post.py
│       ├── test_report_fix_simple.py
│       ├── test_report_service.py
│       ├── test_simple.py
│       ├── test_simulator_connection.py
│       ├── test_system_ascii.py
│       ├── test_system_working.py
│       ├── test_telemetry.py
│       ├── test_telemetry_detailed.py
│       ├── test_telemetry_detailed_final.py
│       └── tmp_test_satellite.py
│
├── 📁 docs/                             # Documentação
│   ├── architecture.md                  # Arquitetura do sistema
│   ├── api_reference.md                 # Referência da API
│   ├── api_proxy_guide.md               # Guia do proxy API
│   ├── cbam_compliance.md               # Guia CBAM
│   ├── delegation_guide.md              # Guia de delegação
│   ├── deployment.md                    # Guia de deploy
│   └── namibia_reference.md             # Modelo Namíbia
│
├── 📁 alembic/                          # Migrações de banco
│   ├── env.py                           # Config Alembic
│   ├── README                           # Instruções Alembic
│   ├── script.py.mako                   # Template de migração
│   └── 📁 versions/
│       └── 6fef8df01c1e_init_timescaledb.py  # Migração inicial
│
├── 📁 logs/                             # Logs e outputs
│   ├── audit_results.json
│   ├── auditoria_resultado.txt
│   ├── backend_files_nonempty.json
│   ├── empty_files.txt
│   ├── frontend_files.json
│   ├── frontend_files.txt
│   ├── frontend_files_nonempty.json
│   ├── frontend_tree.txt
│   ├── frontend_tree_clean.txt
│   ├── scan_results.txt
│   ├── tree_frontend.txt
│   └── ... (outros logs)
│
├── docker-compose.yml                   # Orquestração Docker (dev)
├── docker-compose.prod.yml              # Docker produção
├── Makefile                             # Comandos make
├── alembic.ini                          # Config Alembic
├── render.yaml                          # Config Render.com
├── .env                                 # Variáveis de ambiente
├── .env.example                         # Exemplo de env
├── .env.production                      # Env produção
├── .gitignore                           # Git ignore
├── LICENSE                              # Licença MIT
├── README.md                            # Documentação principal
│
├── 📁 test-next-app/                    # App Next.js de teste
│
├── 📁 raiz/                             # Scripts de teste na raiz
│   ├── test_backend_mint.py
│   ├── test_backend_mint2.py
│   ├── test_mint_debug.py
│   ├── test_mint_direct.py
│   ├── test_mint_quick.py
│   ├── test_sbt_mint.py
│   ├── backup_h2v_20260427.sql
│   ├── relatorio.pdf
│   ├── test_cbam.pdf
│   └── ... (outros arquivos de output)
│
└── 📁 relatórios de auditoria/
    ├── AUDITORIA_COMPLETA.md
    ├── AUDITORIA_SAUDE_PROJETO.md
    ├── RELATORIO_AUDITORIA_PRODUCAO.md
    ├── RELATORIO_DE_TESTES_FUNCIONALIDADES.md
    └── RELATORIO_PROJETO.md
```

---

## 2. VISÃO GERAL DO PROJETO

**H2V-Trust** é uma plataforma de certificação blockchain para hidrogênio verde (H₂V) com conformidade com o **CBAM 2026** (Carbon Border Adjustment Mechanism) da União Europeia. O sistema utiliza **Soulbound Tokens (SBT)** não-transferíveis para prevenir double counting e garantir rastreabilidade completa da produção à exportação.

### 🎯 Objetivos Principais
- ✅ Certificar hidrogênio verde com verificação automática de compliance CBAM
- ✅ Prevenir fraudes e double counting via blockchain
- ✅ Integrar dados IoT de sensores de produção em tempo real
- ✅ Gerar relatórios CBAM automaticamente
- ✅ Suportar delegação para Declarantes Delegados CBAM
- ✅ Monitoramento por satélite (modelo Namíbia)

---

## 3. ESTATÍSTICAS DO PROJETO

| Métrica | Valor |
|---------|-------|
| **Total de arquivos** | **282** |
| **Total de linhas de código** | **~19.378** |
| **Arquivos Python** | 145 |
| **Arquivos TypeScript/TSX** | 54 |
| **Smart Contracts Solidity** | 14 (4 contratos + interfaces) |
| **Arquivos JavaScript** | 13 |
| **Documentos Markdown** | 28 |
| **Arquivos YAML** | 6 |
| **Arquivos CSS** | 1 |
| **Dockerfiles** | 4 |
| **Arquivos JSON** | 14 |
| **Shell Scripts** | 1 |
| **Arquivos de Configuração** | 2 |

---

## 4. FUNCIONALIDADES DETALHADAS

### 4.1 🔙 Backend (FastAPI)

#### API REST (`backend/api/routes/`) — Rotas Reais (Testadas)

| Rota | Endpoint | Método | Descrição | Status |
|------|----------|--------|-----------|--------|
| **Telemetria** | `/api/v1/telemetry` | `POST` | Ingestão de dados de sensores IoT (cria lote automaticamente) | ✅ |
| | `/api/v1/telemetry/{sensor_id}` | `GET` | Histórico de telemetria por sensor | ✅ |
| **Lotes** | `/api/v1/batches` | `GET` | Listar lotes (filtros: `producer_id`, `compliant_only`, `skip`, `limit`) | ✅ |
| | `/api/v1/batches/{batch_id}` | `GET` | Detalhes do lote (ex: `batch_001`) | ✅ |
| **Certificados** | `/api/v1/certificates/{certificate_id}` | `GET` | Verificar certificado por ID (ex: `1000`) | ✅ |
| | `/api/v1/certificates/{certificate_id}/consume` | `POST` | Consumir certificado (prevenir double counting) | ✅ |
| **Compliance** | `/api/v1/compliance/check/{batch_id}` | `GET` | Verificar compliance CBAM de um lote | ✅ |
| **Delegação** | `/api/v1/delegation/authorize` | `POST` | Autorizar declarante delegado CBAM | ✅ |
| | `/api/v1/delegation/status/{producer_id}` | `GET` | Status da delegação | ✅ |
| | `/api/v1/delegation/revoke` | `POST` | Revogar delegação | ✅ |
| **Relatórios** | `/api/v1/reports/cbam/{year}` | `GET` | Relatório CBAM anual (ex: `2026`) | ✅ |
| | `/api/v1/reports/cbam/{year}/download` | `GET` | Download do relatório (PDF/CSV) | ✅ |

> **Nota:** Lotes são criados indiretamente via `POST /api/v1/telemetry`. Não existe `POST /api/v1/batches` nem `GET /api/v1/certificates` (lista). A certificação (mint SBT) ocorre automaticamente durante o fluxo de telemetria.

#### Core de Negócio (`backend/core/`)

**1. Compliance CBAM (`compliance.py`)**
- `CBAMComplianceChecker` - Classe principal de verificação
- `check_ghg_emissions()` - Verifica limite de 3.4 kgCO₂e/kgH₂
- `check_water_compliance()` - Verifica Diretiva-Quadro da Água
- `check_energy_source()` - Verifica fonte 100% renovável (RFNBO)
- `check_additionality()` - Verifica adicionalidade RFNBO
- `full_compliance_check()` - Executa todas as verificações consolidadas

**2. Emissões (`emissions.py`)**
- `EmissionsCalculator` - Calculadora de emissões
- `calculate_emissions_intensity()` - Intensidade por fonte de energia
- `calculate_carbon_footprint()` - Pegada de carbono do lote
- `estimate_cbam_penalty()` - Estimativa de multa CBAM (€50/ton CO₂)
- Fatores de emissão: wind(0.011), solar(0.045), hydro(0.024), grid(0.5) kgCO₂/kWh

**3. Água (`water.py`)**
- `WaterComplianceChecker` - Verificador de conformidade hídrica
- `check_water_consumption()` - Consumo máximo 20 L/kgH₂
- `calculate_water_efficiency()` - Eficiência vs mínimo teórico (9 L/kgH₂)
- `assess_water_risk()` - Avaliação de risco hídrico (0-10)
- `estimate_water_footprint()` - Pegada hídrica total (inclui água virtual)

**4. Certificados (`certificates.py`)**
- `CertificateGenerator` - Geração de certificados
- `generate_certificate_id()` - ID único via SHA-256
- `generate_qr_code_data()` - Dados para QR Code
- `create_certificate_data()` - Estrutura completa do certificado
- `CertificateVerifier` - Verificação de autenticidade
- `verify_certificate_chain()` - Verificação da cadeia telemetria → lote → certificado
- `generate_verification_report()` - Relatório com trust score (0-100)

**5. Delegação (`delegation.py`)**
- `DelegationManager` - Gestão de delegação CBAM
- `create_delegation()` - Criar delegação (validade: 365 dias)
- `validate_delegation()` - Validar delegação
- `check_authorization()` - Verificar autorização para ação específica
- `revoke_delegation()` - Revogar delegação
- `generate_delegation_proof()` - Prova de delegação para blockchain

**6. Constantes (`constants.py`)**
- Limite CBAM: **3.4 kgCO₂e/kgH₂**
- Multa CBAM: **€50/ton CO₂** excedente
- Consumo água máx: **20 L/kgH₂**
- Fontes água permitidas: desalination, treated_wastewater, surface_water, groundwater, recycled
- Fontes renováveis: wind, solar, hydro, biomass

#### Blockchain (`backend/blockchain/`)

- `web3_client.py` - Cliente Web3 para conexão com Polygon/Hardhat
- `contract_abi.py` - ABIs dos contratos inteligentes
- `minting.py` - Mint de Soulbound Tokens (SBT) na blockchain
- `sbt_manager.py` - Gerenciamento de SBTs
- `verification.py` - Verificação on-chain de certificados

#### Oráculo (`backend/oracle/`)

- `satellite_monitor.py` - **Monitoramento por satélite** (modelo Namíbia)
  - `get_co2_data()` - Dados de CO₂ por localização
  - `get_water_data()` - Qualidade/disponibilidade de água
  - `get_renewable_energy_production()` - Verificação de energia renovável
  - `verify_additionality()` - Verificação de adicionalidade via satélite
- `automation.py` - Automação de tarefas periódicas
- `chainlink_client.py` - Integração com Chainlink Oracle
- `sensor_aggregator.py` - Agregação de dados de sensores

#### Banco de Dados (`backend/db/`)

- **TimescaleDB** - Banco de séries temporais para telemetria
- Modelos: batch, certificate, telemetry_record, audit_log, delegation
- Migrações via Alembic

---

### 4.2 ⛓️ Smart Contracts (Solidity)

#### GreenHydrogenSBT.sol
- **Token Soulbound (não-transferível)** baseado em ERC-721
- Estrutura `CertificateData`: batchId, producer, timestamp, sizeKg, ghgEmissions, waterConsumption, isCompliant, complianceHash, isConsumed
- `mintCertificate()` - Emite novo certificado SBT
- `consumeCertificate()` - Consome certificado (previne double counting)
- `isValidCertificate()` - Verifica validade
- `calculateCarbonSavings()` - Calcula economia de CO₂ vs H₂ cinza
- Override de `transferFrom()` e `safeTransferFrom()` para prevenir transferências

#### BatchRegistry.sol
- Registro descentralizado de lotes de produção

#### ComplianceVerifier.sol
- Verificação on-chain de limites de emissão
- Integração com oráculos para dados externos

#### DelegationManager.sol
- Gestão de autorizações para Delegated CBAM Declarant

---

### 4.3 🎨 Frontend (Next.js 14 + TypeScript)

#### Páginas Principais

**Landing Page (`/`)**
- Apresentação institucional
- Links para Dashboard, Auditor e Produtor
- Cards destacando: Blockchain Imutável, CBAM 2026 Ready, Rastreabilidade Total

**Dashboard (`/dashboard`)**
- **Métricas**: Certificados emitidos, Conformidade CBAM, Emissões médias, Consumo de água
- **Gráficos**: ProductionChart (Recharts), EmissionsGauge, WaterCompliance
- **Tabela**: CertificatesTable com lotes recentes
- **Status do Sistema**: Frontend, Backend, Blockchain
- Fallback para dados de demonstração quando API offline

**Portal do Auditor (`/auditor`)**
- Verificação de lotes e certificados
- Validação de conformidade CBAM
- Verificação individual por batchId

**Portal do Produtor (`/producer`)**

O Portal do Produtor é composto por **4 páginas** com funcionalidades completas:

#### Página Principal (`/producer/page.tsx`) - Painel do Produtor
- **Métricas principais** (4 cards):
  - **Produção Total** (kg de H₂ verde produzido)
  - **Taxa de Conformidade** (% de lotes conformes com tendência)
  - **Média Emissões GHG** (kgCO₂e/kgH₂ com indicador vs limite CBAM)
  - **Certificados Emitidos** (total de SBTs emitidos)
- **Gráfico de Tendência Mensal**: LineChart com emissões GHG, consumo de água e taxa de conformidade ao longo dos meses
- **Visão Geral dos Lotes**: Distribuição por status (Verificados, Pendentes, Atenção, Certificados)
- **Ações Rápidas**:
  - **Gerar Relatório CBAM** → Download de PDF oficial de certificação
  - **Exportar Dados** → Download de CSV com dados de telemetria
- **Tabela de Lotes Recentes**: Lista com ID, tamanho, emissões GHG, consumo de água, status (Verificado/Pendente/Atenção), pontuação (0-100) e ações (baixar certificado SBT, corrigir não-conformidades)
- **Modal de Novo Lote**: Formulário para registrar novo lote com campos de tamanho (kg), emissões GHG e consumo de água
- **Botão "Enviar Dados"**: Upload manual de dados de telemetria
- **Dicas de Conformidade**: Seção educativa com recomendações para reduzir emissões GHG e melhorar eficiência hídrica
- **Fallback para dados mock**: Funciona offline com dados de demonstração

#### Gerenciamento de Lotes (`/producer/batches/page.tsx`)
- **Lista completa de lotes** com paginação (até 50 lotes)
- **Barra de pesquisa**: Filtro por ID do lote ou produtor
- **Resumo estatístico**: Total de lotes, conformes e pendentes
- **Tabela detalhada**: ID, tamanho, emissões GHG, consumo de água, status (Verificado/Pendente), data de criação
- **Ações por lote**: Link para verificação detalhada, download de certificado
- **Botão "Novo Lote"**: Criação de novos lotes
- **Loading state**: Spinner durante carregamento
- **Error state**: Mensagem de erro quando API falha

#### Certificados (`/producer/certificates/page.tsx`)
- Página estrutural para gerenciamento de certificados de hidrogênio verde
- *(Em desenvolvimento - página placeholder)*

#### Delegação CBAM (`/producer/delegation/page.tsx`)
- Página estrutural para gerenciamento de delegações de certificação
- *(Em desenvolvimento - página placeholder)*

#### Componentes UI (shadcn)
- badge, button, card, dialog, dropdown-menu, input, label, progress, table, tabs

#### Hooks React
- `useBatch()` - Gerenciamento de lotes
- `useCertificate()` - Gerenciamento de certificados
- `useCompliance()` - Verificação de compliance

---

### 4.4 📡 IoT Simulator

**`iot/simulator.py`**
- Simula sensores de produção de H₂ verde
- Envia telemetria para API via HTTP
- Configurável via `config.yaml`
- Gera dados: energy_source, power_generated_mwh, ghg_emissions, water_consumption
- Modo `force_compliant` para simular lotes conformes

---

### 4.5 📊 Monitoramento

- **Prometheus** (`monitoring/prometheus.yml`) - Coleta de métricas
- **Grafana** (`monitoring/grafana/`) - Dashboards visuais
- **Alertas** (`monitoring/alerts/`) - Regras de notificação
- Métricas: telemetria por segundo, batches certificados, compliance rate

---

### 4.6 🧪 Testes

| Arquivo | Escopo |
|---------|--------|
| `tests/test_api.py` | Testes de endpoints REST |
| `tests/test_blockchain.py` | Testes de integração blockchain |
| `tests/test_compliance.py` | Testes de verificação CBAM |
| `tests/test_delegation.py` | Testes de delegação |
| `tests/test_integration.py` | Testes de integração geral |
| `tests/test_oracle.py` | Testes do oráculo/satélite |
| `contracts/test/GreenHydrogenSBT.test.js` | Testes do contrato SBT |
| `contracts/test/BatchRegistry.test.js` | Testes do BatchRegistry |
| `contracts/test/ComplianceVerifier.test.js` | Testes do ComplianceVerifier |
| `contracts/test/integration.test.js` | Testes de integração dos contratos |

---

## 5. FLUXO DE TRABALHO COMPLETO

### 🔄 Produção → Certificação → Exportação

```
SENSORES IoT
     │
     ▼
┌─────────────────┐
│  API Telemetria  │  ← POST /api/v1/telemetry
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Criar Lote      │  ← POST /api/v1/batches
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Verificação Compliance │  ← CBAMComplianceChecker
│  • Emissões (≤3.4)     │     • Água (≤20 L/kg)
│  • Energia Renovável   │     • Adicionalidade
│  • Satélite (opcional) │
└────────┬────────────────┘
         │
    ┌────┴────┐
    │         │
  ✅ OK      ❌ FAIL
    │         │
    ▼         ▼
┌────────┐  ┌──────────────┐
│ Mint   │  │ Relatório de │
│ SBT na Blockchain │
└───┬────┘
    │
    ▼
┌─────────────────┐
│  Certificado     │  ← QR Code + Blockchain
│  SBT na Polygon  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Exportação      │  ← Consume Certificate
│  (prevenir       │     Relatório CBAM
│   double count)  │
└─────────────────┘
```

---

## 6. TECNOLOGIAS UTILIZADAS

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11+ | Backend API |
| **FastAPI** | - | Framework REST |
| **Next.js** | 14 | Frontend React |
| **TypeScript** | 5.x | Tipagem frontend |
| **Solidity** | 0.8.24 | Smart Contracts |
| **Hardhat** | - | Desenvolvimento Ethereum |
| **TimescaleDB** | PG16 | Séries temporais |
| **Redis** | 7 | Cache |
| **Docker** | - | Containerização |
| **Prometheus** | - | Métricas |
| **Grafana** | - | Dashboards |
| **Recharts** | - | Gráficos React |
| **shadcn/ui** | - | Componentes UI |
| **Tailwind CSS** | - | Estilização |
| **Alembic** | - | Migrações BD |
| **Pytest** | - | Testes Python |
| **Web3.py** | - | Integração blockchain |
| **SQLAlchemy** | - | ORM |
| **Pydantic** | - | Validação de dados |

---

## 7. CONFORMIDADE CBAM 2026

### Requisitos Atendidos

| Requisito | Status | Implementação |
|-----------|--------|---------------|
| Limite 3.4 tCO₂e/tH₂ | ✅ | `constants.py` + `compliance.py` |
| Verificação RFNBO | ✅ | `check_energy_source()` |
| Adicionalidade | ✅ | `check_additionality()` + satélite |
| Diretiva-Quadro Água | ✅ | `water.py` + `check_water_compliance()` |
| Declarante Delegado | ✅ | `delegation.py` + `DelegationManager.sol` |
| Prevenção Double Counting | ✅ | SBT + `consumeCertificate()` |
| Rastreabilidade | ✅ | Blockchain + QR Code |
| Relatórios Automáticos | ✅ | `report_service.py` |

---

## 8. ESTRUTURA DE DADOS

### Telemetria (IoT)
```json
{
  "sensor_id": "pecem_wind_01",
  "timestamp": "2026-04-24T12:00:00Z",
  "energy_source": "wind",
  "power_generated_mwh": 12.5,
  "ghg_emissions_kgCO2_per_kgH2": 2.3,
  "water_consumption_liters": 180.0,
  "water_source": "desalination"
}
```

### Certificado SBT (Blockchain)
```solidity
struct CertificateData {
    bytes32 batchId;
    address producer;
    uint256 timestamp;
    uint256 sizeKg;
    uint256 ghgEmissions;      // kgCO2e/kgH2 * 1000
    uint256 waterConsumption;  // liters/kgH2 * 1000
    bool isCompliant;
    bytes32 complianceHash;
    bool isConsumed;
    uint256 consumedAt;
    address consumedBy;
}
```

---

## 9. PRÓXIMOS PASSOS (ROADMAP)

### Fase 1 - MVP (✅ Concluído)
- [x] Estrutura do projeto
- [x] Smart Contract SBT básico
- [x] API de telemetria
- [x] Verificação de compliance CBAM
- [x] Dashboard básico
- [x] Verificação por satélite (modelo Namíbia)

### Fase 2 (Em andamento)
- [ ] Integração Chainlink Oracle
- [ ] Módulo de delegação CBAM completo
- [ ] Relatórios automáticos CBAM
- [ ] Testes de integração completos

### Fase 3 (Futuro)
- [ ] Integração com sistemas ERP
- [ ] Marketplace de certificados
- [ ] Análise preditiva de emissões
- [ ] Certificação multi-jurisdicional

---

## 10. COMANDOS PARA RODAR O PROJETO

### 🚀 Opção 1: Docker (Tudo de uma vez - Recomendado)

```bash
# Subir todos os serviços
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f

# Parar tudo
docker-compose down

# Acessar:
# - Frontend: http://localhost:3000
# - Backend:  http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### 🚀 Opção 2: Desenvolvimento Local

#### Terminal 1 - Banco de Dados
```bash
docker run -d --name h2v_timescaledb -p 5432:5432 \
  -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=h2v_trust \
  timescale/timescaledb:latest-pg16

docker run -d --name h2v_redis -p 6379:6379 redis:7-alpine
```

#### Terminal 2 - Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python ..\scripts\init_db.py
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 3 - Smart Contracts
```bash
cd contracts
npm install
npx hardhat node
```

#### Terminal 4 - Deploy dos Contratos
```bash
cd contracts
npx hardhat run scripts/deploy.js --network localhost
```

#### Terminal 5 - Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Terminal 6 - Simulador IoT (Opcional)
```bash
cd iot
pip install httpx pyyaml
python simulator.py
```

### 🧪 Testes

```bash
# Backend
cd backend && pytest tests/ -v

# Testes específicos
pytest tests/test_compliance.py -v
pytest tests/test_api.py -v
pytest tests/test_blockchain.py -v
pytest tests/test_delegation.py -v
pytest tests/test_integration.py -v
pytest tests/test_oracle.py -v

# Smart Contracts
cd contracts && npx hardhat test

# Frontend
cd frontend && npm test
```

### 🔄 Ordem de inicialização recomendada

```
1º → Banco de Dados (TimescaleDB + Redis)
2º → Backend (FastAPI)
3º → Smart Contracts (Hardhat Node)
4º → Deploy dos Contratos
5º → Frontend (Next.js)
6º → Simulador IoT (opcional)
```

---

## 11. ARQUIVOS DE RELATÓRIO E AUDITORIA

| Arquivo | Descrição |
|---------|-----------|
| `RELATORIO_PROJETO.md` | 📋 Este relatório - visão completa do projeto |
| `AUDITORIA_COMPLETA.md` | 🔍 Auditoria completa de código e arquitetura |
| `AUDITORIA_SAUDE_PROJETO.md` | 🏥 Auditoria de saúde do projeto |
| `RELATORIO_AUDITORIA_PRODUCAO.md` | ⚙️ Auditoria para produção/deploy |
| `RELATORIO_DE_TESTES_FUNCIONALIDADES.md` | 🧪 Relatório de testes de funcionalidades |
| `docs/architecture.md` | 🏗️ Documentação de arquitetura |
| `docs/api_reference.md` | 📖 Referência completa da API |
| `docs/cbam_compliance.md` | 📜 Guia de conformidade CBAM |
| `docs/delegation_guide.md` | 🤝 Guia de delegação CBAM |
| `docs/deployment.md` | 🚀 Guia de deploy |
| `docs/namibia_reference.md` | 🌍 Modelo de monitoramento Namíbia |

---

*Relatório gerado em 27/04/2026*
*H2V-Trust - Plataforma de Rastreabilidade Blockchain para Hidrogênio Verde*
*Total: ~19.378 linhas de código em 282 arquivos*

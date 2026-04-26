# Estrutura do Projeto h2v-trust

## Visão Geral

```
h2v-trust/
├── backend/          # API REST (Python/FastAPI)
├── frontend/         # Interface Web (Next.js/React)
├── contracts/        # Smart Contracts (Solidity/Ethereum)
├── iot/              # Simulador IoT
├── monitoring/       # Monitoramento (Prometheus/Grafana)
├── tests/            # Testes oficiais do backend
├── docs/             # Documentação
├── scripts/          # Scripts utilitários
├── alembic/          # Migrations do banco de dados
├── test-next-app/    # App Next.js de teste (experimental)
└── (arquivos raiz)   # Configurações e scripts diversos
```

---

## 📁 PASTAS PRINCIPAIS

### `backend/` — API REST (Python/FastAPI)
**Funcionalidade:** Backend principal do sistema. Fornece API REST para gerenciar batches de hidrogênio verde, certificados, compliance, delegação e telemetria.

```
backend/
├── main.py              # Ponto de entrada da aplicação FastAPI
├── config.py            # Configurações (DB, blockchain, etc.)
├── Dockerfile           # Build da imagem Docker
├── requirements.txt     # Dependências Python
├── requirements-minimal.txt  # Dependências mínimas
├── requirements.dev.txt      # Dependências de desenvolvimento
│
├── api/                 # Rotas da API
│   ├── routes/
│   │   ├── batches.py       # CRUD de batches
│   │   ├── certificates.py  # Certificados SBT
│   │   ├── compliance.py    # Verificação de compliance
│   │   ├── delegation.py    # Delegação de autoridade
│   │   ├── reports.py       # Relatórios CBAM
│   │   └── telemetry.py     # Telemetria IoT
│   └── dependencies/
│       ├── auth.py          # Autenticação
│       ├── db.py            # Sessão do banco
│       └── rate_limit.py    # Rate limiting
│
├── blockchain/          # Integração com Ethereum
│   ├── web3_client.py       # Cliente Web3
│   ├── minting.py           # Mint de certificados SBT
│   ├── verification.py      # Verificação on-chain
│   ├── sbt_manager.py       # Gerenciamento SBT
│   └── contract_abi.py      # ABIs dos contratos
│
├── core/                # Lógica de negócio
│   ├── certificates.py      # Lógica de certificados
│   ├── compliance.py        # Regras de compliance CBAM
│   ├── delegation.py        # Lógica de delegação
│   ├── emissions.py         # Cálculo de emissões
│   ├── water.py             # Consumo de água
│   └── constants.py         # Constantes do sistema
│
├── db/                  # Banco de dados
│   ├── database.py          # Conexão e sessão SQLAlchemy
│   ├── models.py            # Modelos ORM (legado)
│   └── models/
│       ├── batch.py             # Modelo Batch
│       ├── certificate.py       # Modelo Certificate
│       ├── delegation.py        # Modelo Delegation
│       ├── telemetry_record.py  # Modelo TelemetryRecord
│       └── audit_log.py         # Modelo AuditLog
│
├── models/              # Modelos Pydantic (schemas)
│   ├── batch.py             # Schema Batch
│   ├── certificate.py       # Schema Certificate
│   ├── compliance.py        # Schema Compliance
│   ├── delegation.py        # Schema Delegation
│   └── telemetry.py         # Schema Telemetry
│
├── oracle/              # Oráculos (dados externos)
│   ├── satellite_monitor.py    # Monitor de satélite
│   ├── chainlink_client.py     # Cliente Chainlink
│   ├── sensor_aggregator.py    # Agregador de sensores
│   └── automation.py           # Automação de tarefas
│
├── services/            # Serviços de negócio
│   ├── batch_service.py       # Serviço de batches
│   ├── certificate_service.py # Serviço de certificados
│   ├── delegation_service.py  # Serviço de delegação
│   ├── report_service.py      # Relatórios CBAM
│   ├── exporter_service.py    # Exportação de dados
│   └── qrcode_service.py      # Geração de QR codes
│
├── utils/               # Utilitários
│   ├── hashing.py            # Funções de hash
│   ├── logging.py            # Configuração de logs
│   ├── metrics.py            # Métricas Prometheus
│   └── validators.py         # Validadores
│
└── tests/               # Testes do backend
    └── __init__.py
```

---

### `frontend/` — Interface Web (Next.js 14.2.3)
**Funcionalidade:** Interface de usuário para produtores, auditores e dashboard de hidrogênio verde.

```
frontend/
├── next.config.js       # Configuração do Next.js
├── package.json         # Dependências Node.js
├── tailwind.config.js   # Configuração Tailwind CSS
├── postcss.config.js    # Configuração PostCSS
├── tsconfig.json        # Configuração TypeScript
├── Dockerfile           # Build da imagem Docker
│
├── app/                 # Páginas (App Router)
│   ├── layout.tsx           # Layout principal
│   ├── page.tsx             # Home page
│   │
│   ├── dashboard/           # Dashboard do produtor
│   │   ├── page.tsx
│   │   └── components/
│   │       ├── ProductionChart.tsx    # Gráfico de produção
│   │       ├── EmissionsGauge.tsx     # Medidor de emissões
│   │       ├── WaterCompliance.tsx    # Compliance de água
│   │       └── CertificatesTable.tsx  # Tabela de certificados
│   │
│   ├── producer/            # Área do produtor
│   │   ├── page.tsx
│   │   ├── batches/page.tsx       # Gerenciar batches
│   │   ├── certificates/page.tsx  # Ver certificados
│   │   └── delegation/page.tsx    # Delegar autoridade
│   │
│   ├── auditor/             # Área do auditor
│   │   ├── page.tsx
│   │   ├── verify/[batchId]/page.tsx  # Verificar batch
│   │   └── components/
│   │       ├── BatchVerification.tsx   # Verificação de batch
│   │       ├── BlockchainProof.tsx     # Prova blockchain
│   │       └── ComplianceReport.tsx    # Relatório compliance
│   │
│   ├── api/[...path]/route.ts  # Proxy API
│   └── (páginas de teste)
│
├── src/                 # Código fonte
│   ├── components/
│   │   ├── ui/              # Componentes shadcn/ui
│   │   │   ├── badge.tsx, button.tsx, card.tsx
│   │   │   ├── dialog.tsx, dropdown-menu.tsx
│   │   │   ├── input.tsx, label.tsx, progress.tsx
│   │   │   ├── table.tsx, tabs.tsx
│   │   └── shared/          # Componentes compartilhados
│   │       ├── ErrorBoundary.tsx
│   │       ├── LoadingSpinner.tsx
│   │       └── QRCode.tsx
│   │
│   ├── hooks/            # Hooks React
│   │   ├── useBatch.ts        # Hook para batches
│   │   ├── useCertificate.ts  # Hook para certificados
│   │   └── useCompliance.ts   # Hook para compliance
│   │
│   ├── lib/              # Bibliotecas
│   │   ├── api.ts            # Cliente HTTP
│   │   ├── web3.ts           # Conexão Web3
│   │   ├── constants.ts      # Constantes
│   │   └── utils.ts          # Utilitários
│   │
│   └── types/            # Tipos TypeScript
│       ├── batch.ts
│       ├── certificate.ts
│       └── compliance.ts
│
├── public/              # Arquivos estáticos
└── tests/               # Testes do frontend
```

---

### `contracts/` — Smart Contracts (Solidity/Hardhat)
**Funcionalidade:** Contratos inteligentes Ethereum para certificação de hidrogênio verde.

```
contracts/
├── hardhat.config.js    # Configuração Hardhat
├── package.json         # Dependências
├── check_balance.js     # Script para verificar saldo
│
├── contracts/           # Contratos Solidity
│   ├── GreenHydrogenSBT.sol       # Token SBT principal
│   ├── BatchRegistry.sol          # Registro de batches
│   ├── ComplianceVerifier.sol     # Verificador de compliance
│   ├── DelegationManager.sol      # Gerenciador de delegação
│   └── interfaces/                # Interfaces
│       ├── IGreenHydrogenSBT.sol
│       ├── IBatchRegistry.sol
│       ├── IComplianceVerifier.sol
│       └── IDelegationManager.sol
│
├── scripts/             # Scripts de deploy
└── test/                # Testes dos contratos
    └── GreenHydrogenSBT.test.js
```

---

### `tests/` — Testes Oficiais do Backend
**Funcionalidade:** Testes automatizados do backend usando pytest.

```
tests/
├── conftest.py              # Fixtures compartilhadas
├── test_api.py              # Testes da API REST
├── test_blockchain.py       # Testes de blockchain
├── test_compliance.py       # Testes de compliance
├── test_delegation.py       # Testes de delegação
├── test_integration.py      # Testes de integração
└── test_oracle.py           # Testes do oráculo
```

---

### `docs/` — Documentação
**Funcionalidade:** Documentação técnica do projeto.

```
docs/
├── architecture.md          # Arquitetura do sistema
├── api_reference.md         # Referência da API
├── api_proxy_guide.md       # Guia do proxy de API
├── cbam_compliance.md       # Compliance CBAM
├── delegation_guide.md      # Guia de delegação
├── deployment.md            # Guia de deploy
└── namibia_reference.md     # Referência Namíbia
```

---

### `iot/` — Simulador IoT
**Funcionalidade:** Simula sensores IoT para coleta de dados de produção.

```
iot/
├── simulator.py         # Simulador principal
├── config.yaml          # Configuração do simulador
├── data/                # Dados gerados
└── scripts/             # Scripts auxiliares
```

---

### `monitoring/` — Monitoramento
**Funcionalidade:** Configurações de monitoramento com Prometheus e Grafana.

```
monitoring/
├── prometheus.yml       # Configuração Prometheus
├── alerts/              # Regras de alerta
└── grafana/             # Dashboards Grafana
```

---

### `scripts/` — Scripts Utilitários
**Funcionalidade:** Scripts para tarefas administrativas.

```
scripts/
├── init_db.py              # Inicialização do banco
├── seed_data.py            # Dados de exemplo
├── create_cbam_report.py   # Gerar relatório CBAM
├── deploy_contracts.sh     # Deploy de contratos
└── test_compliance.py      # Teste de compliance
```

---

### `alembic/` — Migrations do Banco
**Funcionalidade:** Gerenciamento de versões do schema do banco de dados.

```
alembic/
├── env.py              # Configuração do Alembic
├── script.py.mako      # Template para migrations
└── versions/           # Migrations
    └── 6fef8df01c1e_init_timescaledb.py  # Init TimescaleDB
```

---

## 📄 ARQUIVOS NA RAIZ

### Configuração Principal

| Arquivo | Funcionalidade |
|---------|---------------|
| `package.json` | Dependências Node.js do frontend (Next.js, React, shadcn/ui, ethers) |
| `package-lock.json` | Lockfile das dependências Node.js |
| `docker-compose.yml` | Orquestração Docker (backend + frontend + banco) |
| `docker-compose.prod.yml` | Docker Compose para produção |
| `.env` | Variáveis de ambiente (config local) |
| `.env.example` | Template das variáveis de ambiente |
| `alembic.ini` | Configuração do Alembic |
| `Makefile` | Comandos make para tarefas comuns |
| `tsconfig.json` | Configuração TypeScript (raiz) |
| `next-env.d.ts` | Tipos Next.js |
| `next.config.js` | Configuração Next.js (raiz) |

### Scripts de Análise e Diagnóstico

| Arquivo | Funcionalidade |
|---------|---------------|
| `audit_state.py` | Auditoria do estado atual do projeto |
| `analyze_repo.py` | Análise geral do repositório |
| `scan_repo.py` | Escaneamento de arquivos |
| `check_imports.py` | Verificação de imports Python |
| `fix_imports.py` | Correção de imports |
| `final_check.py` | Verificação final do sistema |
| `simple_check.py` | Verificação simples |
| `dump_tree.py` | Exportar árvore de diretórios |
| `start_backend_test.py` | Iniciar backend para testes |

### Relatórios de Auditoria

| Arquivo | Funcionalidade |
|---------|---------------|
| `auditoria_resumo_dificuldades.md` | Resumo das maiores dificuldades |
| `auditoria_completa_final.md` | Auditoria completa final |
| `auditoria_completa_projeto_final.md` | Auditoria final do projeto |
| `auditoria_completa_projeto.md` | Auditoria completa do projeto |
| `auditoria_arquivos_vazios.md` | Relatório de arquivos vazios |
| `auditoria_resultado.txt` | Resultado da auditoria |
| `technical_audit_report.md` | Relatório técnico de auditoria |
| `technical_audit_report_final.md` | Relatório técnico final |
| `e2e_test_report.md` | Relatório de testes E2E |
| `frontend_fix_summary.md` | Resumo de correções frontend |
| `plano_testes_pendentes.md` | Plano de testes pendentes |
| `delegation_fix_plan.md` | Plano de correção delegação |
| `explicacao_problema_detalhada.md` | Explicação detalhada de problemas |
| `relatorio_problema_nextjs.md` | Relatório de problemas Next.js |

### Testes (Raiz)

| Arquivo | Funcionalidade |
|---------|---------------|
| `test_api.py` | Teste da API |
| `test_api_clean.py` | Teste limpo da API |
| `test_api_simple.py` | Teste simples da API |
| `test_api_simple_final.py` | Teste final simples da API |
| `test_api_detailed.py` | Teste detalhado da API |
| `test_api_final_no_unicode.py` | Teste final sem unicode |
| `test_api_route.py` | Teste de rotas da API |
| `test_backend.py` | Teste geral do backend |
| `test_blockchain_connection.py` | Teste conexão blockchain |
| `test_complete_flow.py` | Teste de fluxo completo |
| `test_compliance.py` | Teste de compliance |
| `test_db.py` | Teste do banco de dados |
| `test_db_connection.py` | Teste de conexão DB |
| `test_delegation_import.py` | Teste de import delegação |
| `test_direct_mock.py` | Teste com mock direto |
| `test_e2e.py` | Teste end-to-end |
| `test_e2e_simple.py` | Teste E2E simples |
| `test_flow.py` | Teste de fluxo |
| `test_flow_fixed.py` | Teste de fluxo corrigido |
| `test_fix_final.py` | Teste de correção final |
| `test_import.py` | Teste de imports |
| `test_minting_direct.py` | Teste de minting direto |
| `test_minting_simple.py` | Teste de minting simples |
| `test_model.py` | Teste de modelos |
| `test_model_simple.py` | Teste simples de modelos |
| `test_post.py` | Teste de requisições POST |
| `test_report_service.py` | Teste do serviço de relatórios |
| `test_report_fix_simple.py` | Teste de correção de relatório |
| `test_simple.py` | Teste simples |
| `test_simulator_connection.py` | Teste conexão simulador |
| `test_system_working.py` | Teste sistema funcionando |
| `test_system_ascii.py` | Teste sistema ASCII |
| `test_telemetry.py` | Teste de telemetria |
| `test_telemetry_detailed.py` | Teste detalhado telemetria |
| `test_telemetry_detailed_final.py` | Teste final telemetria |
| `test_account_balance.py` | Teste saldo conta |
| `test_batch_service.py` | Teste serviço de batches |
| `test_ascii.py` | Teste ASCII |
| `tmp_test_satellite.py` | Teste temporário satélite |

### Outros Arquivos

| Arquivo | Funcionalidade |
|---------|---------------|
| `README.md` | Documentação principal do projeto |
| `LICENSE` | Licença do projeto |
| `.gitignore` | Arquivos ignorados pelo Git |
| `audit_results.json` | Resultados de auditoria em JSON |
| `backend_files_nonempty.json` | Arquivos backend não vazios |
| `frontend_files_nonempty.json` | Arquivos frontend não vazios |
| `frontend_files.json` | Lista de arquivos frontend |
| `frontend_files.txt` | Lista texto arquivos frontend |
| `frontend_tree.txt` | Árvore frontend |
| `frontend_tree_clean.txt` | Árvore frontend limpa |
| `tree_frontend.txt` | Árvore frontend |
| `empty_files.txt` | Lista de arquivos vazios |
| `scan_results.txt` | Resultados de scan |
| `sat_out.txt` | Saída de satélite |
| `out.txt` | Saída genérica |
| `out2.txt` | Saída genérica 2 |
| `e2e_test_plan.md` | Plano de testes E2E |

---

## 🔄 FLUXO DE DADOS

```
IoT/Sensores → backend/oracle/ → backend/api/ → Banco de Dados
                                                    ↓
                                            backend/blockchain/ (minting)
                                                    ↓
                                            Smart Contracts (Ethereum)
                                                    ↓
                                            frontend/ (consulta)
```

1. **IoT Simulator** → Envia dados de telemetria para API
2. **Backend API** → Processa e valida dados
3. **Banco de Dados** → Armazena batches, certificados, telemetria
4. **Blockchain** → Mina certificados SBT na Ethereum
5. **Frontend** → Consulta e exibe dados para usuários

---

## 🚀 COMO RODAR

```bash
# Backend
cd backend && uvicorn main:app --reload

# Frontend (da raiz)
npx next dev frontend

# Testes
cd tests && pytest -v

# Docker
docker-compose up
```

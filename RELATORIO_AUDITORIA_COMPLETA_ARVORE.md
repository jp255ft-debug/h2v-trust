# 📋 Relatório de Auditoria Completa - H2V-Trust

**Data:** 05/05/2026  
**Versão:** 1.0.0  
**Status:** Em Desenvolvimento  
**Stack:** Python 3.11, FastAPI, Next.js 14, Solidity 0.8.24, Docker

---

## 🔷 1. Visão Geral do Projeto

**H2V-Trust** é uma plataforma de certificação baseada em blockchain para Hidrogênio Verde (H2V), garantindo conformidade com o **CBAM 2026** (Carbon Border Adjustment Mechanism). Utiliza Soulbound Tokens (SBT) não-transferíveis para prevenir double counting e garantir rastreabilidade completa da produção à exportação.

### Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| **Backend** | Python 3.11, FastAPI, SQLAlchemy, TimescaleDB |
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui |
| **Blockchain** | Solidity 0.8.24, Hardhat, Web3.py |
| **Infra** | Docker, Docker Compose, Nginx, Prometheus, Grafana |
| **Banco** | TimescaleDB (PostgreSQL), Redis |
| **Oracle** | Chainlink (integração com dados externos) |

### Serviços (Docker Compose Dev)

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| `timescaledb` | 5432 | Banco de séries temporais |
| `redis` | 6379 | Cache e filas |
| `hardhat` | 8545 | Nó blockchain local (chain_id: 1337) |
| `backend` | 8000 | API FastAPI |
| `frontend` | 3000 | Next.js 14 |

---

## 🌳 2. Árvore de Diretórios Anotada

```
📁 h2v-trust/
│
├── 📄 .clinerules.md                          # Regras de conduta para IA (Cline)
├── 📄 .env.example                            # Template de variáveis de ambiente
├── 📄 .gitignore                              # Arquivos ignorados pelo Git
│
├── 📁 .cline/                                 # Memória de longo prazo do agente Cline
│   └── 📄 memory-bank.md                      # Estado atual do projeto
│
├── 📁 .clinerules/                            # Regras específicas do projeto
│   ├── 📄 01-docker.md                        # Regras de Docker (comandos, emergência)
│   ├── 📄 02-coding-standards.md              # Padrões de código e segurança
│   └── 📄 03-project-context.md               # Contexto geral do projeto
│
├── 📁 alembic/                                # Migrations do banco de dados
│   ├── 📄 env.py                              # Configuração do Alembic
│   ├── 📄 script.py.mako                      # Template para novas migrations
│   └── 📁 versions/                           # Versões de migration
│       └── 📄 6fef8df01c1e_init_timescaledb.py # Migration inicial (TimescaleDB)
│
├── 📄 alembic.ini                             # Configuração do Alembic
│
├── 📁 backend/                                # 🟢 API FastAPI (Python 3.11)
│   ├── 📄 __init__.py
│   ├── 📄 .dockerignore                       # Arquivos ignorados no build Docker
│   ├── 📄 config.py                           # Configurações via Pydantic Settings
│   ├── 📄 Dockerfile                          # Dockerfile para desenvolvimento
│   ├── 📄 Dockerfile.prod                     # Dockerfile para produção (multi-stage)
│   ├── 📄 main.py                             # Entry point da aplicação + health check
│   ├── 📄 requirements.dev.txt                # Dependências de desenvolvimento
│   ├── 📄 requirements.prod.txt               # Dependências de produção
│   │
│   ├── 📁 api/                                # Camada de API (rotas)
│   │   ├── 📄 __init__.py
│   │   ├── 📁 dependencies/                   # Dependências injetáveis
│   │   │   └── 📄 rate_limit.py               # Rate limiting via Redis
│   │   └── 📁 routes/                         # Endpoints REST
│   │       ├── 📄 __init__.py
│   │       ├── 📄 batches.py                  # CRUD de lotes de produção
│   │       ├── 📄 certificates.py             # Emissão/verificação de certificados
│   │       ├── 📄 compliance.py               # Verificação de compliance CBAM
│   │       ├── 📄 delegation.py               # Delegação CBAM (Declarantes)
│   │       ├── 📄 reports.py                  # Geração de relatórios
│   │       └── 📄 telemetry.py                # Ingestão de dados IoT
│   │
│   ├── 📁 blockchain/                         # Integração com blockchain
│   │   ├── 📄 __init__.py
│   │   ├── 📄 contract_abi.py                 # ABIs dos contratos
│   │   ├── 📄 GreenHydrogenSBT.json           # ABI do contrato SBT
│   │   ├── 📄 minting.py                      # Lógica de mint de SBTs
│   │   ├── 📄 sbt_manager.py                  # Gerenciamento de SBTs
│   │   ├── 📄 verification.py                 # Verificação on-chain
│   │   └── 📄 web3_client.py                  # Cliente Web3 (conexão blockchain)
│   │
│   ├── 📁 core/                               # 🧠 Lógica de negócio (core)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 certificates.py                 # Lógica de certificação
│   │   ├── 📄 compliance.py                   # Regras de compliance CBAM
│   │   ├── 📄 constants.py                    # Constantes do domínio
│   │   ├── 📄 delegation.py                   # Lógica de delegação
│   │   ├── 📄 emissions.py                    # Cálculo de emissões
│   │   └── 📄 water.py                        # Conformidade com Diretiva-Quadro da Água
│   │
│   ├── 📁 db/                                 # Camada de banco de dados
│   │   ├── 📄 __init__.py
│   │   ├── 📄 database.py                     # Engine SQLAlchemy + setup TimescaleDB
│   │   ├── 📄 models.py                       # Re-export dos modelos
│   │   └── 📁 models/                         # Modelos SQLAlchemy
│   │       ├── 📄 __init__.py
│   │       ├── 📄 audit_log.py                # Log de auditoria
│   │       ├── 📄 batch.py                    # Lote de produção
│   │       ├── 📄 certificate.py              # Certificado SBT
│   │       ├── 📄 delegation.py               # Delegação CBAM
│   │       └── 📄 telemetry_record.py         # Dados de telemetria (hypertable)
│   │
│   ├── 📁 models/                             # Modelos Pydantic (schemas)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 batch.py                        # Schema de lote
│   │   ├── 📄 certificate.py                  # Schema de certificado
│   │   ├── 📄 compliance.py                   # Schema de compliance
│   │   ├── 📄 delegation.py                   # Schema de delegação
│   │   └── 📄 telemetry.py                    # Schema de telemetria
│   │
│   ├── 📁 oracle/                             # 🛰️ Integração Chainlink/Oráculo
│   │   ├── 📄 __init__.py
│   │   ├── 📄 automation.py                   # Automação de tarefas
│   │   ├── 📄 chainlink_client.py             # Cliente Chainlink
│   │   ├── 📄 satellite_monitor.py            # Monitoramento via satélite
│   │   └── 📄 sensor_aggregator.py            # Agregador de sensores IoT
│   │
│   ├── 📁 scripts/                            # Scripts utilitários do backend
│   │   └── 📄 seed_data.py                    # Popula banco com dados de exemplo
│   │
│   ├── 📁 services/                           # 🏗️ Serviços (lógica de aplicação)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 batch_service.py                # Serviço de lotes
│   │   ├── 📄 certificate_service.py          # Serviço de certificados
│   │   ├── 📄 delegation_service.py           # Serviço de delegação
│   │   ├── 📄 exporter_service.py             # Exportação de dados
│   │   ├── 📄 qrcode_service.py               # Geração de QR codes
│   │   └── 📄 report_service.py               # Geração de relatórios
│   │
│   ├── 📁 tests/                              # Testes do backend
│   │   └── 📄 __init__.py
│   │
│   └── 📁 utils/                              # Utilitários
│       ├── 📄 __init__.py
│       ├── 📄 hashing.py                      # Funções de hash
│       ├── 📄 logging.py                      # Configuração de logging
│       ├── 📄 metrics.py                      # Métricas Prometheus
│       └── 📄 validators.py                   # Validadores diversos
│
├── 📁 contracts/                              # 📜 Smart Contracts Solidity
│   ├── 📄 __init__.py
│   ├── 📄 .env.example                        # Template .env para contratos
│   ├── 📄 check_balance.js                    # Script para verificar saldo
│   ├── 📄 hardhat.config.js                   # Configuração do Hardhat
│   ├── 📄 package.json                        # Dependências Node.js
│   │
│   ├── 📁 artifacts/                          # ABIs compiladas (gerado)
│   ├── 📁 cache/                              # Cache do Hardhat (gerado)
│   │
│   ├── 📁 contracts/                          # Contratos Solidity
│   │   ├── 📄 __init__.py
│   │   ├── 📄 BatchRegistry.sol               # Registro de lotes on-chain
│   │   ├── 📄 ComplianceVerifier.sol          # Verificador de compliance
│   │   ├── 📄 DelegationManager.sol           # Gerenciamento de delegação
│   │   ├── 📄 GreenHydrogenSBT.sol            # 🏆 Soulbound Token principal
│   │   ├── 📄 IBatchRegistry.sol              # Interface BatchRegistry
│   │   ├── 📄 IComplianceVerifier.sol         # Interface ComplianceVerifier
│   │   ├── 📄 IDelegationManager.sol          # Interface DelegationManager
│   │   ├── 📄 IGreenHydrogenSBT.sol           # Interface GreenHydrogenSBT
│   │   └── 📁 interfaces/                     # Interfaces básicas
│   │       ├── 📄 IBasicBatchRegistry.sol
│   │       ├── 📄 IBasicComplianceVerifier.sol
│   │       └── 📄 IBasicGreenHydrogenSBT.sol
│   │
│   ├── 📁 scripts/                            # Scripts de deploy
│   │   ├── 📄 __init__.py
│   │   ├── 📄 deploy.js                       # Deploy dos contratos
│   │   ├── 📄 test_mint.js                    # Teste de mint
│   │   ├── 📄 upgrade.js                      # Upgrade de contratos
│   │   └── 📄 verify.js                       # Verificação pós-deploy
│   │
│   └── 📁 test/                               # Testes dos contratos
│       ├── 📄 __init__.py
│       ├── 📄 BatchRegistry.test.js           # Testes do BatchRegistry
│       ├── 📄 ComplianceVerifier.test.js      # Testes do ComplianceVerifier
│       ├── 📄 GreenHydrogenSBT.test.js        # Testes do SBT
│       └── 📄 integration.test.js             # Testes de integração
│
├── 📁 docs/                                   # 📚 Documentação
│   ├── 📄 __init__.py
│   ├── 📄 api_proxy_guide.md                  # Guia do proxy de API
│   ├── 📄 api_reference.md                    # Referência da API
│   ├── 📄 architecture.md                     # Arquitetura do sistema
│   ├── 📄 cbam_compliance.md                  # Conformidade CBAM
│   ├── 📄 delegation_guide.md                 # Guia de delegação
│   ├── 📄 deployment.md                       # Guia de deploy
│   ├── 📄 namibia_reference.md                # Referência Namíbia (projeto real)
│   ├── 📄 plano_trabalho_funcap.md            # Plano de trabalho FUNCAP
│   ├── 📄 sumario_executivo.md                # Sumário executivo
│   └── 📁 audits/                             # Relatórios de auditoria anteriores
│       ├── 📄 ESTRUTURA_PROJETO.md
│       ├── 📄 technical_audit_report.md
│       ├── 📄 technical_audit_report_final.md
│       └── ... (outros relatórios)
│
├── 📁 frontend/                               # 🎨 Next.js 14 (App Router)
│   ├── 📄 .dockerignore
│   ├── 📄 .env.local                          # Variáveis de ambiente (não expor)
│   ├── 📄 .nvmrc                              # Versão do Node.js
│   ├── 📄 Dockerfile                          # Dockerfile dev
│   ├── 📄 Dockerfile.prod                     # Dockerfile produção
│   ├── 📄 next.config.js                      # Configuração Next.js
│   ├── 📄 package.json                        # Dependências
│   ├── 📄 postcss.config.js                   # Config PostCSS
│   ├── 📄 tailwind.config.js                  # Config Tailwind CSS
│   ├── 📄 tsconfig.json                       # Config TypeScript
│   │
│   ├── 📁 app/                                # 📄 Páginas (App Router)
│   │   ├── 📄 globals.css                     # Estilos globais
│   │   ├── 📄 layout.tsx                      # Layout raiz
│   │   ├── 📄 page.tsx                        # Página inicial (Landing)
│   │   │
│   │   ├── 📁 api/                            # API Routes (proxy)
│   │   │   └── 📁 [...path]/
│   │   │       └── 📄 route.ts                # Proxy para backend
│   │   │
│   │   ├── 📁 auditor/                        # 👁️ Módulo do Auditor
│   │   │   ├── 📄 page.tsx                    # Dashboard do auditor
│   │   │   ├── 📄 page-backup.tsx             # Backup da página
│   │   │   ├── 📁 components/                 # Componentes do auditor
│   │   │   │   └── 📄 BatchVerification.tsx   # Verificação de lotes
│   │   │   └── 📁 verify/
│   │   │       └── 📁 [batchId]/
│   │   │           └── 📄 page.tsx            # Verificação de lote específico
│   │   │
│   │   ├── 📁 dashboard/                      # 📊 Dashboard principal
│   │   │   ├── 📄 page.tsx                    # Dashboard principal
│   │   │   ├── 📄 page-simple.tsx             # Versão simplificada
│   │   │   ├── 📄 test-page.tsx               # Página de teste
│   │   │   └── 📁 components/                 # Componentes do dashboard
│   │   │       ├── 📄 CertificatesTable.tsx   # Tabela de certificados
│   │   │       ├── 📄 EmissionsGauge.tsx      # Medidor de emissões
│   │   │       ├── 📄 ProductionChart.tsx     # Gráfico de produção
│   │   │       └── 📄 WaterCompliance.tsx     # Compliance hídrico
│   │   │
│   │   ├── 📁 debug/                          # 🐛 Páginas de debug
│   │   │   └── 📄 page.tsx
│   │   │
│   │   ├── 📁 producer/                       # 🏭 Módulo do Produtor
│   │   │   ├── 📄 page.tsx                    # Dashboard do produtor
│   │   │   ├── 📁 batches/                    # Gerenciamento de lotes
│   │   │   │   └── 📄 page.tsx
│   │   │   ├── 📁 certificates/               # Gerenciamento de certificados
│   │   │   │   └── 📄 page.tsx
│   │   │   └── 📁 delegation/                 # Delegação CBAM
│   │   │       └── 📄 page.tsx
│   │   │
│   │   ├── 📁 simple/                         # Página simples (teste)
│   │   │   └── 📄 page.tsx
│   │   │
│   │   └── 📁 test/                           # Página de teste
│   │       └── 📄 page.tsx
│   │
│   ├── 📁 public/                             # Arquivos estáticos
│   │   ├── 📄 favicon.ico
│   │   └── 📄 logo.svg
│   │
│   ├── 📁 src/                                # Código fonte
│   │   ├── 📁 api/                            # Cliente API
│   │   ├── 📁 components/                     # Componentes React
│   │   │   ├── 📁 layout/                     # Componentes de layout
│   │   │   │   └── 📄 Navbar.tsx              # Barra de navegação
│   │   │   ├── 📁 shared/                     # Componentes compartilhados
│   │   │   │   ├── 📄 ErrorBoundary.tsx       # Tratamento de erros
│   │   │   │   ├── 📄 LoadingSpinner.tsx      # Spinner de loading
│   │   │   │   └── 📄 QRCode.tsx              # Gerador de QR code
│   │   │   └── 📁 ui/                         # Componentes shadcn/ui
│   │   │       ├── 📄 badge.tsx
│   │   │       ├── 📄 button.tsx
│   │   │       ├── 📄 card.tsx
│   │   │       ├── 📄 dialog.tsx
│   │   │       ├── 📄 dropdown-menu.tsx
│   │   │       ├── 📄 input.tsx
│   │   │       ├── 📄 label.tsx
│   │   │       ├── 📄 progress.tsx
│   │   │       ├── 📄 table.tsx
│   │   │       └── 📄 tabs.tsx
│   │   │
│   │   ├── 📁 config/                         # Configurações do frontend
│   │   ├── 📁 constants/                      # Constantes
│   │   ├── 📁 context/                        # Contextos React
│   │   ├── 📁 features/                       # Features/modules
│   │   ├── 📁 hooks/                          # Custom hooks
│   │   │   ├── 📄 index.ts                    # Re-export
│   │   │   ├── 📄 useBatch.ts                 # Hook de lotes
│   │   │   ├── 📄 useCertificate.ts           # Hook de certificados
│   │   │   ├── 📄 useCompliance.ts            # Hook de compliance
│   │   │   └── 📁 example/                    # Exemplo de hook
│   │   │       └── 📄 HookExample.tsx
│   │   │
│   │   ├── 📁 layouts/                        # Layouts
│   │   ├── 📁 lib/                            # Bibliotecas/utilitários
│   │   │   ├── 📄 api.ts                      # Cliente HTTP (axios/fetch)
│   │   │   ├── 📄 constants.ts                # Constantes compartilhadas
│   │   │   ├── 📄 utils.ts                    # Funções utilitárias
│   │   │   └── 📄 web3.ts                     # Integração Web3 (MetaMask)
│   │   │
│   │   ├── 📁 theme/                          # Tema (Tailwind/shadcn)
│   │   ├── 📁 types/                          # Tipos TypeScript
│   │   │   ├── 📄 index.ts                    # Re-export
│   │   │   ├── 📄 batch.ts                    # Tipos de lote
│   │   │   ├── 📄 certificate.ts              # Tipos de certificado
│   │   │   └── 📄 compliance.ts               # Tipos de compliance
│   │   └── 📁 utils/                          # Utilitários
│   │
│   └── 📁 tests/                              # Testes do frontend
│       └── 📄 __init__.py
│
├── 📁 iot/                                    # 📡 Simulador IoT
│   ├── 📄 __init__.py
│   ├── 📄 config.yaml                         # Configuração do simulador
│   ├── 📄 simulator.py                        # Simulador de sensores
│   ├── 📁 data/                               # Dados de exemplo
│   │   └── 📄 sample_readings.json            # Leituras de exemplo
│   └── 📁 scripts/                            # Scripts IoT
│       └── 📄 generate_mock_data.py           # Geração de dados mock
│
├── 📁 logs/                                   # 📝 Logs e outputs
│   ├── 📄 audit_results.json
│   ├── 📄 auditoria_resultado.txt
│   ├── 📄 backend_files_nonempty.json
│   ├── 📄 empty_files.txt
│   ├── 📄 frontend_files.json
│   ├── 📄 frontend_files.txt
│   ├── 📄 frontend_tree.txt
│   ├── 📄 out.txt
│   ├── 📄 sat_out.txt
│   ├── 📄 scan_results.txt
│   └── 📄 test_out.txt
│
├── 📁 monitoring/                             # 📊 Monitoramento
│   ├── 📄 __init__.py
│   ├── 📄 prometheus.yml                      # Config Prometheus
│   ├── 📁 alerts/                             # Regras de alerta
│   │   └── 📄 alert_rules.yml
│   └── 📁 grafana/                            # Dashboards Grafana
│       ├── 📄 __init__.py
│       ├── 📁 dashboards/                     # Dashboards provisionados
│       └── 📁 datasources/                    # Fontes de dados
│
├── 📁 nginx/                                  # 🌐 Proxy reverso
│   ├── 📄 nginx.conf                          # Configuração Nginx
│   └── 📁 ssl/                                # Certificados SSL
│       └── 📄 .gitkeep
│
├── 📁 scripts/                                # 🔧 Scripts de automação
│   ├── 📄 __init__.py
│   ├── 📄 analyze_repo.py                     # Análise do repositório
│   ├── 📄 audit_secrets.py                    # Auditoria de secrets
│   ├── 📄 audit_state.py                      # Auditoria de estado
│   ├── 📄 check_imports.py                    # Verificação de imports
│   ├── 📄 count_stats.py                      # Estatísticas do projeto
│   ├── 📄 create_cbam_report.py               # Geração relatório CBAM
│   ├── 📄 deploy_contracts.sh                 # Deploy de contratos
│   ├── 📄 dump_tree.py                        # Árvore de diretórios
│   ├── 📄 final_check.py                      # Verificação final
│   ├── 📄 fix_imports.py                      # Correção de imports
│   ├── 📄 generate_audit_report.py            # Geração relatório auditoria
│   ├── 📄 generate_tree.py                    # Geração árvore
│   ├── 📄 init_db.py                          # Inicialização do banco
│   ├── 📄 reset-docker.bat                    # Reset Docker (Windows)
│   ├── 📄 reset-docker.sh                     # Reset Docker (Linux/WSL)
│   ├── 📄 scan_repo.py                        # Scan do repositório
│   ├── 📄 seed_data.py                        # Popula dados iniciais
│   ├── 📄 simple_check.py                     # Verificação simples
│   ├── 📄 start_backend_test.py               # Inicia teste backend
│   ├── 📄 start-prod.bat                      # Inicia produção (Windows)
│   ├── 📄 stop-prod.bat                       # Para produção (Windows)
│   └── 📄 test_compliance.py                  # Teste de compliance
│
├── 📁 tests/                                  # 🧪 Testes de integração
│   ├── 📄 conftest.py                         # Fixtures compartilhadas
│   ├── 📄 test_api.py                         # Testes de API
│   ├── 📄 test_blockchain.py                  # Testes de blockchain
│   ├── 📄 test_compliance.py                  # Testes de compliance
│   ├── 📄 test_delegation.py                  # Testes de delegação
│   ├── 📄 test_integration.py                 # Testes de integração
│   └── 📄 test_oracle.py                      # Testes do oráculo
│
├── 📄 docker-compose.yml                      # 🐳 Orquestração dev
├── 📄 docker-compose.dev.yml                  # Override para desenvolvimento
├── 📄 docker-compose.prod.yml                 # Orquestração produção
├── 📄 Makefile                                # Comandos make
├── 📄 package.json                            # Dependências raiz
├── 📄 README.md                               # Documentação principal
├── 📄 render.yaml                             # Config deploy Render
│
├── 📄 AUDITORIA_COMPLETA.md                   # Relatório auditoria anterior
├── 📄 AUDITORIA_DOCKER_NATIVE.md              # Auditoria Docker
├── 📄 AUDITORIA_SAUDE_PROJETO.md              # Auditoria saúde do projeto
├── 📄 AUDITORIA_SEGURANCA_CODIGO.md           # Auditoria segurança
├── 📄 RELATORIO_AUDITORIA_DEPENDENCIAS.md     # Auditoria dependências
├── 📄 RELATORIO_AUDITORIA_PRODUCAO.md         # Auditoria produção
├── 📄 RELATORIO_AUDITORIA_RESILIENCIA.md      # Auditoria resiliência
├── 📄 RELATORIO_DE_TESTES_FUNCIONALIDADES.md  # Testes de funcionalidades
├── 📄 RELATORIO_PROJETO.md                    # Relatório geral do projeto
└── 📄 RELATORIO_THE_GAUNTLET.md               # Resultado The Gauntlet
```

---

## 📦 3. Docker & Infraestrutura

### 3.1 Arquivos de Orquestração

| Arquivo | Propósito |
|---------|-----------|
| `docker-compose.yml` | Base com 5 serviços (timescaledb, redis, hardhat, backend, frontend) |
| `docker-compose.dev.yml` | Override dev: hot-reload, volumes sincronizados, `develop.watch` |
| `docker-compose.prod.yml` | Produção: +nginx, prometheus, grafana; healthchecks, restart policies |

### 3.2 Dockerfiles

| Arquivo | Estágios | Propósito |
|---------|----------|-----------|
| `backend/Dockerfile` | Single-stage | Dev com `--reload` |
| `backend/Dockerfile.prod` | Multi-stage | Produção otimizada |
| `frontend/Dockerfile` | Single-stage | Dev com `npm run dev` |
| `frontend/Dockerfile.prod` | Multi-stage | Build + produção |

### 3.3 Serviços de Produção (Adicionais)

| Serviço | Porta | Função |
|---------|-------|--------|
| `nginx` | 80/443 | Proxy reverso + SSL |
| `prometheus` | 9090 | Métricas e alertas |
| `grafana` | 3001 | Dashboards de monitoramento |

---

## ⚙️ 4. Backend (FastAPI)

### 4.1 Rotas da API

| Rota | Prefixo | Descrição |
|------|---------|-----------|
| `telemetry.py` | `/api/v1` | Ingestão de dados IoT (POST sensores) |
| `batches.py` | `/api/v1` | CRUD de lotes de produção |
| `certificates.py` | `/api/v1` | Emissão e verificação de certificados SBT |
| `compliance.py` | `/api/v1` | Verificação de conformidade CBAM |
| `delegation.py` | `/api/v1` | Gerenciamento de Declarantes Delegados |
| `reports.py` | `/api/v1` | Geração de relatórios CBAM |
| `/health` | - | Health check (banco, blockchain, redis) |

### 4.2 Core (Lógica de Negócio)

| Módulo | Responsabilidade |
|--------|-----------------|
| `compliance.py` | Regras CBAM: limite 3.4 tCO₂e/tH₂, verificação adicionalidade |
| `emissions.py` | Cálculo de emissões de carbono |
| `water.py` | Conformidade com Diretiva-Quadro da Água |
| `certificates.py` | Lógica de certificação e SBT |
| `delegation.py` | Lógica de delegação CBAM |
| `constants.py` | Constantes: limites, prazos, parâmetros |

### 4.3 Blockchain

| Módulo | Função |
|--------|--------|
| `web3_client.py` | Conexão com nó blockchain (Hardhat/Polygon) |
| `sbt_manager.py` | Gerenciamento de Soulbound Tokens |
| `minting.py` | Mint de novos certificados |
| `verification.py` | Verificação on-chain |
| `contract_abi.py` | ABIs dos contratos |

### 4.4 Oracle/Chainlink

| Módulo | Função |
|--------|--------|
| `chainlink_client.py` | Integração com Chainlink |
| `satellite_monitor.py` | Monitoramento via satélite (adicionalidade) |
| `sensor_aggregator.py` | Agregação de dados de sensores IoT |
| `automation.py` | Automação de tarefas periódicas |

### 4.5 Banco de Dados (TimescaleDB)

**Modelos:**
- `telemetry_record` - Hypertable particionado por timestamp (compressão após 7 dias)
- `batch` - Lotes de produção
- `certificate` - Certificados SBT
- `audit_log` - Log de auditoria
- `delegation` - Delegações CBAM

---

## 🎨 5. Frontend (Next.js 14)

### 5.1 Páginas (App Router)

| Rota | Módulo | Descrição |
|------|--------|-----------|
| `/` | Landing | Página inicial |
| `/dashboard` | Dashboard | Visão geral com gráficos e métricas |
| `/auditor` | Auditor | Verificação de lotes e certificados |
| `/auditor/verify/[batchId]` | Auditor | Verificação detalhada de lote |
| `/producer` | Produtor | Dashboard do produtor |
| `/producer/batches` | Produtor | Gerenciamento de lotes |
| `/producer/certificates` | Produtor | Gerenciamento de certificados |
| `/producer/delegation` | Produtor | Delegação CBAM |
| `/api/[...path]` | Proxy | Proxy para backend |

### 5.2 Componentes

| Categoria | Componentes |
|-----------|-------------|
| **Layout** | `Navbar.tsx` |
| **Shared** | `ErrorBoundary.tsx`, `LoadingSpinner.tsx`, `QRCode.tsx` |
| **UI (shadcn)** | `badge`, `button`, `card`, `dialog`, `dropdown-menu`, `input`, `label`, `progress`, `table`, `tabs` |
| **Dashboard** | `CertificatesTable`, `EmissionsGauge`, `ProductionChart`, `WaterCompliance` |
| **Auditor** | `BatchVerification` |

### 5.3 Hooks

| Hook | Função |
|------|--------|
| `useBatch` | Operações com lotes |
| `useCertificate` | Operações com certificados |
| `useCompliance` | Verificação de compliance |

### 5.4 Tipos TypeScript

| Arquivo | Interfaces |
|---------|------------|
| `batch.ts` | `Batch`, `BatchCreate`, `BatchStatus` |
| `certificate.ts` | `Certificate`, `CertificateCreate` |
| `compliance.ts` | `ComplianceResult`, `ComplianceCheck` |

---

## 📜 6. Smart Contracts (Solidity)

| Contrato | Função Principal |
|----------|-----------------|
| `GreenHydrogenSBT.sol` | 🏆 Soulbound Token ERC-721 não-transferível |
| `BatchRegistry.sol` | Registro de lotes de produção on-chain |
| `ComplianceVerifier.sol` | Verificação automática de compliance CBAM |
| `DelegationManager.sol` | Gerenciamento de Declarantes Delegados |

### Interfaces
- `IGreenHydrogenSBT`, `IBatchRegistry`, `IComplianceVerifier`, `IDelegationManager`
- Interfaces básicas: `IBasicGreenHydrogenSBT`, `IBasicBatchRegistry`, `IBasicComplianceVerifier`

---

## 🧪 7. Testes & Qualidade

### 7.1 Testes de Integração (raiz `/tests`)

| Arquivo | Escopo |
|---------|--------|
| `test_api.py` | Testes de
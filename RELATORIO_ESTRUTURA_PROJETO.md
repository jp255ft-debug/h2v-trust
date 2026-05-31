# 📂 Relatório da Estrutura do Projeto H2V-Trust

> **Data:** 18/05/2026
> **Versão:** 1.0
> **Autor:** Cline (DeepSeek)

---

## 1. Árvore Completa do Projeto

```
h2v-trust/
│
├── 📜 .clinerules/                          # Regras do Cline (5 arquivos)
│   ├── 01-docker.md                         # Docker + protocolo emergência
│   ├── 02-coding-standards.md               # Padrões de código
│   ├── 03-project-context.md                # Contexto do projeto
│   ├── 04-python-constraints.md             # Regras anti-alucinação Python
│   └── 05-workflows.md                      # Workflows padronizados
│
├── 📜 .cline/
│   └── memory-bank.md                       # Memória de longo prazo do agente
│
├── 📜 .clinerules.md                        # Regras raiz (stack, comandos, segurança)
├── 📜 .env.example                          # Exemplo de variáveis de ambiente
├── 📜 .gitignore                            # Arquivos ignorados pelo Git
├── 📜 Makefile                              # Comandos make (dev-start, dev-check, dev-reset)
├── 📜 README.md                             # Documentação principal
├── 📜 LICENSE                               # Licença do projeto
│
├── 📜 docker-compose.yml                    # Orquestração dev (5 serviços)
├── 📜 docker-compose.dev.yml                # Override dev (hot-reload, volumes)
├── 📜 docker-compose.prod.yml               # Override prod (nginx, prometheus, grafana)
│
├── 🐍 backend/                              # Python 3.11 + FastAPI
│   ├── main.py                              # Entry point FastAPI
│   ├── config.py                            # Configurações centralizadas
│   ├── Dockerfile                           # Imagem Docker dev
│   ├── Dockerfile.prod                      # Imagem Docker produção
│   ├── requirements.dev.txt                 # Dependências dev
│   ├── requirements.prod.txt                # Dependências produção
│   │
│   ├── 📁 api/                              # Camada HTTP (FastAPI)
│   │   ├── __init__.py
│   │   ├── 📁 routes/                       # Endpoints da API
│   │   │   ├── __init__.py
│   │   │   ├── admin.py                     # GET/POST/PATCH /admin/tenants
│   │   │   ├── auth.py                      # POST /auth/login
│   │   │   ├── batches.py                   # CRUD batches
│   │   │   ├── certificates.py              # CRUD certificados
│   │   │   ├── compliance.py                # Rota compliance
│   │   │   ├── delegation.py                # Rota delegações CBAM
│   │   │   ├── reports.py                   # Relatórios
│   │   │   └── telemetry.py                 # Telemetria IoT
│   │   └── 📁 dependencies/                 # Dependências FastAPI
│   │       ├── __init__.py
│   │       ├── auth.py                      # API Key auth
│   │       ├── db.py                        # Sessão DB
│   │       ├── jwt_auth.py                  # JWT + bcrypt + RBAC
│   │       ├── rate_limit.py                # Rate limiting
│   │       └── tenant.py                    # Isolamento multi-tenant
│   │
│   ├── 📁 blockchain/                       # Integração Web3
│   │   ├── __init__.py
│   │   ├── web3_client.py                   # Cliente Web3.py
│   │   ├── minting.py                       # Mint de certificados on-chain
│   │   ├── sbt_manager.py                   # SBT manager (Soulbound Tokens)
│   │   ├── verification.py                  # Verificação on-chain
│   │   ├── contract_abi.py                  # ABI loader
│   │   └── GreenHydrogenSBT.json            # ABI do contrato
│   │
│   ├── 📁 core/                             # Regras de negócio
│   │   ├── __init__.py
│   │   ├── compliance.py                    # Motor de compliance CBAM
│   │   ├── certificates.py                  # Lógica de certificação
│   │   ├── delegation.py                    # Delegações CBAM
│   │   ├── emissions.py                     # Cálculo de emissões GHG
│   │   ├── water.py                         # Consumo de água
│   │   └── constants.py                     # Constantes (limiares GHG, etc.)
│   │
│   ├── 📁 db/                               # Banco de Dados
│   │   ├── __init__.py
│   │   ├── database.py                      # Engine SQLAlchemy + TimescaleDB
│   │   ├── models.py                        # Modelos ORM (legado)
│   │   └── 📁 models/                       # Modelos SQLAlchemy atuais
│   │       ├── __init__.py
│   │       ├── audit_log.py                 # Logs de auditoria
│   │       ├── batch.py                     # Lotes de produção
│   │       ├── certificate.py               # Certificados
│   │       ├── delegation.py                # Delegações CBAM
│   │       ├── tenant.py                    # Tenants (multi-tenant)
│   │       ├── user.py                      # Usuários
│   │       ├── user_tenant.py               # Associação N:N user↔tenant
│   │       └── telemetry_record.py          # Registros de telemetria
│   │
│   ├── 📁 models/                           # Modelos Pydantic (schemas)
│   │   ├── __init__.py
│   │   ├── auth.py                          # LoginRequest, TokenResponse
│   │   ├── batch.py                         # Schema de lote
│   │   ├── certificate.py                   # Schema de certificado
│   │   ├── compliance.py                    # Schema de compliance
│   │   ├── delegation.py                    # Schema de delegação
│   │   ├── telemetry.py                     # Schema de telemetria
│   │   ├── tenant.py                        # Schema de tenant
│   │   └── user.py                          # Schema de usuário
│   │
│   ├── 📁 oracle/                           # Oráculo IoT
│   │   ├── __init__.py
│   │   ├── satellite_monitor.py             # Monitor via satélite
│   │   ├── sensor_aggregator.py             # Agregador de sensores
│   │   ├── chainlink_client.py              # Integração Chainlink
│   │   └── automation.py                    # Automação de processos
│   │
│   ├── 📁 services/                         # Lógica de negócio (serviços)
│   │   ├── __init__.py
│   │   ├── auth_service.py                  # Autenticação (JWT)
│   │   ├── batch_service.py                 # Gerenciamento de lotes
│   │   ├── certificate_service.py           # Gerenciamento de certificados
│   │   ├── delegation_service.py            # Delegações CBAM
│   │   ├── tenant_service.py                # CRUD de tenants
│   │   ├── user_service.py                  # Convidar/remover usuários
│   │   ├── report_service.py                # Relatórios CBAM
│   │   ├── exporter_service.py              # Exportação de dados
│   │   └── qrcode_service.py                # Geração de QR Code
│   │
│   ├── 📁 scripts/                          # Scripts utilitários
│   │   ├── seed_data.py                     # Seed inicial (20 lotes)
│   │   ├── seed_users_tenants.py            # Seed auth multi-tenant
│   │   ├── seed_demo_data.py                # Dados de demonstração
│   │   ├── reset_demo_data.py               # Limpa dados demo
│   │   ├── db_report.py                     # Relatório do banco
│   │   └── db_simple_report.py              # Relatório simplificado
│   │
│   ├── 📁 tests/                            # Testes unitários
│   │   ├── __init__.py
│   │   └── test_health.py                   # Teste health check
│   │
│   ├── 📁 utils/                            # Utilitários
│   │   ├── __init__.py
│   │   ├── hashing.py                       # Hash de senhas
│   │   ├── logging.py                       # Config de logging
│   │   ├── metrics.py                       # Métricas de desempenho
│   │   └── validators.py                    # Validadores diversos
│   │
│   └── 📁 alembic/                          # Migrações de banco
│       ├── env.py                           # Config Alembic
│       ├── script.py.mako                   # Template de migração
│       └── 📁 versions/
│           ├── 6fef8df01c1e_init_timescaledb.py
│           ├── 6b1464dad020_add_tenant_id_to_tables.py
│           └── add_users_tenants_and_audit_fields.py
│
├── ⚛️ frontend/                             # Next.js 14 + TypeScript
│   ├── middleware.ts                        # Middleware (proteção /admin)
│   ├── next.config.js                       # Config Next.js
│   ├── tailwind.config.js                   # Tailwind CSS
│   ├── tsconfig.json                        # TypeScript strict
│   ├── postcss.config.js                    # PostCSS config
│   ├── Dockerfile                           # Imagem Docker dev
│   ├── Dockerfile.prod                      # Imagem Docker produção
│   ├── .env.local                           # Variáveis de ambiente locais
│   ├── .nvmrc                               # Versão do Node.js
│   │
│   ├── 📁 app/                              # App Router (páginas)
│   │   ├── layout.tsx                       # Layout raiz (NavbarWrapper)
│   │   ├── page.tsx                         # Home (/)
│   │   ├── globals.css                      # Estilos globais
│   │   │
│   │   ├── 📁 admin/                        # Painel admin (protegido)
│   │   │   ├── layout.tsx                   # Sidebar + header admin
│   │   │   ├── page.tsx                     # CRUD Tenants
│   │   │   └── 📁 logs/                     # Logs de auditoria
│   │   │       └── page.tsx                 # Filtros + paginação
│   │   │
│   │   ├── 📁 dashboard/                    # Dashboard geral
│   │   │   ├── page.tsx                     # Dashboard principal
│   │   │   ├── page-simple.tsx              # Versão simplificada
│   │   │   ├── test-page.tsx                # Página de teste
│   │   │   └── 📁 components/               # Componentes do dashboard
│   │   │       ├── CertificatesTable.tsx    # Tabela de certificados
│   │   │       ├── EmissionsGauge.tsx       # Medidor de emissões
│   │   │       ├── ProductionChart.tsx      # Gráfico de produção
│   │   │       └── WaterCompliance.tsx      # Conformidade hídrica
│   │   │
│   │   ├── 📁 auditor/                      # Painel do auditor
│   │   │   ├── page.tsx                     # Lista lotes p/ auditoria
│   │   │   ├── page-backup.tsx              # Backup da página
│   │   │   ├── 📁 components/               # Componentes de auditoria
│   │   │   │   └── BatchVerification.tsx    # Verificação de lote
│   │   │   └── 📁 verify/                   # Verificação detalhada
│   │   │       └── [batchId]/page.tsx       # Página dinâmica de verificação
│   │   │
│   │   ├── 📁 producer/                     # Painel do produtor
│   │   │   ├── page.tsx                     # Home do produtor
│   │   │   ├── 📁 batches/                  # Gerenciar lotes
│   │   │   │   └── page.tsx
│   │   │   ├── 📁 certificates/             # Gerenciar certificados
│   │   │   │   └── page.tsx
│   │   │   └── 📁 delegation/               # Delegações CBAM
│   │   │       └── page.tsx
│   │   │
│   │   ├── 📁 login/                        # Autenticação
│   │   │   └── page.tsx                     # Formulário de login
│   │   │
│   │   ├── 📁 api/                          # API Routes (Next.js)
│   │   │   ├── 📁 [...path]/route.ts        # Proxy reverso para backend
│   │   │   └── 📁 health/route.ts           # Health check (força IPv4)
│   │   │
│   │   ├── 📁 debug/                        # Debug
│   │   │   └── page.tsx
│   │   ├── 📁 test/                         # Página de testes
│   │   │   └── page.tsx
│   │   └── 📁 simple/                       # Página simples
│   │       └── page.tsx
│   │
│   ├── 📁 src/                              # Componentes e lógica
│   │   ├── 📁 lib/                          # Bibliotecas auxiliares
│   │   │   ├── api.ts                       # Cliente HTTP (fetch wrapper)
│   │   │   ├── constants.ts                 # Constantes
│   │   │   ├── utils.ts                     # Utilitários (cn)
│   │   │   └── web3.ts                      # Integração Web3 (frontend)
│   │   │
│   │   ├── 📁 hooks/                        # React Hooks
│   │   │   ├── index.ts                     # Exportações
│   │   │   ├── useAuth.ts                   # Login/logout/token
│   │   │   ├── useBatch.ts                  # CRUD lotes
│   │   │   ├── useCertificate.ts            # CRUD certificados
│   │   │   ├── useCompliance.ts             # Compliance checks
│   │   │   └── 📁 example/                  # Exemplo de hook
│   │   │       └── HookExample.tsx
│   │   │
│   │   ├── 📁 components/                   # Componentes React
│   │   │   ├── 📁 layout/                   # Navbar, NavbarWrapper
│   │   │   │   ├── Navbar.tsx
│   │   │   │   └── NavbarWrapper.tsx
│   │   │   ├── 📁 shared/                   # Componentes compartilhados
│   │   │   │   ├── SystemStatus.tsx         # Status do sistema
│   │   │   │   ├── ErrorBoundary.tsx        # Boundary de erro
│   │   │   │   ├── QRCode.tsx               # QR Code generator
│   │   │   │   └── LoadingSpinner.tsx       # Spinner de loading
│   │   │   └── 📁 ui/                       # shadcn/ui
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
│   │   ├── 📁 types/                        # Tipos TypeScript
│   │   │   ├── index.ts
│   │   │   ├── batch.ts
│   │   │   ├── certificate.ts
│   │   │   └── compliance.ts
│   │   │
│   │   ├── 📁 context/                      # React Context (auth)
│   │   ├── 📁 config/                       # Configurações frontend
│   │   ├── 📁 constants/                    # Constantes frontend
│   │   ├── 📁 features/                     # Feature modules
│   │   ├── 📁 layouts/                      # Layouts adicionais
│   │   ├── 📁 theme/                        # Tema (dark/light)
│   │   ├── 📁 utils/                        # Utilitários frontend
│   │   └── 📁 api/                          # API helpers
│   │
│   ├── 📁 public/                           # Arquivos estáticos
│   │   ├── favicon.ico
│   │   └── logo.svg
│   │
│   └── 📁 tests/                            # Testes frontend
│       └── __init__.py
│
├── 🔷 contracts/                            # Solidity + Hardhat
│   ├── hardhat.config.js                    # Config Hardhat (Polygon/localhost)
│   ├── package.json                         # Dependências npm
│   ├── check_balance.js                     # Script de verificação de saldo
│   │
│   ├── 📁 contracts/                        # Smart Contracts
│   │   ├── GreenHydrogenSBT.sol             # ERC-721 SBT (Soulbound Token)
│   │   ├── BatchRegistry.sol                # Registro de lotes on-chain
│   │   ├── ComplianceVerifier.sol           # Verificador de compliance
│   │   ├── DelegationManager.sol            # Gerenciador de delegações CBAM
│   │   ├── IGreenHydrogenSBT.sol            # Interfaces
│   │   ├── IBatchRegistry.sol
│   │   ├── IComplianceVerifier.sol
│   │   ├── IDelegationManager.sol
│   │   └── 📁 interfaces/                   # Interfaces básicas
│   │       ├── IBasicGreenHydrogenSBT.sol
│   │       ├── IBasicBatchRegistry.sol
│   │       ├── IBasicComplianceVerifier.sol
│   │       └── IBasicDelegationManager.sol
│   │
│   ├── 📁 test/                             # Testes JavaScript (Mocha)
│   │   ├── GreenHydrogenSBT.test.js
│   │   ├── BatchRegistry.test.js
│   │   ├── ComplianceVerifier.test.js
│   │   └── integration.test.js
│   │
│   ├── 📁 scripts/                          # Scripts de deploy
│   │   ├── deploy.js                        # Deploy completo
│   │   ├── test_mint.js                     # Teste de mint
│   │   ├── upgrade.js                       # Upgrade de contratos
│   │   └── verify.js                        # Verificação (Polygonscan)
│   │
│   ├── 📁 artifacts/                        # Compilados Solidity
│   │   ├── 📁 @openzeppelin/
│   │   ├── 📁 build-info/
│   │   └── 📁 contracts/
│   │
│   └── 📁 cache/                            # Cache Hardhat
│       └── solidity-files-cache.json
│
├── 🔧 scripts/                              # Scripts de DevOps
│   ├── deep-clean.sh                        # Faxina completa Docker (Linux)
│   ├── deep-clean.bat                       # Faxina completa Docker (Windows)
│   ├── reset-docker.sh                      # Reset do ambiente Docker (Linux)
│   ├── reset-docker.bat                     # Reset do ambiente Docker (Windows)
│   ├── maintenance-weekly.sh                # Manutenção semanal
│   ├── generate_tree.py                     # Gera árvore do projeto
│   ├── generate_audit_report.py             # Gera relatório de auditoria
│   ├── audit_secrets.py                     # Auditoria de secrets
│   ├── audit_state.py                       # Auditoria de estado
│   ├── check_imports.py                     # Verificação de imports
│   ├── fix_imports.py                       # Correção de imports
│   ├── fix_audit_logs.py                    # Correção de audit logs
│   ├── count_stats.py                       # Estatísticas do projeto
│   ├── db_report.py                         # Relatório do banco
│   ├── db_simple_report.py                  # Relatório simplificado
│   ├── init_db.py                           # Inicialização do banco
│   ├── seed_data.py                         # Seed de dados
│   ├── seed_demo_data.py                    # Seed de dados demo
│   ├── reset_demo_data.py                   # Reset dados demo
│   ├── deploy_contracts.sh                  # Deploy de contratos
│   ├── start-prod.bat                       # Iniciar produção
│   ├── stop-prod.bat                        # Parar produção
│   ├── start_backend_test.py                # Iniciar teste backend
│   ├── test_compliance.py                   # Teste de compliance
│   ├── scan_repo.py                         # Scan do repositório
│   ├── analyze_repo.py                      # Análise do repositório
│   ├── dump_tree.py                         # Dump da árvore
│   ├── final_check.py                       # Verificação final
│   ├── simple_check.py                      # Verificação simples
│   └── create_cbam_report.py                # Relatório CBAM
│
├── 🧪 tests/                                # Testes integrados (pytest)
│   ├── conftest.py                          # Fixtures
│   ├── test_api.py                          # Testes de API
│   ├── test_blockchain.py                   # Testes blockchain
│   ├── test_compliance.py                   # Testes compliance
│   ├── test_delegation.py                   # Testes delegação
│   ├── test_integration.py                  # Testes integração
│   └── test_oracle.py                       # Testes oráculo
│
├── 🌐 nginx/                                # Proxy reverso (produção)
│   ├── nginx.conf                           # Configuração Nginx
│   └── 📁 ssl/                              # Certificados SSL
│       └── .gitkeep
│
├── 📊 monitoring/                           # Observabilidade
│   ├── prometheus.yml                       # Métricas Prometheus
│   ├── 📁 grafana/                          # Dashboards Grafana
│   └── 📁 alerts/                           # Alertas
│
├── 📡 iot/                                  # Simulador IoT
│   ├── simulator.py                         # Simulador de sensores
│   ├── config.yaml                          # Configuração
│   ├── 📁 data/                             # Dados simulados
│   └── 📁 scripts/                          # Scripts IoT
│
├── 📚 docs/                                 # Documentação
│   ├── architecture.md                      # Arquitetura do sistema
│   ├── api_reference.md                     # Referência da API
│   ├── api_proxy_guide.md                   # Guia do proxy
│   ├── cbam_compliance.md                   # Compliance CBAM
│   ├── delegation_guide.md                  # Guia de delegação
│   ├── deployment.md                        # Guia de deploy
│   ├── namibia_reference.md                 # Referência Namíbia
│   ├── plano_trabalho_funcap.md             # Plano FUNCAP
│   ├── sumario_executivo.md                 # Sumário executivo
│   └── 📁 audits/                           # Relatórios de auditoria
│
├── 📁 alembic/                              # Migrações (raiz, legado)
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── 📁 versions/
│       └── 6fef8df01c1e_init_timescaledb.py
│
├── 📁 logs/                                 # Logs e outputs
│   ├── audit_results.json
│   ├── auditoria_resultado.txt
│   ├── backend_files_nonempty.json
│   ├── empty_files.txt
│   ├── frontend_files.json / .txt
│   ├── frontend_tree.txt / _clean.txt
│   ├── out.txt / out2.txt
│   ├── sat_out.txt
│   ├── scan_results.txt
│   └── test_out.txt
│
├── 📁 .github/workflows/                    # CI/CD
│   └── ci.yml                               # GitHub Actions (3 jobs)
│
├── 📄 RELATORIO_PROJETO.md                  # Relatório do projeto
├── 📄 RELATORIO_BANCO_DADOS.md              # Relatório do banco
├── 📄 RELATORIO_THE_GAUNTLET.md             # Resultado The Gauntlet
├── 📄 RELATORIO_AUDITORIA_PRODUCAO.md       # Auditoria produção
├── 📄 RELATORIO_AUDITORIA_DEPENDENCIAS.md   # Auditoria dependências
├── 📄 RELATORIO_AUDITORIA_RESILIENCIA.md    # Auditoria resiliência
├── 📄 RELATORIO_AUDITORIA_COMPLETA_ARVORE.md# Auditoria árvore completa
├── 📄 RELATORIO_DE_TESTES_FUNCIONALIDADES.md# Testes de funcionalidades
├── 📄 AUDITORIA_COMPLETA.md                 # Auditoria completa
├── 📄 AUDITORIA_DOCKER_NATIVE.md            # Auditoria Docker
├── 📄 AUDITORIA_INTEGRACAO_FRONTEND.md      # Auditoria frontend
├── 📄 AUDITORIA_SAUDE_PROJETO.md            # Auditoria saúde
├── 📄 AUDITORIA_SEGURANCA_CODIGO.md         # Auditoria segurança
├── 📄 AUDITORIA_VERIFY_API_KEY.md           # Auditoria API Key
├── 📄 VALIDACAO_RELATORIO_AUDITORIA.md      # Validação auditoria
├── 📄 tmp_telemetry.json                    # Telemetria temporária
├── 📄 audit_secrets_result.json             # Resultado audit secrets
├── 📄 render.yaml                           # Config Render.com
└── 📄 package.json                          # Dependências raiz
```

---

## 2. Tecnologias por Camada

| Camada | Tecnologia | Versão | Função |
|--------|-----------|--------|--------|
| **Backend** | Python | 3.11 | Linguagem principal |
| **Framework** | FastAPI | ^0.109 | Framework web assíncrono |
| **ORM** | SQLAlchemy | ^2.0 | Mapeamento objeto-relacional |
| **Migrações** | Alembic | ^1.13 | Controle de versão do schema |
| **Banco** | TimescaleDB | pg16 | Banco temporal + PostgreSQL |
| **Cache/Fila** | Redis | 7-alpine | Cache e filas de mensagens |
| **Blockchain** | Web3.py | ^6.15 | Integração Ethereum |
| **Autenticação** | python-jose | ^3.3 | JWT tokens |
| **Hash** | bcrypt | ^4.1 | Hash de senhas |
| **Validação** | Pydantic | ^2.5 | Validação de dados |
| **HTTP** | httpx | ^0.26 | Cliente HTTP assíncrono |
| **Driver DB** | psycopg2-binary | ^2.9 | Driver PostgreSQL |
| | | | |
| **Frontend** | Next.js | 14.x | Framework React SSR |
| **Linguagem** | TypeScript | ^5.x | Tipagem estática |
| **Estilização** | Tailwind CSS | ^3.x | CSS utility-first |
| **Componentes** | shadcn/ui | latest | Biblioteca de componentes |
| **Roteamento** | App Router | 14.x | Roteamento baseado em pastas |
| | | | |
| **Blockchain** | Solidity | ^0.8.24 | Linguagem de contratos |
| **Framework** | Hardhat | ^2.19 | Desenvolvimento Ethereum |
| **Padrão** | OpenZeppelin | ^5.x | Contratos auditados (ERC-721) |
| **Rede** | Hardhat local | chain 1337 | Node local de desenvolvimento |
| | | | |
| **Infra** | Docker | latest | Containerização |
| **Orquestração** | Docker Compose | v2 | Orquestração multi-container |
| **Proxy** | Nginx | latest | Proxy reverso (produção) |
| **Monitoramento** | Prometheus | latest | Métricas |
| **Dashboards** | Grafana | latest | Visualização de métricas |
| **CI/CD** | GitHub Actions | — | Pipeline de integração contínua |

---

## 3. Estatísticas do Projeto

| Métrica | Valor |
|---------|-------|
| **Total de diretórios** | ~60 |
| **Total de arquivos** | ~220+ |
| **Arquivos de código** | ~150+ |
| **Documentos** | 25+ (docs, relatórios, auditorias) |
| **Smart Contracts** | 4 principais + 4 interfaces + 4 básicas |
| **Rotas da API** | 9 módulos (18+ endpoints) |
| **Páginas Frontend** | 16 (App Router) |
| **Componentes React** | 20+ (ui + shared + layout) |
| **Serviços Docker (dev)** | 5 (timescaledb, redis, hardhat, backend, frontend) |
| **Serviços Docker (prod)** | 8 (+ nginx, prometheus, grafana) |
| **Migrações de Banco** | 3 (Alembic) |
| **Testes Backend** | 7 suites (pytest) |
| **Testes Contratos** | 4 suites (Mocha/Chai) |
| **Scripts DevOps** | 25+ |
| **Arquivos de Config** | 15+ (Docker, Nginx, Prometheus, etc.) |

---

## 4. Estrutura de Dados (Banco de Dados)

| Tabela | Descrição | Tipo |
|--------|-----------|------|
| `batches` | Lotes de produção de H2V | TimescaleDB (hipertabela) |
| `certificates` | Certificados de H2V | Relacional |
| `delegations` | Delegações CBAM | Relacional |
| `audit_logs` | Logs de auditoria | TimescaleDB (hipertabela) |
| `telemetry_records` | Registros de telemetria IoT | TimescaleDB (hipertabela) |
| `tenants` | Inquilinos multi-tenant | Relacional |
| `users` | Usuários do sistema | Relacional |
| `user_tenants` | Associação N:N user↔tenant | Relacional |

---

## 5. Endpoints da API

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|-------------|
| POST | `/api/v1/auth/login` | Login (email+senha) | Pública |
| GET | `/api/v1/admin/tenants` | Listar tenants | JWT (admin) |
| POST | `/api/v1/admin/tenants` | Criar tenant | JWT (admin) |
| GET | `/api/v1/admin/tenants/{id}` | Detalhes tenant | JWT (admin) |
| PATCH | `/api/v1/admin/tenants/{id}` | Atualizar tenant | JWT (admin) |
| GET | `/api/v1/admin/tenants/{id}/users` | Listar usuários | JWT (admin) |
| POST | `/api/v1/admin/tenants/{id}/users` | Convidar usuário | JWT (admin) |
| DELETE | `/api/v1/admin/tenants/{id}/users/{uid}` | Remover usuário | JWT (admin) |
| GET | `/api/v1/admin/audit-logs` | Listar audit logs | JWT (admin) |
| GET | `/batches` | Listar lotes | API Key |
| POST | `/batches` | Criar lote | API Key |
| GET | `/certificates` | Listar certificados | API Key |
| POST | `/certificates` | Criar certificado | API Key |
| GET | `/compliance/check` | Verificar compliance | API Key |
| POST | `/delegation` | Criar delegação | API Key |
| GET | `/reports` | Relatórios | API Key |
| POST | `/telemetry` | Receber telemetria | API Key |
| GET | `/health` | Health check | Pública |

---

## 6. Contratos Smart Contracts

| Contrato | Endereço (Hardhat local) | Descrição |
|----------|--------------------------|-----------|
| GreenHydrogenSBT | `0x0165878A594ca255338adfa4d48449f69242Eb8F` | ERC-721 Soulbound Token |
| BatchRegistry | `0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9` | Registro de lotes on-chain |
| ComplianceVerifier | `0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9` | Verificador de compliance |
| DelegationManager | `0x5FC8d32690cc91D4c39d9d3abcBD16989F875707` | Gerenciador de delegações |

---

## 7. Fluxo de Dados (Arquitetura)

```
[IoT Sensors] ──► [Backend API] ──► [TimescaleDB]
                      │
                      ├──► [Blockchain (Hardhat/Polygon)]
                      │       └── Mint SBT Certificate
                      │
                      ├──► [Redis Cache]
                      │
                      └──► [Frontend Next.js]
                              ├── Dashboard (produtor)
                              ├── Auditor (verificação)
                              ├── Admin (gestão)
                              └── Login (autenticação JWT)
```

---

## 8. Comandos Úteis

```bash
# Ambiente Dev
make dev-start                    # Iniciar ambiente
make dev-check                    # Verificar saúde
make dev-reset                    # Reset completo

# Docker
docker compose ps                 # Status dos containers
docker compose logs --tail=50 backend  # Logs do backend
docker compose exec backend python scripts/seed_demo_data.py  # Seed dados

# Testes
docker compose exec backend pytest  # Testes backend
cd contracts && npx hardhat
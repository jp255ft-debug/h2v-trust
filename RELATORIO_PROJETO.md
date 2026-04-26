# 📋 Relatório Completo do Projeto H2V-Trust

## 🌿 Plataforma de Rastreabilidade Blockchain para Hidrogênio Verde

---

## 1. ÁRVORE COMPLETA DO PROJETO

```
h2v-trust/
│
├── 📁 backend/                    # API FastAPI (Python 3.11+)
│   ├── main.py                    # Ponto de entrada da API
│   ├── config.py                  # Configurações centralizadas
│   ├── Dockerfile                 # Container da API
│   ├── requirements.txt           # Dependências Python
│   │
│   ├── 📁 api/                    # Rotas REST
│   │   └── 📁 routes/
│   │       ├── telemetry.py       # Ingestão de dados IoT
│   │       ├── batches.py         # Gerenciamento de lotes
│   │       ├── certificates.py    # Certificação de lotes
│   │       ├── compliance.py      # Verificação CBAM
│   │       ├── delegation.py      # Delegação CBAM
│   │       └── reports.py         # Relatórios CBAM
│   │
│   ├── 📁 core/                   # Lógica de negócio
│   │   ├── constants.py           # Constantes CBAM 2026
│   │   ├── compliance.py          # Verificador de compliance
│   │   ├── emissions.py           # Cálculo de emissões
│   │   ├── water.py               # Conformidade hídrica
│   │   ├── certificates.py        # Geração de certificados
│   │   └── delegation.py          # Gestão de delegação
│   │
│   ├── 📁 blockchain/             # Integração blockchain
│   │   ├── web3_client.py         # Cliente Web3
│   │   ├── contract_abi.py        # ABIs dos contratos
│   │   ├── minting.py             # Mint de SBTs
│   │   └── verification.py        # Verificação on-chain
│   │
│   ├── 📁 oracle/                 # Oráculos e dados externos
│   │   ├── satellite_monitor.py   # Monitoramento por satélite
│   │   └── automation.py          # Automação de tarefas
│   │
│   ├── 📁 db/                     # Banco de dados
│   │   ├── database.py            # Conexão TimescaleDB
│   │   └── 📁 models/
│   │       ├── batch.py           # Modelo de lote
│   │       ├── certificate.py     # Modelo de certificado
│   │       ├── telemetry_record.py# Modelo de telemetria
│   │       ├── audit_log.py       # Log de auditoria
│   │       └── delegation.py      # Modelo de delegação
│   │
│   ├── 📁 models/                 # Modelos Pydantic
│   │   ├── batch.py
│   │   ├── certificate.py
│   │   ├── compliance.py
│   │   ├── delegation.py
│   │   └── telemetry.py
│   │
│   ├── 📁 services/               # Serviços de negócio
│   │   ├── certificate_service.py # Serviço de certificados
│   │   ├── delegation_service.py  # Serviço de delegação
│   │   ├── report_service.py      # Geração de relatórios
│   │   └── exporter_service.py    # Exportação de dados
│   │
│   └── 📁 utils/                  # Utilitários
│       ├── hashing.py             # Funções de hash
│       └── metrics.py             # Métricas Prometheus
│
├── 📁 contracts/                  # Smart Contracts Solidity
│   ├── hardhat.config.js          # Config Hardhat
│   ├── 📁 contracts/
│   │   ├── GreenHydrogenSBT.sol   # Token Soulbound (SBT)
│   │   ├── BatchRegistry.sol      # Registro de lotes
│   │   ├── ComplianceVerifier.sol # Verificação on-chain
│   │   ├── DelegationManager.sol  # Gestão de delegação
│   │   └── 📁 interfaces/         # Interfaces dos contratos
│   ├── 📁 scripts/                # Scripts de deploy
│   └── 📁 test/                   # Testes dos contratos
│
├── 📁 frontend/                   # Next.js 14 + TypeScript
│   ├── next.config.js
│   ├── package.json
│   ├── Dockerfile
│   │
│   ├── 📁 app/                    # App Router
│   │   ├── page.tsx               # Landing page
│   │   ├── layout.tsx             # Layout principal
│   │   │
│   │   ├── 📁 dashboard/          # Dashboard principal
│   │   │   ├── page.tsx           # Dashboard com métricas
│   │   │   └── 📁 components/
│   │   │       ├── ProductionChart.tsx    # Gráfico de produção
│   │   │       ├── EmissionsGauge.tsx     # Medidor de emissões
│   │   │       ├── CertificatesTable.tsx  # Tabela de certificados
│   │   │       └── WaterCompliance.tsx    # Conformidade hídrica
│   │   │
│   │   ├── 📁 auditor/            # Portal do Auditor
│   │   │   ├── page.tsx           # Página principal
│   │   │   ├── 📁 components/
│   │   │   │   └── BatchVerification.tsx  # Verificação de lotes
│   │   │   └── 📁 verify/[batchId]/
│   │   │       └── page.tsx       # Verificação individual
│   │   │
│   │   ├── 📁 producer/           # Portal do Produtor
│   │   │   ├── page.tsx           # Página principal
│   │   │   └── 📁 batches/
│   │   │       └── page.tsx       # Gerenciamento de lotes
│   │   │
│   │   └── 📁 api/                # API Proxy
│   │       └── [...path]/route.ts # Proxy para backend
│   │
│   └── 📁 src/
│       ├── 📁 components/
│       │   ├── 📁 layout/         # Componentes de layout
│       │   │   └── Navbar.tsx
│       │   ├── 📁 shared/         # Componentes compartilhados
│       │   │   ├── ErrorBoundary.tsx
│       │   │   ├── LoadingSpinner.tsx
│       │   │   └── QRCode.tsx
│       │   └── 📁 ui/             # Componentes UI (shadcn)
│       │       ├── button.tsx
│       │       ├── card.tsx
│       │       ├── badge.tsx
│       │       ├── dialog.tsx
│       │       ├── dropdown-menu.tsx
│       │       ├── input.tsx
│       │       ├── label.tsx
│       │       ├── progress.tsx
│       │       ├── table.tsx
│       │       └── tabs.tsx
│       │
│       ├── 📁 hooks/              # React Hooks
│       │   ├── useBatch.ts        # Hook de lotes
│       │   ├── useCertificate.ts  # Hook de certificados
│       │   └── useCompliance.ts   # Hook de compliance
│       │
│       ├── 📁 lib/                # Utilitários
│       │   ├── api.ts             # Cliente API
│       │   ├── web3.ts            # Conexão Web3
│       │   └── constants.ts       # Constantes
│       │
│       └── 📁 types/              # Tipos TypeScript
│           ├── index.ts
│           ├── batch.ts
│           ├── certificate.ts
│           └── compliance.ts
│
├── 📁 iot/                        # Simulador IoT
│   ├── simulator.py               # Simulador de sensores
│   └── config.yaml                # Configuração dos sensores
│
├── 📁 monitoring/                 # Monitoramento
│   ├── prometheus.yml             # Config Prometheus
│   ├── 📁 alerts/                 # Regras de alerta
│   └── 📁 grafana/                # Dashboards Grafana
│
├── 📁 scripts/                    # Scripts utilitários
│   ├── init_db.py                 # Inicialização do banco
│   ├── seed_data.py               # Dados de exemplo
│   ├── deploy_contracts.sh        # Deploy de contratos
│   ├── generate_tree.py           # Gerador de árvore
│   └── create_cbam_report.py      # Relatório CBAM
│
├── 📁 tests/                      # Testes automatizados
│   ├── conftest.py                # Configuração pytest
│   ├── test_api.py                # Testes de API
│   ├── test_blockchain.py         # Testes blockchain
│   ├── test_compliance.py         # Testes compliance
│   ├── test_delegation.py         # Testes delegação
│   ├── test_integration.py        # Testes integração
│   └── test_oracle.py             # Testes oráculo
│
├── 📁 docs/                       # Documentação
│   ├── architecture.md            # Arquitetura do sistema
│   ├── api_reference.md           # Referência da API
│   ├── cbam_compliance.md         # Guia CBAM
│   ├── delegation_guide.md        # Guia de delegação
│   ├── deployment.md              # Guia de deploy
│   └── namibia_reference.md       # Modelo Namíbia
│
├── 📁 alembic/                    # Migrações de banco
│   ├── env.py                     # Config Alembic
│   └── 📁 versions/               # Versões de migração
│
├── docker-compose.yml             # Orquestração Docker
├── docker-compose.prod.yml        # Docker produção
├── Makefile                       # Comandos make
└── README.md                      # Documentação principal
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

---

## 3. FUNCIONALIDADES DETALHADAS

### 3.1 🔙 Backend (FastAPI)

#### API REST (`backend/api/routes/`)

| Rota | Endpoint | Descrição |
|------|----------|-----------|
| **Telemetria** | `POST /api/v1/telemetry` | Ingestão de dados de sensores IoT |
| | `GET /api/v1/telemetry/{sensor_id}` | Histórico de telemetria |
| **Lotes** | `POST /api/v1/batches` | Criar novo lote de H₂ |
| | `GET /api/v1/batches/{batch_id}` | Detalhes do lote |
| | `POST /api/v1/batches/{batch_id}/certify` | Certificar lote (mint SBT) |
| **Certificados** | `GET /api/v1/certificates` | Listar certificados |
| | `GET /api/v1/certificates/{token_id}` | Verificar certificado |
| | `POST /api/v1/certificates/{token_id}/consume` | Consumir certificado |
| **Compliance** | `POST /api/v1/compliance/check` | Verificar compliance |
| | `GET /api/v1/compliance/report/{batch_id}` | Relatório CBAM |
| **Delegação** | `POST /api/v1/delegation/authorize` | Autorizar declarante |
| | `GET /api/v1/delegation/status/{producer_id}` | Status delegação |
| **Relatórios** | `GET /api/v1/reports/cbam/{batch_id}` | Relatório CBAM completo |

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
- `verification.py` - Verificação on-chain de certificados

#### Oráculo (`backend/oracle/`)

- `satellite_monitor.py` - **Monitoramento por satélite** (modelo Namíbia)
  - `get_co2_data()` - Dados de CO₂ por localização
  - `get_water_data()` - Qualidade/disponibilidade de água
  - `get_renewable_energy_production()` - Verificação de energia renovável
  - `verify_additionality()` - Verificação de adicionalidade via satélite
- `automation.py` - Automação de tarefas periódicas

#### Banco de Dados (`backend/db/`)

- **TimescaleDB** - Banco de séries temporais para telemetria
- Modelos: batch, certificate, telemetry_record, audit_log, delegation
- Migrações via Alembic

---

### 3.2 ⛓️ Smart Contracts (Solidity)

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

### 3.3 🎨 Frontend (Next.js 14 + TypeScript)

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
- Gerenciamento de lotes de produção
- Visualização de telemetria dos sensores

#### Componentes

- **UI (shadcn)**: button, card, badge, dialog, dropdown-menu, input, label, progress, table, tabs
- **Shared**: ErrorBoundary, LoadingSpinner, QRCode
- **Layout**: Navbar com navegação entre portais

#### Hooks React
- `useBatch()` - Gerenciamento de lotes
- `useCertificate()` - Gerenciamento de certificados
- `useCompliance()` - Verificação de compliance

---

### 3.4 📡 IoT Simulator

**`iot/simulator.py`**
- Simula sensores de produção de H₂ verde
- Envia telemetria para API via HTTP
- Configurável via `config.yaml`
- Gera dados: energy_source, power_generated_mwh, ghg_emissions, water_consumption
- Modo `force_compliant` para simular lotes conformes

---

### 3.5 📊 Monitoramento

- **Prometheus** (`monitoring/prometheus.yml`) - Coleta de métricas
- **Grafana** (`monitoring/grafana/`) - Dashboards visuais
- **Alertas** (`monitoring/alerts/`) - Regras de notificação
- Métricas: telemetria por segundo, batches certificados, compliance rate

---

### 3.6 🧪 Testes

| Arquivo | Escopo |
|---------|--------|
| `test_api.py` | Testes de endpoints REST |
| `test_blockchain.py` | Testes de integração blockchain |
| `test_compliance.py` | Testes de verificação CBAM |
| `test_delegation.py` | Testes de delegação |
| `test_integration.py` | Testes de integração geral |
| `test_oracle.py` | Testes do oráculo/satélite |

---

## 4. FLUXO DE TRABALHO COMPLETO

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
│ SBT    │  │ Não-Conform. │
└───┬────┘  └──────────────┘
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

## 5. TECNOLOGIAS UTILIZADAS

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

---

## 6. CONFORMIDADE CBAM 2026

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

## 7. ESTRUTURA DE DADOS

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

## 8. PRÓXIMOS PASSOS (ROADMAP)

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

## 9. COMANDOS PARA RODAR O PROJETO NO TERMINAL

### 🚀 Opção 1: Docker (Tudo de uma vez - Recomendado)

```bash
# 1. Subir todos os serviços (backend, frontend, banco, blockchain)
docker-compose up -d

# 2. Verificar se tudo está rodando
docker-compose ps

# 3. Ver logs em tempo real
docker-compose logs -f

# 4. Parar tudo
docker-compose down

# Acessar:
# - Frontend: http://localhost:3000
# - Backend:  http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Hardhat:  http://localhost:8545
```

---

### 🚀 Opção 2: Desenvolvimento Local (Passo a Passo)

#### Terminal 1 - Banco de Dados (TimescaleDB + Redis)
```bash
# Iniciar TimescaleDB
docker run -d --name h2v_timescaledb -p 5432:5432 ^
  -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password ^
  -e POSTGRES_DB=h2v_trust ^
  timescale/timescaledb:latest-pg16

# Iniciar Redis (cache)
docker run -d --name h2v_redis -p 6379:6379 redis:7-alpine
```

#### Terminal 2 - Backend (FastAPI)
```bash
# Navegar para o diretório do backend
cd c:\Source\Repos\h2v-trust\backend

# Criar ambiente virtual (primeira vez)
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências (primeira vez)
pip install -r requirements.txt

# Inicializar banco de dados (primeira vez)
python ..\scripts\init_db.py

# Rodar servidor de desenvolvimento
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# API disponível em: http://localhost:8000
# Documentação: http://localhost:8000/docs
```

#### Terminal 3 - Smart Contracts (Blockchain)
```bash
# Navegar para o diretório de contratos
cd c:\Source\Repos\h2v-trust\contracts

# Instalar dependências (primeira vez)
npm install

# Iniciar nó Hardhat local (blockchain de desenvolvimento)
npx hardhat node

# Nó rodando em: http://localhost:8545
```

#### Terminal 4 - Deploy dos Contratos (após nó Hardhat estar rodando)
```bash
# Em outro terminal, com o nó Hardhat rodando:
cd c:\Source\Repos\h2v-trust\contracts

# Fazer deploy dos contratos
npx hardhat run scripts/deploy.js --network localhost

# (Alternativa via script shell)
# .\scripts\deploy_contracts.sh
```

#### Terminal 5 - Frontend (Next.js)
```bash
# Navegar para o diretório do frontend
cd c:\Source\Repos\h2v-trust\frontend

# Instalar dependências (primeira vez)
npm install

# Rodar servidor de desenvolvimento
npm run dev

# Frontend disponível em: http://localhost:3000
```

#### Terminal 6 - Simulador IoT (Opcional)
```bash
# Navegar para o diretório IoT
cd c:\Source\Repos\h2v-trust\iot

# Instalar dependências (primeira vez)
pip install httpx pyyaml

# Rodar simulador de sensores
python simulator.py

# O simulador envia dados de telemetria para a API automaticamente
```

---

### 🧪 Comandos de Teste

```bash
# Testes do Backend
cd c:\Source\Repos\h2v-trust\backend
pytest tests/ -v

# Testes específicos
pytest tests/test_compliance.py -v
pytest tests/test_api.py -v
pytest tests/test_blockchain.py -v
pytest tests/test_delegation.py -v
pytest tests/test_integration.py -v
pytest tests/test_oracle.py -v

# Testes dos Smart Contracts
cd c:\Source\Repos\h2v-trust\contracts
npx hardhat test

# Testes do Frontend
cd c:\Source\Repos\h2v-trust\frontend
npm test
```

---

### 📋 Comandos Úteis

```bash
# Verificar versões
python --version
node --version
npm --version
docker --version

# Verificar containers rodando
docker ps

# Parar container específico
docker stop h2v_timescaledb

# Remover container
docker rm h2v_timescaledb

# Ver logs do backend
docker logs h2v-trust-backend -f

# Acessar banco de dados via CLI
docker exec -it h2v_timescaledb psql -U user -d h2v_trust

# Recriar banco de dados do zero
cd c:\Source\Repos\h2v-trust
python scripts\init_db.py

# Popular com dados de exemplo
python scripts\seed_data.py

# Gerar relatório CBAM de teste
python scripts\create_cbam_report.py
```

---

### 🔄 Ordem de inicialização recomendada

```
1º → Banco de Dados (TimescaleDB + Redis)
2º → Backend (FastAPI)
3º → Smart Contracts (Hardhat Node)
4º → Deploy dos Contratos
5º → Frontend (Next.js)
6º → Simulador IoT (opcional)
```

### ✅ Verificação rápida de tudo funcionando

```bash
# Testar health check do backend
curl http://localhost:8000/health

# Resposta esperada:
# {"status": "ok", "service": "H2V-Trust"}

# Testar documentação da API
start http://localhost:8000/docs

# Testar frontend
start http://localhost:3000
```

---

## 10. ESTATÍSTICAS DO PROJETO

| Item | Quantidade |
|------|------------|
| Arquivos Python | ~40 |
| Arquivos TypeScript/TSX | ~30 |
| Smart Contracts Solidity | 7 (4 contratos + 3 interfaces) |
| Testes | 7 suites |
| Documentos | 8+ |
| Scripts utilitários | 12 |
| Componentes UI | 10 (shadcn) |
| Endpoints API | 12+ |
| Dockerfiles | 3 |

---

*Relatório gerado em 24/04/2026*
*H2V-Trust - Plataforma de Rastreabilidade Blockchain para Hidrogênio Verde*

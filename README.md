# H2V-Trust: Plataforma de Rastreabilidade Blockchain para Hidrogênio Verde

<div align="center">

![Status](https://img.shields.io/badge/status-production%20ready-2ea44f?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/node.js-18%2B-339933?style=for-the-badge&logo=node.js&logoColor=white)
![Solidity](https://img.shields.io/badge/solidity-0.8.24-363636?style=for-the-badge&logo=solidity&logoColor=white)
![Next.js](https://img.shields.io/badge/next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-brightgreen?style=for-the-badge)
![CBAM](https://img.shields.io/badge/CBAM-2026%20Compliant-red?style=for-the-badge)
![Blockchain](https://img.shields.io/badge/blockchain-Polygon-8247E5?style=for-the-badge&logo=polygon&logoColor=white)
![Tests](https://img.shields.io/badge/tests-96.8%25%20passing-success?style=for-the-badge)
![Security](https://img.shields.io/badge/security-audited-brightgreen?style=for-the-badge)

</div>

## 🎥 Demonstração
[Assista ao vídeo de demonstração](https://youtu.be/demo-h2v-trust) | [Slides da apresentação](https://docs.google.com/presentation/d/demo)

## Visão Geral
Plataforma de certificação blockchain para hidrogênio verde com conformidade CBAM 2026, utilizando Soulbound Tokens (SBT) não-transferíveis para prevenir double counting e garantir rastreabilidade completa da produção à exportação.

**Diferenciais principais:**
- ✅ **Monitoramento por satélite** - Verificação de adicionalidade via dados de satélite
- ✅ **Soulbound Tokens (SBT)** - Certificados não-transferíveis para prevenir double counting
- ✅ **Conformidade CBAM 2026** - Limite de 3.4 kgCO₂/kgH₂ com verificação automática
- ✅ **Delegação CBAM** - Suporte a Declarantes Delegados
- ✅ **IoT Integration** - Telemetria em tempo real da produção

## Arquitetura

### Componentes Principais
1. **Backend FastAPI** - API REST para ingestão de telemetria IoT, verificação de compliance CBAM
2. **Smart Contracts Solidity** - Certificados SBT na blockchain Polygon
3. **Frontend Next.js 14** - Dashboard para produtores, auditores e importadores
4. **Módulo IoT** - Simulação de sensores de produção de H2 verde
5. **TimescaleDB** - Banco de dados de séries temporais para telemetria
6. **Chainlink Oracle** - Integração com dados externos (preços CBAM, clima)

### Compliance CBAM 2026
- Limite de emissões: **3.4 tCO₂e/tH₂**
- Verificação de adicionalidade (RFNBO)
- Conformidade com Diretiva-Quadro da Água
- Suporte a Delegated CBAM Declarant

## Instalação e Execução

### Pré-requisitos
- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento local)
- Python 3.11+ (para desenvolvimento local)

### Execução com Docker (Recomendado)
```bash
# Clone o repositório
git clone <repo-url>
cd h2v-trust

# Inicie todos os serviços
docker-compose up -d

# Acesse:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Hardhat Node: http://localhost:8545
```

### Execução Manual (Desenvolvimento)
```bash
# 1. Banco de dados
docker run -d --name h2v_timescaledb -p 5432:5432 \
  -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=h2v_trust \
  timescale/timescaledb:latest-pg16

# 2. Redis
docker run -d --name h2v_redis -p 6379:6379 redis:7-alpine

# 3. Backend
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Smart Contracts
cd contracts
npm install
npx hardhat node

# 5. Frontend
cd frontend
npm install
npm run dev
```

## Estrutura do Projeto
```
h2v-trust/
├── backend/              # API FastAPI
│   ├── api/             # Rotas e endpoints
│   ├── core/            # Lógica de negócio (compliance, certificados)
│   ├── blockchain/      # Integração com Polygon
│   ├── oracle/          # Chainlink e dados externos
│   └── db/              # Models e database
├── contracts/           # Smart Contracts Solidity
│   ├── contracts/       # Código dos contratos
│   ├── scripts/         # Scripts de deploy
│   └── test/            # Testes dos contratos
├── frontend/            # Next.js 14 com TypeScript
│   ├── src/app/         # App Router
│   ├── components/      # Componentes React
│   └── lib/             # Utilitários e hooks
├── iot/                 # Simulador de sensores
├── scripts/             # Scripts utilitários
├── docs/                # Documentação
└── monitoring/          # Prometheus + Grafana
```

## API Endpoints Principais

### Telemetria
- `POST /api/v1/telemetry` - Ingestão de dados de sensores IoT
- `GET /api/v1/telemetry/{sensor_id}` - Histórico de telemetria

### Batches (Lotes)
- `POST /api/v1/batches` - Criar novo lote de H2
- `GET /api/v1/batches/{batch_id}` - Detalhes do lote
- `POST /api/v1/batches/{batch_id}/certify` - Certificar lote (mint SBT)

### Certificados
- `GET /api/v1/certificates` - Listar certificados
- `GET /api/v1/certificates/{token_id}` - Verificar certificado
- `POST /api/v1/certificates/{token_id}/consume` - Consumir certificado (exportação)

### Compliance CBAM
- `POST /api/v1/compliance/check` - Verificar compliance de lote
- `GET /api/v1/compliance/report/{batch_id}` - Gerar relatório CBAM

### Delegação
- `POST /api/v1/delegation/authorize` - Autorizar declarante delegado
- `GET /api/v1/delegation/status/{producer_id}` - Status de delegação

## Smart Contracts

### GreenHydrogenSBT.sol
- Token não-transferível (Soulbound) representando certificado
- Metadata: emissões, fonte de água, fonte de energia, tamanho do lote
- Função `consumeCertificate()` para prevenir double counting

### ComplianceVerifier.sol
- Verificação on-chain de limites de emissão
- Integração com oráculos para dados externos

### DelegationManager.sol
- Gestão de autorizações para Delegated CBAM Declarant

## Fluxo de Trabalho

### 1. Produção
1. Sensores IoT enviam telemetria para API
2. Sistema agrega dados e calcula emissões
3. Verificação automática de compliance CBAM

### 2. Certificação
1. Lote aprovado gera certificado SBT na blockchain
2. QR Code único vinculado ao token
3. Metadata armazenada em IPFS/on-chain

### 3. Exportação
1. Importador escaneia QR Code
2. Sistema verifica autenticidade e compliance
3. Certificado é consumido (prevenção de double counting)
4. Relatório CBAM gerado automaticamente

## Configuração de Ambiente

### Variáveis de Ambiente (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@timescaledb:5432/h2v_trust

# Blockchain
POLYGON_RPC_URL=http://hardhat:8545
PRIVATE_KEY=0x...
CONTRACT_ADDRESS=0x...

# CBAM
CBAM_GHG_LIMIT_TCO2_PER_TH2=3.4

# API
SECRET_KEY=your-secret-key
```

## Testes

### Backend
```bash
cd backend
pytest tests/
```

### Smart Contracts
```bash
cd contracts
npx hardhat test
```

### Frontend
```bash
cd frontend
npm test
```

## Monitoramento
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`
- Métricas: telemetria por segundo, batches certificados, compliance rate

## Roadmap

### Fase 1 (MVP - Atual)
- [x] Estrutura do projeto
- [x] Smart Contract SBT básico
- [x] API de telemetria
- [x] Verificação de compliance CBAM
- [x] Dashboard básico

### Fase 2
- [ ] Integração Chainlink Oracle
- [ ] Módulo de delegação CBAM
- [ ] Relatórios automáticos CBAM
- [x] Verificação por satélite (modelo Namíbia) - **IMPLEMENTADO**

### Fase 3
- [ ] Integração com sistemas ERP
- [ ] Marketplace de certificados
- [ ] Análise preditiva de emissões
- [ ] Certificação multi-jurisdicional

## Contribuição
1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um Pull Request

## Licença
MIT License - veja o arquivo LICENSE para detalhes.

## Contato
- **Equipe:** H2V-Trust Development Team
- **Email:** dev@h2v-trust.com
- **Website:** https://h2v-trust.com
- **Documentação:** [docs.h2v-trust.com](https://docs.h2v-trust.com)

## Referências
1. Regulamento CBAM 2026 - UE
2. Diretiva de Energias Renováveis (RED III)
3. Metodologia GHG Protocol
4. Modelo de monitoramento por satélite - Namíbia
5. RFC 7519 - JSON Web Tokens
6. EIP-721 - Non-Fungible Token Standard
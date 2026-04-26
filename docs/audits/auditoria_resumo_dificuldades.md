# Auditoria do Projeto h2v-trust - Resumo e Maiores Dificuldades

## 📊 Estado Atual do Projeto

### Backend (Python/FastAPI)
- **61 arquivos Python** - Cobertura completa
- API REST com FastAPI, SQLAlchemy, Web3.py
- Rotas: batches, certificates, compliance, delegation, reports, telemetry
- Blockchain: minting, verification, SBT manager, Web3 client
- Oracle: satellite monitor, chainlink client, sensor aggregator
- DB: TimescaleDB (hypertable), SQLite (fallback), Alembic migrations
- **Testes: 7 em tests/ + 38 na raiz**

### Frontend (Next.js 14.2.3)
- **23 páginas/componentes** em frontend/app/
- **30 componentes/hooks/lib** em frontend/src/
- UI: shadcn/ui components (badge, button, card, dialog, dropdown-menu, etc.)
- Hooks: useBatch, useCertificate, useCompliance
- Páginas: dashboard, auditor, producer (batches, certificates, delegation)

### Smart Contracts (Solidity)
- **8 contratos**: GreenHydrogenSBT, BatchRegistry, ComplianceVerifier, DelegationManager + interfaces

### Documentação
- **7 documentos**: architecture, api_reference, cbam_compliance, delegation_guide, deployment, namibia_reference

---

## 🔴 MAIORES DIFICULDADES

### 1. 🏗️ ESTRUTURA MONOREPO CONFUSA (CRÍTICO)
**Problema:** O projeto tem `package.json` na raiz E no `frontend/`, mas o npm faz hoisting para a raiz. O Next.js 14.2.3 está instalado no `node_modules` da raiz, mas o diretório `app/` está em `frontend/app/`. Para rodar o Next.js, precisa-se usar `npx next dev frontend` em vez de apenas `npx next dev`.

**Impacto:** Dificuldade em iniciar o frontend, confusão sobre onde instalar dependências.

**Solução:** 
- Decidir se o projeto é monorepo (com workspaces) ou se o frontend é independente
- Se monorepo: configurar npm workspaces corretamente no `package.json` da raiz
- Se independente: remover `package.json` da raiz e instalar tudo em `frontend/`

### 2. 🔗 INTEGRAÇÃO BLOCKCHAIN VS MOCK (ALTA)
**Problema:** O sistema tem lógica completa de blockchain (Web3, minting, eventos) mas não há uma blockchain real rodando. Os testes usam mocks extensivos. O fluxo de telemetria tenta mintar antes de salvar no DB, mas falha se não há blockchain.

**Impacto:** Funcionalidade blockchain não testável em ambiente de desenvolvimento sem Hardhat/Ganache.

**Solução:** 
- Manter mock para desenvolvimento
- Criar script docker-compose para subir Hardhat local
- Documentar claramente quando usar mock vs real

### 3. 🐍 VENV DUPLICADO (MÉDIO)
**Problema:** Existem dois ambientes virtuais Python:
- `venv/` (Python 3.12, Linux .so files - provavelmente de WSL/Docker)
- `venv/` (Python 3.13, Windows .pyd files)

**Impacto:** Pode causar conflitos de importação, especialmente com bibliotecas nativas.

**Solução:** 
- Recriar venv do zero para Windows
- Usar `requirements.txt` para garantir consistência

### 4. 📦 DEPENDÊNCIAS NPM PESADAS (MÉDIO)
**Problema:** O `package.json` inclui `wagmi`, `viem`, `ethers` (bibliotecas Web3) que puxam muitas dependências (WalletConnect, Metamask SDK, etc.). O `package-lock.json` tem **460 KB**.

**Impacto:** `npm install` demora muito, node_modules grande.

**Solução:**
- Avaliar se wagmi/viem são realmente necessários ou se ethers basta
- Considerar lazy loading para bibliotecas Web3

### 5. 🧪 45 ARQUIVOS DE TESTE (MÉDIO)
**Problema:** Existem **38 testes na raiz** + **7 em tests/**. Muitos são experimentais/descartáveis (test_api_clean.py, test_api_simple.py, test_api_final_no_unicode.py, etc.).

**Impacto:** Poluição visual, dificuldade de saber quais testes são oficiais.

**Solução:**
- Manter apenas os 7 testes em `tests/` como oficiais
- Mover/remover os 38 testes da raiz
- Criar um `Makefile` com comandos `test`, `test-api`, `test-blockchain`

### 6. 🗄️ TIMESCALEDB VS SQLITE (MÉDIO)
**Problema:** O sistema tenta usar TimescaleDB (PostgreSQL) mas faz fallback para SQLite. As migrations Alembic estão configuradas para TimescaleDB.

**Impacto:** Comportamento diferente em dev vs prod, hypertables não funcionam em SQLite.

**Solução:**
- Usar SQLite para desenvolvimento (sem hypertables)
- Usar TimescaleDB apenas em produção (Docker)
- Documentar claramente as diferenças

### 7. 🔄 FLUXO TELEMETRIA-BLOCKCHAIN (BAIXO)
**Problema:** O endpoint de telemetria faz minting blockchain antes de salvar no DB. Se blockchain falha, salva como "pending". Isso é correto mas complexo.

**Impacto:** Lógica de auditoria e reconciliação necessária para certificados "pending".

**Solução:** Já implementada - audit logging em cada passo.

### 8. 📝 ARQUIVOS DE AUDITORIA (.md) (BAIXO)
**Problema:** Muitos arquivos de documentação/auditoria na raiz (auditoria_completa_final.md, auditoria_completa_projeto_final.md, etc.).

**Impacto:** Poluição visual na raiz do projeto.

**Solução:** Mover para `docs/` ou `audits/`.

---

## ✅ O QUE FUNCIONA BEM

1. **Backend Python** - Completo e bem estruturado (61 arquivos)
2. **Testes oficiais** (`tests/`) - 7 testes passando cobrindo API, blockchain, compliance, delegação, integração, oracle
3. **Smart Contracts** - 8 contratos Solidity com interfaces
4. **Componentes UI** - 30 componentes bem organizados (shadcn/ui)
5. **Documentação** - 7 documentos de referência
6. **Alembic Migrations** - Configurado com TimescaleDB
7. **Docker** - docker-compose.yml e docker-compose.prod.yml configurados

---

## 🎯 PRÓXIMOS PASSOS RECOMENDADOS

1. **Resolver estrutura monorepo** (dificuldade #1)
2. **Limpar testes** - manter só os oficiais em `tests/` (dificuldade #5)
3. **Mover arquivos de auditoria** para `docs/` (dificuldade #8)
4. **Recriar venv** limpo para Windows (dificuldade #3)
5. **Fazer o Next.js rodar** sem precisar de `npx next dev frontend`
6. **Subir ambiente completo** com Docker (backend + frontend + blockchain)

# CLAUDE.md — H2V-Trust

## Stack
- Backend: Python 3.11, FastAPI 0.115, SQLAlchemy 2.0, TimescaleDB, Alembic
- Frontend: Next.js 14 (App Router), TypeScript 5.4, Tailwind CSS, shadcn/ui
- Blockchain: Solidity 0.8.24, Hardhat, Web3.py, Polygon
- Infra: Docker Compose (dev/prod), Nginx, Prometheus, Grafana

## Comandos Essenciais
- `make dev-start` — Iniciar ambiente dev (USA SEMPRE ESTE)
- `make dev-check` — Verificar saúde (contêineres, órfãos, fantasmas)
- `make dev-reset` — Reset completo + emergência
- `make dev-seed` — Popular banco com dados demo
- **NUNCA** executar 2 comandos Docker em simultâneo

## 12 Regras de Ouro
1. **Bibliotecas permitidas:** FastAPI, SQLAlchemy, Pydantic, Web3, httpx, alembic, python-jose, passlib[bcrypt], bcrypt, redis, psycopg2-binary
2. **Type hints obrigatórios** em todas as funções (args + return)
3. **Try/except + logger.error** em todas as rotas
4. **Isolamento multi-tenant:** queries filtradas por `tenant_id` (`get_tenant_id()`)
5. **Controlo de contexto:** Não ler ficheiros > 500 linhas sem aprovação explícita
6. **Checkpoints:** Em tarefas multi-passo, validar cada etapa antes de avançar
7. **Conflitos:** Se detetares código conflituoso, PARA e pergunta
8. **Proibição de "limpezas laterais":** Não mexer em código não relacionado
9. **Auto-verificação:** Depois de cada tarefa, rever o próprio código antes de finalizar
10. **Registo de decisões:** Escrever notas de decisão no `.cline/memory-bank.md`
11. **Limite de abstração:** Máximo 1 nível de abstração por tarefa
12. **Confirmação de sucesso:** Provar que o código funciona (teste, curl, screenshot)

## Autenticação
- JWT Bearer (prioridade) > X-API-Key (fallback legado)
- Roles: admin (2) > operator (1) > auditor (0)
- Tokens expiram em 60min; refresh token em desenvolvimento

## Estrutura de Diretórios
- `backend/api/routes/` — Endpoints REST (batches, certificates, compliance, delegation, reports, telemetry, auth, admin)
- `backend/core/` — Regras CBAM (compliance.py, emissions.py, water.py)
- `backend/db/models/` — 9 modelos SQLAlchemy (Batch, Certificate, Tenant, User, etc.)
- `frontend/app/` — 16 páginas (producer, auditor, admin, dashboard, login)
- `contracts/contracts/` — 4 contratos Solidity + interfaces

## Credenciais de Teste (Seed Data)
- **Admin:** admin@h2v-trust.com / H2v@Trust!2026
- **Operator:** operator@produtor-alfa.com / H2v@Trust!2026
- **Auditor:** auditor@h2v-trust.com / H2v@Trust!2026
- **API Keys de Tenant (legacy):**
  - Produtor Alfa: `key-produtor-alfa-123`
  - Produtor Beta: `key-produtor-beta-456`
  - Auditor Global: `key-auditor-global-789`

## URLs de Desenvolvimento
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- Frontend: http://localhost:3000
- Hardhat RPC: http://localhost:8545

## Ambiente
- **5 contêineres:** timescaledb, redis, hardhat, backend, frontend
- **Health:** `curl http://localhost:8000/health`
- **Blockchain:** Hardhat local (chain_id 1337), Polygon Amoy (testnet planejada)
- **Fallback offline:** O sistema continua a funcionar mesmo sem blockchain (MOCK_MODE)

## Protocolos de Emergência
- **Container fantasma:** Siga `.clinerules/01-docker.md` — Protocolo Níveis 1-4
- **Build do frontend:** Aguarde 5-10min, monitore com `docker compose logs -f frontend`
- **Health check fail:** Execute `make dev-check` antes de qualquer reset

## Memória de Longo Prazo
- **Arquivo:** `.cline/memory-bank.md`
- **Quando atualizar:** Após bugs significativos, novas funcionalidades, mudanças de arquitetura
- **Formato:** Problema → Solução → Resultado → Observações

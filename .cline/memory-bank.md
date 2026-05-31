# H2V-Trust Memory Bank

## Contexto Ativo (2026-05-28)

- **Fase Atual**: Correção de erros de compilação do frontend (GOVBR-DS) + Correção de import do web3.py no backend + Correção do proxy (duplex).
- **Últimas Ações**: 
  - Corrigido `BrHeaderWrapper.tsx` — prop `dark` → `dark={true}`
  - Corrigido `VlibrasWrapper.tsx` — mapeamento correto do export default
  - Substituído `BrSignInWrapper.tsx` — `BrSignIn` não existe na biblioteca GOVBR-DS, substituído por formulário Tailwind funcional com integração JWT
  - Frontend compilado com sucesso: `✓ Compiled / in 16.5s (586 modules)`, `✓ Compiled /login in 1072ms (543 modules)`
  - Corrigido `backend/blockchain/web3_client.py` — `ExtraDataToPOAMiddleware` renomeado para `geth_poa_middleware` no web3.py >= 7.x
  - Corrigido `frontend/app/api/[...path]/route.ts` — adicionado `duplex: 'half'` no fetch do proxy para compatibilidade com Node.js >= 18
  - Login via proxy do frontend testado com sucesso: JWT token retornado ✅
- **Problemas Conhecidos**: Bug fantasma do Docker (#253) — ver `.clinerules/01-docker.md` para protocolo de emergência.
- **Credenciais de Teste**:
  | Usuário | Email | Senha | Role |
  |---------|-------|-------|------|
  | Admin | admin@h2v-trust.com | H2v@Trust!2026 | admin |
  | Operator | operator@produtor-alfa.com | H2v@Trust!2026 | operator |
  | Auditor | auditor@h2v-trust.com | H2v@Trust!2026 | auditor |
- **Comandos Chave**: `make dev-start`, `make dev-check`, `make dev-reset`.

## Estado Atual (2026-05-28)

### Ambiente
- **Status:** Rodando via Docker Compose (modo dev)
- **Containers:** 5 serviços (timescaledb, redis, hardhat, backend, frontend) — todos `Up` e `healthy`
- **Backend:** FastAPI na porta 8000 - Health check: todos os sistemas OK
- **Frontend:** Next.js 14 na porta 3000 - Compilado com sucesso (0 erros TypeScript)
- **Blockchain:** Hardhat local node na porta 8545 (chain_id: 1337)
- **Banco de Dados:** TimescaleDB na porta 5432

### Últimas Atividades

#### Correção: BrSignIn não existe na biblioteca GOVBR-DS (5/28/2026 - 21:11)

##### Problema
- **Sintoma:** Erro `Element type is invalid. Received a promise that resolves to: undefined` ao acessar `/login`
- **Log:** `mod.BrSignIn` era `undefined` — o componente não existe na biblioteca `@govbr-ds/react-components`
- **Causa raiz:** O `BrSignInWrapper.tsx` tentava importar `BrSignIn` de `@govbr-ds/react-components`, mas este componente não faz parte da biblioteca

##### Diagnóstico
- Verificado via `docker compose exec frontend sh -c "ls node_modules/@govbr-ds/react-components/dist/components/"` — lista completa de 35 componentes
- **BrSignIn NÃO está na lista.** Componentes disponíveis: BrAccordion, BrAvatar, BrBreadcrumbs, BrButton, BrCard, BrCarousel, BrCheckbox, BrDateTimePicker, BrDivider, BrFooter, BrHeader, BrInput, BrList, BrLoading, BrMagicButton, BrMenu, BrMessage, BrModal, BrNotification, BrPagination, BrRadio, BrSelect, BrSkeleton, BrSkipLink, BrSwitch, BrTab, BrTable, BrTag, BrTextarea, BrTooltip, BrUpload, BrWizard

##### Solução Implementada
1. **`frontend/src/components/auth/BrSignInWrapper.tsx`** — Substituído completamente por formulário Tailwind puro:
   - Tema escuro com gradiente (`from-slate-900 via-slate-800 to-slate-900`)
   - Logo H2V-Trust com ícone verde
   - Campos de email e senha com validação
   - Loading state com spinner SVG
   - Tratamento de erro (exibição em caixa vermelha)
   - Redirecionamento inteligente baseado no perfil do usuário (admin → /admin, operator → /producer, auditor → /auditor)
   - Integração com `useAuth` hook existente (login JWT)

##### Resultado
- Frontend compilado: `✓ Compiled / in 16.5s (586 modules)` ✅
- Frontend compilado: `✓ Compiled /login in 1072ms (543 modules)` ✅
- Landing page (`/`): HTTP 200 ✅
- Login (`/login`): HTTP 200 ✅
- Middleware: `✓ Compiled /middleware in 496ms (73 modules)` ✅
- Health check backend: `{"status":"ok"}` ✅
- Zero erros de compilação ✅

#### Correção: Prop `dark` sem chaves no BrHeaderWrapper (5/28/2026 - 21:11)

##### Problema
- **Sintoma:** Warning de compilação: `Received true for a non-boolean attribute dark`
- **Causa raiz:** JSX prop `dark` sem chaves `{}` era interpretada como string `"dark"` em vez de booleano `true`

##### Solução
- **`frontend/src/components/layout/BrHeaderWrapper.tsx`** — Linha 37: `dark` → `dark={true}`

#### Correção: Export default do VLibras (5/28/2026 - 21:11)

##### Problema
- **Sintoma:** Erro `Element type is invalid. Received a promise that resolves to: undefined` ao acessar qualquer página
- **Causa raiz:** O `VlibrasWrapper.tsx` usava `mod.default` para acessar o componente VLibras, mas a biblioteca `vlibras-nextjs` exporta o componente diretamente, não como `default`

##### Solução
- **`frontend/src/components/layout/VlibrasWrapper.tsx`** — Substituído `mod.default` por `mod` no `dynamic()`:
  ```tsx
  const VLibras = dynamic(() => import("vlibras-nextjs").then((mod) => mod), { ssr: false });
  ```

### Comandos Úteis

```bash
# Rebuild e restart
docker compose up -d --build backend

# Executar migration
docker compose exec backend alembic upgrade head

# Seed completo (auth + dados de demonstração)
make dev-seed
# ou
bash scripts/seed_all.sh

# Seed apenas infraestrutura de auth
docker compose exec backend python scripts/seed_users_tenants.py

# Seed apenas dados de demonstração (requer auth)
docker compose exec backend python scripts/seed_demo_data.py

# Reset dados de demonstração (preserva auth)
docker compose exec backend python scripts/reset_demo_data.py

# Testar login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@h2v-trust.com","password":"H2v@Trust!2026"}'

# Testar admin (substitua TOKEN pelo JWT obtido)
curl http://localhost:8000/api/v1/admin/tenants \
  -H "Authorization: Bearer TOKEN"

# Verificar health
curl http://localhost:8000/health
```

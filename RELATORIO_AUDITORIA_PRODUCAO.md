# RELATÓRIO DE AUDITORIA PARA PRODUÇÃO (Docker Native)
**Projeto:** H2V-Trust — Blockchain Green Hydrogen Certification  
**Data:** 27/04/2026  
**Contexto:** Pivot de Vercel/Render → Infraestrutura Governamental Docker Native  
**Arquiteto:** CTO (Auditoria Sênior)

---

## 1. ÁRVORE DO PROJETO (ESTRUTURA DE PASTAS)

```
h2v-trust/
│
├── 📁 backend/                          # 🟢 CORAÇÃO: FastAPI Backend
│   ├── Dockerfile                       # Dockerfile DEV (uvicorn --reload)
│   ├── requirements.txt                 # Dependências Python (dev)
│   ├── requirements.prod.txt            # Dependências Python (prod + gunicorn)
│   ├── main.py                          # Entrypoint FastAPI
│   ├── config.py                        # Config central (pydantic-settings)
│   ├── api/routes/                      # Rotas: batches, certificates, compliance, delegation, telemetry, reports
│   ├── blockchain/                      # Web3 client, minting, verification, contract_abi
│   ├── core/                            # Lógica de negócio: compliance, emissions, water, certificates, delegation
│   ├── db/                              # Database: models (Batch, Certificate, TelemetryRecord, AuditLog, Delegation)
│   ├── models/                          # Pydantic models (batch, certificate, compliance, delegation, telemetry)
│   ├── services/                        # Serviços: certificate, delegation, exporter, report
│   ├── oracle/                          # Satellite monitor + automation
│   └── utils/                           # Hashing, metrics
│
├── 📁 frontend/                         # 🟢 CORAÇÃO: Next.js 14 App Router
│   ├── Dockerfile                       # Dockerfile DEV (npm run dev)
│   ├── package.json                     # Next 14.2.3, React 18, ethers, wagmi, recharts
│   ├── next.config.js                   # Rewrites API, webpack alias, Turbopack experimental
│   ├── tsconfig.json                    # TypeScript strict, path alias @/src
│   ├── tailwind.config.js               # Tailwind com CSS variables (shadcn/ui)
│   ├── app/                             # App Router: dashboard, auditor, producer, api proxy
│   │   ├── layout.tsx                   # Root layout (dark mode, Inter font)
│   │   ├── page.tsx                     # Landing page
│   │   ├── dashboard/                   # Dashboard principal
│   │   ├── auditor/                     # Auditoria + verificação de lotes
│   │   ├── producer/                    # Painel do produtor, lotes, certificados, delegação
│   │   └── api/[...path]/route.ts       # 🟡 API Proxy (Vercel legacy — ver seção 4)
│   └── src/                             # Components, hooks, lib, types, UI (shadcn)
│
├── 📁 contracts/                        # 🟢 CORAÇÃO: Smart Contracts Solidity
│   ├── contracts/                       # BatchRegistry, ComplianceVerifier, DelegationManager, GreenHydrogenSBT
│   ├── scripts/                         # deploy.js, test_mint.js
│   ├── test/                            # Testes Hardhat
│   └── hardhat.config.js                # Config Hardhat
│
├── 📁 iot/                              # Simulador IoT (dados de telemetria)
│   ├── simulator.py
│   └── config.yaml
│
├── 📁 monitoring/                       # Prometheus + Grafana
│   ├── prometheus.yml
│   ├── alerts/alert_rules.yml
│   └── grafana/dashboards/ + datasources/
│
├── 📁 tests/                            # Testes Python (pytest)
│   ├── test_api.py, test_blockchain.py, test_compliance.py, etc.
│   └── conftest.py
│
├── 📁 docs/                             # Documentação técnica
│
├── 📁 scripts/                          # Scripts auxiliares (init_db, seed_data, deploy_contracts)
│
├── 🟢 docker-compose.yml                # 🟢 COMPOSE DEV (TimescaleDB + Redis + Hardhat + Backend + Frontend)
├── 🟡 docker-compose.prod.yml           # 🟡 COMPOSE PROD (TimescaleDB + Redis + Backend + Frontend + Nginx + Prometheus + Grafana)
│
├── 🟡 render.yaml                       # 🔴 Render.com config (ABANDONADO)
├── 🟡 .env                              # 🔴 .env local (SQLite + Hardhat local)
│
└── 🟡 RELATORIO_AUDITORIA_PRODUCAO.md   # 📄 Este arquivo
```

### Legenda:
- 🟢 **Coração do sistema** — Essencial para funcionamento
- 🟡 **Atenção** — Precisa de revisão/modificação
- 🔴 **Resíduo** — Deve ser removido ou adaptado

---

## 2. DIAGNÓSTICO DE DEPENDÊNCIAS

### 2.1 Frontend (`frontend/package.json`)

| Pacote | Versão | Status | Observação |
|--------|--------|--------|------------|
| `next` | **14.2.3** | ✅ OK | Versão estável LTS |
| `react` / `react-dom` | 18.3.1 | ✅ OK | Compatível |
| `ethers` | 6.11.1 | ✅ OK | Blockchain |
| `wagmi` / `viem` | 2.9.0 | ✅ OK | Wallet connection |
| `recharts` | 2.12.7 | ✅ OK | Gráficos |
| `lucide-react` | 0.378.0 | ✅ OK | Ícones |
| `tailwindcss` | 3.4.3 | ✅ OK | CSS |
| `@radix-ui/react-dialog` | 1.0.5 | ✅ OK | UI |
| `typescript` | 5.4.5 | ✅ OK | |

**⚠️ Problema detectado:** O `next.config.js` usa `experimental.turbo` (Turbopack), que é do Next.js 16+. No Next.js 14.2.3, essa chave é **ignorada** (não quebra, mas não faz nada). O `next.config.js` também referencia `path` com `__dirname`, o que funciona apenas em CommonJS (está correto pois o config usa `module.exports`).

**Conclusão:** Dependências do frontend estão saudáveis. Nenhum conflito de versão grave.

### 2.2 Backend (`backend/requirements.txt` vs `backend/requirements.prod.txt`)

| Pacote | requirements.txt | requirements.prod.txt | Status |
|--------|-----------------|----------------------|--------|
| `fastapi` | 0.115.0 | 0.115.0 | ✅ OK |
| `uvicorn[standard]` | 0.30.0 | 0.30.0 | ✅ OK |
| `gunicorn` | ❌ Ausente | 22.0.0 | ⚠️ Só em prod |
| `sqlalchemy` | 2.0.30 | 2.0.30 | ✅ OK |
| `alembic` | 1.13.0 | 1.13.0 | ✅ OK |
| `psycopg2-binary` | 2.9.9 | 2.9.9 | ✅ OK |
| `web3` | 6.11.0 | 6.11.0 | ✅ OK |
| `celery` | 5.3.6 | ❌ Ausente | ⚠️ Só em dev |
| `redis` | 5.0.1 | 5.0.1 | ✅ OK |
| `httpx` | 0.27.0 | 0.27.0 | ✅ OK |
| `pandas` / `numpy` | 2.2.1 / 1.26.4 | 2.2.1 / 1.26.4 | ✅ OK |
| `reportlab` | 4.2.0 | 4.2.0 | ✅ OK |

**⚠️ Problema detectado:** O `docker-compose.prod.yml` referencia `Dockerfile.prod` (linha 37 e 63), mas **esse arquivo não existe**. Só existe `Dockerfile` (dev). Isso vai quebrar o build em produção.

**⚠️ Problema detectado:** O `docker-compose.prod.yml` usa `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker` no `command`, mas o `Dockerfile` (dev) não instala `gunicorn`. O `requirements.prod.txt` tem `gunicorn`, mas o Dockerfile dev copia `requirements.txt` (que não tem gunicorn).

**Conclusão:** Dependências do backend estão saudáveis, mas o Dockerfile precisa ser ajustado para produção.

---

## 3. AUDITORIA DO PADRÃO DOCKER

### 3.1 `docker-compose.prod.yml` — Análise Detalhada

| Serviço | Imagem/Dockerfile | Portas | Healthcheck | Status |
|---------|------------------|--------|-------------|--------|
| **timescaledb** | `timescale/timescaledb:latest-pg16` | 5432:5432 | ✅ pg_isready | ✅ OK |
| **redis** | `redis:7-alpine` | 6379:6379 | ✅ redis-cli ping | ✅ OK |
| **backend** | `Dockerfile.prod` ❌ **NÃO EXISTE** | 8000:8000 | ❌ Ausente | 🔴 **QUEBRA** |
| **frontend** | `Dockerfile.prod` ❌ **NÃO EXISTE** | 3000:3000 | ❌ Ausente | 🔴 **QUEBRA** |
| **nginx** | `nginx:alpine` | 80:80, 443:443 | ❌ Ausente | ⚠️ Precisa de config |
| **prometheus** | `prom/prometheus:latest` | 9090:9090 | ❌ Ausente | ✅ OK |
| **grafana** | `grafana/grafana:latest` | 3001:3000 | ❌ Ausente | ✅ OK |

### 3.2 Problemas Críticos no `docker-compose.prod.yml`

#### 🔴 CRÍTICO 1: `Dockerfile.prod` não existe
O compose.prod referencia `Dockerfile.prod` para backend e frontend, mas só existe `Dockerfile` (configurado para dev com `--reload` e sem `gunicorn`).

**Solução:** Renomear/criar `Dockerfile.prod` para cada serviço, ou alterar o compose.prod para usar `Dockerfile` com argumentos de build.

#### 🔴 CRÍTICO 2: Nginx sem configuração
O volume `./nginx/nginx.conf:/etc/nginx/nginx.conf:ro` referencia uma pasta `nginx/` que **não existe**. O diretório `nginx/` está vazio (0 arquivos).

**Solução:** Criar `nginx/nginx.conf` e `nginx/ssl/` com certificados.

#### 🔴 CRÍTICO 3: Volume do frontend `.next/static` no Nginx
O volume `./frontend/.next/static:/usr/share/nginx/html/_next/static:ro` tenta montar o `.next` **antes do build**. Isso não funciona — o `.next` é gerado durante o build do Docker.

**Solução:** Remover esse volume. O Nginx deve servir o frontend como proxy reverso para o container Next.js, não diretamente.

#### ⚠️ ATENÇÃO 4: Porta do Grafana conflita com frontend dev
Grafana mapeia `3001:3000`. Se o frontend dev estiver rodando em 3001, haverá conflito. Em produção isolada (Docker), não há problema.

#### ⚠️ ATENÇÃO 5: Variáveis de ambiente sensíveis
`PRIVATE_KEY` e `CONTRACT_ADDRESS` estão no `.env` com valores de teste (Hardhat local). Para produção, precisam ser substituídas por valores reais da Polygon.

#### ⚠️ ATENÇÃO 6: Backend sem healthcheck
O backend não tem healthcheck, mas depende de `timescaledb` e `redis` com `condition: service_healthy`. Isso está correto, mas o backend em si deveria ter um healthcheck no `/health`.

### 3.3 Rede e Portas

| Porta | Serviço | Uso |
|-------|---------|-----|
| 5432 | TimescaleDB | Banco de dados |
| 6379 | Redis | Cache/Celery |
| 8000 | Backend API | FastAPI |
| 3000 | Frontend | Next.js |
| 80/443 | Nginx | Proxy reverso + SSL |
| 9090 | Prometheus | Métricas |
| 3001 → 3000 | Grafana | Dashboards |

**Todas as portas estão mapeadas corretamente.** A comunicação entre containers usa os nomes dos serviços (ex: `timescaledb:5432`, `redis:6379`, `backend:8000`).

### 3.4 Variáveis de Ambiente Essenciais Faltando

O `docker-compose.prod.yml` espera estas variáveis do `.env` ou defaults:

| Variável | Default | Obrigatória? | Status |
|----------|---------|-------------|--------|
| `DB_USER` | `user` | Não | ✅ |
| `DB_PASSWORD` | `password` | Não | ✅ |
| `DB_NAME` | `h2v_trust` | Não | ✅ |
| `POLYGON_RPC_URL` | — | **Sim** | 🔴 **Faltando no .env local** |
| `PRIVATE_KEY` | — | **Sim** | 🔴 **Faltando no .env local** |
| `CONTRACT_ADDRESS` | — | **Sim** | 🔴 **Faltando no .env local** |
| `SECRET_KEY` | — | **Sim** | 🔴 **Faltando no .env local** |
| `CORS_ORIGINS` | `https://h2v-trust.com` | Não | ✅ |
| `NEXT_PUBLIC_API_URL` | `https://api.h2v-trust.com` | **Sim** | 🔴 **Faltando no .env local** |
| `GRAFANA_PASSWORD` | `admin` | Não | ✅ |

**Nota:** O `.env` atual tem valores para Hardhat local (teste), não para produção. Para subir com `docker-compose.prod.yml`, é necessário criar um `.env.production` com valores reais.

---

## 4. RESÍDUOS DA VERCEL (DÍVIDA TÉCNICA)

### 4.1 `frontend/next.config.js` — Rewrites para API

```javascript
async rewrites() {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/v1/:path*`,
      },
    ];
  },
```

**Problema:** Este rewrite foi criado para o deploy na Vercel, onde o frontend e backend estão em domínios diferentes. No Docker, o frontend e backend estão na **mesma rede Docker** e o frontend pode chamar `http://backend:8000/api/v1/...` diretamente.

**Impacto:** Não quebra, mas adiciona uma camada desnecessária de proxy. O frontend faz uma requisição para si mesmo (`/api/...`), que o Next.js redireciona para o backend. Isso funciona, mas é ineficiente.

**Solução:** Em produção Docker, o frontend deve chamar o backend diretamente via `NEXT_PUBLIC_API_URL=http://backend:8000`. O rewrite pode ser removido ou mantido como fallback.

### 4.2 `frontend/app/api/[...path]/route.ts` — API Proxy (317 linhas)

**Problema:** Este arquivo de 317 linhas implementa um proxy de API completo com autenticação JWT, timeout, CORS, etc. Foi criado para a Vercel onde o frontend precisava fazer proxy para o backend no Render.

**Impacto:** 
- Adiciona complexidade desnecessária no Docker
- O proxy verifica autenticação JWT, mas o backend também verifica
- Duplicação de lógica de CORS e headers
- Pode causar timeouts e erros 500 se o backend não estiver acessível

**Solução:** Em produção Docker, este proxy pode ser **removido** ou **simplificado** para apenas repassar requisições. O Nginx ou o próprio Next.js (via rewrites) já fazem isso.

### 4.3 `render.yaml` — Config do Render.com

**Problema:** Arquivo de deploy do Render.com com 56 linhas de configuração. Inclui referências a `h2v-trust-api.onrender.com`, `h2v-trust.vercel.app`, e banco de dados gerenciado pelo Render.

**Impacto:** Não afeta a execução local/Docker, mas é um artefato que pode causar confusão. Deve ser removido ou arquivado.

### 4.4 `frontend/tsconfig.json` — Include paths da Vercel

```json
"include": [
    ".next/types/**/*.ts",
    ".next/dev/types/**/*.ts"
]
```

**Problema:** Esses paths são específicos do Next.js e não causam problemas. São gerados automaticamente pelo Next.js durante o build.

**Impacto:** Nenhum. É seguro manter.

### 4.5 Erros 500 Recentes (Resolvidos)

Os erros 500 que ocorreram anteriormente foram causados por:

1. **Next.js 16 global vs Next.js 14 local**: O comando `next dev` estava usando o Next.js 16.2.4 instalado globalmente, que tem Turbopack como padrão. O cache `.next` foi gerado pelo Next.js 16 e era incompatível com o Next.js 14.2.3 do `package.json`.

2. **Solução aplicada**: 
   - Limpeza do `.next` (`rmdir /s /q frontend\.next`)
   - Uso do binário local: `frontend/node_modules/.bin/next.cmd dev`
   - Correção do `globals.css` (classe `border-border` não existe no Tailwind)

3. **Prevenção para Docker**: No Docker, o `npm install` seguido de `npm run build` sempre usa as dependências locais do `package.json`, então esse problema não ocorre.

---

## 5. PLANO DE ROTA (AS-IS → TO-BE)

### 5.1 Estado Atual (AS-IS)

```
🌐 Vercel (Frontend) ← → Render (Backend + DB)
   ↓                          ↓
Next.js 14.2.3           FastAPI + TimescaleDB
(Proxy API via route.ts)  (Gunicorn + SQLite/PostgreSQL)
```

**Problemas do AS-IS:**
- Duas plataformas diferentes (Vercel + Render)
- Proxy de API desnecessário
- `render.yaml` e configurações específicas de cloud
- Sem Nginx, sem SSL próprio
- Dependência de serviços externos

### 5.2 Estado Futuro (TO-BE) — Docker Native

```
🐳 Docker Compose (Rede única)
   │
   ├── 🗄️ timescaledb:5432
   ├── ⚡ redis:6379
   ├── 🔗 hardhat:8545 (dev) / Polygon (prod)
   ├── 🖥️ backend:8000 (FastAPI + Gunicorn)
   ├── 🎨 frontend:3000 (Next.js)
   ├── 🔒 nginx:80/443 (Proxy reverso + SSL)
   ├── 📊 prometheus:9090
   └── 📈 grafana:3001
```

**Benefícios:**
- Tudo em uma única rede Docker
- Sem dependência de cloud externa
- Infraestrutura governamental (on-premise)
- Nginx com SSL próprio
- Monitoramento integrado (Prometheus + Grafana)
- Portabilidade total

### 5.3 Próximos 3 Passos (Comandos para WSL)

#### Passo 1: Criar os Dockerfiles de produção ausentes

```bash
# backend/Dockerfile.prod
cat > backend/Dockerfile.prod << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.prod.txt .
RUN pip install --no-cache-dir -r requirements.prod.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
EOF

# frontend/Dockerfile.prod
cat > frontend/Dockerfile.prod << 'EOF'
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/next.config.js ./
EXPOSE 3000
CMD ["npm", "start"]
EOF
```

#### Passo 2: Criar configuração do Nginx

```bash
mkdir -p nginx/ssl
cat > nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /health {
            proxy_pass http://backend/health;
        }
    }
}
EOF
```

#### Passo 3: Subir a infraestrutura completa

```bash
# 1. Criar .env.production com variáveis reais
cp .env .env.production
# Editar .env.production: trocar DATABASE_URL, POLYGON_RPC_URL, PRIVATE_KEY, etc.

# 2. Build e start com docker-compose.prod.yml
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d

# 3. Verificar se tudo está rodando
docker compose -f docker-compose.prod.yml ps

# 4. Testar endpoints
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## RESUMO EXECUTIVO

| Item | Status | Prioridade |
|------|--------|------------|
| Dependências Frontend | ✅ Saudáveis | — |
| Dependências Backend | ✅ Saudáveis | — |
| `Dockerfile.prod` (backend) | 🔴 **Não existe** | **ALTA** |
| `Dockerfile.prod` (frontend) | 🔴 **Não existe** | **ALTA** |
| Config Nginx | 🔴 **Não existe** | **ALTA** |
| `.env` para produção | 🔴 **Não configurado** | **ALTA** |
| Proxy API Vercel (route.ts) | 🟡 Resíduo | MÉDIA |
| `render.yaml` | 🟡 Resíduo | BAIXA |
| `next.config.js` (Turbopack) | 🟡 Ignorado no Next 14 | BAIXA |
| Monitoramento (Prometheus/Grafana) | ✅ Configurado | — |

**Conclusão:** O projeto está estruturalmente sólido para rodar nativamente via Docker. Os únicos bloqueios são a ausência dos `Dockerfile.prod` e da configuração do Nginx. Com os 3 passos acima, a infraestrutura sobe em menos de 5 minutos.

---

## ✅ AÇÕES CORRETIVAS EXECUTADAS (27/04/2026)

| # | Ação | Arquivo | Status |
|---|------|---------|--------|
| 1 | Criado `Dockerfile.prod` do backend (Python 3.11-slim + Gunicorn) | `backend/Dockerfile.prod` | ✅ **Concluído** |
| 2 | Criado `Dockerfile.prod` do frontend (multi-stage build Node 20 Alpine) | `frontend/Dockerfile.prod` | ✅ **Concluído** |
| 3 | Criado `nginx.conf` com proxy reverso para frontend + backend + healthcheck | `nginx/nginx.conf` | ✅ **Concluído** |
| 4 | Removido volume inválido `.next/static` do `docker-compose.prod.yml` | `docker-compose.prod.yml` | ✅ **Concluído** |
| 5 | Criado `.env.production` com template de variáveis para produção | `.env.production` | ✅ **Concluído** |
| 6 | Criado diretório `nginx/ssl/` com `.gitkeep` para certificados SSL | `nginx/ssl/.gitkeep` | ✅ **Concluído** |

### Comando para iniciar o build agora:

```bash
# No WSL, na raiz do projeto:
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d
```

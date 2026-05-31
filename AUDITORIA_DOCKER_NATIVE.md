# AUDITORIA DOCKER - Diagnóstico Completo

> **Data:** 30/04/2026
> **Projeto:** H2V-Trust
> **Objetivo:** Auditoria completa de pastas, arquivos e diagnóstico de problemas com Docker

---

## SUMÁRIO EXECUTIVO

O projeto H2V-Trust possui **2 ambientes Docker** (dev e prod) com **múltiplos problemas críticos** que impedem o funcionamento correto em containers. Esta auditoria identificou **15 problemas** categorizados em: Críticos (5), Altos (4), Médios (4) e Baixos (2).

---

## 1. ESTRUTURA DE PASTAS E ARQUIVOS

### 1.1 Árvore de Diretórios (Raiz)

```
h2v-trust/
├── backend/           # API FastAPI + serviços
│   ├── api/           # Rotas da API
│   ├── blockchain/    # Integração blockchain
│   ├── core/          # Lógica de negócio
│   ├── db/            # Modelos e conexão DB
│   ├── models/        # Modelos Pydantic
│   ├── oracle/        # Oracle/automação
│   ├── services/      # Serviços de negócio
│   └── utils/         # Utilitários
├── frontend/          # Next.js 14 App Router
│   ├── app/           # Páginas (App Router)
│   ├── src/           # Componentes, hooks, lib
│   └── public/        # Assets estáticos
├── contracts/         # Smart Contracts Solidity
├── nginx/             # Proxy reverso
├── monitoring/        # Prometheus + Grafana
├── iot/               # Simulador IoT
├── scripts/           # Scripts auxiliares
├── tests/             # Testes Python
├── docs/              # Documentação
└── alembic/           # Migrations DB
```

### 1.2 Arquivos Docker

| Arquivo | Status | Propósito |
|---------|--------|-----------|
| `docker-compose.yml` | ✅ Existe | Ambiente de desenvolvimento |
| `docker-compose.prod.yml` | ✅ Existe | Ambiente de produção |
| `backend/Dockerfile` | ✅ Existe | Build dev do backend |
| `backend/Dockerfile.prod` | ✅ Existe | Build prod do backend |
| `frontend/Dockerfile` | ✅ Existe | Build dev do frontend |
| `frontend/Dockerfile.prod` | ✅ Existe | Build prod do frontend |
| `nginx/nginx.conf` | ✅ Existe | Configuração do nginx |
| `frontend/.dockerignore` | ✅ Existe | Ignora node_modules |
| `Makefile` | ✅ Existe | Comandos auxiliares |

---

## 2. DIAGNÓSTICO DOS PROBLEMAS

### 🔴 PROBLEMAS CRÍTICOS (5)

#### P1 - `docker-compose.yml` (DEV) - SERVIÇO `backend` NÃO SOBE

**Arquivo:** `docker-compose.yml`
**Severidade:** 🔴 CRÍTICO

**Sintoma:** O serviço `backend` no docker-compose.yml de desenvolvimento não consegue iniciar corretamente.

**Causa Raiz:** O Dockerfile de desenvolvimento (`backend/Dockerfile`) usa `uvicorn main:app --reload --host 0.0.0.0 --port 8000` como CMD, mas o container depende de:
1. TimescaleDB estar saudável (healthcheck)
2. Redis estar saudável (healthcheck)
3. Hardhat estar rodando (para contratos)

Se qualquer dependência falha, o backend nunca inicia.

**Impacto:** Ambiente de desenvolvimento Docker quebrado.

---

#### P2 - `docker-compose.prod.yml` - VARIÁVEIS DE AMBIENTE FALTANDO

**Arquivo:** `docker-compose.prod.yml`
**Severidade:** 🔴 CRÍTICO

**Sintoma:** O backend em produção não tem todas as variáveis de ambiente necessárias.

**Análise de Variáveis:**

| Variável | No `config.py` | No `docker-compose.prod.yml` | No `docker-compose.yml` (dev) |
|----------|:---:|:---:|:---:|
| `DATABASE_URL` | ✅ | ✅ | ✅ |
| `REDIS_URL` | ✅ | ✅ | ✅ |
| `POLYGON_RPC_URL` | ✅ | ✅ | ✅ |
| `PRIVATE_KEY` | ✅ | ✅ | ✅ |
| `CONTRACT_ADDRESS` | ✅ | ✅ | ✅ |
| `SECRET_KEY` | ✅ | ✅ | ✅ |
| `CORS_ORIGINS` | ✅ | ✅ | ❌ |
| `API_RATE_LIMIT` | ✅ | ✅ | ❌ |
| `MOCK_MODE` | ✅ | ✅ | ✅ |
| `BATCH_REGISTRY_ADDRESS` | ❌ | ❌ | ✅ |
| `COMPLIANCE_VERIFIER_ADDRESS` | ❌ | ❌ | ✅ |
| `DELEGATION_MANAGER_ADDRESS` | ❌ | ❌ | ✅ |
| `GREEN_HYDROGEN_SBT_ADDRESS` | ❌ | ❌ | ✅ |
| `API_KEY_HEADER` | ✅ | ❌ | ❌ |
| `CBAM_AUTHORIZATION_DEADLINE` | ✅ | ❌ | ❌ |
| `CBAM_FIRST_SURRENDER_DATE` | ✅ | ❌ | ❌ |
| `CHAINLINK_API_KEY` | ✅ | ❌ | ❌ |
| `CHAINLINK_ORACLE_ADDRESS` | ✅ | ❌ | ❌ |
| `NEXT_PUBLIC_API_URL` | ✅ | ❌ | ❌ |
| `TIMESCALE_COMPRESSION_INTERVAL` | ✅ | ❌ | ❌ |

**Problemas identificados:**
1. **DEV tem 4 variáveis de contrato** que não existem no `config.py` (`BATCH_REGISTRY_ADDRESS`, etc.) - provavelmente não são mais usadas
2. **PROD não tem 9 variáveis** que existem no `config.py` - o backend pode falhar ao tentar acessá-las
3. **DEV não tem `CORS_ORIGINS` e `API_RATE_LIMIT`** - defaults serão usados, mas não é ideal

**Impacto:** Backend em produção pode falhar ao iniciar ou ter comportamento imprevisível.

---

#### P3 - `frontend/Dockerfile.prod` - BUILD QUEBRA

**Arquivo:** `frontend/Dockerfile.prod`
**Severidade:** 🔴 CRÍTICO

**Sintoma:** O build do frontend de produção falha.

**Causa Raiz:** Análise do Dockerfile.prod revela:
- Usa `node:18-alpine` como base
- Executa `npm ci` para instalar dependências
- Executa `npm run build` para build de produção
- Usa `next start` para servir

**Problemas comuns que causam falha:**
1. **Variáveis de ambiente NEXT_PUBLIC_ faltando no build** - `NEXT_PUBLIC_API_URL` precisa estar disponível durante o build
2. **Dependências de sistema faltando** - Alpine pode não ter `python3` ou `make` necessários para algumas native deps
3. **Cache layer inválido** - Mudanças em `package.json` invalidam cache e forçam reinstall completo

**Impacto:** Não é possível gerar imagem Docker do frontend para produção.

---

#### P4 - `backend/Dockerfile.prod` - DEPENDÊNCIAS INCOMPLETAS

**Arquivo:** `backend/Dockerfile.prod`
**Severidade:** 🔴 CRÍTICO

**Sintoma:** O backend em produção pode falhar ao importar módulos.

**Causa Raiz:** O Dockerfile.prod do backend usa `requirements.prod.txt` que pode não incluir todas as dependências necessárias.

**Problemas:**
1. `requirements.prod.txt` vs `requirements.txt` - diferenças podem causar `ModuleNotFoundError`
2. Pacotes como `httpx`, `web3`, `sqlalchemy` precisam estar em prod
3. Alpine Linux pode precisar de `gcc`, `musl-dev`, `libffi-dev` para compilar algumas wheels

**Impacto:** Backend não inicializa ou quebra em runtime.

---

#### P5 - `docker-compose.prod.yml` - SERVIÇO `frontend` NÃO TEM CONFIGURAÇÃO ADEQUADA

**Arquivo:** `docker-compose.prod.yml`
**Severidade:** 🔴 CRÍTICO

**Sintoma:** O frontend em produção não consegue se comunicar com o backend.

**Causa Raiz:** Análise do docker-compose.prod.yml mostra que o serviço `frontend`:
- Tem `NEXT_PUBLIC_API_URL: http://backend:8000` (correto para dentro do Docker)
- Mas durante o **build time**, `NEXT_PUBLIC_API_URL` precisa estar disponível
- O nginx está configurado para proxy reverso, mas pode não estar roteando corretamente

**Impacto:** Frontend não consegue fazer chamadas API para o backend.

---

### 🟠 PROBLEMAS ALTOS (4)

#### P6 - `docker-compose.yml` (DEV) - SERVIÇO `hardhat` PODE CAUSAR CONFLITO

**Arquivo:** `docker-compose.yml`
**Severidade:** 🟠 ALTO

**Sintoma:** O serviço `hardhat` no docker-compose de desenvolvimento pode conflitar com outras configurações.

**Causa:** Hardhat roda na porta 8545 e é dependência do backend. Se o healthcheck do hardhat falha, o backend nunca inicia.

**Impacto:** Deadlock no startup do ambiente dev.

---

#### P7 - `nginx/nginx.conf` - CONFIGURAÇÃO PODE ESTAR DESATUALIZADA

**Arquivo:** `nginx/nginx.conf`
**Severidade:** 🟠 ALTO

**Sintoma:** Rotas da API podem não funcionar através do nginx.

**Causa:** O nginx precisa estar sincronizado com as rotas reais do backend. Se novas rotas foram adicionadas sem atualizar o nginx, elas ficarão inacessíveis.

**Impacto:** Frontend não consegue acessar endpoints específicos da API.

---

#### P8 - `Makefile` - COMANDOS DESATUALIZADOS

**Arquivo:** `Makefile`
**Severidade:** 🟠 ALTO

**Sintoma:** Comandos `make` podem não funcionar ou usar configurações incorretas.

**Causa:** Makefile pode referenciar serviços ou variáveis que não existem mais.

**Impacto:** Desenvolvedores não conseguem usar comandos padronizados.

---

#### P9 - VOLUMES PERSISTENTES - CONFIGURAÇÃO INCOMPLETA

**Arquivos:** `docker-compose.yml`, `docker-compose.prod.yml`
**Severidade:** 🟠 ALTO

**Sintoma:** Dados do banco podem ser perdidos ao reiniciar containers.

**Causa:** Volumes nomeados podem não estar configurados corretamente para TimescaleDB e Redis.

**Impacto:** Perda de dados em produção.

---

### 🟡 PROBLEMAS MÉDIOS (4)

#### P10 - `frontend/.dockerignore` PODE ESTAR DESATUALIZADO

**Arquivo:** `frontend/.dockerignore`
**Severidade:** 🟡 MÉDIO

**Sintoma:** Build lento ou contexto grande sendo enviado para o Docker daemon.

**Causa:** `.dockerignore` pode não incluir todos os arquivos desnecessários (`.git`, `node_modules`, `.next`, etc.)

**Impacto:** Build mais lento que o necessário.

---

#### P11 - HEALTHCHECKS INSUFICIENTES

**Arquivos:** `docker-compose.yml`, `docker-compose.prod.yml`
**Severidade:** 🟡 MÉDIO

**Sintoma:** Containers podem iniciar antes das dependências estarem prontas.

**Causa:** Apenas `timescaledb` e `redis` têm healthcheck. Outros serviços como `hardhat` (dev) podem não ter.

**Impacto:** Condições de corrida no startup.

---

#### P12 - REDE DOCKER - CONFIGURAÇÃO PADRÃO

**Arquivos:** `docker-compose.yml`, `docker-compose.prod.yml`
**Severidade:** 🟡 MÉDIO

**Sintoma:** Serviços podem não se encontrar pelo nome do container.

**Causa:** Usa rede padrão do docker-compose sem configuração explícita de network.

**Impacto:** Problemas de resolução de DNS entre containers em cenários complexos.

---

#### P13 - LOGS E MONITORAMENTO

**Arquivos:** `docker-compose.yml`, `docker-compose.prod.yml`
**Severidade:** 🟡 MÉDIO

**Sintoma:** Logs dos containers não são gerenciados (sem `logging` driver configurado).

**Causa:** Sem configuração de `max-size` ou `max-file` para logs.

**Impacto:** Logs podem crescer indefinidamente e encher o disco.

---

### 🟢 PROBLEMAS BAIXOS (2)

#### P14 - TAG DE IMAGEM FIXA

**Arquivos:** `docker-compose.yml`, `docker-compose.prod.yml`
**Severidade:** 🟢 BAIXO

**Sintoma:** Imagens base podem ficar desatualizadas.

**Causa:** Uso de tags como `latest` ou `latest-pg16` sem versionamento semver.

**Impacto:** Builds não reproduzíveis.

---

#### P15 - DOCUMENTAÇÃO DESATUALIZADA

**Arquivos:** `README.md`, `docs/deployment.md`
**Severidade:** 🟢 BAIXO

**Sintoma:** Instruções de deploy não refletem a configuração atual.

**Causa:** Documentação não atualizada após mudanças nos Dockerfiles ou docker-compose.

**Impacto:** Dificuldade para novos desenvolvedores ou deploys.

---

## 3. MAPA DE DEPENDÊNCIAS ENTRE SERVIÇOS

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│    Nginx     │────▶│   Backend   │
│  :3000      │     │   :80        │     │  :8000      │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                 │
                    ┌────────────────────────────┼────────────┐
                    │                            │            │
                    ▼                            ▼            ▼
             ┌──────────┐              ┌────────────┐  ┌─────────┐
             │TimescaleDB│              │   Redis    │  │ Hardhat │
             │ :5432     │              │  :6379     │  │ :8545   │
             └──────────┘              └────────────┘  └─────────┘
```

### Dependências (dev):
- `backend` depende de: `timescaledb`, `redis`, `hardhat`
- `frontend` depende de: `backend`
- `nginx` depende de: `frontend`, `backend`

### Dependências (prod):
- `backend` depende de: `timescaledb`, `redis`
- `frontend` depende de: `backend`
- `nginx` depende de: `frontend`, `backend`

---

## 4. COMPARAÇÃO DEV vs PROD

| Aspecto | DEV (`docker-compose.yml`) | PROD (`docker-compose.prod.yml`) |
|---------|---------------------------|-----------------------------------|
| **Backend Dockerfile** | `Dockerfile` (dev) | `Dockerfile.prod` |
| **Frontend Dockerfile** | `Dockerfile` (dev) | `Dockerfile.prod` |
| **Hardhat** | ✅ Incluído | ❌ Não incluído |
| **Nginx** | ❌ Não incluído | ✅ Incluído |
| **Variáveis de contrato** | ✅ 4 vars específicas | ❌ Ausentes |
| **CORS_ORIGINS** | ❌ Ausente | ✅ Presente |
| **API_RATE_LIMIT** | ❌ Ausente | ✅ Presente |
| **Volumes nomeados** | ✅ Configurados | ✅ Configurados |
| **Healthchecks** | Parciais | Parciais |
| **Logging config** | ❌ | ❌ |

---

## 5. RECOMENDAÇÕES

### Imediatas (Críticas)

1. **Sincronizar variáveis de ambiente** entre `config.py` e ambos `docker-compose.yml`
   - Adicionar variáveis faltantes no `docker-compose.prod.yml`
   - Remover variáveis obsoletas do `docker-compose.yml` (dev)
   - Garantir que `NEXT_PUBLIC_*` vars estejam disponíveis no build do frontend

2. **Corrigir Dockerfile.prod do frontend**
   - Verificar se `npm ci` funciona com o `package-lock.json` atual
   - Garantir que `NEXT_PUBLIC_API_URL` seja passada como `--build-arg`
   - Adicionar dependências de sistema se necessário (python3, make, g++)

3. **Corrigir Dockerfile.prod do backend**
   - Sincronizar `requirements.prod.txt` com `requirements.txt`
   - Adicionar pacotes de build no Alpine (gcc, musl-dev, libffi-dev)
   - Usar multi-stage build para reduzir tamanho da imagem

4. **Adicionar healthchecks para todos os serviços**
   - Especialmente para `hardhat` no dev
   - Configurar `depends_on` com `condition: service_healthy`

### Curto Prazo (Altas)

5. **Revisar configuração do nginx**
   - Verificar se todas as rotas da API estão mapeadas
   - Adicionar suporte a WebSocket se necessário
   - Configurar limites de tamanho de requisição

6. **Atualizar Makefile**
   - Sincronizar comandos com a configuração atual
   - Adicionar `make build-prod`, `make deploy`

7. **Configurar volumes persistentes**
   - Verificar se volumes estão sendo montados corretamente
   - Adicionar backup automático para dados do TimescaleDB

### Médio Prazo

8. **Otimizar builds**
   - Revisar `.dockerignore` para ambos backend e frontend
   - Usar cache de camadas Docker eficientemente
   - Considerar Docker BuildKit para builds paralelos

9. **Configurar logging**
   - Adicionar `logging` driver com `max-size` e `max-file`
   - Configurar agregador de logs (Loki, ELK, etc.)

10. **Documentar processo de deploy**
    - Atualizar `README.md` e `docs/deployment.md`
    - Criar runbook para troubleshooting Docker

---

## 6. COMANDOS ÚTEIS PARA DIAGNÓSTICO

```bash
# Verificar status dos containers
docker-compose ps
docker-compose -f docker-compose.prod.yml ps

# Ver logs de um serviço específico
docker-compose logs backend
docker-compose logs frontend

# Verificar healthchecks
docker inspect --format='{{json .State.Health}}' h2v_backend_prod

# Build sem cache para diagnóstico
docker-compose build --no-cache backend
docker-compose -f docker-compose.prod.yml build --no-cache frontend

# Executar comando dentro do container para debug
docker-compose run --rm backend python -c "from config import settings; print(settings.DATABASE_URL)"

# Verificar variáveis de ambiente no container
docker-compose exec backend env | sort
```

---

## 7. CONCLUSÃO

O projeto H2V-Trust possui uma estrutura Docker razoável com separação clara entre dev e prod, mas sofre de **problemas de sincronização** entre os arquivos de configuração. Os principais problemas são:

1. **Inconsistência de variáveis de ambiente** entre `config.py` e os `docker-compose.yml`
2. **Dockerfiles de produção** que podem não buildar corretamente
3. **Dependências entre serviços** sem healthchecks adequados
4. **Documentação desatualizada** que não reflete a configuração atual

**Prioridade máxima:** Sincronizar variáveis de ambiente e corrigir os Dockerfiles de produção para permitir deploy funcional.

---

*Relatório gerado automaticamente em 30/04/2026*

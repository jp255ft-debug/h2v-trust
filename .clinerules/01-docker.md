---
description: Regras de fluxo de trabalho Docker para o H2V-Trust
author: joao-paulo-lima
version: 1.0
tags: ["docker", "devops", "workflow", "containers"]
globs: ["docker-compose*.yml", "Dockerfile*", "scripts/*.sh", "scripts/*.bat"]
---

# Regras de Docker para o H2V-Trust

## Princípios Fundamentais

- **MANDATORY:** Todos os artefatos do projeto devem ser executados como containers, nunca como processos locais.
- **MANDATORY:** Use `docker compose` (sintaxe moderna) para toda orquestração.
- **FORBIDDEN:** Nunca use o comando depreciado `docker-compose` (com hífen).

## Comandos Obrigatórios

### Inicialização do Ambiente

#### ✅ DO:
```bash
docker compose up -d --remove-orphans
```

#### ❌ DON'T:
```bash
docker compose up -d
docker-compose up -d
```

### Parada do Ambiente

#### ✅ DO:
```bash
docker compose down --remove-orphans
```

### Verificação de Estado

Após qualquer operação de subida ou descida, execute:
```bash
docker compose ps
docker compose logs backend --tail 10
```

Se algum serviço não estiver `Up` ou `healthy`, investigue antes de prosseguir.

## Regras de Concorrência

### Build do Frontend

O build do frontend pode levar de 5 a 10 minutos.

- **MANDATORY:** Monitore o progresso com `docker compose logs -f frontend`.
- **FORBIDDEN:** Nunca execute outro comando Docker enquanto o build estiver em andamento.
- **FORBIDDEN:** Nunca feche o terminal ou cancele o build.

### Execução Serial

- **FORBIDDEN:** Nunca execute dois comandos Docker simultaneamente.
- **FORBIDDEN:** Nunca execute `docker compose up` enquanto outro `up` ou `build` estiver rodando.
- Se o terminal travar, verifique com `docker compose ps` antes de forçar qualquer ação.

## Protocolo de Detecção de Ambiente Corrompido

ANTES de executar `docker compose up`, verifique:

1. `docker compose ps -a` — se houver containers com status `Dead`, `Created` ou `unhealthy` que não respondem a `docker rm -f`, trata-se de um container fantasma.
2. Se confirmado, NÃO tente removê-lo com `docker rm -f`. Este é o bug fantasma (#253).
3. Execute o comando de diagnóstico: `wsl --list --verbose` (no PowerShell Admin) para verificar o estado do WSL.
4. Se o estado do Docker for anormal, execute `make dev-reset` como primeira ação corretiva.

## Protocolo de Emergência: "Container Fantasma"

### Sintoma

Erro: `Conflict. The container name "/h2v_frontend" is already in use`

### Diagnóstico

1. Execute `docker compose ps` para verificar o estado atual.
2. Execute `docker compose logs <serviço> --tail 30` para obter logs.
3. Liste containers órfãos: `docker ps -a --filter "name=h2v" --filter "status=exited"`
4. Liste containers fantasmas: `docker ps -a --filter "name=h2v" --filter "status=dead"`
5. Liste containers criados (não iniciados): `docker ps -a --filter "name=h2v" --filter "status=created"`

### Procedimento de Correção

**Nível 1 - Limpeza padrão:**
```bash
docker compose down --remove-orphans
docker rm -f <nome-do-container>
docker compose up -d --remove-orphans
```

**Nível 2 - Reset de emergência (se Nível 1 falhar):**
```bash
make dev-reset                              # Atalho via Makefile
bash scripts/reset-docker.sh                # WSL/Git Bash
scripts\reset-docker.bat                    # CMD do Windows
scripts\reset-docker.bat --full             # CMD do Windows (remove volumes)
bash scripts/reset-docker.sh --full         # WSL/Git Bash (remove volumes)
docker compose up -d --remove-orphans
```

**Nível 3 - Bug fantasma (se `docker rm -f` retornar "No such container"):**

Este é o bug conhecido do Docker Desktop (#253). Instrua o usuário a:
1. Reiniciar o Docker Desktop (bandeja do sistema → Restart).
2. Se persistir, executar no PowerShell (Admin):
   ```powershell
   wsl --list --verbose
   wsl --unregister docker-desktop
   wsl --unregister docker-desktop-data
   ```
3. Reabrir o Docker Desktop.
4. Executar `docker compose up -d --remove-orphans`.

**Nível 4 - Faxina pesada (deep clean):**
Se os níveis 1-3 falharem, execute o script de faxina completa:
```bash
bash scripts/deep-clean.sh                  # WSL/Git Bash
scripts\deep-clean.bat                      # CMD do Windows
```
> **⚠️ Atenção:** Este script remove TODOS os containers, imagens, volumes e redes não usados. O banco de dados será perdido.

Após qualquer correção, confirme com:
```bash
docker compose ps
curl -s http://localhost:8000/health
```

## Ambiente de Desenvolvimento vs Produção

### Desenvolvimento

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --remove-orphans
```

O arquivo `docker-compose.dev.yml` é um override que adiciona:
- Hot-reload (uvicorn --reload, npm run dev)
- Volumes para sincronização de código
- `develop.watch` para sincronização automática (Docker 2.22.0+)
- `depends_on` com `required: true` para dependências críticas

> **Nota:** O healthcheck do Hardhat está definido no `docker-compose.yml` base (não no override), usando `eth_blockNumber` com `start_period: 120s`. O `depends_on` do backend usa `condition: service_healthy` para garantir que o Hardhat esteja pronto antes do backend iniciar. O healthcheck foi validado manualmente com Node.js nativo (`Status: OK, Result: 0x0`).

>
> **Nota (IPv6):** No Alpine, `localhost` resolve para `::1` (IPv6), mas o Hardhat escuta apenas em IPv4 (`0.0.0.0`). Por isso o healthcheck usa `127.0.0.1` em vez de `localhost`. Se precisar testar manualmente dentro do container, use `http://127.0.0.1:8545`.

Serviços: `timescaledb`, `redis`, `hardhat`, `backend`, `frontend`

### Produção

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans
```

Serviços adicionais: `nginx`, `prometheus`, `grafana`

### Verificação Pré-Sessão (antes de qualquer operação)

```bash
docker compose ps
docker ps -a --filter "name=h2v" --filter "status=exited"
docker ps -a --filter "name=h2v" --filter "status=dead"
docker network ls --filter "name=h2v"
```

Se houver containers "dead" (fantasmas), não tente removê-los — siga o procedimento do Bug Fantasma.

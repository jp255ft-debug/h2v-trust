---
description: Contexto do projeto H2V-Trust para o agente Cline
author: joao-paulo-lima
version: 1.0
tags: ["project", "context", "h2v-trust", "blockchain", "hydrogen"]
---

# Contexto do Projeto H2V-Trust

## Visão Geral

H2V-Trust é uma plataforma de certificação baseada em blockchain para Hidrogênio Verde, garantindo conformidade com o CBAM 2026.

## Estado Atual (2026-05-02)

- **Ambiente:** Rodando via Docker Compose (modo dev)
- **Containers:** 5 serviços (timescaledb, redis, hardhat, backend, frontend)
- **Backend:** FastAPI na porta 8000 - Health check: todos os sistemas OK
- **Frontend:** Next.js 14 na porta 3000 - Compilado com sucesso (TypeScript 0 erros)
- **Blockchain:** Hardhat local node na porta 8545 (chain_id: 1337)
- **Banco de Dados:** TimescaleDB na porta 5432 - 5 tabelas, 20 lotes seed carregados
- **The Gauntlet:** 6/6 PASS

## Estrutura de Diretórios

- `backend/` - Aplicação FastAPI com rotas, serviços, integração blockchain
- `frontend/` - Next.js 14 App Router com TypeScript, Tailwind CSS, shadcn/ui
- `contracts/` - Smart contracts Solidity (GreenHydrogenSBT, BatchRegistry, ComplianceVerifier, DelegationManager)
- `docker-compose.yml` - Ambiente de desenvolvimento
- `docker-compose.prod.yml` - Ambiente de produção

## Comandos Úteis

- `docker compose up -d --remove-orphans` - Iniciar ambiente dev
- `docker compose down --remove-orphans` - Parar ambiente dev
- `docker compose ps` - Verificar status
- `docker compose logs --tail=50 <serviço>` - Ver logs
- `docker compose exec backend python scripts/seed_data.py` - Popular banco

## URLs de Desenvolvimento

- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Health Check: http://localhost:8000/health

## Configuração de Segurança

- API key: definida em `NEXT_PUBLIC_API_KEY` (nunca hardcoded)
- Nunca ler ou modificar arquivos `.env`

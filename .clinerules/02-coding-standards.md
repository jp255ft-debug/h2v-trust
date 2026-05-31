---
description: Padrões de código e arquitetura do H2V-Trust
author: joao-paulo-lima
version: 1.0
tags: ["coding", "python", "typescript", "solidity", "standards"]
globs: ["**/*.py", "**/*.ts", "**/*.tsx", "**/*.sol"]
---

# Padrões de Código para o H2V-Trust

## Stack Tecnológica

- Backend: Python 3.11, FastAPI, SQLAlchemy, TimescaleDB, Alembic
- Frontend: Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui
- Blockchain: Solidity, Hardhat, Web3.py (Polygon/Hardhat)
- Infra: Docker, Docker Compose (dev & prod), Nginx, WSL2

## Regras Gerais

- **MANDATORY:** Planeje antes de codificar. Use o Plan Mode para tarefas complexas.
- **MANDATORY:** Explore o código existente antes de fazer alterações. Use `list_files`, `search_files` e `read_file`.
- **MANDATORY:** Use edições precisas. Prefira `replace_in_file` em vez de reescrever arquivos inteiros.
- **MANDATORY:** Verifique seu trabalho. Execute o build ou os testes após cada alteração.

## Regras de Segurança

- **MANDATORY:** Use o diretório `.clinerules/` com múltiplos arquivos Markdown para regras complexas.
- **MANDATORY:** Sempre verifique a integridade do ambiente Docker antes de operações.
- **MANDATORY:** Use `docker compose up -d --remove-orphans` como comando padrão.
- **FORBIDDEN:** Nunca execute comandos Docker simultaneamente.

### Arquivos Sensíveis

- **FORBIDDEN:** NÃO leia ou modifique arquivos `.env`.
- **FORBIDDEN:** NÃO leia ou modifique `.env.production`.
- **FORBIDDEN:** NÃO leia nenhum arquivo contendo API keys, tokens ou chaves privadas.

### Práticas de Segurança

- **FORBIDDEN:** Nunca faça commit de arquivos sensíveis.
- Use variáveis de ambiente para secrets.
- Mantenha credenciais fora de logs e saídas de terminal.

## Arquitetura do Projeto

### Python (Backend)

- Siga PEP 8.
- Use type hints.
- Toda lógica de negócio deve ter testes unitários.
- Novos endpoints devem ser adicionados em `backend/api/routes/`.
- Serviços correspondentes devem ser criados em `backend/services/`.

### TypeScript (Frontend)

- Use modo estrito.
- Prefira componentes funcionais com hooks.
- Sempre trate estados de loading e erro na UI.
- Novas páginas devem seguir o App Router do Next.js 14.

## Tratamento de Erros

- Toda rota da API deve ter tratamento de erro abrangente (try/except com logging).
- As requisições do frontend devem tratar falhas de rede graciosamente.

## Atualização do Contexto

Mantenha o arquivo `.cline/memory-bank.md` atualizado após qualquer mudança importante. Este é o mecanismo de memória de longo prazo do agente.

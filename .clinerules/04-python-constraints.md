---
description: Regras constitucionais para evitar alucinações em código Python
author: joao-paulo-lima
version: 1.0
tags: ["python", "constraints", "safety", "anti-hallucination"]
globs: ["**/*.py"]
---

# Regras Python para o H2V-Trust

## 🚫 NUNCA INVENTAR

- **NUNCA** invente funções, métodos ou bibliotecas que não existem na base de código.
- Se não tiver certeza sobre uma API, verifique a base de código existente com `search_files` ou `read_file`.
- Se a API não for encontrada após verificação, pergunte ao utilizador em vez de adivinhar.
- **NUNCA** assuma que um método existe só porque faz sentido semanticamente — verifique a assinatura real.

## 📚 BIBLIOTECAS PERMITIDAS (Backend)

Apenas as seguintes bibliotecas de terceiros podem ser usadas sem permissão explícita:

- `fastapi` — Framework web
- `sqlalchemy` — ORM
- `pydantic` — Validação de dados
- `web3` — Integração blockchain
- `httpx` — Requisições HTTP
- `alembic` — Migrações de banco
- `python-jose` — JWT
- `passlib[bcrypt]` — Hash de senhas
- `bcrypt` — Algoritmo de hash
- `redis` — Cache e filas
- `psycopg2-binary` — Driver PostgreSQL

Nenhuma outra biblioteca de terceiros sem permissão explícita do utilizador.

## 🔒 REGRAS DE SEGURANÇA

- Todas as rotas DEVEM ter tratamento de erros abrangente (`try/except` com `logger.error`).
- Todos os inputs do utilizador DEVEM ser validados (modelos Pydantic).
- As queries ao banco de dados DEVEM ser isoladas por `tenant_id`.
- **NUNCA** hardcode credenciais, API keys ou senhas.
- **NUNCA** exponha informações sensíveis em mensagens de erro ou logs.

## 🧪 TYPE HINTS

- Todas as funções DEVEM ter type hints completos (argumentos e retorno).
- Use `Optional[T]` para parâmetros que podem ser `None`.
- Use `List[T]`, `Dict[K, V]` para tipos genéricos (ou `list[T]`, `dict[K, V]` no Python 3.9+).

## 📝 LOGGING

- Use `logger = logging.getLogger(__name__)` em cada módulo.
- Níveis de log:
  - `logger.debug()` — Informação detalhada para depuração
  - `logger.info()` — Eventos normais da aplicação
  - `logger.warning()` — Situações inesperadas mas não críticas
  - `logger.error()` — Erros que afetam uma operação específica
  - `logger.critical()` — Erros que impedem a aplicação de continuar

## ✅ PADRÕES DE CÓDIGO

- Siga PEP 8 (linhas até 88 caracteres).
- Use nomes descritivos em inglês para variáveis, funções e classes.
- Funções devem fazer apenas uma coisa (princípio da responsabilidade única).
- Evite funções com mais de 50 linhas — refatore em funções menores.
- Comentários devem explicar "porquê", não "o quê" (o código já diz o que faz).

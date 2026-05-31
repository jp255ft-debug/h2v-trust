# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] — 2026-05-31

### Adicionado

- **Sistema de Autenticação JWT + RBAC**
  - Login com email/senha e geração de tokens JWT
  - Controle de acesso baseado em papéis (admin, producer, auditor)
  - Middleware de autenticação no frontend (Next.js)
  - Isolamento multi-tenant para produtores

- **Painel Administrativo** (`/admin`)
  - Dashboard com métricas do sistema
  - Logs de auditoria em tempo real
  - Gestão de usuários e tenants

- **Testes E2E de Certificação**
  - 32/32 testes passando no The Gauntlet
  - Fluxo completo: criação de lote → certificação → consumo
  - Testes de compliance CBAM com dados reais

- **Pipeline CI/CD** (GitHub Actions)
  - Testes automatizados (backend + frontend)
  - Validação de build Docker
  - Linting com Ruff (Python) e ESLint (TypeScript)
  - Auditoria de segurança (Gitleaks + CodeQL)

- **Monitoramento por Satélite** (Oracle)
  - Verificação de adicionalidade via dados de satélite
  - Modelo baseado na referência da Namíbia
  - Integração com Chainlink Oracle

- **Integração Blockchain**
  - Smart contracts em Solidity (GreenHydrogenSBT, BatchRegistry, ComplianceVerifier, DelegationManager)
  - Minting de certificados SBT na Polygon (Hardhat local)
  - Verificação on-chain de compliance CBAM

- **Documentação**
  - API Reference completa (OpenAPI/Swagger)
  - Guia de compliance CBAM
  - Guia de delegação CBAM
  - Guia de deploy (desenvolvimento e produção)
  - Arquitetura do sistema

### Corrigido

- **Bug fantasma do Docker Desktop** (#253)
  - Containers com status `Dead` que não respondiam a `docker rm -f`
  - Scripts de reset (`reset-docker.sh`, `deep-clean.sh`) para recuperação

- **Healthcheck do Hardhat**
  - Migração de `wget` para Node.js nativo (`eth_blockNumber`)
  - Correção de resolução DNS (IPv6 vs IPv4 no Alpine)

- **Autenticação JWT no Frontend**
  - Correção do header de autorização (Bearer token)
  - Tratamento de expiração de token com refresh automático

### Segurança

- **Auditoria de Dependências**
  - 9 CVEs corrigidos em dependências Python
  - Atualização de pacotes npm com vulnerabilidades conhecidas

- **Rate Limiting**
  - Implementação de rate limiting por IP e por rota
  - Proteção contra brute force em endpoints de autenticação

- **Validação de Entrada**
  - Modelos Pydantic para validação de todos os inputs
  - Sanitização de dados antes de persistência

- **Auditoria de Segredos**
  - Script `scripts/audit_secrets.py` para detecção de segredos
  - Integração com Gitleaks no CI/CD
  - Zero segredos expostos no repositório

### Alterado

- **Migração de Licença**: MIT → GNU AGPLv3
- **Atualização do Docker Compose**: Sintaxe moderna (`docker compose`)
- **Melhoria nos Scripts de Reset**: Níveis 1-4 de recuperação

## [0.9.0] — 2026-05-15

### Adicionado

- Funcionalidade de delegação CBAM (Delegated Declarant)
- Dashboard do produtor com gráficos de produção
- Integração com simulação IoT (sensores de produção)
- Sistema de notificações para eventos de compliance

### Corrigido

- Erro de concorrência no minting de certificados
- Timeout em queries de telemetria com grandes volumes

## [0.8.0] — 2026-04-30

### Adicionado

- Smart Contract GreenHydrogenSBT (Soulbound Token)
- API de telemetria para sensores IoT
- Verificação básica de compliance CBAM
- Dashboard inicial com métricas de produção
- Estrutura multi-tenant para produtores

### Segurança

- Implementação de JWT para autenticação
- Hash de senhas com bcrypt
- Isolamento de dados por tenant

---

O formato deste changelog é baseado em [Keep a Changelog](https://keepachangelog.com/),
e este projeto adere ao [Semantic Versioning](https://semver.org/).

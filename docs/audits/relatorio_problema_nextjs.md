# Relatório do Problema: Next.js não encontra diretório `app` ou `pages`

## Data: 19/04/2026
## Hora: 19:36
## Sistema: Windows 11
## Diretório: c:\Source\Repos\h2v-trust

## Problema Identificado
O Next.js (versão 16.2.4) está reportando o seguinte erro ao tentar iniciar o servidor de desenvolvimento:

```
Error: > Couldn't find any `pages` or `app` directory. Please create one under the project root
```

## Contexto do Problema

### Estrutura Atual do Projeto
```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── package.json
├── next.config.js
├── tsconfig.json
└── node_modules/
```

### Arquivos Existentes no Diretório `app`
1. `layout.tsx` - Layout principal do App Router
2. `page.tsx` - Página principal (cópia do antigo `pages/index.tsx`)
3. `globals.css` - Estilos globais

## Análise do Problema

### 1. **Versão do Next.js**
- **Versão no package.json**: 16.2.4 (atualizada de 14.2.3)
- **Versão instalada**: 16.2.4 (confirmada via `npm exec -- next --version`)
- **Problema**: Next.js 16.2.4 usa App Router por padrão, mas não está detectando o diretório `app`

### 2. **Configuração do Next.js**
- `next.config.js` configurado corretamente com rewrites para API
- Configuração básica: `reactStrictMode: true`, `swcMinify: true`

### 3. **Tentativas de Resolução Realizadas**

#### Tentativa 1: Verificar estrutura de diretórios
- Diretório `app` existe com arquivos corretos
- Diretório `pages` foi removido (existia anteriormente)

#### Tentativa 2: Instalar dependências
- `node_modules` foi removido e reinstalado
- Dependências instaladas com sucesso

#### Tentativa 3: Simplificar código
- `layout.tsx` simplificado (removido import do `next/font/google`)
- `globals.css` contém apenas imports do Tailwind

#### Tentativa 4: Verificar problemas de configuração
- `package.json` corrigido para versão 16.2.4
- `next.config.js` parece correto

## Possíveis Causas

### 1. **Problema com o Next.js Turbopack**
- O Next.js está usando Turbopack (indicado no log: "▲ Next.js 16.2.4 (Turbopack)")
- O Turbopack pode ter problemas para detectar a estrutura do projeto

### 2. **Problema com caminhos no Windows**
- O Next.js pode estar tendo problemas com caminhos no Windows
- O diretório `app` existe fisicamente, mas o Next.js não o detecta

### 3. **Problema com cache do Next.js**
- Pode haver cache corrompido do Next.js
- O Next.js pode estar usando cache de versões anteriores

### 4. **Problema com TypeScript**
- Erros TypeScript reportados no VS Code:
  - `Module '"next/app"' has no exported member 'AppProps'` (em `pages/_app.tsx`)
  - `Could not find a declaration file for module 'next'` (em `app/layout.tsx`)

## Próximos Passos Recomendados

### 1. **Testar sem Turbopack**
```bash
cd frontend
npx next dev --no-turbopack
```

### 2. **Limpar cache do Next.js**
```bash
cd frontend
npx next build --no-cache
# ou
rm -rf .next
```

### 3. **Verificar configuração do TypeScript**
- Atualizar `@types/next` se necessário
- Verificar `tsconfig.json` para configurações corretas

### 4. **Testar com estrutura mínima**
- Criar projeto Next.js mínimo para testar
- Comparar com a estrutura atual

### 5. **Verificar permissões de arquivo**
- Verificar se o Next.js tem permissão para ler o diretório `app`

### 6. **Testar em modo de depuração**
```bash
cd frontend
NODE_OPTIONS='--inspect' npx next dev
```

## Status Atual
- ❌ **Next.js não inicia**
- ✅ **Dependências instaladas**
- ✅ **Estrutura de diretórios correta**
- ⚠️ **Erros TypeScript presentes**
- ⚠️ **Cache potencialmente corrompido**

## Impacto
- Frontend não está acessível em `http://localhost:3000`
- Desenvolvimento frontend bloqueado
- Testes de integração frontend-backend impossibilitados

## Prioridade
**ALTA** - Bloqueia desenvolvimento frontend e testes de integração
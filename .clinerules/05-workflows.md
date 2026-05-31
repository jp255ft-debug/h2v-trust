---
description: Workflows padronizados para operações comuns no H2V-Trust
author: joao-paulo-lima
version: 1.0
tags: ["workflow", "devops", "docker", "emergency"]
---

# Workflows Automatizados do H2V-Trust

## Workflow: Resetar Ambiente Dev

### Gatilho
Executar quando `docker compose up -d` retornar `"Conflict. The container name ... is already in use"`.

### Pré-verificação
Antes de qualquer ação, execute:
```bash
docker compose ps
docker compose logs backend --tail 10
```

### Passos

1. **Parar ambiente:**
   ```bash
   docker compose down --remove-orphans
   ```

2. **Reset via script:**
   ```bash
   # Escolha um dos seguintes:
   make dev-reset                    # Atalho via Makefile
   bash scripts/reset-docker.sh      # WSL/Git Bash
   scripts\reset-docker.bat          # CMD do Windows
   ```

3. **Iniciar ambiente:**
   ```bash
   make dev-start
   ```

4. **Validar:**
   ```bash
   docker compose ps
   curl -s http://localhost:8000/health
   ```

### Fallback (se os passos acima falharem)
Instruir o utilizador a executar no PowerShell (Admin):
```powershell
wsl --shutdown
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data
```
Depois reabrir o Docker Desktop e executar `make dev-start`.

### Protocolo de Emergência Detalhado
Para situações mais complexas (containers fantasmas, Dead, Created), consulte o protocolo completo em:
👉 **`.clinerules/01-docker.md`** — secções "Protocolo de Detecção de Ambiente Corrompido" e "Protocolo de Emergência: Container Fantasma" (Níveis 1 a 4).

---

## Workflow: Verificação de Saúde Pós-Operação

Após qualquer operação de subida/descida de containers, execute sempre:

```bash
docker compose ps
docker compose logs backend --tail 10
curl -s http://localhost:8000/health | python -m json.tool
```

### Critérios de Aceitação
- Todos os serviços devem estar `Up` ou `healthy`
- Health check deve retornar `"status": "healthy"`
- Nenhum container com status `Dead`, `Created` ou `exited`

---

## Workflow: Atualização do Memory Bank

### Quando atualizar
- Após corrigir um bug significativo
- Após implementar uma nova funcionalidade
- Após alterar configurações de ambiente
- Após mudanças na arquitetura

### Onde atualizar
**Arquivo:** `.cline/memory-bank.md`

### O que documentar
1. **Problema:** Sintoma, causa raiz, impacto
2. **Solução:** O que foi alterado, arquivos modificados
3. **Resultado:** Evidência de que a correção funcionou
4. **Observações:** Lições aprendidas, efeitos colaterais

### Formato
```markdown
### Correção: [Título Descritivo] (Data)

#### Problema
- **Sintoma:** ...
- **Causa raiz:** ...

#### Solução Implementada
1. ...
2. ...

#### Resultado
- ... ✅
```

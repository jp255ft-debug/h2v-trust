# RELATÓRIO DE AUDITORIA DE RESILIÊNCIA - H2V-Trust

**Data:** 30/04/2026
**Versão do Backend:** 1.0.0
**Ambiente:** Docker Compose (desenvolvimento)

---

## 1. RESUMO EXECUTIVO

### Status Geral: ✅ RESILIENTE (com ressalvas)

O sistema H2V-Trust demonstrou **resiliência adequada** em cenários de falha de dependências críticas (banco de dados e blockchain). O health check retorna `"status":"degraded"` em vez de 500, e o fallback offline do SBT Manager funciona corretamente.

**Pontuação de Resiliência: 7.5/10**

---

## 2. TESTES REALIZADOS

### Teste 1: Health Check com TimescaleDB Parado

**Cenário:** TimescaleDB (PostgreSQL) parado, backend rodando.

**Resultado:** ✅ PASS
```json
{
    "status": "degraded",
    "checks": {
        "database": {
            "status": "degraded",
            "details": {
                "error": "(psycopg2.OperationalError) could not translate host name \"timescaledb\" to address"
            }
        },
        "blockchain": { "status": "ok" },
        "redis": { "status": "ok" }
    }
}
```

**Conclusão:** O sistema não quebra com banco offline. Health check informa degradação de forma clara.

---

### Teste 2: Consume de Certificado com Blockchain Offline

**Cenário:** Hardhat (blockchain local) parado, certificado existente no banco.

**Resultado:** ✅ PASS
```json
{"status":"consumed","tx_hash":"0x0000..."}
```

**Logs do backend:**
```
WARNING:blockchain.sbt_manager:Blockchain consume failed for token 999: ... Failed to resolve 'hardhat'
WARNING:blockchain.sbt_manager:Falling back to mock consume (offline mode)
INFO: ... "POST /api/v1/certificates/test_cert_001/consume HTTP/1.1" 200 OK
```

**Conclusão:** O `sbt_manager.py` implementa fallback offline corretamente. O certificado é marcado como consumido no banco mesmo sem blockchain.

---

### Teste 3: Logs Estruturados

**Cenário:** Verificação dos logs do backend durante falhas.

**Resultado:** ✅ PASS
- Logs usam formato `LEVEL:module:mensagem`
- Falhas de blockchain são registradas como `WARNING` (não `ERROR`)
- Fallback offline é claramente indicado
- Requisições HTTP são logadas com status code

---

## 3. ANÁLISE DE RESILIÊNCIA POR COMPONENTE

### 3.1 Health Check (`backend/main.py`)

| Aspecto | Status | Observação |
|---------|--------|------------|
| Retorna degraded (não 500) | ✅ | Correto |
| Database check | ✅ | Captura exceção psycopg2 |
| Blockchain check | ✅ | Captura ConnectionError |
| Redis check | ✅ | Verifica conectividade |
| TimescaleDB setup | ⚠️ | WARNING não-fatal se EXTENSION falhar |

### 3.2 SBT Manager (`backend/blockchain/sbt_manager.py`)

| Aspecto | Status | Observação |
|---------|--------|------------|
| Fallback offline no consume | ✅ | Funciona perfeitamente |
| Logging de falha | ✅ | WARNING com detalhes |
| Retorno de tx_hash mock | ✅ | `0x0000...` |
| Fallback offline no mint | ❌ | **NÃO implementado** - `minting.py` não tem fallback |

### 3.3 Web3 Client (`backend/blockchain/web3_client.py`)

| Aspecto | Status | Observação |
|---------|--------|------------|
| Conexão com RPC | ✅ | Tenta reconectar |
| MOCK_MODE | ✅ | Configurável via env |
| Injeção de dependência | ✅ | Singleton pattern |
| Timeout em falha | ⚠️ | Pode travar por até 30s |

### 3.4 Database (`backend/db/database.py`)

| Aspecto | Status | Observação |
|---------|--------|------------|
| Conexão com PostgreSQL | ✅ | SQLAlchemy com pool |
| TimescaleDB EXTENSION | ⚠️ | Falha silenciosa (WARNING) |
| Criação de tabelas | ✅ | `create_all()` no startup |
| Session management | ✅ | Dependency injection |

---

## 4. PROBLEMAS IDENTIFICADOS

### 🔴 Críticos

1. **`minting.py` sem fallback offline**
   - **Arquivo:** `backend/blockchain/minting.py`
   - **Problema:** Se o blockchain estiver offline, o mint lança exceção não tratada
   - **Impacto:** Produtor não consegue mintar certificados sem blockchain
   - **Solução:** Implementar fallback offline similar ao `sbt_manager.py`

2. **`verification.py` sem fallback offline**
   - **Arquivo:** `backend/blockchain/verification.py`
   - **Problema:** Verificação on-chain falha sem fallback
   - **Impacto:** Auditor não consegue verificar certificados
   - **Solução:** Implementar fallback que retorna dados do banco

### 🟡 Médios

3. **TimescaleDB EXTENSION falha silenciosamente**
   - **Arquivo:** `backend/db/database.py`
   - **Problema:** `CREATE EXTENSION IF NOT EXISTS timescaledb` falha com WARNING
   - **Impacto:** Perda de otimizações de hypertable
   - **Solução:** Verificar se a extensão está disponível antes de tentar criar

4. **Hardhat com Node.js 18 (não suportado)**
   - **Arquivo:** `contracts/Dockerfile`
   - **Problema:** Hardhat não suporta Node.js 18
   - **Impacto:** Comportamento imprevisível no hardhat
   - **Solução:** Atualizar para Node.js 20+ no Dockerfile

5. **Backend com --reload em produção**
   - **Arquivo:** `docker-compose.yml`
   - **Problema:** `uvicorn main:app --reload` usado no docker-compose
   - **Impacto:** Reinicialização automática em produção não desejada
   - **Solução:** Usar `docker-compose.prod.yml` sem --reload

### 🟢 Baixos

6. **API Key hardcoded como SECRET_KEY**
   - **Arquivo:** `backend/api/dependencies/auth.py`
   - **Problema:** API key é o mesmo valor de SECRET_KEY
   - **Impacto:** Baixo, mas não segue boas práticas
   - **Solução:** Criar API_KEY separada no .env

7. **Sem health check no frontend**
   - **Problema:** Frontend não verifica status do backend
   - **Impacto:** Usuário não vê quando backend está degradado
   - **Solução:** Adicionar verificação periódica de health

---

## 5. RECOMENDAÇÕES

### Imediatas (Prioridade Alta)

1. **Adicionar fallback offline em `minting.py`**
   ```python
   # Exemplo de implementação
   try:
       tx_hash = mint_on_chain(batch_id, wallet)
   except ConnectionError:
       logger.warning("Blockchain offline, using mock mint")
       tx_hash = "0x" + "0" * 64  # Mock hash
   ```

2. **Adicionar fallback offline em `verification.py`**
   ```python
   try:
       return verify_on_chain(token_id)
   except ConnectionError:
       logger.warning("Blockchain offline, returning DB data")
       return {"verified": False, "source": "database"}
   ```

### Curto Prazo (Prioridade Média)

3. **Atualizar Node.js no Dockerfile do hardhat** para 20.x
4. **Separar API_KEY de SECRET_KEY** no arquivo .env
5. **Adicionar health check no frontend** com indicador visual

### Longo Prazo (Prioridade Baixa)

6. **Implementar fila de retry** para operações blockchain
7. **Adicionar cache Redis** para dados de blockchain
8. **Implementar circuit breaker** para chamadas RPC

---

## 6. MATRIZ DE RESILIÊNCIA

| Componente | Falha | Comportamento | Severidade |
|------------|-------|---------------|------------|
| TimescaleDB | Offline | Health degraded, app continua | 🟡 Médio |
| Hardhat | Offline | Consume funciona (fallback), mint quebra | 🔴 Crítico |
| Redis | Offline | Health degraded, cache perdido | 🟡 Médio |
| Hardhat + TimescaleDB | Ambos offline | App inicia, mas sem dados | 🔴 Crítico |
| Contrato não deployado | Mint/Verify falham | Erro 500 | 🔴 Crítico |

---

## 7. CONCLUSÃO

O sistema H2V-Trust possui **boa resiliência básica** com health check robusto e fallback offline para consumo de certificados. No entanto, **operações de mint e verificação on-chain não possuem fallback**, o que pode causar indisponibilidade parcial em cenários de falha do blockchain.

**Nota de Resiliência: 7.5/10**

### Próximos Passos Recomendados:
1. ✅ Implementar fallback offline em `minting.py`
2. ✅ Implementar fallback offline em `verification.py`
3. ✅ Atualizar Node.js do hardhat para 20.x
4. ✅ Separar API_KEY de SECRET_KEY
5. ✅ Adicionar health check visual no frontend

---

*Relatório gerado automaticamente em 30/04/2026 às 15:13 BRT*

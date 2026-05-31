# AUDITORIA DE SEGURANCA DE CODIGO - H2V-Trust

> **Data:** 30/04/2026
> **Arquivos escaneados:** 298
> **Total de achados (brutos):** 758
> **Achados reais (apos filtro):** 59
> **Falsos positivos removidos:** 699

---

## SUMARIO EXECUTIVO

| Severidade | Quantidade | Descricao |
|------------|:----------:|-----------|
| **CRITICO** | 4 | Secrets reais expostos (private keys, API keys) |
| **ALTO** | 40 | Fallbacks inseguros, URLs Docker no frontend, enderecos fixos |
| **MEDIO** | 15 | Secrets em testes, enderecos de contrato em codigo de teste |
| **BAIXO** | 0 | URLs localhost em testes/arquivos |

---

## 🔴 PROBLEMAS CRITICO (4)

### 1. `.env.production` linha 12

**Tipo:** `PRIVATE_KEY_HEX`

**Descricao:** Chave privada Ethereum (64 hex chars)

**Codigo:**
```
PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

**Valor:** `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efc`

**Recomendacao:** Substituir por variavel de ambiente obrigatoria. Remover do arquivo e usar secrets do Docker/CI.

---

### 2. `frontend\app\api\[...path]\route.ts` linha 10

**Tipo:** `FALLBACK_TEST`

**Descricao:** Fallback para valor de teste

**Codigo:**
```
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'test-secret-key-for-local-development-12345';
```

**Valor:** `|| 'test-`

**Recomendacao:** Remover fallback de teste. Tornar a variavel de ambiente obrigatoria com validacao no startup.

---

### 3. `frontend\src\lib\api.ts` linha 8

**Tipo:** `FALLBACK_TEST`

**Descricao:** Fallback para valor de teste

**Codigo:**
```
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'test-secret-key-for-local-development-12345';
```

**Valor:** `|| 'test-`

**Recomendacao:** Remover fallback de teste. Tornar a variavel de ambiente obrigatoria com validacao no startup.

---

### 4. `tests\archive\test_api_route.py` linha 35

**Tipo:** `HARDCODED_SECRET`

**Descricao:** Secret/Key hardcoded no codigo

**Codigo:**
```
api_key="test-secret-key-for-local-development-12345"
```

**Valor:** `api_key="test-secret-key-for-local-development-123`

**Recomendacao:** Substituir por variavel de ambiente. NUNCA hardcodar secrets no codigo fonte.

---

## 🟠 PROBLEMAS ALTO (40)

### 1. `.env.production` linha 12

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

**Valor:** `0xac0974bec39a17e36ba4a6b4d238ff944bacb478`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 2. `.env.production` linha 13

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
CONTRACT_ADDRESS=0xa513E6E4b8f2a923D98304ec87F64353C4D5C853
```

**Valor:** `0xa513E6E4b8f2a923D98304ec87F64353C4D5C853`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 3. `.env.production` linha 27

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
BATCH_REGISTRY_ADDRESS=0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9
```

**Valor:** `0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 4. `.env.production` linha 28

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
COMPLIANCE_VERIFIER_ADDRESS=0x5FC8d32690cc91D4c39d9d3abcBD16989F875707
```

**Valor:** `0x5FC8d32690cc91D4c39d9d3abcBD16989F875707`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 5. `.env.production` linha 29

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
DELEGATION_MANAGER_ADDRESS=0x0165878A594ca255338adfa4d48449f69242Eb8F
```

**Valor:** `0x0165878A594ca255338adfa4d48449f69242Eb8F`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 6. `.env.production` linha 30

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
GREEN_HYDROGEN_SBT_ADDRESS=0xa513E6E4b8f2a923D98304ec87F64353C4D5C853
```

**Valor:** `0xa513E6E4b8f2a923D98304ec87F64353C4D5C853`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 7. `backend\api\routes\telemetry.py` linha 130

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
"wallet_address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
```

**Valor:** `0x70997970C51812dc3A010C7d01b50e0d17dc79C8`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 8. `backend\api\routes\telemetry.py` linha 146

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
{"batch_hash": batch_hash, "producer": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"}
```

**Valor:** `0x70997970C51812dc3A010C7d01b50e0d17dc79C8`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 9. `backend\api\routes\telemetry.py` linha 152

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
producer_address="0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
```

**Valor:** `0x70997970C51812dc3A010C7d01b50e0d17dc79C8`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 10. `backend\config.py` linha 13

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
POLYGON_RPC_URL: str = "http://localhost:8545"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 11. `backend\config.py` linha 45

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
NEXT_PUBLIC_API_URL: str = "http://localhost:8000"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 12. `contracts\check_balance.js` linha 6

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
const privateKey = process.env.PRIVATE_KEY || '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80';
```

**Valor:** `0xac0974bec39a17e36ba4a6b4d238ff944bacb478`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 13. `docker-compose.yml` linha 49

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
CONTRACT_ADDRESS: 0xa513E6E4b8f2a923D98304ec87F64353C4D5C853
```

**Valor:** `0xa513E6E4b8f2a923D98304ec87F64353C4D5C853`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 14. `docker-compose.yml` linha 50

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
PRIVATE_KEY: ${PRIVATE_KEY:-0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80}
```

**Valor:** `0xac0974bec39a17e36ba4a6b4d238ff944bacb478`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 15. `docker-compose.yml` linha 53

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
BATCH_REGISTRY_ADDRESS: 0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9
```

**Valor:** `0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 16. `docker-compose.yml` linha 54

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
COMPLIANCE_VERIFIER_ADDRESS: 0x5FC8d32690cc91D4c39d9d3abcBD16989F875707
```

**Valor:** `0x5FC8d32690cc91D4c39d9d3abcBD16989F875707`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 17. `docker-compose.yml` linha 55

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
DELEGATION_MANAGER_ADDRESS: 0x0165878A594ca255338adfa4d48449f69242Eb8F
```

**Valor:** `0x0165878A594ca255338adfa4d48449f69242Eb8F`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 18. `docker-compose.yml` linha 56

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
GREEN_HYDROGEN_SBT_ADDRESS: 0xa513E6E4b8f2a923D98304ec87F64353C4D5C853
```

**Valor:** `0xa513E6E4b8f2a923D98304ec87F64353C4D5C853`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 19. `frontend\app\api\[...path]\route.ts` linha 4

**Tipo:** `DOCKER_INTERNAL_URL`

**Descricao:** URL interna do servico Docker (backend:porta)

**Codigo:**
```
// Em produção (Docker), o backend está no serviço 'backend:8000'
```

**Valor:** `backend:8000`

**Recomendacao:** URL interna do Docker no frontend. Usar apenas em next.config.js para rewrites.

---

### 20. `frontend\app\api\[...path]\route.ts` linha 6

**Tipo:** `DOCKER_INTERNAL_URL`

**Descricao:** URL interna do servico Docker (backend:porta)

**Codigo:**
```
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';
```

**Valor:** `backend:8000`

**Recomendacao:** URL interna do Docker no frontend. Usar apenas em next.config.js para rewrites.

---

### 21. `frontend\app\producer\certificates\page.tsx` linha 9

**Tipo:** `FALLBACK_LOCALHOST`

**Descricao:** Fallback para localhost (nao funciona em producao)

**Codigo:**
```
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost";
```

**Valor:** `|| "http://localhost`

**Recomendacao:** Substituir fallback por variavel de ambiente. Em producao, localhost nao funciona.

---

### 22. `frontend\app\producer\delegation\page.tsx` linha 9

**Tipo:** `FALLBACK_LOCALHOST`

**Descricao:** Fallback para localhost (nao funciona em producao)

**Codigo:**
```
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost";
```

**Valor:** `|| "http://localhost`

**Recomendacao:** Substituir fallback por variavel de ambiente. Em producao, localhost nao funciona.

---

### 23. `frontend\src\lib\web3.ts` linha 6

**Tipo:** `FALLBACK_LOCALHOST`

**Descricao:** Fallback para localhost (nao funciona em producao)

**Codigo:**
```
rpcUrl: process.env.NEXT_PUBLIC_RPC_URL || "http://localhost:8545",
```

**Valor:** `|| "http://localhost`

**Recomendacao:** Substituir fallback por variavel de ambiente. Em producao, localhost nao funciona.

---

### 24. `scripts\seed_data.py` linha 98

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
producer_wallet="0x2345678901234567890123456789012345678901"
```

**Valor:** `0x2345678901234567890123456789012345678901`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 25. `scripts\seed_data.py` linha 116

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
producer_wallet="0x3456789012345678901234567890123456789012"
```

**Valor:** `0x3456789012345678901234567890123456789012`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 26. `scripts\seed_data.py` linha 137

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
blockchain_tx_hash="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
```

**Valor:** `0xabcdef1234567890abcdef1234567890abcdef12`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 27. `scripts\seed_data.py` linha 148

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
declarant_address="0x4567890123456789012345678901234567890123",
```

**Valor:** `0x4567890123456789012345678901234567890123`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 28. `scripts\seed_data.py` linha 155

**Tipo:** `CONTRACT_ADDRESS`

**Descricao:** Endereco de contrato/carteira

**Codigo:**
```
declarant_address="0x5678901234567890123456789012345678901234",
```

**Valor:** `0x5678901234567890123456789012345678901234`

**Recomendacao:** Substituir endereco fixo por variavel de ambiente.

---

### 29. `tests\archive\test_api_final_no_unicode.py` linha 9

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
BASE_URL = "http://localhost:8000"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 30. `tests\archive\test_api_simple.py` linha 6

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
url = "http://localhost:8000/api/v1/telemetry"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 31. `tests\archive\test_api_simple_final.py` linha 9

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
BASE_URL = "http://localhost:8000"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 32. `tests\archive\test_complete_flow.py` linha 14

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
BASE_URL = "http://localhost:8000"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 33. `tests\archive\test_e2e.py` linha 10

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
BASE_URL = "http://localhost:8000"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 34. `tests\archive\test_e2e_simple.py` linha 9

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
BASE_URL = "http://localhost:8000"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 35. `tests\archive\test_post.py` linha 4

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
url = "http://localhost:8000/api/v1/telemetry"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 36. `tests\archive\test_system_ascii.py` linha 8

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
BASE_URL = "http://localhost:8000"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 37. `tests\archive\test_system_working.py` linha 8

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
BASE_URL = "http://localhost:8000"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 38. `tests\archive\test_telemetry.py` linha 4

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
url = "http://localhost:8000/api/v1/telemetry"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 39. `tests\archive\test_telemetry_detailed.py` linha 8

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
url = "http://localhost:8000/api/v1/telemetry"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

### 40. `tests\archive\test_telemetry_detailed_final.py` linha 10

**Tipo:** `DEFAULT_LOCALHOST`

**Descricao:** Valor default apontando para localhost

**Codigo:**
```
BASE_URL = "http://localhost:8000"
```

**Valor:** `= "http://localhost`

**Recomendacao:** Substituir valor default hardcoded por variavel de ambiente.

---

## 🟡 PROBLEMAS MEDIO (15)

### 1. `contracts\check_balance.js` linha 6

**Tipo:** `PRIVATE_KEY_HEX`

**Descricao:** Chave privada Ethereum (64 hex chars)

**Codigo:**
```
const privateKey = process.env.PRIVATE_KEY || '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80';
```

**Valor:** `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efc`

**Recomendacao:** Substituir por variavel de ambiente obrigatoria. Remover do arquivo e usar secrets do Docker/CI.

---

### 2. `docker-compose.yml` linha 50

**Tipo:** `PRIVATE_KEY_HEX`

**Descricao:** Chave privada Ethereum (64 hex chars)

**Codigo:**
```
PRIVATE_KEY: ${PRIVATE_KEY:-0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80}
```

**Valor:** `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efc`

**Recomendacao:** Substituir por variavel de ambiente obrigatoria. Remover do arquivo e usar secrets do Docker/CI.

---

### 3. `frontend\app\api\[...path]\route.ts` linha 6

**Tipo:** `DOCKER_SERVICE_URL`

**Descricao:** URL de servico Docker interno

**Codigo:**
```
const BACKEND_URL = process.env.BACKEND_URL || 'http://backend:8000';
```

**Valor:** `http://backend:`

**Recomendacao:** Revisar e substituir por variavel de ambiente.

---

### 4. `frontend\app\api\[...path]\route.ts` linha 10

**Tipo:** `PROCESS_ENV_FALLBACK_TEST`

**Descricao:** process.env com fallback test

**Codigo:**
```
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'test-secret-key-for-local-development-12345';
```

**Valor:** `process.env.NEXT_PUBLIC_API_KEY || 'test-`

**Recomendacao:** Revisar e substituir por variavel de ambiente.

---

### 5. `frontend\app\producer\certificates\page.tsx` linha 9

**Tipo:** `PROCESS_ENV_FALLBACK_LOCALHOST`

**Descricao:** process.env com fallback localhost

**Codigo:**
```
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost";
```

**Valor:** `process.env.NEXT_PUBLIC_API_URL || "http://localhost`

**Recomendacao:** Revisar e substituir por variavel de ambiente.

---

### 6. `frontend\app\producer\certificates\page.tsx` linha 10

**Tipo:** `FALLBACK_TEST`

**Descricao:** Fallback para valor de teste

**Codigo:**
```
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "test-secret-key-for-local-development-12345";
```

**Valor:** `|| "test-`

**Recomendacao:** Remover fallback de teste. Tornar a variavel de ambiente obrigatoria com validacao no startup.

---

### 7. `frontend\app\producer\certificates\page.tsx` linha 10

**Tipo:** `PROCESS_ENV_FALLBACK_TEST`

**Descricao:** process.env com fallback test

**Codigo:**
```
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "test-secret-key-for-local-development-12345";
```

**Valor:** `process.env.NEXT_PUBLIC_API_KEY || "test-`

**Recomendacao:** Revisar e substituir por variavel de ambiente.

---

### 8. `frontend\app\producer\delegation\page.tsx` linha 9

**Tipo:** `PROCESS_ENV_FALLBACK_LOCALHOST`

**Descricao:** process.env com fallback localhost

**Codigo:**
```
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost";
```

**Valor:** `process.env.NEXT_PUBLIC_API_URL || "http://localhost`

**Recomendacao:** Revisar e substituir por variavel de ambiente.

---

### 9. `frontend\app\producer\delegation\page.tsx` linha 10

**Tipo:** `FALLBACK_TEST`

**Descricao:** Fallback para valor de teste

**Codigo:**
```
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "test-secret-key-for-local-development-12345";
```

**Valor:** `|| "test-`

**Recomendacao:** Remover fallback de teste. Tornar a variavel de ambiente obrigatoria com validacao no startup.

---

### 10. `frontend\app\producer\delegation\page.tsx` linha 10

**Tipo:** `PROCESS_ENV_FALLBACK_TEST`

**Descricao:** process.env com fallback test

**Codigo:**
```
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "test-secret-key-for-local-development-12345";
```

**Valor:** `process.env.NEXT_PUBLIC_API_KEY || "test-`

**Recomendacao:** Revisar e substituir por variavel de ambiente.

---

### 11. `frontend\src\lib\api.ts` linha 8

**Tipo:** `PROCESS_ENV_FALLBACK_TEST`

**Descricao:** process.env com fallback test

**Codigo:**
```
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || 'test-secret-key-for-local-development-12345';
```

**Valor:** `process.env.NEXT_PUBLIC_API_KEY || 'test-`

**Recomendacao:** Revisar e substituir por variavel de ambiente.

---

### 12. `frontend\src\lib\web3.ts` linha 6

**Tipo:** `PROCESS_ENV_FALLBACK_LOCALHOST`

**Descricao:** process.env com fallback localhost

**Codigo:**
```
rpcUrl: process.env.NEXT_PUBLIC_RPC_URL || "http://localhost:8545",
```

**Valor:** `process.env.NEXT_PUBLIC_RPC_URL || "http://localhost`

**Recomendacao:** Revisar e substituir por variavel de ambiente.

---

### 13. `iot\simulator.py` linha 13

**Tipo:** `GETENV_EMPTY_FALLBACK`

**Descricao:** os.getenv com fallback vazio

**Codigo:**
```
API_KEY = os.getenv("H2V_API_KEY", "")
```

**Valor:** `os.getenv("H2V_API_KEY", ""`

**Recomendacao:** Revisar e substituir por variavel de ambiente.

---

### 14. `scripts\seed_data.py` linha 127

**Tipo:** `PRIVATE_KEY_HEX`

**Descricao:** Chave privada Ethereum (64 hex chars)

**Codigo:**
```
blockchain_tx_hash="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
```

**Valor:** `0x1234567890abcdef1234567890abcdef1234567890abcdef`

**Recomendacao:** Substituir por variavel de ambiente obrigatoria. Remover do arquivo e usar secrets do Docker/CI.

---

### 15. `scripts\seed_data.py` linha 137

**Tipo:** `PRIVATE_KEY_HEX`

**Descricao:** Chave privada Ethereum (64 hex chars)

**Codigo:**
```
blockchain_tx_hash="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
```

**Valor:** `0xabcdef1234567890abcdef1234567890abcdef1234567890`

**Recomendacao:** Substituir por variavel de ambiente obrigatoria. Remover do arquivo e usar secrets do Docker/CI.

---

## DISTRIBUICAO POR ARQUIVO

| Arquivo | CRITICO | ALTO | MEDIO | BAIXO | Total |
|---------|:-------:|:----:|:-----:|:-----:|:-----:|
| `.env.production` | 1 | 6 | 0 | 0 | 7 |
| `backend\api\routes\telemetry.py` | 0 | 3 | 0 | 0 | 3 |
| `backend\config.py` | 0 | 2 | 0 | 0 | 2 |
| `contracts\check_balance.js` | 0 | 1 | 1 | 0 | 2 |
| `docker-compose.yml` | 0 | 6 | 1 | 0 | 7 |
| `frontend\app\api\[...path]\route.ts` | 1 | 2 | 2 | 0 | 5 |
| `frontend\app\producer\certificates\page.tsx` | 0 | 1 | 3 | 0 | 4 |
| `frontend\app\producer\delegation\page.tsx` | 0 | 1 | 3 | 0 | 4 |
| `frontend\src\lib\api.ts` | 1 | 0 | 1 | 0 | 2 |
| `frontend\src\lib\web3.ts` | 0 | 1 | 1 | 0 | 2 |
| `iot\simulator.py` | 0 | 0 | 1 | 0 | 1 |
| `scripts\seed_data.py` | 0 | 5 | 2 | 0 | 7 |
| `tests\archive\test_api_final_no_unicode.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_api_route.py` | 1 | 0 | 0 | 0 | 1 |
| `tests\archive\test_api_simple.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_api_simple_final.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_complete_flow.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_e2e.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_e2e_simple.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_post.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_system_ascii.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_system_working.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_telemetry.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_telemetry_detailed.py` | 0 | 1 | 0 | 0 | 1 |
| `tests\archive\test_telemetry_detailed_final.py` | 0 | 1 | 0 | 0 | 1 |

---

## RECOMENDACOES PRIORIZADAS

### Imediatas (Criticas)

1. **Remover PRIVATE_KEY do `.env.production`** - Usar GitHub Secrets ou vault
2. **Remover API_KEY hardcoded como fallback em `frontend/src/lib/api.ts`** - Tornar `NEXT_PUBLIC_API_KEY` obrigatoria
3. **Remover PRIVATE_KEY do `.env`** - Usar variavel de ambiente exclusivamente
4. **Remover SECRET_KEY hardcoded do `.env.production`** - Gerar em deploy

### Curto Prazo (Altas)

5. **Substituir fallbacks de localhost por env vars obrigatorias** em `backend/config.py`
6. **Remover enderecos de contrato fixos** do `.env.production` - Usar env vars
7. **Adicionar `.env.production` ao `.gitignore`** - Nunca commitar secrets
8. **Remover `tests/archive/`** - Codigo morto com secrets de teste

### Medio Prazo

9. **Implementar validacao de env vars obrigatorias** no startup do backend
10. **Adicionar linter de seguranca** (semgrep, bandit) no CI/CD
11. **Revisar `contracts/artifacts/`** - Nao commitar artifacts do Hardhat
12. **Adicionar `.env.example` sem valores reais**

---

*Relatorio gerado automaticamente em 30/04/2026*
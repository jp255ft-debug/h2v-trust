# Guia do Proxy de API Next.js - H2V-Trust

## 📋 Visão Geral

O proxy de API do Next.js é um componente crítico que permite que o frontend se comunique com o backend FastAPI através de uma única interface unificada. Este proxy oferece:

1. **Roteamento dinâmico** - Todas as rotas da API são automaticamente repassadas
2. **Autenticação centralizada** - Validação de tokens JWT
3. **CORS configurado** - Comunicação segura entre domínios
4. **Logging e monitoramento** - Debug em desenvolvimento
5. **Timeout e retry** - Resiliência de rede

## 🚀 Como Funciona

### Arquitetura:
```
Frontend (Next.js) → Proxy API (/api/[...path]) → Backend (FastAPI:8000)
       ↑                               ↑                     ↑
    Browser                        Next.js Server        FastAPI Server
```

### Fluxo de Requisição:
1. Cliente faz requisição para `/api/algum-endpoint`
2. Next.js intercepta no `app/api/[...path]/route.ts`
3. Proxy valida autenticação (se necessário)
4. Proxy repassa requisição para `http://localhost:8000/algum-endpoint`
5. Proxy processa resposta e retorna ao cliente

## ⚙️ Configuração

### Variáveis de Ambiente (.env.local):

```env
# Backend API Configuration
BACKEND_URL=http://localhost:8000
API_TIMEOUT=10000

# Authentication
VALIDATE_TOKENS=false
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# CORS Configuration
NEXT_PUBLIC_API_BASE_URL=/api
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Development Settings
NODE_ENV=development
LOG_LEVEL=debug

# Security
RATE_LIMIT_ENABLED=true
RATE_LIMIT_MAX_REQUESTS=100
RATE_LIMIT_WINDOW_MS=900000

# Cache Settings
API_CACHE_ENABLED=true
API_CACHE_TTL=300000
```

### Configuração do Next.js (next.config.js):

```javascript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: '/api/:path*',
      },
    ];
  },
};
```

## 🔐 Autenticação

### Rotas Públicas (não requerem autenticação):
- `/api/health` - Health check
- `/api/docs` - Documentação Swagger
- `/api/openapi.json` - Esquema OpenAPI
- `/api/auth/login` - Login de usuário
- `/api/auth/register` - Registro de usuário

### Rotas Protegidas:
Todas as outras rotas requerem token JWT no header:
```http
Authorization: Bearer <seu_token_jwt>
```

### Validação de Token:
1. Verifica se header `Authorization` existe e começa com `Bearer `
2. Extrai o token
3. Valida formato básico (em desenvolvimento)
4. Opcionalmente valida com endpoint `/api/auth/validate` (produção)

## 🌐 CORS (Cross-Origin Resource Sharing)

### Headers Configurados:
- `Access-Control-Allow-Origin: *` (em desenvolvimento)
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`
- `Access-Control-Max-Age: 86400` (24 horas cache)

### Preflight Requests:
Requests `OPTIONS` são automaticamente tratados com headers CORS apropriados.

## 📊 Logging e Monitoramento

### Em Desenvolvimento:
```javascript
console.log(`[API Proxy] ${method} ${apiPath} -> ${fullUrl}`);
console.log(`[API Proxy Response] ${apiPath}:`, {
  status: response.status,
  data: data
});
```

### Em Produção:
- Logs estruturados podem ser enviados para serviços como:
  - Elasticsearch + Kibana
  - Datadog
  - AWS CloudWatch
  - Google Cloud Logging

## ⚡ Performance

### Timeout Configurável:
- **Timeout padrão:** 10 segundos (`API_TIMEOUT=10000`)
- **Timeout máximo do handler:** 30 segundos (`maxDuration: 30`)

### Cache:
- Cache de resposta opcional (`API_CACHE_ENABLED=true`)
- TTL configurável (`API_CACHE_TTL=300000` - 5 minutos)

### Rate Limiting:
- Limite de 100 requisições por IP a cada 15 minutos
- Configurável via `RATE_LIMIT_MAX_REQUESTS` e `RATE_LIMIT_WINDOW_MS`

## 🛡️ Segurança

### Headers de Segurança:
- `X-Forwarded-For` - IP original do cliente
- `X-Forwarded-Host` - Host original
- `X-Forwarded-Proto` - Protocolo original (http/https)

### Validação de Input:
1. **Métodos HTTP:** Apenas métodos suportados (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`)
2. **Content-Type:** Suporte para JSON, form-data, x-www-form-urlencoded
3. **Tamanho do Body:** Limitado pela configuração do Next.js

### Proteção contra DDoS:
- Rate limiting por IP
- Timeout configurável
- Abort controller para cancelar requests lentos

## 🔧 Tipos de Conteúdo Suportados

### Request Body:
- `application/json` - Objetos JSON
- `multipart/form-data` - Upload de arquivos
- `application/x-www-form-urlencoded` - Forms HTML
- `text/*` - Texto simples

### Response Body:
- `application/json` - Retornado como JSON
- `text/*` - Retornado como texto
- `application/octet-stream` - Retornado como buffer
- `application/pdf`, `image/*` - Retornado como binário

## 🧪 Testando o Proxy

### Teste Local:
```bash
# Iniciar backend
cd backend
uvicorn main:app --reload --port 8000

# Iniciar frontend
cd frontend
npm run dev

# Testar proxy
curl http://localhost:3000/api/health
curl -H "Authorization: Bearer test-token" http://localhost:3000/api/batches
```

### Testes Automatizados:
```typescript
// Exemplo de teste com fetch
const response = await fetch('/api/batches', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer test-token',
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
```

## 🐛 Troubleshooting

### Problemas Comuns:

1. **CORS Errors:**
   - Verificar headers `Access-Control-Allow-Origin`
   - Confirmar que preflight requests (`OPTIONS`) funcionam

2. **Timeout Errors:**
   - Aumentar `API_TIMEOUT` no .env.local
   - Verificar se backend está respondendo

3. **Authentication Errors:**
   - Verificar se token JWT está no header `Authorization`
   - Confirmar formato: `Bearer <token>`
   - Validar token com endpoint `/api/auth/validate`

4. **Proxy Not Routing:**
   - Verificar se arquivo `app/api/[...path]/route.ts` existe
   - Confirmar configuração do Next.js
   - Checar logs do servidor Next.js

### Logs de Debug:
```bash
# Habilitar logs detalhados
LOG_LEVEL=debug npm run dev

# Verificar variáveis de ambiente
console.log('BACKEND_URL:', process.env.BACKEND_URL);
```

## 🔄 Deploy

### Configuração de Produção:

```env
# Produção
BACKEND_URL=https://api.h2v-trust.com
VALIDATE_TOKENS=true
JWT_SECRET=<secret-key-from-vault>
NODE_ENV=production
LOG_LEVEL=warn
```

### Considerações de Deploy:

1. **SSL/TLS:** Usar HTTPS em produção
2. **Secrets Management:** Usar vault ou serviço de secrets
3. **Monitoring:** Configurar alertas para errors/timeouts
4. **Scaling:** Considerar load balancer para múltiplas instâncias

## 📈 Métricas e Monitoramento

### Métricas Recomendadas:
- **Taxa de sucesso:** `success_rate = (200 + 201 + 204) / total_requests`
- **Tempo de resposta:** `p50, p95, p99 response_time`
- **Taxa de erro:** `error_rate = (4xx + 5xx) / total_requests`
- **Utilização:** `requests_per_second`

### Alertas:
- **Crítico:** Error rate > 5%
- **Alerta:** Response time p95 > 5s
- **Info:** Success rate < 95%

## 🎯 Melhores Práticas

1. **Sempre usar HTTPS** em produção
2. **Validar tokens JWT** em produção (`VALIDATE_TOKENS=true`)
3. **Configurar rate limiting** apropriado para sua carga
4. **Monitorar logs** e métricas regularmente
5. **Manter secrets** em serviço seguro (não no código)
6. **Testar CORS** em diferentes ambientes
7. **Documentar endpoints** com OpenAPI/Swagger

## 🔗 Links Úteis

- [Next.js Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
- [CORS no Next.js](https://nextjs.org/docs/app/building-your-application/routing/middleware#cors)
- [JWT Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [API Security Checklist](https://github.com/shieldfy/API-Security-Checklist)

---

*Documentação atualizada em 21/04/2026 - Proxy API H2V-Trust v1.0.0*
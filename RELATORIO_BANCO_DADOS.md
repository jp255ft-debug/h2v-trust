# Relatório do Banco de Dados - H2V-Trust

**Data:** 14/05/2026  
**Banco:** TimescaleDB (PostgreSQL)  
**Total de Tabelas:** 9

---

## 📊 Resumo por Tabela

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `alembic_version` | 1 | Controle de versão do Alembic |
| `audit_logs` | 40 | Logs de auditoria do sistema |
| `batches` | 31 | Lotes de produção de hidrogênio |
| `certificates` | 12 | Certificados de conformidade |
| `delegations` | 0 | Delegações CBAM |
| `telemetry_records` | 31 | Dados telemétricos de sensores |
| `tenants` | 3 | Inquilinos (organizações) |
| `user_tenants` | 3 | Associação usuário-tenant |
| `users` | 3 | Usuários do sistema |

---

## 👤 Usuários (3)

| Email | Nome | Ativo |
|-------|------|-------|
| `admin@h2v-trust.com` | Platform Administrator | ✅ |
| `operator@produtor-alfa.com` | Alfa Operator | ✅ |
| `auditor@h2v-trust.com` | Compliance Auditor | ✅ |

---

## 🏢 Tenants (3)

| Nome | Slug | Status |
|------|------|--------|
| Default Platform | `default` | active |
| Produtor Alfa Ltda | `produtor-alfa` | active |
| Produtor Beta S.A. | `produtor-beta` | active |

---

## 📦 Lotes (31)

- **Compliant:** 8 lotes ✅
- **Non-compliant:** 23 lotes ❌
- **Blockchain confirmed:** 2 lotes
- **Blockchain pending:** 29 lotes
- **Localização:** Cedro, Ceará, Brasil
- **Faixa de emissões:** 1.5 ~ 4.32 kgCO2/kgH2
- **Limite CBAM:** 3.4 kgCO2/kgH2

### Últimos lotes compliant:
1. Batch `ed5ad741` - 1000kg - Emissões: 1.5 - **confirmed** ✅
2. Batch `61366fd9` - 1000kg - Emissões: 1.5 - pending ✅
3. Batch `5427d6f4` - 1000kg - Emissões: 1.5 - pending ✅
4. Batch `88b2b044` - 1000kg - Emissões: 1.5 - pending ✅

---

## 📜 Certificados (12)

- **Consumidos:** 3 (token_id: 1000, 1001, 0)
- **Disponíveis:** 9
- **Blockchain:** 2 com tx_hash real, 10 offline
- **Token IDs:** 0, 1, 2, 1000, 1001, 1002, 1003, 1004, 1005, 1006

---

## 📋 Logs de Auditoria (40)

**Tipos de eventos:**
- `blockchain.mint.attempt` - Tentativas de mint
- `blockchain.mint.success` - Mint bem-sucedido
- `blockchain.mint.failed` - Falhas de mint
- `compliance.check` - Verificações de conformidade
- `telemetry.received` - Dados telemétricos recebidos

---

## 📡 Telemetria (31 registros)

- **Fontes de energia:** wind, solar
- **Fontes de água:** desalination, recycled
- **Período:** Nov/2025 a Mai/2026

---

## 🔗 Associações User-Tenant (3)

- admin@h2v-trust.com → Default Platform (admin)
- operator@produtor-alfa.com → Produtor Alfa (operator)
- auditor@h2v-trust.com → Default Platform (auditor)

---

## 📈 Indicadores-Chave

| Indicador | Valor |
|-----------|-------|
| Total de lotes | 31 |
| Lotes compliant | 8 (25.8%) |
| Lotes não-compliant | 23 (74.2%) |
| Certificados emitidos | 12 |
| Certificados consumidos | 3 |
| Delegações ativas | 0 |
| Usuários cadastrados | 3 |
| Tenants ativos | 3 |
| Eventos de auditoria | 40 |
| Registros de telemetria | 31 |

---

*Relatório gerado automaticamente em 14/05/2026 às 21:29 BRT*

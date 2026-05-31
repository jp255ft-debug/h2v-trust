# Política de Segurança do H2V-Trust

## 🔒 Reportando uma Vulnerabilidade

A segurança do H2V-Trust é uma prioridade. Se você descobrir uma vulnerabilidade de segurança, **NÃO** abra uma issue pública no GitHub. Por favor, reporte-a de forma responsável através dos canais abaixo.

### Canais de Reporte

- **Email**: jp255ft@gmail.com
- **Assunto**: "[H2V-Trust Security] - Breve descrição"
- **PGP Key**: [Disponível sob solicitação]

### O que incluir no reporte

1. **Descrição** clara e concisa da vulnerabilidade
2. **Passos para reproduzir** (prova de conceito, se possível)
3. **Impacto potencial** (o que um atacante poderia fazer)
4. **Versão afetada** (commit hash, tag ou versão)
5. **Ambiente** onde a vulnerabilidade foi descoberta
6. **Sugestão de correção** (se aplicável)

### O que esperar

- **Confirmação de recebimento** em até 48 horas
- **Atualização de progresso** a cada 5 dias úteis
- **Tempo de correção** baseado na severidade:
  - Crítica: 7 dias
  - Alta: 14 dias
  - Média: 30 dias
  - Baixa: 60 dias

## 📋 Versões Suportadas

| Versão | Suporte |
|--------|---------|
| 1.0.0 | ✅ Ativo |
| < 1.0.0 | ❌ Não suportado |

## 🔐 Práticas de Segurança do Projeto

### Proteção de Dados

- **Senhas**: Hash com bcrypt (cost factor 12)
- **Tokens JWT**: Assinados com HS256, expiração configurável
- **API Keys**: Armazenadas como hash SHA-256
- **Dados sensíveis**: Criptografia em repouso (AES-256)

### Controle de Acesso

- **RBAC**: Controle de acesso baseado em papéis (admin, producer, auditor)
- **Multi-tenant**: Isolamento completo de dados entre tenants
- **Rate Limiting**: 100 requisições/minuto por IP (configurável)
- **CORS**: Restrito a origens configuradas

### Infraestrutura

- **Docker**: Containers executados como non-root user
- **Rede**: Isolamento de rede entre serviços (Docker networks)
- **SSL/TLS**: HTTPS obrigatório em produção (Nginx + Let's Encrypt)
- **Firewall**: Portas expostas apenas para serviços necessários

### CI/CD Security

- **Gitleaks**: Varredura de segredos em cada push
- **CodeQL**: Análise estática de código (Python, JavaScript, TypeScript)
- **Dependency Audit**: Verificação de vulnerabilidades em dependências
- **SAST**: Análise estática de segurança no pipeline

## 🚨 Processo de Divulgação

1. **Reporte** recebido e confirmado pela equipe de segurança
2. **Análise** da vulnerabilidade e avaliação de impacto
3. **Correção** preparada e testada em ambiente isolado
4. **Patch** lançado em uma nova versão
5. **Divulgação pública** 7 dias após o lançamento do patch

### Timeline de Divulgação

```
Dia 0:  Vulnerabilidade reportada
Dia 2:  Confirmada e em análise
Dia 7:  Correção em desenvolvimento (crítica)
Dia 14: Patch lançado
Dia 21: Divulgação pública
```

## 🛡️ Recompensas

Atualmente não temos um programa formal de bug bounty, mas reconhecemos publicamente contribuições de segurança no nosso arquivo de [Agradecimentos](https://github.com/jp255ft-debug/h2v-trust/blob/main/ACKNOWLEDGMENTS.md).

## 📚 Leia Mais

- [Guia de Contribuição](CONTRIBUTING.md)
- [Código de Conduta](CODE_OF_CONDUCT.md)
- [Documentação de Deploy](docs/deployment.md)
- [Relatório de Auditoria de Segurança](RELATORIO_AUDITORIA_SEGURANCA.md)

---

**Última atualização:** 31 de maio de 2026

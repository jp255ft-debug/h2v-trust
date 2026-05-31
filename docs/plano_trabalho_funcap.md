# Plano de Trabalho - FUNCAP

## H2V-Trust: Certificação Digital de Hidrogênio Verde com Blockchain

---

## 1. Identificação do Projeto

| Campo | Detalhe |
|---|---|
| **Título** | H2V-Trust — Plataforma de Certificação e Rastreabilidade de Hidrogênio Verde |
| **Instituição Proponente** | [Nome da Instituição] |
| **Órgão Financiador** | FUNCAP — Fundação Cearense de Apoio ao Desenvolvimento Científico e Tecnológico |
| **Período** | 12 meses |
| **Valor Solicitado** | R$ [valor a definir] |
| **Coordenador** | [Nome do Coordenador] |

---

## 2. Objetivos

### Objetivo Geral
Desenvolver e validar uma plataforma de certificação digital de hidrogênio verde baseada em blockchain e IoT, em conformidade com o mecanismo CBAM da União Europeia.

### Objetivos Específicos
1. Implantar infraestrutura de produção da plataforma H2V-Trust em nuvem
2. Realizar piloto com produtor de H₂V no Ceará (Complexo do Pecém)
3. Obter certificação junto a auditoria internacional (Bureau Veritas ou similar)
4. Publicar resultados em periódico científico (Qualis A)
5. Capacitar equipe técnica em blockchain aplicada à energia

---

## 3. Metodologia

O projeto segue a metodologia **Design Science Research (DSR)** em 5 ciclos:

```
Ciclo 1: Requisitos e Arquitetura  →  Mês 1-2
Ciclo 2: Desenvolvimento e Testes  →  Mês 3-6
Ciclo 3: Piloto e Validação        →  Mês 7-9
Ciclo 4: Certificação e Ajustes    →  Mês 10-11
Ciclo 5: Disseminação              →  Mês 12
```

---

## 4. Cronograma e Entregáveis

### Mês 1-2: Fundação
- ✅ Arquitetura finalizada (já concluída)
- ✅ Documentação técnica (já concluída)
- 🔄 Ambiente de produção configurado
- **Entregável:** Relatório de arquitetura validado

### Mês 3-4: Infraestrutura de Produção
- Deploy em nuvem (Render/Railway)
- Configuração de domínio e SSL
- Pipeline CI/CD automatizado
- Monitoramento (Prometheus + Grafana)
- **Entregável:** Ambiente de produção operacional

### Mês 5-6: Piloto Controlado
- Integração com IoT simulator real
- Testes de carga e performance
- Validação de conformidade CBAM
- Correções e otimizações
- **Entregável:** Relatório de validação técnica

### Mês 7-8: Piloto com Produtor Real
- Instalação de sensores IoT no Pecém
- Coleta de dados reais de produção
- Emissão de certificados SBT em testnet (Polygon Amoy)
- **Entregável:** Relatório do piloto com dados reais

### Mês 9-10: Certificação e Auditoria
- Submissão a auditoria internacional
- Ajustes conforme requisitos do auditor
- Validação cruzada com certificações existentes
- **Entregável:** Certificado de conformidade da plataforma

### Mês 11-12: Disseminação
- Artigo científico (Qualis A1/A2)
- Participação em evento internacional (World Hydrogen Summit)
- Workshop com stakeholders do Pecém H2V Hub
- Relatório final e prestação de contas
- **Entregável:** Artigo publicado + relatório final

---

## 5. Orçamento Estimado

| Rubrica | Valor (R$) |
|---|---|
| **Pessoal** (1 bolsista DCR + 2 IC) | 120.000 |
| **Infraestrutura em Nuvem** (12 meses) | 24.000 |
| **Sensores IoT** (kit piloto) | 15.000 |
| **Taxas de Blockchain** (testnet + mainnet) | 5.000 |
| **Certificação** (auditoria internacional) | 30.000 |
| **Participação em Evento** (passagens + hospedagem) | 15.000 |
| **Material de Consumo e Publicação** | 6.000 |
| **Total** | **215.000** |

---

## 6. Equipe

| Função | Dedicação | Responsabilidade |
|---|---|---|
| Coordenador | 20h/sem | Gestão técnica e científica |
| Desenvolvedor Blockchain | 40h/sem | Smart contracts, Web3 |
| Desenvolvedor Full-Stack | 40h/sem | Frontend, API, DevOps |
| Estagiário IC 1 | 20h/sem | IoT, sensores, coleta de dados |
| Estagiário IC 2 | 20h/sem | Testes, documentação, validação |

---

## 7. Impactos Esperados

### Científicos
- 1 artigo em periódico Qualis A
- 2 artigos em conferências nacionais/internacionais
- Repositório open source com documentação completa

### Tecnológicos
- Plataforma de certificação H₂V pronta para uso comercial
- Integração com o Complexo do Pecém (Ceará)
- Framework replicável para outras regiões (Namíbia, Chile)

### Socioeconômicos
- Posicionamento do Ceará como hub de inovação em H₂V
- Capacitação de recursos humanos em blockchain e energia
- Atração de investimentos para a cadeia de H₂V no Nordeste

---

## 8. Riscos e Mitigação

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Atraso na instalação de sensores | Média | Alto | Simulador IoT como fallback |
| Mudanças na regulação CBAM | Média | Médio | Arquitetura modular e adaptável |
| Dificuldade de acesso a produtor real | Alta | Alto | Parceria com Pecém H2V Hub |
| Oscilação de preços de blockchain | Baixa | Baixo | Uso de L2 (Polygon) com taxas previsíveis |

---

## 9. Referências

1. Regulamento CBAM (EU) 2023/956 — Parlamento Europeu
2. ERC-5192: Soulbound Token Standard — Ethereum
3. Plano Nacional de Hidrogênio (PNH2) — MME Brasil
4. Roteiro H2V do Ceará — Governo do Estado do Ceará
5. Design Science Research in Information Systems — Hevner et al. (2004)

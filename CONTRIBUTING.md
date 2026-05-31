# Guia de Contribuição para o H2V-Trust

Obrigado pelo interesse em contribuir com o H2V-Trust! 🎉

Este documento descreve como você pode contribuir com o projeto, seja reportando bugs, sugerindo funcionalidades ou enviando código.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Começar](#como-começar)
- [Reportando Bugs](#reportando-bugs)
- [Sugerindo Funcionalidades](#sugerindo-funcionalidades)
- [Fluxo de Desenvolvimento](#fluxo-de-desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Testes](#testes)
- [Pull Requests](#pull-requests)
- [Ambiente de Desenvolvimento](#ambiente-de-desenvolvimento)

## Código de Conduta

Este projeto segue um [Código de Conduta](CODE_OF_CONDUCT.md) que todos os contribuidores devem respeitar. Ao participar, você concorda em manter um ambiente acolhedor e respeitoso para todos.

## Como Começar

1. **Fork** o repositório no GitHub
2. **Clone** seu fork localmente:
   ```bash
   git clone https://github.com/SEU-USUARIO/h2v-trust.git
   cd h2v-trust
   ```
3. **Adicione o repositório upstream**:
   ```bash
   git remote add upstream https://github.com/jp255ft-debug/h2v-trust.git
   ```
4. **Crie uma branch** para sua contribuição:
   ```bash
   git checkout -b feature/nome-da-feature
   ```

## Reportando Bugs

Se encontrar um bug, por favor abra uma [issue](https://github.com/jp255ft-debug/h2v-trust/issues) com:

- **Título descritivo** do problema
- **Passos para reproduzir** o bug
- **Comportamento esperado** vs **comportamento observado**
- **Screenshots** ou logs (se aplicável)
- **Ambiente**: sistema operacional, versão do Docker, Node.js, Python
- **Versão do projeto** (commit hash ou tag)

### Template de Bug Report

```markdown
## Descrição do Bug
[Descrição clara e concisa do bug]

## Passos para Reproduzir
1. Vá para '...'
2. Execute '...'
3. Veja o erro '...'

## Comportamento Esperado
[O que deveria acontecer]

## Screenshots
[Se aplicável]

## Ambiente
- OS: [ex: Windows 11, Ubuntu 22.04]
- Docker: [ex: 24.0.7]
- Node.js: [ex: 20.11.0]
- Python: [ex: 3.11.8]

## Informações Adicionais
[Qualquer contexto adicional]
```

## Sugerindo Funcionalidades

Para sugerir uma nova funcionalidade, abra uma [issue](https://github.com/jp255ft-debug/h2v-trust/issues) com:

- **Descrição clara** da funcionalidade desejada
- **Caso de uso** e por que seria útil
- **Exemplos** de como funcionaria (mockups, diagramas)
- **Alternativas** consideradas

## Fluxo de Desenvolvimento

1. **Atualize sua branch** com a upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```
2. **Faça suas alterações** seguindo os padrões de código
3. **Teste** suas alterações localmente
4. **Commit** com mensagens claras (veja padrão abaixo)
5. **Push** para seu fork:
   ```bash
   git push origin feature/nome-da-feature
   ```
6. **Abra um Pull Request** para a branch `main`

### Padrão de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: adiciona verificação de adicionalidade por satélite

Implementa o módulo de monitoramento por satélite para verificar
a adicionalidade da produção de hidrogênio verde, conforme
modelo da Namíbia.

Closes #123
```

Tipos permitidos:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação, estilo (sem mudança de lógica)
- `refactor`: Refatoração de código
- `test`: Testes
- `chore`: Tarefas de manutenção
- `security`: Correções de segurança

## Padrões de Código

### Python (Backend)

- **PEP 8**: Siga o estilo PEP 8 (linhas até 88 caracteres)
- **Type Hints**: Todas as funções devem ter type hints completos
- **Docstrings**: Use docstrings no formato Google Style
- **Testes**: Toda nova funcionalidade deve ter testes unitários
- **Logging**: Use `logging.getLogger(__name__)` em cada módulo

```python
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def calculate_emissions(
    batch_id: str,
    energy_source: str,
    consumption_kwh: float
) -> Optional[float]:
    \"\"\"Calcula emissões de carbono para um lote de produção.

    Args:
        batch_id: Identificador único do lote
        energy_source: Fonte de energia (solar, eólica, grid)
        consumption_kwh: Consumo energético em kWh

    Returns:
        Emissões em kgCO₂e ou None se não for possível calcular
    \"\"\"
    # Implementação...
    pass
```

### TypeScript / JavaScript (Frontend)

- **ESLint + Prettier**: Use as configurações do projeto
- **Modo Strict**: TypeScript strict mode habilitado
- **Componentes Funcionais**: Prefira componentes funcionais com hooks
- **Estados**: Trate loading, erro e empty states em toda UI

```typescript
interface BatchData {
  id: string;
  producerId: string;
  amountKg: number;
  emissionsKgCO2: number;
  status: 'pending' | 'certified' | 'consumed';
}

const BatchCard: React.FC<{ batch: BatchData }> = ({ batch }) => {
  // Implementação...
};
```

### Solidity (Smart Contracts)

- **OpenZeppelin**: Use padrões e contratos OpenZeppelin
- **Testes**: Testes completos com Hardhat
- **Documentação**: NatSpec completo para todas as funções
- **Segurança**: Siga as práticas recomendadas (ReentrancyGuard, etc.)

```solidity
/// @notice Mints a new green hydrogen certificate as a Soulbound Token
/// @param to Address of the certificate recipient
/// @param batchId Unique identifier for the production batch
/// @param emissions Carbon emissions in kgCO₂e
/// @return tokenId The ID of the newly minted token
function mintCertificate(
    address to,
    string calldata batchId,
    uint256 emissions
) external returns (uint256 tokenId) {
    // Implementação...
}
```

## Testes

### Backend (Python)
```bash
cd backend
pytest tests/ -v --cov=. --cov-report=term-missing
```

### Smart Contracts (Hardhat)
```bash
cd contracts
npx hardhat test
```

### Frontend
```bash
cd frontend
npm test
```

### Testes E2E
```bash
cd tests
python -m pytest test_e2e_certification_flow.py -v
```

**Requisitos mínimos:**
- ✅ Testes unitários para toda nova lógica de negócio
- ✅ Cobertura mínima de 80% para novos código
- ✅ Testes E2E para fluxos críticos (certificação, compliance)
- ✅ Nenhum teste existente deve quebrar

## Pull Requests

### Checklist antes de abrir um PR

- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Todos os testes passam localmente
- [ ] Documentação foi atualizada (se necessário)
- [ ] CHANGELOG.md foi atualizado
- [ ] Commits seguem o padrão Conventional Commits
- [ ] Branch está atualizada com a main

### Processo de Review

1. **Pelo menos 1 approval** de um mantenedor é necessário
2. **Mudanças solicitadas** devem ser endereçadas
3. **CI/CD deve passar** (testes, lint, build)
4. **Security audit** deve passar (Gitleaks, CodeQL)

## Ambiente de Desenvolvimento

### Docker (Recomendado)

```bash
# Iniciar ambiente de desenvolvimento
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --remove-orphans

# Verificar status
docker compose ps

# Ver logs
docker compose logs --tail=50 backend

# Parar ambiente
docker compose down --remove-orphans
```

### Desenvolvimento Local

Consulte o [README.md](README.md) para instruções detalhadas de configuração local.

### Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

**⚠️ NUNCA** commite arquivos `.env` ou credenciais reais.

## Dúvidas?

Se tiver dúvidas, abra uma [discussion](https://github.com/jp255ft-debug/h2v-trust/discussions) ou entre em contato pelo email: dev@h2v-trust.com

---

**Obrigado por contribuir para um futuro mais verde! 🌱**

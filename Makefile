# H2V-Trust Makefile
# Comandos úteis para desenvolvimento e deploy

.PHONY: help install up down build test clean

help:
	@echo "H2V-Trust - Comandos disponíveis:"
	@echo ""
	@echo "  install     Instala dependências de todos os componentes"
	@echo "  up          Inicia todos os serviços com Docker Compose"
	@echo "  down        Para todos os serviços"
	@echo "  build       Constrói imagens Docker"
	@echo "  logs        Mostra logs dos serviços"
	@echo "  backend     Inicia apenas o backend"
	@echo "  frontend    Inicia apenas o frontend"
	@echo "  contracts   Inicia apenas os smart contracts"
	@echo "  test        Executa testes em todos os componentes"
	@echo "  clean       Limpa arquivos temporários e caches"
	@echo "  db-init     Inicializa o banco de dados"
	@echo "  iot-sim     Inicia simulador IoT"
	@echo ""

install:
	@echo "Instalando dependências do backend..."
	cd backend && pip install -r requirements.txt -r requirements.dev.txt
	@echo "Instalando dependências dos smart contracts..."
	cd contracts && npm install
	@echo "Instalando dependências do frontend..."
	cd frontend && npm install

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

backend:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

contracts:
	cd contracts && npx hardhat node

test:
	@echo "Testando backend..."
	cd backend && pytest tests/ -v
	@echo "Testando smart contracts..."
	cd contracts && npx hardhat test
	@echo "Testando frontend..."
	cd frontend && npm test

clean:
	@echo "Limpando arquivos temporários..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "out" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "artifacts" -exec rm -rf {} + 2>/dev/null || true
	@echo "Limpeza concluída!"

db-init:
	python scripts/init_db.py

iot-sim:
	cd iot && python simulator.py

# Comandos de deploy
deploy-local:
	@echo "Deployando smart contracts na rede local..."
	cd contracts && npx hardhat run scripts/deploy.js --network localhost

deploy-polygon:
	@echo "Deployando smart contracts na Polygon..."
	cd contracts && npx hardhat run scripts/deploy.js --network polygon

# Comandos de desenvolvimento
format:
	@echo "Formatando código Python..."
	cd backend && black .
	cd backend && isort .
	@echo "Formatando código TypeScript..."
	cd frontend && npx prettier --write .

lint:
	@echo "Verificando código Python..."
	cd backend && flake8 .
	cd backend && mypy .
	@echo "Verificando código TypeScript..."
	cd frontend && npx eslint .

# Comandos de monitoramento
monitor:
	@echo "Abrindo monitoramento..."
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3001"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Frontend: http://localhost:3000"
	@echo "Hardhat Node: http://localhost:8545"
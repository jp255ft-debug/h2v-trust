# H2V-Trust Makefile
# Comandos úteis para desenvolvimento e deploy

.PHONY: help install up down build test clean prod down-prod rebuild-prod logs-prod dev-start dev-stop dev-reset dev-reset-full dev-status dev-seed dev-logs dev-check seed-all

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
	@echo "--- Ambiente de Desenvolvimento (Override) ---"
	@echo "  dev-start   Inicia ambiente dev (com override)"
	@echo "  dev-stop    Para ambiente dev (com override)"
	@echo "  dev-reset   Reset de emergência + sobe ambiente"
	@echo "  dev-reset-full Reset completo (remove volumes)"
	@echo "  dev-status  Status dos containers + logs backend"
	@echo "  dev-check   Diagnóstico completo (órfãos, fantasmas)"
	@echo "  dev-seed    Popula banco com dados de demonstração"
	@echo "  dev-logs    Logs em tempo real de todos serviços"
	@echo ""
	@echo "--- Ambiente de Produção ---"
	@echo "  prod        Sobe todos os serviços em produção"
	@echo "  down-prod   Derruba todos os serviços de produção"
	@echo "  rebuild-prod Reconstrói e sobe serviços de produção"
	@echo "  logs-prod   Mostra logs dos serviços de produção"
	@echo ""

install:
	@echo "Instalando dependências do backend..."
	cd backend && pip install -r requirements.prod.txt -r requirements.dev.txt
	@echo "Instalando dependências dos smart contracts..."
	cd contracts && npm install
	@echo "Instalando dependências do frontend..."
	cd frontend && npm install

up:
	docker compose up -d

down:
	docker compose down

dev:
	docker compose up -d --remove-orphans

dev-recreate:
	docker compose up -d --force-recreate --remove-orphans

dev-down:
	docker compose down --remove-orphans

# --- Comandos Docker Seguros (Anti-Container Fantasma) ---
COMPOSE_DEV = docker compose -f docker-compose.yml -f docker-compose.dev.yml

dev-start:
	$(COMPOSE_DEV) up -d --remove-orphans

dev-stop:
	$(COMPOSE_DEV) down --remove-orphans

dev-reset:
	scripts\reset-docker.bat
	$(COMPOSE_DEV) up -d --remove-orphans

dev-reset-full:
	scripts\reset-docker.bat --full
	$(COMPOSE_DEV) up -d --remove-orphans

dev-status:
	$(COMPOSE_DEV) ps
	$(COMPOSE_DEV) logs backend --tail 10

dev-seed:
	@echo "🌱 Executando seed completo (auth + dados de demonstração)..."
	$(COMPOSE_DEV) exec backend python scripts/seed_users_tenants.py
	$(COMPOSE_DEV) exec backend python scripts/seed_demo_data.py

dev-logs:
	$(COMPOSE_DEV) logs -f

dev-check:
	@echo "🔍 Ambiente Docker H2V-Trust"
	@echo ""
	@echo "📋 Containers ativos:"
	@docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
	@echo ""
	@echo "📦 Containers órfãos (exited):"
	@docker ps -a --filter "name=h2v" --filter "status=exited" --format "  {{.ID}} {{.Names}}" 2>nul || echo "  Nenhum"
	@echo ""
	@echo "👻 Containers fantasmas (dead):"
	@docker ps -a --filter "name=h2v" --filter "status=dead" --format "  {{.ID}} {{.Names}}" 2>nul || echo "  Nenhum"
	@echo ""
	@echo "🌐 Redes órfãs:"
	@docker network ls --filter "name=h2v" --format "  {{.ID}} {{.Name}}" 2>nul || echo "  Nenhuma"

dev-deep-clean:
	@echo "🧹 Faxina pesada - ATENCAO: Remove TUDO (inclusive banco)"
	scripts\deep-clean.bat

# --- Fim dos Comandos Docker Seguros ---

build:
	docker compose build

logs:
	docker compose logs -f


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
	@echo "  Removendo __pycache__..."
	@for /d /r . %d in (__pycache__) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo .pytest_cache..."
	@for /d /r . %d in (.pytest_cache) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo .mypy_cache..."
	@for /d /r . %d in (.mypy_cache) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo .coverage..."
	@for /d /r . %d in (.coverage) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo dist..."
	@for /d /r . %d in (dist) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo build..."
	@for /d /r . %d in (build) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo node_modules..."
	@for /d /r . %d in (node_modules) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo .next..."
	@for /d /r . %d in (.next) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo out..."
	@for /d /r . %d in (out) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo cache..."
	@for /d /r . %d in (cache) do @if exist "%d" rmdir /s /q "%d" 2>nul
	@echo "  Removendo artifacts..."
	@for /d /r . %d in (artifacts) do @if exist "%d" rmdir /s /q "%d" 2>nul
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

# --- Ambiente de Produção ---
COMPOSE_PROD = docker compose -f docker-compose.prod.yml --env-file .env.production

prod:
	$(COMPOSE_PROD) up -d

down-prod:
	$(COMPOSE_PROD) down

rebuild-prod:
	$(COMPOSE_PROD) build --no-cache
	$(COMPOSE_PROD) up -d

logs-prod:
	$(COMPOSE_PROD) logs -f

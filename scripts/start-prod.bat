@echo off
echo ============================================
echo  H2V-Trust - Iniciar Ambiente de Producao
echo ============================================
echo.
echo Este script vai parar o ambiente dev (se estiver rodando)
echo e iniciar o ambiente de producao.
echo.
echo Pressione Ctrl+C para cancelar ou qualquer tecla para continuar...
pause >nul

echo.
echo [1/3] Parando ambiente dev (se ativo)...
docker compose -f docker-compose.yml down 2>nul

echo [2/3] Parando ambiente prod anterior (se ativo)...
docker compose -f docker-compose.prod.yml --env-file .env.production down 2>nul

echo [3/3] Iniciando ambiente de producao...
docker compose -f docker-compose.prod.yml --env-file .env.production up -d --build

echo.
echo ============================================
echo  Ambiente de Producao iniciado!
echo.
echo  Frontend: http://localhost
echo  Backend:  http://localhost:8000
echo  Grafana:  http://localhost:3001 (admin/admin)
echo  Prometheus: http://localhost:9090
echo ============================================
echo.
echo Para ver logs: docker compose -f docker-compose.prod.yml logs -f
echo Para parar:    scripts\stop-prod.bat

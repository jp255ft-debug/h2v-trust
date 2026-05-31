@echo off
echo ============================================
echo  H2V-Trust - Parar Ambiente de Producao
echo ============================================
echo.
echo Parando ambiente de producao...
docker compose -f docker-compose.prod.yml --env-file .env.production down

echo.
echo ============================================
echo  Ambiente de Producao parado.
echo ============================================
echo.
echo Para iniciar novamente: scripts\start-prod.bat
echo Para iniciar dev:       docker compose -f docker-compose.yml up -d

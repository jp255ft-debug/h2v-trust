@echo off
:: ============================================================
:: H2V-Trust - Reset de Ambiente Docker (Windows CMD)
:: Versao: 2.4
:: Uso:   reset-docker.bat [--full]
::         --full  Remove tambem volumes persistentes
:: ============================================================

title H2V-Trust Docker Reset
echo ============================================================
echo    H2V-Trust - Reset de Ambiente Docker
echo ============================================================
echo.

:: --- NIVEL 1: Limpeza padrao (containers, redes, orfaos) ---
echo [NIVEL 1] Limpeza padrao...
docker compose down --remove-orphans 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   OK - Servicos parados e orfaos removidos.
) else (
    echo   AVISO - Nao foi possivel parar os servicos.
)

:: --- NIVEL 2: Remocao forcada de containers H2V ---
echo.
echo [NIVEL 2] Removendo containers com nome "h2v"...
for /f "tokens=*" %%i in ('docker ps -a --filter "name=h2v" -q 2^>nul') do (
    echo   Removendo container %%i...
    docker rm -f %%i 2>nul
)
echo   OK - Containers H2V removidos.

:: Limpeza de containers parados
echo.
echo [NIVEL 2] Limpando containers parados...
docker container prune -f 2>nul
echo   OK - Containers parados removidos.

:: --- NIVEL 3: Deteccao de container fantasma (bug #253) ---
echo.
echo [NIVEL 3] Verificando containers fantasmas (bug Docker Desktop #253)...

:: Usa PowerShell para detectar containers fantasmas (mais confiavel que CMD)
powershell -Command ^
    "$containers = docker ps -a --filter 'name=h2v' --filter 'status=created' -q 2>$null; " ^
    "$dead = docker ps -a --filter 'name=h2v' --filter 'status=dead' -q 2>$null; " ^
    "$ghosts = @(); " ^
    "if ($containers) { $ghosts += $containers -split '[\r\n]+' | Where-Object { $_ -ne '' } }; " ^
    "if ($dead) { $ghosts += $dead -split '[\r\n]+' | Where-Object { $_ -ne '' } }; " ^
    "if ($ghosts.Count -gt 0) { " ^
    "    Write-Host '  Removendo containers fantasmas...'; " ^
    "    $removed = $true; " ^
    "    foreach ($id in $ghosts) { " ^
    "        $result = docker rm -f $id 2>&1; " ^
    "        if ($LASTEXITCODE -eq 0) { Write-Host ('    OK - Container ' + $id + ' removido.'); } " ^
    "        else { Write-Host ('    FALHA - Container ' + $id + ' nao pode ser removido.'); $removed = $false; } " ^
    "    }; " ^
    "    if (-not $removed) { exit 1 } " ^
    "} else { Write-Host '  OK - Nenhum container fantasma detectado.' }"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo   Container(es) fantasma(s) detectado(s) e nao puderam ser removidos!
    echo   Este e um bug conhecido do Docker Desktop (#253).
    echo.
    echo   Para resolver:
    echo   1. Feche este terminal.
    echo   2. Abra o PowerShell como Administrador.
    echo   3. Execute: wsl --unregister docker-desktop
    echo   4. Execute: wsl --unregister docker-desktop-data
    echo   5. Reabra o Docker Desktop.
    echo   6. Execute novamente: docker compose up -d --remove-orphans
    echo.
    echo   Ou, se preferir uma solucao mais rapida:
    echo   1. Reinicie o Docker Desktop (icone na bandeja -^> Restart).
    echo   2. Execute novamente: docker compose up -d --remove-orphans
    exit /b 1
)

:: --- Limpeza de redes orfas ---
echo.
echo [LIMPEZA] Removendo redes orfas...
docker network prune -f 2>nul
echo   OK - Redes orfas removidas.

:: --- Opcao --full: Remove volumes persistentes ---
echo.
if "%1"=="--full" (
    echo [OPCAO --full] Removendo volumes persistentes...
    echo   ATENCAO: Os dados do banco de dados serao perdidos!
    echo   Pressione Ctrl+C para cancelar ou qualquer tecla para continuar...
    pause >nul
    docker compose down -v 2>nul
    docker volume prune -f 2>nul
    echo   OK - Volumes removidos.
) else (
    echo [INFO] Volumes persistentes preservados (use --full para remove-los).
)

:: --- Resumo final ---
echo.
echo ============================================================
echo    RESET CONCLUIDO COM SUCESSO!
echo ============================================================
echo.
echo Para iniciar o ambiente novamente:
echo   docker compose up -d --remove-orphans
echo.
echo Para popular o banco de dados:
echo   docker compose exec backend python scripts/seed_data.py
echo.

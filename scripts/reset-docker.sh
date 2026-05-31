#!/bin/bash
# ============================================================
# H2V-Trust - Reset de Ambiente Docker (Bash / Git Bash / WSL)
# Versao: 2.0
# Uso:   ./reset-docker.sh [--full]
#         --full  Remove tambem volumes persistentes
# ============================================================

echo "============================================================"
echo "   H2V-Trust - Reset de Ambiente Docker"
echo "============================================================"
echo ""

# --- NIVEL 1: Limpeza padrao (containers, redes, orfaos) ---
echo "[NIVEL 1] Limpeza padrao..."
if docker compose down --remove-orphans 2>/dev/null; then
    echo "  OK - Servicos parados e orfaos removidos."
else
    echo "  AVISO - Nao foi possivel parar os servicos."
fi

# --- NIVEL 2: Remocao forcada de containers H2V ---
echo ""
echo "[NIVEL 2] Removendo containers com nome \"h2v\"..."
for container in $(docker ps -a --filter "name=h2v" -q 2>/dev/null); do
    echo "  Removendo container $container..."
    docker rm -f "$container" 2>/dev/null
done
echo "  OK - Containers H2V removidos."

# Limpeza de containers parados
echo ""
echo "[NIVEL 2] Limpando containers parados..."
docker container prune -f 2>/dev/null
echo "  OK - Containers parados removidos."

# --- NIVEL 3: Deteccao de container fantasma (bug #253) ---
echo ""
echo "[NIVEL 3] Verificando containers fantasmas (bug Docker Desktop #253)..."
STUCK=0
for container in $(docker ps -a --filter "name=h2v" --filter "status=dead" -q 2>/dev/null); do
    STUCK=$((STUCK + 1))
done

if [ "$STUCK" -gt 0 ]; then
    echo "  $STUCK container(s) fantasma(s) detectado(s)!"
    echo "  Este e um bug conhecido do Docker Desktop."
    echo ""
    echo "  Para resolver:"
    echo "  1. Feche este terminal."
    echo "  2. Abra o PowerShell como Administrador."
    echo "  3. Execute: wsl --unregister docker-desktop"
    echo "  4. Execute: wsl --unregister docker-desktop-data"
    echo "  5. Reabra o Docker Desktop."
    echo "  6. Execute novamente: docker compose up -d --remove-orphans"
    echo ""
    echo "  Ou, se preferir uma solucao mais rapida:"
    echo "  1. Reinicie o Docker Desktop (icone na bandeja -> Restart)."
    echo "  2. Execute novamente: docker compose up -d --remove-orphans"
    exit 1
else
    echo "  OK - Nenhum container fantasma detectado."
fi

# --- Limpeza de redes orfas ---
echo ""
echo "[LIMPEZA] Removendo redes orfas..."
docker network prune -f 2>/dev/null
echo "  OK - Redes orfas removidas."

# --- Opcao --full: Remove volumes persistentes ---
echo ""
if [ "$1" = "--full" ]; then
    echo "[OPCAO --full] Removendo volumes persistentes..."
    echo "  ATENCAO: Os dados do banco de dados serao perdidos!"
    echo "  Pressione Ctrl+C para cancelar ou Enter para continuar..."
    read -r
    docker compose down -v 2>/dev/null
    docker volume prune -f 2>/dev/null
    echo "  OK - Volumes removidos."
else
    echo "[INFO] Volumes persistentes preservados (use --full para remove-los)."
fi

# --- Resumo final ---
echo ""
echo "============================================================"
echo "   RESET CONCLUIDO COM SUCESSO!"
echo "============================================================"
echo ""
echo "Para iniciar o ambiente novamente:"
echo "  docker compose up -d --remove-orphans"
echo ""
echo "Para popular o banco de dados:"
echo "  docker compose exec backend python scripts/seed_data.py"
echo ""

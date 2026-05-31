#!/bin/bash
# ============================================================
# H2V-Trust - Manutencao Semanal do Ambiente Docker
# Versao: 1.0
# Uso:   bash scripts/maintenance-weekly.sh
# ATENCAO: Remove containers, imagens e volumes nao usados.
#          O banco de dados sera perdido.
# Execute toda sexta-feira as 17h.
# ============================================================

echo "============================================================"
echo "   H2V-Trust - Manutencao Semanal"
echo "   $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""

# Navegar para o diretorio do projeto
cd /mnt/c/Source/Repos/h2v-trust || exit 1

echo "[1/4] Parando servicos..."
echo "----------------------------------------------"
docker compose down --remove-orphans 2>/dev/null
echo "  OK"

echo ""
echo "[2/4] Removendo containers orfaos..."
echo "----------------------------------------------"
for container_id in $(docker ps -a --filter "name=h2v" -q 2>/dev/null); do
    docker rm -f "$container_id" 2>/dev/null
done
echo "  OK"

echo ""
echo "[3/4] Faxina pesada do Docker..."
echo "----------------------------------------------"
docker system prune -a --volumes -f
echo "  OK"

echo ""
echo "[4/4] Subindo ambiente do zero..."
echo "----------------------------------------------"
docker compose up -d --remove-orphans
echo "  OK"

echo ""
echo "============================================================"
echo "   MANUTENCAO SEMANAL CONCLUIDA!"
echo "============================================================"
echo ""
echo "⚠️  Lembrete: Reinicie o Windows para liberar recursos do WSL2."
echo ""
echo "Proximo passo:"
echo "  docker compose exec backend python scripts/seed_data.py"
echo ""

#!/bin/bash
# ============================================================
# H2V-Trust - Faxina Pesada contra Containers Fantasmas
# Versao: 1.0
# Uso:   bash scripts/deep-clean.sh
# ATENCAO: Remove TODOS os containers, imagens, volumes e
#          redes nao usados. O banco de dados sera perdido.
# ============================================================

echo "============================================================"
echo "   H2V-Trust - Faxina Pesada (Deep Clean)"
echo "============================================================"
echo ""
echo "⚠️  ATENCAO: Este script remove TODOS os containers,"
echo "   imagens, volumes e redes nao usados."
echo "   O BANCO DE DADOS SERA PERDIDO."
echo ""
echo "   Pressione Ctrl+C para cancelar ou Enter para continuar..."
read -r

echo ""
echo "[1/3] Parando todos os servicos..."
echo "----------------------------------------------"
docker compose down --remove-orphans 2>/dev/null
echo "  OK - Servicos parados."

echo ""
echo "[2/3] Removendo todos os containers H2V..."
echo "----------------------------------------------"
for container_id in $(docker ps -a --filter "name=h2v" -q 2>/dev/null); do
    echo "  Removendo container $container_id..."
    docker rm -f "$container_id" 2>/dev/null
done
echo "  OK - Containers H2V removidos."

echo ""
echo "[3/3] Executando faxina pesada do Docker..."
echo "----------------------------------------------"
echo "  Removendo containers, imagens, volumes e redes nao usados..."
docker system prune -a --volumes -f
echo "  OK - Faxina pesada concluida."

echo ""
echo "============================================================"
echo "   FAXINA CONCLUIDA COM SUCESSO!"
echo "============================================================"
echo ""
echo "⚠️  O ambiente foi completamente limpo, incluindo o banco de dados."
echo ""
echo "Para subir o projeto do zero:"
echo "  docker compose up -d --remove-orphans"
echo ""
echo "Para popular o banco de dados:"
echo "  docker compose exec backend python scripts/seed_data.py"
echo ""

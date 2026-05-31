#!/bin/bash
# =============================================================================
# seed_all.sh — Orquestrador de Seed do H2V-Trust
# =============================================================================
# Executa os scripts de seed na ordem correta:
#   1. seed_users_tenants.py  → Infraestrutura de auth (tenants, users, permissões)
#   2. seed_demo_data.py      → Dados de demonstração (lotes, certificados, etc.)
#
# Uso:
#   bash scripts/seed_all.sh
#   make seed-all            (atalho via Makefile)
# =============================================================================

set -euo pipefail

echo "=========================================="
echo "🌱 H2V-Trust — Seed Completo"
echo "=========================================="
echo ""

# ─── Passo 1: Infraestrutura de Auth ────────────────────────────────────────
echo "[1/2] Criando tenants, usuários e permissões..."
echo "      → backend/scripts/seed_users_tenants.py"
echo ""
docker compose exec backend python scripts/seed_users_tenants.py
echo ""

# ─── Passo 2: Dados de Demonstração ─────────────────────────────────────────
echo "[2/2] Gerando dados de demonstração..."
echo "      → scripts/seed_demo_data.py"
echo ""
docker compose exec backend python scripts/seed_demo_data.py
echo ""

echo "=========================================="
echo "✅ Seed completo executado com sucesso!"
echo "=========================================="
echo ""
echo "Credenciais (todos os utilizadores):"
echo "  Admin:    admin@h2v-trust.com / H2v@Trust!2026"
echo "  Operator: operator@produtor-alfa.com / H2v@Trust!2026"
echo "  Auditor:  auditor@h2v-trust.com / H2v@Trust!2026"
echo ""

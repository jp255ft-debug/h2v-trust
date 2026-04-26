"""
Database initialization script.
Creates all tables and sets up TimescaleDB hypertables if applicable.

Usage:
    python scripts/init_db.py              # Initialize database
    python scripts/init_db.py --reset       # Drop and recreate all tables
"""

import sys
import os
import argparse

# Adicionar o diretório raiz do projeto ao PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from backend.db.database import engine, Base, init_db, is_timescaledb
from backend.db.models import TelemetryRecord, Batch, Certificate, AuditLog, Delegation
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reset_db():
    """Drop all tables and recreate."""
    logger.warning("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    logger.info("All tables dropped.")
    init_db()


def main():
    parser = argparse.ArgumentParser(description="Initialize H2V-Trust database")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate all tables")
    args = parser.parse_args()

    db_type = "TimescaleDB" if is_timescaledb() else "SQLite"
    print(f"\n{'='*50}")
    print(f"  H2V-Trust Database Initialization")
    print(f"  Database type: {db_type}")
    print(f"  Connection: {engine.url}")
    print(f"{'='*50}\n")

    if args.reset:
        confirm = input("WARNING: This will DROP ALL TABLES. Continue? (y/N): ")
        if confirm.lower() == "y":
            reset_db()
        else:
            print("Aborted.")
            return
    else:
        init_db()

    print("\nDatabase initialization complete!\n")


if __name__ == "__main__":
    main()

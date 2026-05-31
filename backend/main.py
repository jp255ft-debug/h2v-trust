import sys
import os
import logging
from contextlib import asynccontextmanager

# Adicionar o diretório atual (/app) ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from api.routes import telemetry, batches, certificates, compliance, delegation, reports, auth, admin
from db.database import engine, Base, init_db
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting H2V-Trust Backend...")
    init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title="H2V-Trust API",
    description="Plataforma de Rastreabilidade Blockchain para Hidrogênio Verde",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(telemetry.router, prefix="/api/v1", tags=["Telemetry"])
app.include_router(batches.router, prefix="/api/v1", tags=["Batches"])
app.include_router(certificates.router, prefix="/api/v1", tags=["Certificates"])
app.include_router(compliance.router, prefix="/api/v1", tags=["Compliance"])
app.include_router(delegation.router, prefix="/api/v1", tags=["Delegation"])
app.include_router(reports.router, prefix="/api/v1", tags=["Reports"])
app.include_router(auth.router)
app.include_router(admin.router)


@app.get("/health")
async def health_check():
    """Health check endpoint that verifies database and blockchain connectivity."""
    import time
    
    health = {
        "status": "ok",
        "service": "H2V-Trust",
        "version": "1.0.0",
        "timestamp": time.time(),
        "checks": {}
    }
    
    # 1. Database check
    db_status = "ok"
    db_details = {}
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            db_details["connected"] = True
            
            # Check if tables exist
            result = conn.execute(
                text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
            )
            table_count = result.scalar()
            db_details["table_count"] = table_count
    except Exception as e:
        db_status = "degraded"
        db_details["error"] = str(e)
        health["status"] = "degraded"
    
    health["checks"]["database"] = {
        "status": db_status,
        "details": db_details
    }
    
    # 2. Blockchain check
    blockchain_status = "ok"
    blockchain_details = {}
    try:
        from blockchain.web3_client import is_connected, get_network_info
        blockchain_details["connected"] = is_connected()
        network_info = get_network_info()
        blockchain_details["chain_id"] = network_info.get("chain_id")
        blockchain_details["block_number"] = network_info.get("block_number")
        blockchain_details["rpc_url"] = network_info.get("rpc_url")
        blockchain_details["mock_mode"] = settings.MOCK_MODE
        
        if not blockchain_details["connected"]:
            blockchain_status = "degraded"
            if health["status"] == "ok":
                health["status"] = "degraded"
    except Exception as e:
        blockchain_status = "degraded"
        blockchain_details["error"] = str(e)
        if health["status"] == "ok":
            health["status"] = "degraded"
    
    health["checks"]["blockchain"] = {
        "status": blockchain_status,
        "details": blockchain_details
    }
    
    # 3. Redis check (if configured)
    redis_status = "ok"
    redis_details = {}
    try:
        import redis as redis_lib
        r = redis_lib.from_url(settings.REDIS_URL, socket_connect_timeout=3)
        r.ping()
        redis_details["connected"] = True
    except Exception as e:
        redis_status = "degraded"
        redis_details["error"] = str(e)
        if health["status"] == "ok":
            health["status"] = "degraded"
    
    health["checks"]["redis"] = {
        "status": redis_status,
        "details": redis_details
    }
    
    return health

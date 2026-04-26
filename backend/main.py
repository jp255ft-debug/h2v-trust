import sys
import os
import logging
from contextlib import asynccontextmanager

# Adicionar o diretório atual (/app) ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import telemetry, batches, certificates, compliance, delegation, reports
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
    allow_origins=settings.CORS_ORIGINS,
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


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "H2V-Trust"}
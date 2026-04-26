from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./h2v_trust.db"
    TIMESCALE_COMPRESSION_INTERVAL: str = "7 days"

    # Blockchain
    POLYGON_RPC_URL: str = "http://localhost:8545"
    PRIVATE_KEY: str = ""  # Deve ser definida no .env
    CONTRACT_ADDRESS: str = ""

    # Chainlink
    CHAINLINK_API_KEY: str = ""
    CHAINLINK_ORACLE_ADDRESS: str = ""

    # CBAM
    CBAM_GHG_LIMIT_TCO2_PER_TH2: float = 3.4
    CBAM_AUTHORIZATION_DEADLINE: str = "2026-03-31"
    CBAM_FIRST_SURRENDER_DATE: str = "2027-09-30"

    # API
    API_KEY_HEADER: str = "X-API-Key"
    API_RATE_LIMIT: int = 1000
    SECRET_KEY: str = ""  # Deve ser definida no .env
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Redis/Celery
    REDIS_URL: str = "redis://localhost:6379"

    # Frontend
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"

    # Mock mode for testing without blockchain
    MOCK_MODE: bool = False

    model_config = SettingsConfigDict(
        # Buscar .env na raiz do projeto
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # Ignorar variáveis extras no .env
    )


settings = Settings()

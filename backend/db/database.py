"""
Database configuration with TimescaleDB support.
Supports both SQLite (development/testing) and PostgreSQL/TimescaleDB (production).

The initialization is resilient: if the database is not available (e.g., TimescaleDB
container not running), it logs a warning and continues without crashing.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
import logging

logger = logging.getLogger(__name__)

# Determine if we're using PostgreSQL/TimescaleDB
_is_timescaledb = "postgresql" in settings.DATABASE_URL or "postgres" in settings.DATABASE_URL

# Create database engine with appropriate configuration
if _is_timescaledb:
    # PostgreSQL/TimescaleDB: use connection pooling for high concurrency
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False,
    )
    logger.info(f"Configured TimescaleDB/PostgreSQL engine: {settings.DATABASE_URL}")
else:
    # SQLite: single connection, WAL mode for better concurrency
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
    
    # Enable WAL mode for SQLite to improve concurrent reads
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
        cursor.close()
    
    logger.info(f"Using SQLite engine: {settings.DATABASE_URL}")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database by creating all tables.
    
    For TimescaleDB, also creates the hypertable for telemetry data
    and enables compression.
    
    This function is resilient: if the database is not reachable,
    it logs a warning and returns gracefully.
    """
    logger.info("Initializing database...")
    
    # Import all models to ensure they are registered with Base
    from db.models import TelemetryRecord, Batch, Certificate, AuditLog, Delegation
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
        
        # If using TimescaleDB, set up hypertable and compression
        if _is_timescaledb:
            _setup_timescaledb()
        
        logger.info("Database initialization complete.")
    except Exception as e:
        logger.warning(f"Database initialization failed (non-fatal): {e}")
        logger.warning("The application will continue, but database features may be unavailable.")
        logger.warning("Make sure the database server is running and accessible.")


def _setup_timescaledb():
    """Set up TimescaleDB-specific features:
    - Create hypertable for telemetry_records
    - Enable compression
    """
    logger.info("Setting up TimescaleDB hypertables...")
    
    try:
        with engine.connect() as conn:
            # Enable TimescaleDB extension if not already enabled
            conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE")
            
            # Check if telemetry_records is already a hypertable
            result = conn.execute(
                "SELECT 1 FROM timescaledb_information.hypertables WHERE table_name = 'telemetry_records'"
            )
            is_hypertable = result.fetchone() is not None
            
            if not is_hypertable:
                # Convert telemetry_records to hypertable partitioned by timestamp
                conn.execute(
                    "SELECT create_hypertable('telemetry_records', 'timestamp', "
                    "chunk_time_interval => INTERVAL '1 day', "
                    "if_not_exists => TRUE)"
                )
                logger.info("Created hypertable for telemetry_records")
            else:
                logger.info("telemetry_records is already a hypertable")
            
            # Enable compression on the hypertable
            conn.execute(
                "ALTER TABLE telemetry_records SET ("
                f"timescaledb.compress, "
                f"timescaledb.compress_segmentby = 'sensor_id', "
                f"timescaledb.compress_orderby = 'timestamp DESC'"
                ")"
            )
            logger.info("Enabled compression on telemetry_records")
            
            # Set compression policy (compress chunks older than 7 days)
            conn.execute(
                "SELECT add_compression_policy('telemetry_records', "
                f"INTERVAL '{settings.TIMESCALE_COMPRESSION_INTERVAL}')"
            )
            logger.info(f"Set compression policy to {settings.TIMESCALE_COMPRESSION_INTERVAL}")
            
            conn.commit()
        
        logger.info("TimescaleDB setup complete.")
    except Exception as e:
        logger.warning(f"TimescaleDB setup failed (non-fatal): {e}")
        logger.warning("The application will continue without TimescaleDB optimizations.")


def is_timescaledb() -> bool:
    """Check if the current database is TimescaleDB."""
    return _is_timescaledb


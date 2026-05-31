"""init_timescaledb

Create TimescaleDB extension and convert telemetry_records to hypertable.

This migration:
1. Enables the TimescaleDB extension (if not already enabled)
2. Converts the telemetry_records table to a hypertable partitioned by timestamp
3. Enables compression on the hypertable

Revision ID: 6fef8df01c1e
Revises: 
Create Date: 2026-04-23 11:49:15.491694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fef8df01c1e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: enable TimescaleDB and create hypertable."""
    # Enable TimescaleDB extension
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
    
    # Convert telemetry_records to hypertable partitioned by timestamp
    # Chunk interval: 1 day for optimal query performance
    op.execute(
        "SELECT create_hypertable('telemetry_records', 'timestamp', "
        "chunk_time_interval => INTERVAL '1 day', "
        "if_not_exists => TRUE);"
    )
    
    # Enable compression on the hypertable
    # Segment by sensor_id for efficient per-sensor queries
    # Order by timestamp DESC for time-range queries
    op.execute(
        "ALTER TABLE telemetry_records SET ("
        "timescaledb.compress, "
        "timescaledb.compress_segmentby = 'sensor_id', "
        "timescaledb.compress_orderby = 'timestamp DESC'"
        ");"
    )
    
    # Set compression policy: compress chunks older than 7 days
    op.execute(
        "SELECT add_compression_policy('telemetry_records', "
        "INTERVAL '7 days', if_not_exists => TRUE);"
    )


def downgrade() -> None:
    """Downgrade schema: remove TimescaleDB features."""
    # Remove compression policy
    op.execute(
        "SELECT remove_compression_policy('telemetry_records', if_exists => TRUE);"
    )
    
    # Convert hypertable back to regular table
    op.execute(
        "SELECT set_chunk_time_interval('telemetry_records', INTERVAL '1 year');"
    )

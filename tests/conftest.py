"""
Pytest configuration and shared fixtures for the H2V-Trust test suite.
"""

import pytest
from typing import Generator, Dict, Any
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_web3_client():
    """Fixture providing a mock Web3 client."""
    with patch("backend.blockchain.web3_client.Web3Client") as mock:
        client = mock.return_value
        client.is_connected.return_value = True
        client.get_balance.return_value = 1000000000000000000  # 1 ETH
        client.mint_certificate.return_value = {
            "tx_hash": "0xabc123",
            "token_id": 1,
        }
        yield client


@pytest.fixture
def mock_db_session():
    """Fixture providing a mock database session."""
    with patch("backend.db.database.SessionLocal") as mock:
        session = MagicMock()
        mock.return_value = session
        yield session


@pytest.fixture
def sample_batch_data() -> Dict[str, Any]:
    """Fixture providing sample batch data for testing."""
    return {
        "id": "test_batch_001",
        "telemetry_id": 1,
        "producer_wallet": "0x1234567890abcdef1234567890abcdef12345678",
        "producer_id": "prod_001",
        "facility_id": "facility_001",
        "production_location": "Namibia",
        "size_kg": 1000.0,
        "is_compliant": True,
    }


@pytest.fixture
def sample_telemetry_data() -> Dict[str, Any]:
    """Fixture providing sample telemetry data for testing."""
    return {
        "sensor_id": "sensor_001",
        "timestamp": "2024-06-15T10:00:00Z",
        "energy_source": "solar",
        "power_generated_mwh": 120.0,
        "ghg_emissions": 2.3,
        "water_consumption_liters": 11.8,
        "water_source": "desalination",
    }


@pytest.fixture
def sample_certificate_data() -> Dict[str, Any]:
    """Fixture providing sample certificate data for testing."""
    return {
        "id": "cert_001",
        "batch_id": "test_batch_001",
        "token_id": 1,
        "blockchain_tx_hash": "0xabc123",
        "is_consumed": False,
    }


@pytest.fixture
def app_client():
    """Fixture providing a test client for the FastAPI application."""
    from backend.main import app
    from fastapi.testclient import TestClient
    
    with TestClient(app) as client:
        yield client

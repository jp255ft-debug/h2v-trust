"""
Health check tests for the H2V-Trust backend.
"""

import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(app_client: TestClient):
    """Test that the /health endpoint returns 200 OK with correct status."""
    response = app_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "checks" in data
    assert "database" in data["checks"]
    assert "redis" in data["checks"]
    assert "blockchain" in data["checks"]


def test_health_database_check(app_client: TestClient):
    """Test that the health endpoint reports database status."""
    response = app_client.get("/health")
    data = response.json()
    assert data["checks"]["database"]["status"] == "ok"


def test_health_redis_check(app_client: TestClient):
    """Test that the health endpoint reports redis status."""
    response = app_client.get("/health")
    data = response.json()
    assert data["checks"]["redis"]["status"] == "ok"


def test_root_endpoint(app_client: TestClient):
    """Test that the root endpoint returns a welcome message."""
    response = app_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

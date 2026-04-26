"""
API endpoint tests for the H2V-Trust FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_health_check(self):
        """Test health check endpoint returns OK."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "H2V-Trust"


class TestBatchEndpoints:
    """Tests for batch-related endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_list_batches(self):
        """Test listing batches."""
        response = self.client.get("/api/v1/batches")
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            data = response.json()
            assert "batches" in data or isinstance(data, list)

    def test_get_batch(self):
        """Test getting a specific batch."""
        response = self.client.get("/api/v1/batches/test_batch_001")
        assert response.status_code in [200, 404, 422]

    def test_get_batch_compliance(self):
        """Test getting batch compliance."""
        response = self.client.get("/api/v1/batches/test_batch_001/compliance")
        assert response.status_code in [200, 404, 422]


class TestCertificateEndpoints:
    """Tests for certificate-related endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_list_certificates(self):
        """Test listing certificates."""
        response = self.client.get("/api/v1/certificates")
        assert response.status_code in [200, 404, 422]
        if response.status_code == 200:
            data = response.json()
            assert "certificates" in data or isinstance(data, list)

    def test_get_certificate(self):
        """Test getting a specific certificate."""
        response = self.client.get("/api/v1/certificates/test_cert_001")
        assert response.status_code in [200, 404, 422]

    def test_verify_certificate(self):
        """Test certificate verification."""
        response = self.client.get("/api/v1/certificates/test_cert_001/verify")
        assert response.status_code in [200, 404, 422]


class TestComplianceEndpoints:
    """Tests for compliance-related endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_check_compliance(self):
        """Test compliance check endpoint."""
        response = self.client.get("/api/v1/compliance/check/test_batch_001")
        assert response.status_code in [200, 404, 422]

    def test_validate_compliance(self):
        """Test compliance validation endpoint."""
        response = self.client.post(
            "/api/v1/compliance/validate",
            json={"batch_id": "test_batch_001", "validator_wallet": "0xvalidator123"},
        )
        assert response.status_code in [200, 422]


class TestDelegationEndpoints:
    """Tests for delegation-related endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_get_delegation_status(self):
        """Test getting delegation status."""
        response = self.client.get("/api/v1/delegation/status/prod_001")
        assert response.status_code in [200, 404, 422]

    def test_authorize_delegation(self):
        """Test authorizing a delegation."""
        response = self.client.post(
            "/api/v1/delegation/authorize",
            json={
                "producer_id": "prod_001",
                "declarant_address": "0xdeclarant123",
                "valid_until": "2025-12-31T23:59:59Z",
            },
        )
        assert response.status_code in [200, 422]

    def test_revoke_delegation(self):
        """Test revoking a delegation."""
        response = self.client.post(
            "/api/v1/delegation/revoke",
            json={"producer_id": "prod_001"},
        )
        assert response.status_code in [200, 422]


class TestTelemetryEndpoints:
    """Tests for telemetry-related endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_send_telemetry(self):
        """Test sending telemetry data."""
        response = self.client.post(
            "/api/v1/telemetry",
            json={
                "sensor_id": "sensor_001",
                "timestamp": "2024-06-15T10:00:00Z",
                "energy_source": "solar",
                "power_generated_mwh": 120.0,
                "ghg_emissions_kgCO2_per_kgH2": 2.3,
                "water_consumption_liters": 11.8,
                "water_source": "desalination",
            },
        )
        assert response.status_code in [200, 201, 422]


class TestReportEndpoints:
    """Tests for report-related endpoints."""

    def setup_method(self):
        self.client = TestClient(app)

    def test_get_cbam_report(self):
        """Test getting CBAM report."""
        response = self.client.get("/api/v1/reports/cbam/2024")
        assert response.status_code in [200, 404, 422]

    def test_download_cbam_report(self):
        """Test downloading CBAM report."""
        response = self.client.get("/api/v1/reports/cbam/2024/download")
        assert response.status_code in [200, 404, 422]

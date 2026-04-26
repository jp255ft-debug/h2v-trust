"""
Tests for CBAM delegation management.
"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from backend.core.delegation import DelegationManager


class TestDelegationService:
    """Tests for DelegationManager."""

    def setup_method(self):
        self.manager = DelegationManager()

    def test_create_delegation(self):
        """Test creating a new delegation."""
        delegation = self.manager.create_delegation(
            producer_id="prod_001",
            declarant_address="0xdeclarant1234567890abcdef1234567890abcdef",
        )
        assert delegation is not None
        assert delegation["producer_id"] == "prod_001"
        assert delegation["is_active"] is True

    def test_get_delegation_status(self):
        """Test getting delegation status via validation."""
        delegation = self.manager.create_delegation(
            producer_id="prod_001",
            declarant_address="0xdeclarant123",
        )
        validation = self.manager.validate_delegation(delegation)
        assert validation is not None
        assert validation["is_active"] is True

    def test_revoke_delegation(self):
        """Test revoking a delegation."""
        delegation = self.manager.create_delegation(
            producer_id="prod_001",
            declarant_address="0xdeclarant123",
        )
        revoked = self.manager.revoke_delegation(delegation)
        assert revoked is not None
        assert revoked["is_active"] is False
        assert revoked["revoked_at"] is not None

    def test_revoke_nonexistent_delegation(self):
        """Test revoking a non-existent delegation (should still work on dict)."""
        delegation = {
            "delegation_id": "nonexistent",
            "producer_id": "prod_001",
            "declarant_address": "0xdeclarant123",
            "is_active": True,
        }
        revoked = self.manager.revoke_delegation(delegation)
        assert revoked is not None
        assert revoked["is_active"] is False

    def test_delegation_expiry_check(self):
        """Test checking if delegation is expired."""
        delegation = self.manager.create_delegation(
            producer_id="prod_001",
            declarant_address="0xdeclarant123",
            valid_days=365,
        )
        validation = self.manager.validate_delegation(delegation)
        assert validation is not None
        assert "is_expired" in validation
        assert validation["is_expired"] is False  # Should not be expired yet

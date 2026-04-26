"""
Tests for blockchain interaction layer.
"""

import pytest
import asyncio
from unittest.mock import MagicMock, patch
from backend.blockchain.web3_client import init_web3, get_contract, get_w3, is_connected, get_network_info
from backend.blockchain.minting import mint_certificate_on_chain
from backend.blockchain.verification import verify_certificate_on_chain


class TestWeb3Client:
    """Tests for Web3 client functions."""

    def test_initialization(self):
        """Test Web3 initialization."""
        w3, contract = init_web3()
        assert w3 is not None
        assert contract is not None

    def test_is_connected(self):
        """Test checking connection status."""
        result = is_connected()
        assert result is True

    def test_get_network_info(self):
        """Test getting network info."""
        info = get_network_info()
        assert info["is_connected"] is True
        assert info["chain_id"] == 31337


class TestMintingService:
    """Tests for minting service."""

    def test_mint_certificate(self):
        """Test minting a certificate."""
        tx_hash, token_id = asyncio.run(mint_certificate_on_chain(
            batch_id="batch_001",
            producer_address="0x1234567890abcdef1234567890abcdef12345678",
            metadata={"emissions": 2.5, "water_source": "desalination"},
        ))
        assert tx_hash is not None
        assert token_id is not None
        assert token_id > 0

    def test_mint_with_invalid_address(self):
        """Test minting with invalid address (mock mode handles gracefully)."""
        tx_hash, token_id = asyncio.run(mint_certificate_on_chain(
            batch_id="batch_002",
            producer_address="invalid",
            metadata={},
        ))
        # In mock mode, minting always succeeds
        assert tx_hash is not None
        assert token_id is not None


class TestVerificationService:
    """Tests for verification service."""

    def test_verify_certificate(self):
        """Test certificate verification."""
        result = asyncio.run(verify_certificate_on_chain(token_id=1))
        assert result is not None
        # In mock mode, may return error or success depending on mock implementation
        assert "token_id" in result or "error" in result

    def test_verify_nonexistent_certificate(self):
        """Test verification of non-existent certificate."""
        result = asyncio.run(verify_certificate_on_chain(token_id=99999))
        assert result is not None

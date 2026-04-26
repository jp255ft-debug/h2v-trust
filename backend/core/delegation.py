"""Delegation management for CBAM compliance reporting."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
import hashlib
import json

logger = logging.getLogger(__name__)


class DelegationManager:
    """Manages delegation of CBAM reporting responsibilities."""

    @staticmethod
    def create_delegation(
        producer_id: str,
        declarant_address: str,
        valid_days: int = 365,
        scope: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new delegation record.
        
        Args:
            producer_id: ID of the hydrogen producer
            declarant_address: Ethereum address of the declarant
            valid_days: Delegation validity period in days
            scope: Optional list of delegated responsibilities
            
        Returns:
            Delegation record
        """
        if scope is None:
            scope = ["cbam_reporting", "certificate_minting", "compliance_verification"]
        
        delegation_id = DelegationManager.generate_delegation_id(producer_id, declarant_address)
        created_at = datetime.utcnow()
        valid_until = created_at + timedelta(days=valid_days)
        
        delegation = {
            "delegation_id": delegation_id,
            "producer_id": producer_id,
            "declarant_address": declarant_address.lower(),  # Normalize address
            "created_at": created_at.isoformat(),
            "valid_until": valid_until.isoformat(),
            "scope": scope,
            "is_active": True,
            "revoked_at": None,
            "revocation_reason": None,
            "metadata": {
                "version": "1.0",
                "standard": "H2V-Trust Delegation",
                "purpose": "CBAM compliance reporting delegation",
            },
        }
        
        # Generate authorization hash for blockchain
        delegation["authorization_hash"] = DelegationManager.generate_authorization_hash(
            delegation
        )
        
        return delegation

    @staticmethod
    def generate_delegation_id(producer_id: str, declarant_address: str) -> str:
        """
        Generate a unique delegation ID.
        
        Args:
            producer_id: ID of the producer
            declarant_address: Address of the declarant
            
        Returns:
            Unique delegation ID
        """
        timestamp = datetime.utcnow().isoformat()
        hash_input = f"{producer_id}:{declarant_address}:{timestamp}"
        hash_value = hashlib.sha256(hash_input.encode()).hexdigest()[:32]
        return f"deleg_{hash_value}"

    @staticmethod
    def generate_authorization_hash(delegation: Dict[str, Any]) -> str:
        """
        Generate authorization hash for blockchain verification.
        
        Args:
            delegation: Delegation record
            
        Returns:
            SHA-256 hash of authorization data
        """
        auth_data = {
            "delegation_id": delegation["delegation_id"],
            "producer_id": delegation["producer_id"],
            "declarant_address": delegation["declarant_address"],
            "valid_until": delegation["valid_until"],
            "scope": delegation["scope"],
        }
        
        auth_string = json.dumps(auth_data, sort_keys=True)
        return hashlib.sha256(auth_string.encode()).hexdigest()

    @staticmethod
    def validate_delegation(
        delegation: Dict[str, Any],
        producer_id: Optional[str] = None,
        declarant_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Validate delegation record and check authorization.
        
        Args:
            delegation: Delegation record to validate
            producer_id: Expected producer ID (optional)
            declarant_address: Expected declarant address (optional)
            
        Returns:
            Validation results
        """
        validation = {
            "is_valid": True,
            "is_active": True,
            "is_expired": False,
            "errors": [],
            "warnings": [],
            "checks": {},
        }
        
        # Check required fields
        required_fields = [
            "delegation_id", "producer_id", "declarant_address",
            "created_at", "valid_until", "scope", "is_active"
        ]
        
        for field in required_fields:
            if field not in delegation:
                validation["is_valid"] = False
                validation["errors"].append(f"Missing required field: {field}")
        
        # Check expiration
        if "valid_until" in delegation:
            try:
                valid_until = datetime.fromisoformat(delegation["valid_until"].replace("Z", "+00:00"))
                is_expired = datetime.utcnow() > valid_until
                validation["is_expired"] = is_expired
                validation["checks"]["is_expired"] = is_expired
                
                if is_expired:
                    validation["warnings"].append("Delegation has expired")
                    validation["is_active"] = False
            except (ValueError, TypeError):
                validation["is_valid"] = False
                validation["errors"].append("Invalid date format for valid_until")
        
        # Check if revoked
        is_revoked = delegation.get("revoked_at") is not None
        validation["checks"]["is_revoked"] = is_revoked
        
        if is_revoked:
            validation["is_active"] = False
            validation["warnings"].append("Delegation has been revoked")
        
        # Check active status
        is_active = delegation.get("is_active", False)
        validation["checks"]["is_active"] = is_active
        
        if not is_active:
            validation["is_active"] = False
            validation["warnings"].append("Delegation is not active")
        
        # Verify producer ID if provided
        if producer_id and delegation.get("producer_id") != producer_id:
            validation["warnings"].append(
                f"Producer ID mismatch: expected={producer_id}, got={delegation.get('producer_id')}"
            )
        
        # Verify declarant address if provided
        if declarant_address and delegation.get("declarant_address") != declarant_address.lower():
            validation["warnings"].append(
                f"Declarant address mismatch: expected={declarant_address.lower()}, "
                f"got={delegation.get('declarant_address')}"
            )
        
        # Verify authorization hash
        if "authorization_hash" in delegation:
            expected_hash = DelegationManager.generate_authorization_hash(delegation)
            hash_matches = delegation["authorization_hash"] == expected_hash
            validation["checks"]["hash_matches"] = hash_matches
            
            if not hash_matches:
                validation["is_valid"] = False
                validation["errors"].append("Authorization hash mismatch - possible tampering")
        
        # Overall validity
        validation["is_valid"] = (
            validation["is_valid"] and
            not validation["is_expired"] and
            validation["is_active"] and
            not is_revoked
        )
        
        return validation

    @staticmethod
    def check_authorization(
        delegation: Dict[str, Any],
        action: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bool, str]:
        """
        Check if delegation authorizes a specific action.
        
        Args:
            delegation: Delegation record
            action: Action to check authorization for
            context: Additional context for authorization check
            
        Returns:
            Tuple of (is_authorized, message)
        """
        # First validate the delegation
        validation = DelegationManager.validate_delegation(delegation)
        
        if not validation["is_valid"]:
            return False, "Delegation is not valid"
        
        if not validation["is_active"]:
            return False, "Delegation is not active"
        
        # Check if action is in scope
        scope = delegation.get("scope", [])
        
        if action not in scope:
            return False, f"Action '{action}' not in delegation scope: {scope}"
        
        # Additional context-based checks
        if context:
            # Check if producer matches context
            context_producer = context.get("producer_id")
            if context_producer and context_producer != delegation["producer_id"]:
                return False, f"Producer mismatch: delegation for {delegation['producer_id']}, context has {context_producer}"
            
            # Check if declarant matches context
            context_declarant = context.get("declarant_address")
            if context_declarant and context_declarant.lower() != delegation["declarant_address"]:
                return False, f"Declarant mismatch: delegation for {delegation['declarant_address']}, context has {context_declarant}"
        
        return True, f"Action '{action}' authorized by delegation {delegation['delegation_id']}"

    @staticmethod
    def revoke_delegation(
        delegation: Dict[str, Any],
        reason: str = "Manual revocation",
        revoked_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Revoke a delegation.
        
        Args:
            delegation: Delegation record to revoke
            reason: Reason for revocation
            revoked_by: Who revoked the delegation
            
        Returns:
            Updated delegation record
        """
        updated_delegation = delegation.copy()
        updated_delegation["is_active"] = False
        updated_delegation["revoked_at"] = datetime.utcnow().isoformat()
        updated_delegation["revocation_reason"] = reason
        
        if revoked_by:
            updated_delegation["revoked_by"] = revoked_by
        
        logger.info(
            f"Delegation {delegation['delegation_id']} revoked by {revoked_by or 'unknown'}: {reason}"
        )
        
        return updated_delegation

    @staticmethod
    def generate_delegation_proof(
        delegation: Dict[str, Any],
        batch_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate proof of delegation for blockchain or verification.
        
        Args:
            delegation: Delegation record
            batch_id: Optional batch ID for context
            
        Returns:
            Delegation proof
        """
        proof = {
            "delegation_id": delegation["delegation_id"],
            "producer_id": delegation["producer_id"],
            "declarant_address": delegation["declarant_address"],
            "valid_until": delegation["valid_until"],
            "scope": delegation["scope"],
            "authorization_hash": delegation.get("authorization_hash"),
            "validation_timestamp": datetime.utcnow().isoformat(),
            "batch_id": batch_id,
            "proof_type": "delegation_authorization",
        }
        
        # Add validation results
        validation = DelegationManager.validate_delegation(delegation)
        proof["validation"] = {
            "is_valid": validation["is_valid"],
            "is_active": validation["is_active"],
            "is_expired": validation["is_expired"],
        }
        
        return proof


def create_delegation_request(
    producer_address: str,
    declarant_address: str,
    scope: List[str],
    valid_days: int = 365,
) -> Dict[str, Any]:
    """
    Create a delegation request for CBAM reporting.
    
    Args:
        producer_address: Ethereum address of the producer
        declarant_address: Ethereum address of the declarant
        scope: List of delegated responsibilities
        valid_days: Delegation validity period in days
        
    Returns:
        Delegation request dictionary
    """
    manager = DelegationManager()
    
    # Create delegation
    delegation = manager.create_delegation(
        producer_id=producer_address,
        declarant_address=declarant_address,
        valid_days=valid_days,
        scope=scope,
    )
    
    # Add request-specific fields
    delegation["request_hash"] = hashlib.sha256(
        json.dumps(delegation, sort_keys=True).encode()
    ).hexdigest()
    
    delegation["timestamp"] = datetime.utcnow().isoformat()
    
    return delegation

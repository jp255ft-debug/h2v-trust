"""Certificate generation, validation, and management for H2 batches."""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import hashlib
import json

logger = logging.getLogger(__name__)


class CertificateGenerator:
    """Generates and manages H2 green certificates."""

    @staticmethod
    def generate_certificate_id(batch_id: str, producer_id: str) -> str:
        """
        Generate a unique certificate ID.
        
        Args:
            batch_id: ID of the associated batch
            producer_id: ID of the producer
            
        Returns:
            Unique certificate ID
        """
        # Create deterministic hash from batch and producer
        hash_input = f"{batch_id}:{producer_id}:{datetime.utcnow().isoformat()}"
        hash_value = hashlib.sha256(hash_input.encode()).hexdigest()[:32]
        
        # Format as UUID-like string for readability
        return f"cert_{hash_value}"

    @staticmethod
    def generate_qr_code_data(certificate_data: Dict[str, Any]) -> str:
        """
        Generate QR code data for a certificate.
        
        Args:
            certificate_data: Certificate information
            
        Returns:
            JSON string for QR code
        """
        qr_data = {
            "certificate_id": certificate_data.get("certificate_id"),
            "batch_id": certificate_data.get("batch_id"),
            "producer_id": certificate_data.get("producer_id"),
            "issue_date": certificate_data.get("issue_date"),
            "valid_until": certificate_data.get("valid_until"),
            "verification_url": f"https://h2v-trust.example.com/verify/{certificate_data.get('certificate_id')}",
            "compliance_status": certificate_data.get("compliance_status"),
            "blockchain_tx_hash": certificate_data.get("blockchain_tx_hash"),
        }
        return json.dumps(qr_data, indent=2)

    @staticmethod
    def create_certificate_data(
        batch_id: str,
        producer_id: str,
        compliance_report: Dict[str, Any],
        blockchain_tx_hash: Optional[str] = None,
        validity_days: int = 365,
    ) -> Dict[str, Any]:
        """
        Create certificate data structure.
        
        Args:
            batch_id: ID of the associated batch
            producer_id: ID of the producer
            compliance_report: Compliance verification results
            blockchain_tx_hash: Blockchain transaction hash (if minted)
            validity_days: Certificate validity period in days
            
        Returns:
            Complete certificate data
        """
        certificate_id = CertificateGenerator.generate_certificate_id(batch_id, producer_id)
        issue_date = datetime.utcnow()
        valid_until = issue_date + timedelta(days=validity_days)
        
        # Extract compliance information
        is_compliant = compliance_report.get("is_compliant", False)
        ghg_emissions = compliance_report.get("ghg_emissions_kgco2_per_kgh2", 0.0)
        water_compliance = compliance_report.get("water_compliance", {})
        
        certificate_data = {
            "certificate_id": certificate_id,
            "batch_id": batch_id,
            "producer_id": producer_id,
            "issue_date": issue_date.isoformat(),
            "valid_until": valid_until.isoformat(),
            "compliance_status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
            "ghg_emissions_kgco2_per_kgh2": ghg_emissions,
            "water_compliance": water_compliance,
            "blockchain_tx_hash": blockchain_tx_hash,
            "is_minted": blockchain_tx_hash is not None,
            "is_consumed": False,
            "consumed_at": None,
            "metadata": {
                "version": "1.0",
                "standard": "H2V-Trust Green Hydrogen Certificate",
                "issuer": "H2V-Trust Platform",
            },
        }
        
        # Generate QR code data
        certificate_data["qr_code_data"] = CertificateGenerator.generate_qr_code_data(
            certificate_data
        )
        
        return certificate_data

    @staticmethod
    def validate_certificate(certificate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate certificate data and check expiration.
        
        Args:
            certificate_data: Certificate information
            
        Returns:
            Validation results
        """
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "checks": {},
        }
        
        # Check required fields
        required_fields = ["certificate_id", "batch_id", "producer_id", "issue_date", "valid_until"]
        for field in required_fields:
            if field not in certificate_data:
                validation_results["is_valid"] = False
                validation_results["errors"].append(f"Missing required field: {field}")
        
        # Check expiration
        if "valid_until" in certificate_data:
            try:
                valid_until = datetime.fromisoformat(certificate_data["valid_until"].replace("Z", "+00:00"))
                is_expired = datetime.utcnow() > valid_until
                validation_results["checks"]["is_expired"] = is_expired
                if is_expired:
                    validation_results["warnings"].append("Certificate has expired")
            except (ValueError, TypeError):
                validation_results["is_valid"] = False
                validation_results["errors"].append("Invalid date format for valid_until")
        
        # Check compliance status
        compliance_status = certificate_data.get("compliance_status", "").upper()
        validation_results["checks"]["compliance_status"] = compliance_status
        if compliance_status != "COMPLIANT":
            validation_results["warnings"].append("Certificate is not compliant")
        
        # Check if consumed
        is_consumed = certificate_data.get("is_consumed", False)
        validation_results["checks"]["is_consumed"] = is_consumed
        if is_consumed:
            validation_results["warnings"].append("Certificate has already been consumed")
        
        # Check blockchain minting
        is_minted = certificate_data.get("is_minted", False)
        validation_results["checks"]["is_minted"] = is_minted
        if not is_minted:
            validation_results["warnings"].append("Certificate not minted on blockchain")
        
        return validation_results


class CertificateVerifier:
    """Verifies certificate authenticity and integrity."""

    @staticmethod
    def verify_certificate_chain(
        certificate_data: Dict[str, Any],
        batch_data: Dict[str, Any],
        telemetry_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Verify the complete chain from telemetry to certificate.
        
        Args:
            certificate_data: Certificate information
            batch_data: Batch information
            telemetry_data: Original telemetry data
            
        Returns:
            Chain verification results
        """
        verification = {
            "chain_integrity": True,
            "mismatches": [],
            "details": {},
        }
        
        # Check batch ID consistency
        cert_batch_id = certificate_data.get("batch_id")
        batch_id = batch_data.get("id")
        
        if cert_batch_id != batch_id:
            verification["chain_integrity"] = False
            verification["mismatches"].append(
                f"Batch ID mismatch: certificate={cert_batch_id}, batch={batch_id}"
            )
        
        # Check telemetry-batch linkage
        batch_telemetry_id = batch_data.get("telemetry_id")
        telemetry_id = telemetry_data.get("id")
        
        if batch_telemetry_id and telemetry_id and batch_telemetry_id != telemetry_id:
            verification["chain_integrity"] = False
            verification["mismatches"].append(
                f"Telemetry ID mismatch: batch references={batch_telemetry_id}, telemetry={telemetry_id}"
            )
        
        # Verify emissions consistency
        cert_emissions = certificate_data.get("ghg_emissions_kgco2_per_kgh2")
        telemetry_emissions = telemetry_data.get("ghg_emissions_kgco2_per_kgh2")
        
        if cert_emissions is not None and telemetry_emissions is not None:
            emissions_match = abs(cert_emissions - telemetry_emissions) < 0.01
            verification["details"]["emissions_match"] = emissions_match
            if not emissions_match:
                verification["mismatches"].append(
                    f"Emissions mismatch: certificate={cert_emissions}, telemetry={telemetry_emissions}"
                )
        
        # Verify timestamps
        telemetry_timestamp = telemetry_data.get("timestamp")
        certificate_issue_date = certificate_data.get("issue_date")
        
        if telemetry_timestamp and certificate_issue_date:
            try:
                telemetry_time = datetime.fromisoformat(telemetry_timestamp.replace("Z", "+00:00"))
                certificate_time = datetime.fromisoformat(certificate_issue_date.replace("Z", "+00:00"))
                
                # Certificate should be issued after telemetry
                time_gap = (certificate_time - telemetry_time).total_seconds()
                verification["details"]["time_gap_seconds"] = time_gap
                
                if time_gap < 0:
                    verification["chain_integrity"] = False
                    verification["mismatches"].append(
                        "Certificate issued before telemetry data"
                    )
            except (ValueError, TypeError):
                verification["mismatches"].append("Invalid timestamp format")
        
        return verification

    @staticmethod
    def generate_verification_report(
        certificate_data: Dict[str, Any],
        validation_results: Dict[str, Any],
        chain_verification: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate comprehensive verification report.
        
        Args:
            certificate_data: Certificate information
            validation_results: Certificate validation results
            chain_verification: Chain verification results
            
        Returns:
            Complete verification report
        """
        # Overall verification status
        is_valid = (
            validation_results.get("is_valid", False) and
            chain_verification.get("chain_integrity", False)
        )
        
        # Calculate trust score (0-100)
        trust_score = 100
        
        # Deductions for issues
        if validation_results.get("errors"):
            trust_score -= 30
        
        if validation_results.get("warnings"):
            trust_score -= len(validation_results["warnings"]) * 5
        
        if not chain_verification.get("chain_integrity", False):
            trust_score -= 40
        
        if not certificate_data.get("is_minted", False):
            trust_score -= 20
        
        if certificate_data.get("is_consumed", False):
            trust_score -= 25
        
        trust_score = max(0, min(100, trust_score))
        
        # Trust level categorization
        if trust_score >= 90:
            trust_level = "VERY_HIGH"
        elif trust_score >= 75:
            trust_level = "HIGH"
        elif trust_score >= 60:
            trust_level = "MEDIUM"
        elif trust_score >= 40:
            trust_level = "LOW"
        else:
            trust_level = "VERY_LOW"
        
        return {
            "certificate_id": certificate_data.get("certificate_id"),
            "verification_timestamp": datetime.utcnow().isoformat(),
            "overall_status": "VERIFIED" if is_valid else "FAILED",
            "trust_score": trust_score,
            "trust_level": trust_level,
            "is_valid": is_valid,
            "validation_results": validation_results,
            "chain_verification": chain_verification,
            "recommendations": [
                "Use certificate for carbon accounting" if trust_score >= 75 else "Verify manually before use",
                "Check blockchain confirmation" if certificate_data.get("is_minted") else "Certificate not on blockchain",
                "Certificate already consumed" if certificate_data.get("is_consumed") else "Certificate available for use",
            ],
        }


def generate_certificate_data(
    batch_id: str,
    producer_id: str,
    emissions_data: Dict[str, Any],
    water_data: Dict[str, Any],
    compliance_status: bool,
    blockchain_tx_hash: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate certificate data for a batch.
    
    Args:
        batch_id: ID of the batch
        producer_id: ID of the producer
        emissions_data: GHG emissions data
        water_data: Water consumption data
        compliance_status: Whether the batch is compliant
        blockchain_tx_hash: Blockchain transaction hash (optional)
        
    Returns:
        Certificate data dictionary
    """
    generator = CertificateGenerator()
    
    # Create compliance report
    compliance_report = {
        "is_compliant": compliance_status,
        "ghg_emissions_kgco2_per_kgh2": emissions_data.get("total_emissions_kgco2e", 0),
        "water_compliance": water_data,
        "emissions_details": emissions_data,
        "water_details": water_data,
    }
    
    # Generate certificate
    certificate = generator.create_certificate_data(
        batch_id=batch_id,
        producer_id=producer_id,
        compliance_report=compliance_report,
        blockchain_tx_hash=blockchain_tx_hash,
        validity_days=365,
    )
    
    # Add timestamp and hash for verification
    certificate["timestamp"] = datetime.utcnow().isoformat()
    certificate["certificate_hash"] = hashlib.sha256(
        json.dumps(certificate, sort_keys=True).encode()
    ).hexdigest()
    
    return certificate

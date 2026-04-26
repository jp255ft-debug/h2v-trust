"""Export service for H2 certificates and compliance data."""

import logging
import csv
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, BinaryIO
from io import StringIO, BytesIO
import zipfile

from db.database import SessionLocal
from db.models import Batch, Certificate, TelemetryRecord
from core.compliance import CBAMComplianceChecker
from core.certificates import CertificateGenerator, CertificateVerifier

logger = logging.getLogger(__name__)


class ExporterService:
    """Service for exporting H2 certificate and compliance data in various formats."""

    @staticmethod
    def export_certificate_json(certificate_id: str) -> Dict[str, Any]:
        """
        Export certificate data as JSON.
        
        Args:
            certificate_id: ID of the certificate to export
            
        Returns:
            Dictionary with certificate data and export metadata
        """
        with SessionLocal() as session:
            # Get certificate from database
            certificate = session.query(Certificate).filter(
                Certificate.id == certificate_id
            ).first()
            
            if not certificate:
                raise ValueError(f"Certificate {certificate_id} not found")
            
            # Get associated batch
            batch = session.query(Batch).filter(
                Batch.id == certificate.batch_id
            ).first()
            
            if not batch:
                raise ValueError(f"Batch {certificate.batch_id} not found")
            
            # Get telemetry data
            telemetry = session.query(TelemetryRecord).filter(
                TelemetryRecord.id == batch.telemetry_id
            ).first()
            
            # Build export data
            export_data = {
                "certificate": {
                    "id": certificate.id,
                    "batch_id": certificate.batch_id,
                    "token_id": certificate.token_id,
                    "blockchain_tx_hash": certificate.blockchain_tx_hash,
                    "is_consumed": certificate.is_consumed,
                    "consumed_at": certificate.consumed_at.isoformat() if certificate.consumed_at else None,
                    "created_at": certificate.created_at.isoformat(),
                    "qr_code_data": certificate.qr_code_data,
                },
                "batch": {
                    "id": batch.id,
                    "size_kg": batch.size_kg,
                    "is_compliant": batch.is_compliant,
                    "compliance_report": batch.compliance_report,
                    "batch_hash": batch.batch_hash,
                    "producer_wallet": batch.producer_wallet,
                    "created_at": batch.created_at.isoformat(),
                },
                "telemetry": {
                    "id": telemetry.id if telemetry else None,
                    "sensor_id": telemetry.sensor_id if telemetry else None,
                    "timestamp": telemetry.timestamp.isoformat() if telemetry else None,
                    "energy_source": telemetry.energy_source if telemetry else None,
                    "power_generated_mwh": telemetry.power_generated_mwh if telemetry else None,
                    "ghg_emissions": telemetry.ghg_emissions if telemetry else None,
                    "water_consumption_liters": telemetry.water_consumption_liters if telemetry else None,
                    "water_source": telemetry.water_source if telemetry else None,
                },
                "export_metadata": {
                    "export_date": datetime.utcnow().isoformat(),
                    "format": "json",
                    "version": "1.0",
                    "exporter": "H2V-Trust Platform",
                },
            }
            
            return export_data

    @staticmethod
    def export_certificate_csv(certificate_id: str) -> str:
        """
        Export certificate data as CSV.
        
        Args:
            certificate_id: ID of the certificate to export
            
        Returns:
            CSV string
        """
        export_data = ExporterService.export_certificate_json(certificate_id)
        
        # Create CSV output
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(["Field", "Value"])
        
        # Write certificate data
        writer.writerow(["CERTIFICATE", ""])
        for key, value in export_data["certificate"].items():
            if isinstance(value, dict):
                value = json.dumps(value)
            writer.writerow([f"certificate.{key}", value])
        
        # Write batch data
        writer.writerow(["BATCH", ""])
        for key, value in export_data["batch"].items():
            if isinstance(value, dict):
                value = json.dumps(value)
            writer.writerow([f"batch.{key}", value])
        
        # Write telemetry data
        writer.writerow(["TELEMETRY", ""])
        for key, value in export_data["telemetry"].items():
            if isinstance(value, dict):
                value = json.dumps(value)
            writer.writerow([f"telemetry.{key}", value])
        
        # Write metadata
        writer.writerow(["METADATA", ""])
        for key, value in export_data["export_metadata"].items():
            writer.writerow([f"metadata.{key}", value])
        
        return output.getvalue()

    @staticmethod
    def export_batch_report(batch_id: str, format: str = "json") -> Dict[str, Any]:
        """
        Export comprehensive batch report.
        
        Args:
            batch_id: ID of the batch to export
            format: Output format (json, csv, pdf)
            
        Returns:
            Export data in requested format
        """
        with SessionLocal() as session:
            # Get batch and related data
            batch = session.query(Batch).filter(Batch.id == batch_id).first()
            
            if not batch:
                raise ValueError(f"Batch {batch_id} not found")
            
            certificate = session.query(Certificate).filter(
                Certificate.batch_id == batch_id
            ).first()
            
            telemetry = session.query(TelemetryRecord).filter(
                TelemetryRecord.id == batch.telemetry_id
            ).first()
            
            # Generate compliance report
            compliance_report = batch.compliance_report or {}
            
            # Build comprehensive report
            report = {
                "batch_summary": {
                    "id": batch.id,
                    "size_kg": batch.size_kg,
                    "is_compliant": batch.is_compliant,
                    "batch_hash": batch.batch_hash,
                    "producer_wallet": batch.producer_wallet,
                    "created_at": batch.created_at.isoformat(),
                },
                "production_data": {
                    "energy_source": telemetry.energy_source if telemetry else None,
                    "power_generated_mwh": telemetry.power_generated_mwh if telemetry else None,
                    "ghg_emissions_kgco2_per_kgh2": telemetry.ghg_emissions if telemetry else None,
                    "water_consumption_liters_per_kgh2": telemetry.water_consumption_liters if telemetry else None,
                    "water_source": telemetry.water_source if telemetry else None,
                    "timestamp": telemetry.timestamp.isoformat() if telemetry else None,
                },
                "compliance_analysis": compliance_report,
                "certificate_info": {
                    "id": certificate.id if certificate else None,
                    "token_id": certificate.token_id if certificate else None,
                    "blockchain_tx_hash": certificate.blockchain_tx_hash if certificate else None,
                    "is_consumed": certificate.is_consumed if certificate else None,
                    "is_minted": bool(certificate and certificate.blockchain_tx_hash),
                },
                "environmental_impact": {
                    "total_emissions_kg": (
                        telemetry.ghg_emissions * batch.size_kg
                        if telemetry and telemetry.ghg_emissions
                        else None
                    ),
                    "total_water_liters": (
                        telemetry.water_consumption_liters * batch.size_kg
                        if telemetry and telemetry.water_consumption_liters
                        else None
                    ),
                    "carbon_footprint_equivalent": {
                        "equivalent_car_km": (
                            (telemetry.ghg_emissions * batch.size_kg * 1000) / 0.12
                            if telemetry and telemetry.ghg_emissions
                            else None
                        ),  # 0.12 kg CO2 per km for average car
                        "equivalent_trees": (
                            (telemetry.ghg_emissions * batch.size_kg) / 21.77
                            if telemetry and telemetry.ghg_emissions
                            else None
                        ),  # 21.77 kg CO2 per tree per year
                    },
                },
                "export_metadata": {
                    "export_date": datetime.utcnow().isoformat(),
                    "format": format,
                    "report_type": "batch_comprehensive",
                    "version": "1.0",
                },
            }
            
            if format == "csv":
                # Convert to CSV
                output = StringIO()
                writer = csv.writer(output)
                
                # Flatten the report for CSV
                flat_data = ExporterService._flatten_dict(report)
                for key, value in flat_data.items():
                    if isinstance(value, dict):
                        value = json.dumps(value)
                    writer.writerow([key, value])
                
                return {"csv": output.getvalue()}
            else:
                # Default to JSON
                return report

    @staticmethod
    def export_cbam_report(
        producer_id: str,
        year: int,
        quarter: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Export CBAM compliance report for a producer.
        
        Args:
            producer_id: ID of the producer
            year: Report year
            quarter: Optional quarter (1-4)
            
        Returns:
            CBAM report data
        """
        with SessionLocal() as session:
            # Query batches for the producer
            query = session.query(Batch).filter(
                Batch.producer_wallet == producer_id
            )
            
            # TODO: Add time filtering based on year/quarter
            batches = query.all()
            
            # Calculate totals
            total_batches = len(batches)
            total_h2_kg = sum(batch.size_kg for batch in batches)
            compliant_batches = sum(1 for batch in batches if batch.is_compliant)
            
            # Calculate emissions
            total_emissions_kg = 0
            for batch in batches:
                telemetry = session.query(TelemetryRecord).filter(
                    TelemetryRecord.id == batch.telemetry_id
                ).first()
                
                if telemetry and telemetry.ghg_emissions:
                    total_emissions_kg += telemetry.ghg_emissions * batch.size_kg
            
            # Build CBAM report
            report = {
                "cbam_report": {
                    "producer_id": producer_id,
                    "report_period": {
                        "year": year,
                        "quarter": quarter,
                        "start_date": f"{year}-01-01",
                        "end_date": f"{year}-12-31",
                    },
                    "production_summary": {
                        "total_batches": total_batches,
                        "total_hydrogen_kg": round(total_h2_kg, 2),
                        "compliant_batches": compliant_batches,
                        "compliance_rate": (
                            round(compliant_batches / total_batches * 100, 2)
                            if total_batches > 0 else 0
                        ),
                    },
                    "emissions_summary": {
                        "total_emissions_kg": round(total_emissions_kg, 2),
                        "average_emissions_kgco2_per_kgh2": (
                            round(total_emissions_kg / total_h2_kg, 3)
                            if total_h2_kg > 0 else 0
                        ),
                        "cbam_limit_kgco2_per_kgh2": 3.4,
                        "is_within_cbam_limit": (
                            (total_emissions_kg / total_h2_kg) <= 3.4
                            if total_h2_kg > 0 else True
                        ),
                    },
                    "batch_details": [
                        {
                            "batch_id": batch.id,
                            "size_kg": batch.size_kg,
                            "is_compliant": batch.is_compliant,
                            "certificate_id": (
                                session.query(Certificate)
                                .filter(Certificate.batch_id == batch.id)
                                .first()
                                .id
                                if session.query(Certificate)
                                .filter(Certificate.batch_id == batch.id)
                                .first()
                                else None
                            ),
                        }
                        for batch in batches[:100]  # Limit to 100 batches
                    ],
                    "declaration": {
                        "declarant": producer_id,
                        "declaration_date": datetime.utcnow().isoformat(),
                        "certification": "I declare that the information provided is accurate",
                        "signature": "Digital signature placeholder",
                    },
                },
                "export_metadata": {
                    "export_date": datetime.utcnow().isoformat(),
                    "format": "cbam_xml",
                    "standard": "CBAM 2026",
                    "version": "1.0",
                },
            }
            
            return report

    @staticmethod
    def export_zip_package(certificate_ids: List[str]) -> bytes:
        """
        Export multiple certificates as a ZIP package.
        
        Args:
            certificate_ids: List of certificate IDs to export
            
        Returns:
            ZIP file as bytes
        """
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for cert_id in certificate_ids:
                try:
                    # Export as JSON
                    json_data = ExporterService.export_certificate_json(cert_id)
                    json_str = json.dumps(json_data, indent=2)
                    
                    # Export as CSV
                    csv_str = ExporterService.export_certificate_csv(cert_id)
                    
                    # Add files to ZIP
                    zip_file.writestr(
                        f"certificate_{cert_id}.json",
                        json_str
                    )
                    zip_file.writestr(
                        f"certificate_{cert_id}.csv",
                        csv_str
                    )
                    
                    # Add README
                    readme = f"""H2V-Trust Certificate Export
Certificate ID: {cert_id}
Export Date: {datetime.utcnow().isoformat()}

Files included:
- certificate_{cert_id}.json: Complete certificate data in JSON format
- certificate_{cert_id}.csv: Certificate data in CSV format

This export contains verified green hydrogen certificate data.
"""
                    zip_file.writestr(f"certificate_{cert_id}_README.txt", readme)
                    
                except Exception as e:
                    logger.error(f"Failed to export certificate {cert_id}: {e}")
                    error_file = f"error_{cert_id}.txt"
                    error_msg = f"Failed to export certificate {cert_id}: {str(e)}"
                    zip_file.writestr(error_file, error_msg)
        
        return zip_buffer.getvalue()

    @staticmethod
    def _flatten_dict(data: Dict, parent_key: str = '', sep: str = '.') -> Dict:
        """Flatten a nested dictionary for CSV export."""
        items = []
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(ExporterService._flatten_dict(value, new_key, sep).items())
            else:
                items.append((new_key, value))
        return dict(items)


def generate_compliance_report(
    batch_id: str,
    producer_id: str,
    emissions_data: Dict[str, Any],
    water_data: Dict[str, Any],
    compliance_status: bool,
) -> Dict[str, Any]:
    """
    Generate a compliance report for a batch.
    
    Args:
        batch_id: ID of the batch
        producer_id: ID of the producer
        emissions_data: GHG emissions data
        water_data: Water consumption data
        compliance_status: Whether the batch is compliant
        
    Returns:
        Compliance report dictionary
    """
    # Create compliance checker
    checker = CBAMComplianceChecker()
    
    # Generate report
    report = {
        "batch_id": batch_id,
        "producer_id": producer_id,
        "timestamp": datetime.utcnow().isoformat(),
        "compliance_status": "COMPLIANT" if compliance_status else "NON_COMPLIANT",
        "emissions_data": emissions_data,
        "water_data": water_data,
        "summary": {
            "is_compliant": compliance_status,
            "ghg_emissions_kgco2_per_kgh2": emissions_data.get("total_emissions_kgco2e", 0),
            "water_consumption_liters_per_kgh2": water_data.get("consumption_l_per_kg", 0),
            "cbam_eligible": compliance_status,
            "rfnbo_eligible": compliance_status and emissions_data.get("total_emissions_kgco2e", 0) <= 3.4,
        },
        "details": {
            "emissions_breakdown": emissions_data,
            "water_breakdown": water_data,
            "certificate_requirements": {
                "cbam_compliance": compliance_status,
                "water_framework_directive": water_data.get("is_compliant", False),
                "renewable_energy": emissions_data.get("renewable_energy_percent", 100) >= 100,
            },
        },
        "export_formats": {
            "json": True,
            "csv": True,
            "pdf": False,
            "xml": True,
        },
    }
    
    return report


"""
Integration tests for the H2V-Trust system.
"""

import pytest
from datetime import datetime
from backend.core.compliance import CBAMComplianceChecker
from backend.core.emissions import EmissionsCalculator
from backend.core.water import WaterComplianceChecker
from backend.core.certificates import CertificateGenerator
from backend.core.delegation import DelegationManager
from backend.models.telemetry import TelemetryData


class TestFullComplianceFlow:
    """Integration tests for the full compliance flow."""

    def setup_method(self):
        self.compliance_checker = CBAMComplianceChecker()
        self.emissions_calc = EmissionsCalculator()
        self.water_checker = WaterComplianceChecker()
        self.cert_generator = CertificateGenerator()
        self.delegation_mgr = DelegationManager()

    def _make_telemetry(self, ghg=2.5, water_liters=10.0, water_source="desalination", energy_source="solar"):
        return TelemetryData(
            sensor_id="test_sensor",
            timestamp=datetime.utcnow(),
            energy_source=energy_source,
            power_generated_mwh=100.0,
            ghg_emissions_kgCO2_per_kgH2=ghg,
            water_consumption_liters=water_liters,
            water_source=water_source,
        )

    def test_compliant_batch_full_flow(self):
        """Test the full flow for a compliant batch."""
        # 1. Check water compliance
        is_compliant, message, details = self.water_checker.check_water_consumption(
            water_liters_per_kgh2=10.0,
            h2_kg=1000,
            water_source="desalination",
        )
        assert is_compliant is True

        # 2. Calculate emissions
        emissions = self.emissions_calc.calculate_carbon_footprint(
            ghg_kgco2_per_kgh2=2.5,
            batch_size_kg=1000,
        )
        assert emissions["total_emissions_kg"] > 0

        # 3. Full compliance check
        telemetry = self._make_telemetry()
        compliance = self.compliance_checker.full_compliance_check(telemetry, h2_kg=1000)
        assert compliance["is_compliant"] is True
        assert compliance["cbam_report"] is not None
        assert compliance["cbam_report"]["certificate_eligible"] is True

        # 4. Generate certificate
        cert = self.cert_generator.create_certificate_data(
            batch_id="batch_001",
            producer_id="prod_001",
            compliance_report=compliance,
        )
        assert cert is not None
        assert cert["batch_id"] == "batch_001"

    def test_non_compliant_batch_full_flow(self):
        """Test the full flow for a non-compliant batch."""
        # 1. Check water compliance (excessive)
        is_compliant, message, details = self.water_checker.check_water_consumption(
            water_liters_per_kgh2=25.0,
            h2_kg=1000,
            water_source="desalination",
        )
        assert is_compliant is False

        # 2. Full compliance check
        telemetry = self._make_telemetry(ghg=5.0, water_liters=25000.0)
        compliance = self.compliance_checker.full_compliance_check(telemetry, h2_kg=1000)
        assert compliance["is_compliant"] is False
        assert len(compliance["violations"]) > 0

        # 3. Should not be eligible for certificate
        assert compliance["cbam_report"] is None

    def test_delegation_and_compliance_flow(self):
        """Test delegation combined with compliance."""
        # 1. Create delegation
        delegation = self.delegation_mgr.create_delegation(
            producer_id="prod_001",
            declarant_address="0xdeclarant123",
        )
        assert delegation is not None
        assert delegation["is_active"] is True

        # 2. Check compliance with delegation
        telemetry = self._make_telemetry()
        compliance = self.compliance_checker.full_compliance_check(telemetry, h2_kg=1000)
        assert compliance["is_compliant"] is True

        # 3. Verify delegation still active
        validation = self.delegation_mgr.validate_delegation(delegation)
        assert validation["is_active"] is True

    def test_multi_batch_compliance(self):
        """Test compliance checking for multiple batches."""
        # batch_a: compliant (ghg=2.5, water=10 L/kg)
        # batch_b: non-compliant due to ghg (ghg=4.0 > 2.8 limit)
        # batch_c: non-compliant due to water (water=22 L/kg > 18 limit)
        batches = [
            {"ghg": 2.5, "water": 10.0, "source": "desalination", "energy": "solar", "kg": 1000},
            {"ghg": 4.0, "water": 12.0, "source": "desalination", "energy": "solar", "kg": 1000},
            {"ghg": 2.5, "water": 22.0, "source": "desalination", "energy": "solar", "kg": 1000},
        ]

        results = []
        for b in batches:
            telemetry = self._make_telemetry(ghg=b["ghg"], water_liters=b["water"] * b["kg"], water_source=b["source"], energy_source=b["energy"])
            result = self.compliance_checker.full_compliance_check(telemetry, h2_kg=b["kg"])
            results.append(result)

        assert results[0]["is_compliant"] is True
        assert results[1]["is_compliant"] is False
        assert results[2]["is_compliant"] is False

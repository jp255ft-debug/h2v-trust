"""
Tests for compliance checking and CBAM reporting.
"""

import pytest
from datetime import datetime
from backend.core.compliance import CBAMComplianceChecker
from backend.core.emissions import EmissionsCalculator
from backend.core.water import WaterComplianceChecker
from backend.models.telemetry import TelemetryData
from backend.core.constants import (
    CBAM_GHG_LIMIT_KGCO2_PER_KGH2,
    WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2,
)


class TestComplianceChecker:
    """Tests for CBAMComplianceChecker."""

    def setup_method(self):
        self.checker = CBAMComplianceChecker()

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

    def test_check_compliant_batch(self):
        """Test checking a compliant batch."""
        telemetry = self._make_telemetry()
        result = self.checker.full_compliance_check(telemetry, h2_kg=1000)
        assert result["is_compliant"] is True
        assert len(result["violations"]) == 0

    def test_check_non_compliant_ghg(self):
        """Test checking a batch with high GHG emissions."""
        telemetry = self._make_telemetry(ghg=5.0)
        result = self.checker.full_compliance_check(telemetry, h2_kg=1000)
        assert result["is_compliant"] is False
        assert any("GHG" in v or "Emissions" in v for v in result["violations"])

    def test_check_non_compliant_water(self):
        """Test checking a batch with high water consumption."""
        telemetry = self._make_telemetry(water_liters=25000.0)
        result = self.checker.full_compliance_check(telemetry, h2_kg=1000)
        assert result["is_compliant"] is False
        assert any("água" in v.lower() or "water" in v.lower() for v in result["violations"])

    def test_check_non_renewable_energy(self):
        """Test checking a batch with non-renewable energy."""
        telemetry = self._make_telemetry(energy_source="grid")
        result = self.checker.full_compliance_check(telemetry, h2_kg=1000)
        assert result["is_compliant"] is False
        assert any("energia" in v.lower() or "energy" in v.lower() for v in result["violations"])

    def test_check_invalid_water_source(self):
        """Test checking a batch with invalid water source."""
        # check_water_compliance returns Tuple[bool, str] (2 values)
        is_compliant, message = self.checker.check_water_compliance(
            water_source="invalid_source", water_liters=10.0, h2_kg=1000
        )
        assert is_compliant is False

    def test_cbam_report_generation(self):
        """Test CBAM report generation for a compliant batch."""
        telemetry = self._make_telemetry()
        result = self.checker.full_compliance_check(telemetry, h2_kg=1000)
        assert result["cbam_report"] is not None
        assert result["cbam_report"]["certificate_eligible"] is True
        assert result["cbam_report"]["declared_emissions_tco2"] > 0

    def test_cbam_report_non_compliant(self):
        """Test CBAM report for non-compliant batch."""
        telemetry = self._make_telemetry(ghg=5.0)
        result = self.checker.full_compliance_check(telemetry, h2_kg=1000)
        assert result["cbam_report"] is None


class TestEmissionsCalculator:
    """Tests for EmissionsCalculator."""

    def setup_method(self):
        self.calculator = EmissionsCalculator()

    def test_calculate_emissions(self):
        """Test calculating emissions."""
        result = self.calculator.calculate_carbon_footprint(
            ghg_kgco2_per_kgh2=2.5,
            batch_size_kg=1000,
        )
        assert result["total_emissions_kg"] > 0

    def test_calculate_zero_emissions(self):
        """Test calculating with zero emissions."""
        result = self.calculator.calculate_carbon_footprint(
            ghg_kgco2_per_kgh2=0,
            batch_size_kg=1000,
        )
        assert result["total_emissions_kg"] == 0

    def test_calculate_large_batch(self):
        """Test calculating emissions for a large batch."""
        result = self.calculator.calculate_carbon_footprint(
            ghg_kgco2_per_kgh2=2.5,
            batch_size_kg=10000,
        )
        assert result["total_emissions_kg"] > 0


class TestWaterCompliance:
    """Tests for WaterComplianceChecker."""

    def setup_method(self):
        self.water_checker = WaterComplianceChecker()

    def test_check_compliant_water(self):
        """Test checking compliant water usage."""
        is_compliant, message, details = self.water_checker.check_water_consumption(
            water_liters_per_kgh2=10.0,
            h2_kg=1000,
            water_source="desalination",
        )
        assert is_compliant is True

    def test_check_excessive_water(self):
        """Test checking excessive water usage."""
        is_compliant, message, details = self.water_checker.check_water_consumption(
            water_liters_per_kgh2=25.0,
            h2_kg=1000,
            water_source="desalination",
        )
        assert is_compliant is False

    def test_check_invalid_source(self):
        """Test checking invalid water source."""
        is_compliant, message, details = self.water_checker.check_water_consumption(
            water_liters_per_kgh2=10.0,
            h2_kg=1000,
            water_source="invalid_source",
        )
        assert is_compliant is False

    def test_check_recycled_water(self):
        """Test checking recycled water usage."""
        is_compliant, message, details = self.water_checker.check_water_consumption(
            water_liters_per_kgh2=15.0,
            h2_kg=1000,
            water_source="treated_wastewater",
        )
        assert is_compliant is True

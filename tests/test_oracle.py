"""
Tests for oracle/satellite monitoring services.
"""

import pytest
import asyncio
from unittest.mock import MagicMock, patch
from backend.oracle.satellite_monitor import SatelliteMonitor
from backend.oracle.automation import TaskScheduler, ComplianceAutomation


class TestSatelliteMonitor:
    """Tests for SatelliteMonitor."""

    def test_connect(self):
        """Test connecting to satellite service."""
        monitor = SatelliteMonitor()
        result = asyncio.run(monitor.connect())
        assert result is True

    def test_get_co2_data(self):
        """Test fetching CO2 data."""
        monitor = SatelliteMonitor()
        data = asyncio.run(monitor.get_co2_data("Namibia"))
        assert data is not None
        assert "location" in data
        assert data["location"] == "Namibia"
        assert "co2_concentration_ppm" in data

    def test_get_water_data(self):
        """Test fetching water data."""
        monitor = SatelliteMonitor()
        data = asyncio.run(monitor.get_water_data("Namibia"))
        assert data is not None
        assert "water_availability_index" in data
        assert "water_quality_index" in data

    def test_get_renewable_energy_production(self):
        """Test fetching renewable energy production data."""
        monitor = SatelliteMonitor()
        data = asyncio.run(monitor.get_renewable_energy_production("facility_001"))
        assert data is not None
        assert data["facility_id"] == "facility_001"
        assert data["verification_status"] == "verified"

    def test_verify_additionality(self):
        """Test additionality verification."""
        monitor = SatelliteMonitor()
        data = asyncio.run(monitor.verify_additionality("facility_001", "solar"))
        assert data is not None
        assert data["is_additional"] is True


class TestTaskScheduler:
    """Tests for TaskScheduler."""

    def test_register_task(self):
        """Test registering a scheduled task."""
        scheduler = TaskScheduler()
        
        async def dummy_task():
            pass
        
        scheduler.register_task("test_task", 60, dummy_task)
        assert "test_task" in scheduler.tasks
        assert scheduler.tasks["test_task"].interval_seconds == 60

    def test_unregister_task(self):
        """Test unregistering a scheduled task."""
        scheduler = TaskScheduler()
        
        async def dummy_task():
            pass
        
        scheduler.register_task("test_task", 60, dummy_task)
        scheduler.unregister_task("test_task")
        assert "test_task" not in scheduler.tasks


class TestComplianceAutomation:
    """Tests for ComplianceAutomation."""

    def test_initialization(self):
        """Test ComplianceAutomation initialization."""
        scheduler = TaskScheduler()
        automation = ComplianceAutomation(scheduler)
        assert automation is not None
        assert "check_pending_batches" in scheduler.tasks
        assert "daily_compliance_summary" in scheduler.tasks

    def test_run_compliance_check(self):
        """Test running automated compliance check."""
        scheduler = TaskScheduler()
        automation = ComplianceAutomation(scheduler)
        result = asyncio.run(automation.run_compliance_check("batch_001"))
        assert result is not None
        assert result["batch_id"] == "batch_001"
        assert "status" in result

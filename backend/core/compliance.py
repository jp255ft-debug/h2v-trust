import logging
from datetime import datetime
from typing import Dict, Any, Tuple

from core.constants import (
    CBAM_GHG_LIMIT_KGCO2_PER_KGH2,
    WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2,
    ALLOWED_WATER_SOURCES,
    RENEWABLE_SOURCES,
)
from models.telemetry import TelemetryData

logger = logging.getLogger(__name__)


class CBAMComplianceChecker:
    """Verifica se um lote de H2 atende aos requisitos do CBAM 2026."""

    @staticmethod
    def check_ghg_emissions(ghg_kgco2_per_kgh2: float) -> Tuple[bool, str]:
        """Verifica limite de emissões de GEE."""
        if ghg_kgco2_per_kgh2 <= CBAM_GHG_LIMIT_KGCO2_PER_KGH2:
            return True, f"Emissions OK: {ghg_kgco2_per_kgh2} <= {CBAM_GHG_LIMIT_KGCO2_PER_KGH2} kgCO2e/kgH2"
        return False, f"Emissions exceed limit: {ghg_kgco2_per_kgh2} > {CBAM_GHG_LIMIT_KGCO2_PER_KGH2}"

    @staticmethod
    def check_water_compliance(water_source: str, water_liters: float, h2_kg: float) -> Tuple[bool, str]:
        """Verifica conformidade com Diretiva-Quadro da Água."""
        if water_source not in ALLOWED_WATER_SOURCES:
            return False, f"Water source '{water_source}' not allowed. Allowed: {ALLOWED_WATER_SOURCES}"
        water_intensity = water_liters / h2_kg if h2_kg > 0 else 0
        if water_intensity > WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2:
            return False, f"Water consumption too high: {water_intensity:.1f} L/kgH2 > {WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2}"
        return True, f"Water compliance OK (source: {water_source}, intensity: {water_intensity:.1f} L/kg)"

    @staticmethod
    def check_energy_source(energy_source: str) -> Tuple[bool, str]:
        """Verifica se a energia é 100% renovável (RFNBO)."""
        if energy_source in RENEWABLE_SOURCES:
            return True, f"Renewable energy source: {energy_source}"
        return False, f"Non-renewable energy source: {energy_source}. Must be 100% renewable for RFNBO."

    @staticmethod
    def check_additionality(timestamp: datetime, energy_source: str) -> Tuple[bool, str]:
        """
        Verifica adicionalidade (requisito RFNBO).
        No MVP, assumimos que energia renovável é adicional se provier de parque dedicado.
        """
        # Simulação: para fontes renováveis, sempre adicional (aprimorar com dados reais)
        if energy_source in RENEWABLE_SOURCES:
            return True, "Additionality satisfied (dedicated renewable plant)"
        return False, "Additionality not proven"

    @classmethod
    def full_compliance_check(cls, telemetry: TelemetryData, h2_kg: float) -> Dict[str, Any]:
        """Executa todas as verificações e retorna resultado consolidado."""
        results = {
            "is_compliant": True,
            "checks": {},
            "violations": [],
            "cbam_report": None,
        }

        # 1. Emissões
        ghg_ok, ghg_msg = cls.check_ghg_emissions(telemetry.ghg_emissions_kgCO2_per_kgH2)
        results["checks"]["ghg"] = {"ok": ghg_ok, "message": ghg_msg}
        if not ghg_ok:
            results["is_compliant"] = False
            results["violations"].append(ghg_msg)

        # 2. Água
        water_ok, water_msg = cls.check_water_compliance(
            telemetry.water_source, telemetry.water_consumption_liters, h2_kg
        )
        results["checks"]["water"] = {"ok": water_ok, "message": water_msg}
        if not water_ok:
            results["is_compliant"] = False
            results["violations"].append(water_msg)

        # 3. Fonte de energia
        energy_ok, energy_msg = cls.check_energy_source(telemetry.energy_source)
        results["checks"]["energy"] = {"ok": energy_ok, "message": energy_msg}
        if not energy_ok:
            results["is_compliant"] = False
            results["violations"].append(energy_msg)

        # 4. Adicionalidade
        additionality_ok, additionality_msg = cls.check_additionality(telemetry.timestamp, telemetry.energy_source)
        results["checks"]["additionality"] = {"ok": additionality_ok, "message": additionality_msg}
        if not additionality_ok:
            results["is_compliant"] = False
            results["violations"].append(additionality_msg)

        # Se conforme, gera resumo CBAM
        if results["is_compliant"]:
            results["cbam_report"] = {
                "declared_emissions_tco2": (telemetry.ghg_emissions_kgCO2_per_kgH2 * h2_kg) / 1000,
                "saved_emissions_vs_grey": cls._calculate_saved_emissions(telemetry.ghg_emissions_kgCO2_per_kgH2, h2_kg),
                "certificate_eligible": True,
            }

        return results

    @staticmethod
    def _calculate_saved_emissions(actual_ghg: float, h2_kg: float) -> float:
        """Emissões economizadas comparado ao H2 cinza (assumindo ~10 kgCO2/kgH2)."""
        GREY_H2_GHG = 10.0  # kgCO2/kgH2
        saved = (GREY_H2_GHG - actual_ghg) * h2_kg / 1000
        return max(saved, 0)

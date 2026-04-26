"""Emissions calculation and validation for H2 production."""

import logging
from typing import Dict, Any, Tuple
from datetime import datetime

from core.constants import (
    CBAM_GHG_LIMIT_KGCO2_PER_KGH2,
    RENEWABLE_SOURCES,
    NON_RENEWABLE_SOURCES,
)

logger = logging.getLogger(__name__)


class EmissionsCalculator:
    """Calculates and validates GHG emissions for H2 production."""

    @staticmethod
    def calculate_emissions_intensity(
        energy_source: str,
        energy_kwh_per_kgh2: float,
        grid_carbon_intensity: float = 0.5,  # kgCO2/kWh (default EU grid)
    ) -> float:
        """
        Calculate GHG emissions intensity based on energy source.
        
        Args:
            energy_source: Type of energy (wind, solar, grid, etc.)
            energy_kwh_per_kgh2: Energy consumption per kg of H2
            grid_carbon_intensity: Carbon intensity of grid electricity (kgCO2/kWh)
            
        Returns:
            GHG emissions in kgCO2e/kgH2
        """
        # Emission factors (kgCO2/kWh) - simplified values
        emission_factors = {
            "wind": 0.011,
            "solar": 0.045,
            "hydro": 0.024,
            "biomass": 0.230,
            "grid": grid_carbon_intensity,
            "natural_gas": 0.490,
            "coal": 0.820,
            "diesel": 0.770,
        }
        
        factor = emission_factors.get(energy_source, grid_carbon_intensity)
        return energy_kwh_per_kgh2 * factor

    @staticmethod
    def validate_emissions_source(energy_source: str) -> Tuple[bool, str]:
        """
        Validate if energy source is allowed for CBAM compliance.
        
        Args:
            energy_source: Type of energy source
            
        Returns:
            Tuple of (is_valid, message)
        """
        if energy_source in RENEWABLE_SOURCES:
            return True, f"Renewable source '{energy_source}' is compliant"
        elif energy_source in NON_RENEWABLE_SOURCES:
            return False, f"Non-renewable source '{energy_source}' may require carbon accounting"
        else:
            return False, f"Unknown energy source '{energy_source}'"

    @staticmethod
    def calculate_carbon_footprint(
        ghg_kgco2_per_kgh2: float,
        batch_size_kg: float,
        include_upstream: bool = True,
    ) -> Dict[str, Any]:
        """
        Calculate total carbon footprint for a batch.
        
        Args:
            ghg_kgco2_per_kgh2: GHG emissions per kg H2
            batch_size_kg: Total batch size in kg
            include_upstream: Whether to include upstream emissions
            
        Returns:
            Dictionary with carbon footprint details
        """
        # Direct emissions from production
        direct_emissions_kg = ghg_kgco2_per_kgh2 * batch_size_kg
        
        # Upstream emissions (simplified estimation)
        upstream_emissions_kg = 0
        if include_upstream:
            # Assume 15% upstream emissions for equipment manufacturing, etc.
            upstream_emissions_kg = direct_emissions_kg * 0.15
        
        total_emissions_kg = direct_emissions_kg + upstream_emissions_kg
        
        return {
            "direct_emissions_kg": round(direct_emissions_kg, 2),
            "upstream_emissions_kg": round(upstream_emissions_kg, 2),
            "total_emissions_kg": round(total_emissions_kg, 2),
            "emissions_intensity_kgco2_per_kgh2": round(ghg_kgco2_per_kgh2, 3),
            "is_cbam_compliant": ghg_kgco2_per_kgh2 <= CBAM_GHG_LIMIT_KGCO2_PER_KGH2,
            "cbam_limit": CBAM_GHG_LIMIT_KGCO2_PER_KGH2,
        }

    @staticmethod
    def estimate_cbam_penalty(
        ghg_kgco2_per_kgh2: float,
        batch_size_kg: float,
        penalty_rate_eur_per_ton: float = 50.0,
    ) -> Dict[str, Any]:
        """
        Estimate CBAM penalty for non-compliant emissions.
        
        Args:
            ghg_kgco2_per_kgh2: GHG emissions per kg H2
            batch_size_kg: Total batch size in kg
            penalty_rate_eur_per_ton: CBAM penalty rate in EUR/ton CO2
            
        Returns:
            Dictionary with penalty estimation
        """
        if ghg_kgco2_per_kgh2 <= CBAM_GHG_LIMIT_KGCO2_PER_KGH2:
            return {
                "penalty_applicable": False,
                "penalty_amount_eur": 0.0,
                "excess_emissions_kg": 0.0,
                "message": "Emissions within CBAM limit, no penalty",
            }
        
        # Calculate excess emissions
        excess_per_kg = ghg_kgco2_per_kgh2 - CBAM_GHG_LIMIT_KGCO2_PER_KGH2
        excess_total_kg = excess_per_kg * batch_size_kg
        excess_total_ton = excess_total_kg / 1000.0
        
        # Calculate penalty
        penalty_amount = excess_total_ton * penalty_rate_eur_per_ton
        
        return {
            "penalty_applicable": True,
            "penalty_amount_eur": round(penalty_amount, 2),
            "excess_emissions_kg": round(excess_total_kg, 2),
            "excess_emissions_ton": round(excess_total_ton, 3),
            "penalty_rate_eur_per_ton": penalty_rate_eur_per_ton,
            "message": f"CBAM penalty applicable: €{penalty_amount:.2f}",
        }


# Convenience functions for direct import (used by tests)
def calculate_ghg_emissions(
    energy_source: str,
    energy_kwh_per_kgh2: float,
    grid_carbon_intensity: float = 0.5
) -> float:
    """Calculate GHG emissions intensity (kgCO2e/kgH2)."""
    return EmissionsCalculator.calculate_emissions_intensity(
        energy_source, energy_kwh_per_kgh2, grid_carbon_intensity
    )


def validate_emissions_source(energy_source: str) -> Tuple[bool, str]:
    """Validate energy source for CBAM compliance."""
    return EmissionsCalculator.validate_emissions_source(energy_source)


def calculate_carbon_footprint(
    ghg_kgco2_per_kgh2: float,
    batch_size_kg: float,
    include_upstream: bool = True
) -> Dict[str, Any]:
    """Calculate carbon footprint for a batch."""
    return EmissionsCalculator.calculate_carbon_footprint(
        ghg_kgco2_per_kgh2, batch_size_kg, include_upstream
    )


def estimate_cbam_penalty(
    ghg_kgco2_per_kgh2: float,
    batch_size_kg: float,
    penalty_rate_eur_per_ton: float = 50.0
) -> Dict[str, Any]:
    """Estimate CBAM penalty."""
    return EmissionsCalculator.estimate_cbam_penalty(
        ghg_kgco2_per_kgh2, batch_size_kg, penalty_rate_eur_per_ton
    )

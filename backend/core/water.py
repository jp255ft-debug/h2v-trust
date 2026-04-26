"""Water consumption calculation and compliance for H2 production."""

import logging
from typing import Dict, Any, Tuple, Optional

from core.constants import (
    WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2,
    ALLOWED_WATER_SOURCES,
)

logger = logging.getLogger(__name__)


class WaterComplianceChecker:
    """Validates water consumption and source compliance for H2 production."""

    @staticmethod
    def check_water_consumption(
        water_liters_per_kgh2: float,
        h2_kg: float,
        water_source: str,
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Check water consumption compliance with Water Framework Directive.
        
        Args:
            water_liters_per_kgh2: Water consumption per kg H2
            h2_kg: Total H2 production in kg
            water_source: Source of water (desalination, treated_wastewater, etc.)
            
        Returns:
            Tuple of (is_compliant, message, details)
        """
        # Check water source
        if water_source not in ALLOWED_WATER_SOURCES:
            return False, f"Water source '{water_source}' not allowed", {
                "allowed_sources": ALLOWED_WATER_SOURCES,
                "provided_source": water_source,
            }
        
        # Calculate total water consumption
        total_water_liters = water_liters_per_kgh2 * h2_kg
        
        # Check consumption limit
        is_within_limit = water_liters_per_kgh2 <= WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2
        
        if not is_within_limit:
            message = (
                f"Water consumption {water_liters_per_kgh2} L/kgH2 exceeds "
                f"limit {WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2} L/kgH2"
            )
        else:
            message = (
                f"Water consumption {water_liters_per_kgh2} L/kgH2 within "
                f"limit {WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2} L/kgH2"
            )
        
        details = {
            "water_consumption_liters_per_kgh2": round(water_liters_per_kgh2, 2),
            "total_water_consumption_liters": round(total_water_liters, 2),
            "water_source": water_source,
            "consumption_limit_liters_per_kgh2": WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2,
            "is_within_limit": is_within_limit,
            "h2_production_kg": round(h2_kg, 2),
        }
        
        return is_within_limit, message, details

    @staticmethod
    def calculate_water_efficiency(
        water_liters_per_kgh2: float,
        electrolyzer_efficiency: float = 0.75,
    ) -> Dict[str, Any]:
        """
        Calculate water efficiency metrics for H2 production.
        
        Args:
            water_liters_per_kgh2: Water consumption per kg H2
            electrolyzer_efficiency: Electrolyzer efficiency (0-1)
            
        Returns:
            Dictionary with water efficiency metrics
        """
        # Theoretical minimum: 9 kg water per kg H2 (stoichiometric)
        theoretical_minimum = 9.0  # kg water per kg H2
        
        # Convert liters to kg (1 L ≈ 1 kg for water)
        actual_kg_per_kgh2 = water_liters_per_kgh2
        
        # Calculate efficiency relative to theoretical minimum
        efficiency_ratio = theoretical_minimum / actual_kg_per_kgh2 if actual_kg_per_kgh2 > 0 else 0
        
        # Adjusted efficiency considering electrolyzer efficiency
        adjusted_efficiency = efficiency_ratio * electrolyzer_efficiency
        
        return {
            "water_consumption_liters_per_kgh2": round(water_liters_per_kgh2, 2),
            "water_consumption_kg_per_kgh2": round(actual_kg_per_kgh2, 2),
            "theoretical_minimum_kg_per_kgh2": theoretical_minimum,
            "efficiency_ratio": round(efficiency_ratio, 3),
            "electrolyzer_efficiency": electrolyzer_efficiency,
            "adjusted_efficiency": round(adjusted_efficiency, 3),
            "water_use_efficiency_percent": round(efficiency_ratio * 100, 1),
        }

    @staticmethod
    def assess_water_risk(
        water_source: str,
        water_liters_per_kgh2: float,
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Assess water-related risks for H2 production.
        
        Args:
            water_source: Source of water
            water_liters_per_kgh2: Water consumption per kg H2
            location: Geographic location (optional)
            
        Returns:
            Dictionary with water risk assessment
        """
        # Risk scores (0-10, higher = more risk)
        source_risk_scores = {
            "desalination": 2,  # Low risk, but energy intensive
            "treated_wastewater": 1,  # Very low risk, circular economy
            "surface_water": 6,  # Medium risk, depends on availability
            "groundwater": 8,  # High risk, depletion concerns
        }
        
        # Consumption risk (based on deviation from limit)
        consumption_risk = 0
        if water_liters_per_kgh2 > WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2:
            excess_ratio = water_liters_per_kgh2 / WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2
            consumption_risk = min(10, int(excess_ratio * 5))
        
        # Source risk
        source_risk = source_risk_scores.get(water_source, 5)
        
        # Overall risk (weighted average)
        overall_risk = (source_risk * 0.6) + (consumption_risk * 0.4)
        
        # Risk level categorization
        if overall_risk <= 3:
            risk_level = "LOW"
            recommendation = "Continue current practices"
        elif overall_risk <= 6:
            risk_level = "MEDIUM"
            recommendation = "Monitor water usage and consider efficiency improvements"
        else:
            risk_level = "HIGH"
            recommendation = "Implement water conservation measures immediately"
        
        return {
            "water_source": water_source,
            "water_consumption_liters_per_kgh2": round(water_liters_per_kgh2, 2),
            "source_risk_score": source_risk,
            "consumption_risk_score": consumption_risk,
            "overall_risk_score": round(overall_risk, 1),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "location": location,
            "consumption_limit": WATER_CONSUMPTION_MAX_LITERS_PER_KG_H2,
        }

    @staticmethod
    def estimate_water_footprint(
        water_liters_per_kgh2: float,
        batch_size_kg: float,
        include_virtual_water: bool = True,
    ) -> Dict[str, Any]:
        """
        Estimate total water footprint for a batch.
        
        Args:
            water_liters_per_kgh2: Water consumption per kg H2
            batch_size_kg: Total batch size in kg
            include_virtual_water: Whether to include virtual water (energy production)
            
        Returns:
            Dictionary with water footprint details
        """
        # Direct water consumption
        direct_water_liters = water_liters_per_kgh2 * batch_size_kg
        
        # Virtual water (water used for energy production)
        virtual_water_liters = 0
        if include_virtual_water:
            # Simplified estimation: 1.5 L water per kWh electricity
            # Assuming 50 kWh per kg H2 for electrolysis
            energy_per_kgh2 = 50.0  # kWh/kg H2
            water_per_kwh = 1.5  # L/kWh (average for electricity generation)
            virtual_water_liters = energy_per_kgh2 * water_per_kwh * batch_size_kg
        
        total_water_liters = direct_water_liters + virtual_water_liters
        
        # Convert to meaningful units
        total_water_cubic_meters = total_water_liters / 1000.0
        total_water_olympic_pools = total_water_cubic_meters / 2500.0  # Olympic pool = 2500 m³
        
        return {
            "direct_water_liters": round(direct_water_liters, 2),
            "virtual_water_liters": round(virtual_water_liters, 2),
            "total_water_liters": round(total_water_liters, 2),
            "total_water_cubic_meters": round(total_water_cubic_meters, 2),
            "equivalent_olympic_pools": round(total_water_olympic_pools, 4),
            "water_intensity_liters_per_kgh2": round(water_liters_per_kgh2, 2),
            "batch_size_kg": round(batch_size_kg, 2),
            "includes_virtual_water": include_virtual_water,
        }


def calculate_water_consumption(
    feedwater_source: str,
    purification_method: str,
    recycling_rate: float,
    batch_size_kg: float,
) -> Dict[str, Any]:
    """
    Calculate water consumption for H2 production.
    
    Args:
        feedwater_source: Source of feedwater (municipal, recycled, etc.)
        purification_method: Purification method used
        recycling_rate: Water recycling rate (0-100%)
        batch_size_kg: Batch size in kg
        
    Returns:
        Dictionary with water consumption details
    """
    checker = WaterComplianceChecker()
    
    # Base water consumption based on source and purification
    base_consumption = {
        "municipal": 15.0,
        "recycled": 12.0,
        "desalination": 13.5,
        "surface_water": 14.0,
    }.get(feedwater_source, 15.0)
    
    # Adjustment based on purification method
    purification_factor = {
        "reverse_osmosis": 0.9,
        "membrane": 0.85,
        "distillation": 1.1,
        "electrodialysis": 0.95,
    }.get(purification_method, 1.0)
    
    # Apply recycling rate
    recycling_factor = 1.0 - (recycling_rate / 100.0)
    
    # Calculate final consumption
    consumption_l_per_kg = base_consumption * purification_factor * recycling_factor
    total_consumption_l = consumption_l_per_kg * batch_size_kg
    
    # Check compliance
    is_compliant, message, details = checker.check_water_consumption(
        consumption_l_per_kg, batch_size_kg, feedwater_source
    )
    
    return {
        "feedwater_source": feedwater_source,
        "purification_method": purification_method,
        "recycling_rate": recycling_rate,
        "consumption_l_per_kg": round(consumption_l_per_kg, 2),
        "total_consumption_l": round(total_consumption_l, 2),
        "batch_size_kg": round(batch_size_kg, 2),
        "is_compliant": is_compliant,
        "compliance_message": message,
        "compliance_details": details,
    }


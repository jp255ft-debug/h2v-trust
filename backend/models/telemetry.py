from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Literal


class TelemetryData(BaseModel):
    sensor_id: str
    timestamp: datetime
    energy_source: Literal["wind", "solar", "hydro", "biomass", "grid", "natural_gas", "diesel", "coal"]
    power_generated_mwh: float = Field(ge=0)
    ghg_emissions_kgCO2_per_kgH2: float = Field(ge=0)
    water_consumption_liters: float = Field(ge=0)
    water_source: Literal["desalination", "treated_wastewater", "surface_water", "groundwater", "recycled"]

    @field_validator("ghg_emissions_kgCO2_per_kgH2", mode="before")
    def validate_ghg(cls, v):
        if v < 0:
            raise ValueError("GHG emissions cannot be negative")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sensor_id": "wind_turbine_01",
                "timestamp": "2026-04-18T10:00:00Z",
                "energy_source": "wind",
                "power_generated_mwh": 10.5,
                "ghg_emissions_kgCO2_per_kgH2": 2.8,
                "water_consumption_liters": 150,
                "water_source": "desalination",
            }
        }
    )

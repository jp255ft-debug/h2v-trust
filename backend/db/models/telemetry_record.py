"""
TelemetryRecord model for IoT sensor data storage.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class TelemetryRecord(Base):
    """Model for storing IoT sensor telemetry data."""
    
    __tablename__ = "telemetry_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    sensor_id = Column(String(100), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    energy_source = Column(String(50), nullable=False)
    power_generated_mwh = Column(Float, default=0.0)
    ghg_emissions = Column(Float, nullable=False)
    water_consumption_liters = Column(Float, default=0.0)
    water_source = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    batch = relationship("Batch", back_populates="telemetry", uselist=False)
    
    def __repr__(self):
        return f"<TelemetryRecord(id={self.id}, sensor={self.sensor_id}, ts={self.timestamp})>"
    
    def to_dict(self):
        """Convert telemetry record to dictionary."""
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "energy_source": self.energy_source,
            "power_generated_mwh": self.power_generated_mwh,
            "ghg_emissions": self.ghg_emissions,
            "water_consumption_liters": self.water_consumption_liters,
            "water_source": self.water_source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

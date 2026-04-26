import re
from datetime import datetime

def validate_sensor_id(sensor_id: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_-]{3,50}$', sensor_id))

def validate_timestamp(ts: datetime) -> bool:
    return ts <= datetime.utcnow()

def validate_emissions(value: float) -> bool:
    return 0 <= value <= 50  # kgCO2/kgH2 realista
import hashlib
import json
from datetime import datetime

def generate_batch_hash(data: dict) -> str:
    """Gera hash SHA256 dos dados de telemetria."""
    # Convert datetime objects to ISO format strings for JSON serialization
    def json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    sorted_data = json.dumps(data, sort_keys=True, default=json_serializer)
    return hashlib.sha256(sorted_data.encode()).hexdigest()

def verify_hash(data: dict, expected_hash: str) -> bool:
    return generate_batch_hash(data) == expected_hash

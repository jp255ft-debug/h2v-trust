import asyncio
from typing import Dict, Any

class SensorAggregator:
    def __init__(self):
        self.sensors = {}

    async def collect_data(self, sensor_ids: list) -> Dict[str, Any]:
        tasks = [self._read_sensor(sid) for sid in sensor_ids]
        results = await asyncio.gather(*tasks)
        return {sid: res for sid, res in zip(sensor_ids, results)}

    async def _read_sensor(self, sensor_id: str) -> float:
        # Mock: retorna um valor aleatório de emissão entre 2.0 e 4.0
        import random
        await asyncio.sleep(0.1)
        return round(random.uniform(2.0, 4.0), 2)
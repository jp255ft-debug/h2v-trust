import logging
from blockchain.web3_client import get_contract

logger = logging.getLogger(__name__)

async def verify_certificate_on_chain(token_id: int) -> dict:
    try:
        contract = get_contract()
    except (ConnectionError, TimeoutError, Exception) as e:
        logger.warning(f"Blockchain connection failed during verification of token {token_id}: {e}")
        return {"error": "Blockchain unavailable", "token_id": token_id}
    
    try:
        is_consumed = contract.functions.isConsumed(token_id).call()
        batch_hash = contract.functions.getBatchDataHash(token_id).call()
        emissions = contract.functions.getEmissions(token_id).call()
        water = contract.functions.getWaterSource(token_id).call()
        energy = contract.functions.getEnergySource(token_id).call()
        size = contract.functions.getBatchSizeKg(token_id).call()
        return {
            "token_id": token_id,
            "is_consumed": is_consumed,
            "batch_hash": batch_hash,
            "emissions_kgco2_per_kg": emissions / 1e6,
            "water_source": water,
            "energy_source": energy,
            "batch_size_kg": size,
        }
    except ConnectionError as e:
        logger.warning(f"Blockchain connection lost during verification of token {token_id}: {e}")
        return {"error": "Blockchain connection lost", "token_id": token_id}
    except Exception as e:
        logger.warning(f"Verification failed for token {token_id}: {e}")
        return {"error": str(e), "token_id": token_id}

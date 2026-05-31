import logging
from blockchain.web3_client import get_contract, get_w3
from config import settings

logger = logging.getLogger(__name__)

async def consume_sbt(token_id: int):
    """
    Consume (burn/surrender) an SBT certificate on-chain.
    
    Falls back to mock mode if blockchain is not available,
    allowing the system to function without a local Hardhat node.
    """
    # Check if mock mode is enabled
    if settings.MOCK_MODE:
        logger.info(f"MOCK_MODE: Simulating consume of token {token_id}")
        return "0x" + "0" * 64
    
    try:
        w3 = get_w3()
        contract = get_contract()
        account = w3.eth.account.from_key(settings.PRIVATE_KEY)
        nonce = w3.eth.get_transaction_count(account.address)
        tx = contract.functions.consumeCertificate(token_id).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 100000,
        })
        signed = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        tx_hash_hex = tx_hash.hex() if hasattr(tx_hash, 'hex') else str(tx_hash)
        logger.info(f"Certificate {token_id} consumed on-chain. TX: {tx_hash_hex}")
        return tx_hash_hex
    except Exception as e:
        logger.warning(f"Blockchain consume failed for token {token_id}: {e}")
        logger.warning("Falling back to mock consume (offline mode)")
        return "0x" + "0" * 64

from blockchain.web3_client import get_contract, get_w3
from config import settings

async def consume_sbt(token_id: int):
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
    return tx_hash.hex()

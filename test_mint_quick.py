import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from config import settings
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider(settings.POLYGON_RPC_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print('Connected:', w3.is_connected(), flush=True)
print('Chain ID:', w3.eth.chain_id, flush=True)

# Load ABI
with open(os.path.join(os.path.dirname(__file__), 'contracts/artifacts/contracts/GreenHydrogenSBT.sol/GreenHydrogenSBT.json'), 'r') as f:
    abi_data = json.load(f)
abi = abi_data.get('abi', [])

contract = w3.eth.contract(address=w3.to_checksum_address(settings.CONTRACT_ADDRESS), abi=abi)
print('Contract loaded', flush=True)

# Check owner
owner = contract.functions.owner().call()
print('Owner:', owner, flush=True)

# Check account
account = w3.eth.account.from_key(settings.PRIVATE_KEY)
print('Account:', account.address, flush=True)
print('Is owner:', account.address.lower() == owner.lower(), flush=True)

# Try to mint
batch_id_bytes = w3.keccak(text='test-quick-001')
nonce = w3.eth.get_transaction_count(account.address)
print('Nonce:', nonce, flush=True)

tx = contract.functions.mintCertificate(
    batch_id_bytes,
    '0x70997970C51812dc3A010C7d01b50e0d17dc79C8',
    'data:application/json,{}'
).build_transaction({
    'from': account.address,
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': w3.eth.gas_price
})

signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print('TX sent:', tx_hash.hex(), flush=True)

receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
print('Receipt status:', receipt.status, flush=True)
print('Block:', receipt.blockNumber, flush=True)

# Try process_receipt
try:
    logs = contract.events.CertificateMinted().process_receipt(receipt)
    print('Logs found:', len(logs), flush=True)
    for log in logs:
        print('Token ID:', log['args']['tokenId'], flush=True)
except Exception as e:
    print('process_receipt error:', e, flush=True)
    print('Raw logs:', receipt.logs, flush=True)

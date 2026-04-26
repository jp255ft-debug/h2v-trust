import json, os, sys
sys.path.insert(0, '.')
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print('Connected:', w3.is_connected())
print('Chain ID:', w3.eth.chain_id)
print('Block:', w3.eth.block_number)

# Load ABI
with open('contracts/artifacts/contracts/GreenHydrogenSBT.sol/GreenHydrogenSBT.json') as f:
    data = json.load(f)
abi = data['abi']

contract_addr = '0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB'
contract = w3.eth.contract(address=w3.to_checksum_address(contract_addr), abi=abi)

# Check if contract has code
code = w3.eth.get_code(w3.to_checksum_address(contract_addr))
print('Contract code length:', len(code))

# Try to mint
acct = w3.eth.account.from_key('0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')
print('Account:', acct.address)

nonce = w3.eth.get_transaction_count(acct.address)
print('Nonce:', nonce)

batch_id_bytes = b'\x00' * 32  # dummy batch id
producer = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
token_uri = 'data:application/json,{"name":"Test"}'

# Estimate gas
try:
    gas_est = contract.functions.mintCertificate(batch_id_bytes, producer, token_uri).estimate_gas({'from': acct.address})
    print('Gas est:', gas_est)
except Exception as e:
    print('Gas est failed:', e)
    gas_est = 2000000

tx = contract.functions.mintCertificate(batch_id_bytes, producer, token_uri).build_transaction({
    'from': acct.address,
    'nonce': nonce,
    'gas': int(gas_est * 1.5),
    'gasPrice': w3.eth.gas_price
})

signed = acct.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print('Tx hash:', tx_hash.hex())

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('Status:', receipt.status)
print('Logs:', len(receipt.logs))

# Try to process event
try:
    logs = contract.events.CertificateMinted().process_receipt(receipt)
    print('Processed logs:', len(logs))
    if logs:
        print('Token ID:', logs[0]['args']['tokenId'])
except Exception as e:
    print('Process error:', e)
    # Fallback: check raw logs
    for log in receipt.logs:
        print('Log address:', log.address)
        print('Log topics:', [t.hex() if isinstance(t, bytes) else t for t in log.topics])

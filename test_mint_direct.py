"""Teste direto de minting no contrato"""
from web3 import Web3
import json
import os

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
print('Connected:', w3.is_connected())
print('Chain ID:', w3.eth.chain_id)
print('Block:', w3.eth.block_number)

addr = '0x7a2088a1bFc9d81c55368AE168C2C02570cB814F'
abi_path = os.path.join('contracts', 'artifacts', 'contracts', 'GreenHydrogenSBT.sol', 'GreenHydrogenSBT.json')
with open(abi_path) as f:
    abi_data = json.load(f)
abi = abi_data.get('abi', [])
contract = w3.eth.contract(address=Web3.to_checksum_address(addr), abi=abi)
print('Name:', contract.functions.name().call())
print('Symbol:', contract.functions.symbol().call())
print('Total:', contract.functions.getTotalCertificates().call())

# Testar mint
acct = w3.eth.account.from_key('0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')
nonce = w3.eth.get_transaction_count(acct.address)
batch_id = '0x' + 'ab' * 32
print(f'Batch ID length: {len(batch_id)}')
print(f'Batch ID: {batch_id}')

tx = contract.functions.mintCertificate(
    batch_id, 
    '0x70997970C51812dc3A010C7d01b50e0d17dc79C8', 
    'https://test.com/1'
).build_transaction({
    'from': acct.address, 
    'nonce': nonce, 
    'gas': 2000000, 
    'gasPrice': w3.eth.gas_price
})
signed = acct.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print('Status:', receipt.status)
print('Logs count:', len(receipt.logs))

# Processar evento
logs = contract.events.CertificateMinted().process_receipt(receipt)
print('Events found:', len(logs))
if logs:
    print('Token ID:', logs[0]['args']['tokenId'])
else:
    print('NO EVENTS FOUND - checking raw logs:')
    for i, log in enumerate(receipt.logs):
        print(f'  Log {i}: address={log["address"]}, topics={log["topics"]}')

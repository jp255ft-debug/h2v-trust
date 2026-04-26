"""Test script to debug the minting process exactly as the backend does it"""
import sys, os, json, logging
sys.path.insert(0, '.')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set env vars exactly as the backend would
os.environ['MOCK_MODE'] = 'false'
os.environ['POLYGON_RPC_URL'] = 'http://127.0.0.1:8545'
os.environ['CONTRACT_ADDRESS'] = '0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB'
os.environ['PRIVATE_KEY'] = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'

from backend.config import settings
print(f"Settings loaded:")
print(f"  RPC: {settings.POLYGON_RPC_URL}")
print(f"  Contract: {settings.CONTRACT_ADDRESS}")
print(f"  Mock: {settings.MOCK_MODE}")

from backend.blockchain.web3_client import init_web3, get_contract, get_w3

# Force re-init
w3, contract = init_web3(force_reload=True)
print(f"\nWeb3 connected: {w3.is_connected()}")
print(f"Chain ID: {w3.eth.chain_id}")
print(f"Contract: {contract}")

if contract:
    print(f"Contract address: {contract.address}")
    events = [e.get('name') for e in contract.abi if e.get('type') == 'event']
    print(f"Events in ABI: {events}")
    
    # Check if CertificateMinted is in ABI
    has_event = any(e.get('name') == 'CertificateMinted' for e in contract.abi if e.get('type') == 'event')
    print(f"Has CertificateMinted event: {has_event}")
    
    # Try to mint
    account = w3.eth.account.from_key(settings.PRIVATE_KEY)
    print(f"Account: {account.address}")
    
    nonce = w3.eth.get_transaction_count(account.address)
    print(f"Nonce: {nonce}")
    
    batch_id = "test-batch-123"
    batch_id_bytes = w3.keccak(text=batch_id)
    producer = account.address
    token_uri = 'data:application/json,{"name":"Test"}'
    
    try:
        gas_est = contract.functions.mintCertificate(
            batch_id_bytes, producer, token_uri
        ).estimate_gas({'from': account.address})
        print(f"Gas est: {gas_est}")
    except Exception as e:
        print(f"Gas est failed: {e}")
        gas_est = 2000000
    
    tx = contract.functions.mintCertificate(
        batch_id_bytes, producer, token_uri
    ).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': int(gas_est * 1.5),
        'gasPrice': w3.eth.gas_price
    })
    
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"Tx hash: {tx_hash.hex()}")
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Status: {receipt.status}")
    print(f"Logs count: {len(receipt.logs)}")
    
    # Try process_receipt
    try:
        logs = contract.events.CertificateMinted().process_receipt(receipt)
        print(f"Processed logs: {len(logs)}")
        if logs:
            print(f"Token ID: {logs[0]['args']['tokenId']}")
    except Exception as e:
        print(f"process_receipt error: {e}")
        # Check raw logs
        for i, log in enumerate(receipt.logs):
            print(f"\nLog {i}:")
            print(f"  address: {log['address']}")
            print(f"  topics: {[t.hex() if isinstance(t, bytes) else t for t in log['topics']]}")
            print(f"  data: {log['data'].hex() if isinstance(log['data'], bytes) else log['data']}")

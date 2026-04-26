import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.blockchain.web3_client import init_web3
from backend.config import settings

print("Testing account balance on Polygon Amoy...")
print("=" * 60)

try:
    # Initialize Web3 connection
    w3, contract = init_web3()
    
    # Get account from private key
    from web3 import Web3
    account = w3.eth.account.from_key(settings.PRIVATE_KEY)
    address = account.address
    
    print(f"Account address: {address}")
    print(f"Private key (first 10 chars): {settings.PRIVATE_KEY[:10]}...")
    
    # Check balance
    balance_wei = w3.eth.get_balance(address)
    balance_matic = w3.from_wei(balance_wei, 'ether')
    
    print(f"Balance: {balance_matic} MATIC")
    print(f"Balance (wei): {balance_wei}")
    
    # Check if we have enough balance for transactions
    if balance_wei < w3.to_wei(0.01, 'ether'):
        print("\n[WARNING] Low balance! You may need to get test MATIC from a faucet.")
        print("Visit: https://faucet.polygon.technology/")
    else:
        print("\n[SUCCESS] Account has sufficient balance for transactions")
        
    # Check contract code
    print(f"\nChecking contract at address: {settings.CONTRACT_ADDRESS}")
    contract_code = w3.eth.get_code(settings.CONTRACT_ADDRESS)
    
    if contract_code and contract_code != b'\x00':
        print(f"Contract code length: {len(contract_code)} bytes")
        print("[SUCCESS] Contract is deployed at this address")
    else:
        print("[ERROR] No contract code at this address")
        print("The contract may need to be deployed")
        
except Exception as e:
    print(f"[ERROR] Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test completed!")
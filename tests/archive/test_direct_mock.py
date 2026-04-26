import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import random
from backend.blockchain.web3_client import init_web3

print("Testing mock Web3 token_id generation...")
print("=" * 60)

# Initialize Web3 in mock mode
w3, contract = init_web3()

# Test token_id generation
print("Testing token_id generation...")
for i in range(5):
    # Simulate process_receipt call
    mock_event = contract.events.CertificateMinted()
    result = mock_event.process_receipt({"transactionHash": "0x" + "0" * 64})
    
    if result and len(result) > 0:
        token_id = result[0]['args']['tokenId']
        print(f"Test {i+1}: token_id = {token_id}")
    else:
        print(f"Test {i+1}: No result returned")
    
    time.sleep(0.1)  # Small delay to ensure different timestamps

print("\n" + "=" * 60)
print("Test completed!")
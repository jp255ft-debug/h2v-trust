import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from backend.blockchain.minting import mint_certificate_on_chain

print("Testing mint_certificate_on_chain function directly...")
print("=" * 60)

async def test_minting():
    try:
        batch_id = "test_batch_123"
        producer_address = "0x1234567890123456789012345678901234567890"
        metadata = {
            "emissions": 2.8,
            "water_source": "desalination",
            "energy_source": "wind",
            "batch_size_kg": 1000
        }
        
        print(f"Batch ID: {batch_id}")
        print(f"Producer address: {producer_address}")
        print(f"Metadata: {metadata}")
        
        print("\nCalling mint_certificate_on_chain...")
        tx_hash, token_id = await mint_certificate_on_chain(
            batch_id=batch_id,
            producer_address=producer_address,
            metadata=metadata
        )
        
        print(f"✅ Success!")
        print(f"Transaction hash: {tx_hash}")
        print(f"Token ID: {token_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_minting())
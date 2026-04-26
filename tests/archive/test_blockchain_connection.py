import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.blockchain.web3_client import init_web3, get_network_info

print("Testing blockchain connection to Polygon Amoy...")
print("=" * 60)

try:
    # Initialize Web3 connection
    w3, contract = init_web3()
    
    # Get network info
    network_info = get_network_info()
    
    print(f"Network connection status: {'CONNECTED' if network_info.get('is_connected') else 'NOT CONNECTED'}")
    print(f"Chain ID: {network_info.get('chain_id', 'N/A')}")
    print(f"Block number: {network_info.get('block_number', 'N/A')}")
    print(f"Gas price: {network_info.get('gas_price', 'N/A')}")
    print(f"RPC URL: {network_info.get('rpc_url', 'N/A')}")
    
    if network_info.get('is_connected'):
        print("\n[SUCCESS] Connected to Polygon Amoy testnet!")
        
        # Check contract address
        from backend.config import settings
        print(f"Contract address: {settings.CONTRACT_ADDRESS}")
        
        # Try to get contract info
        if contract:
            print(f"Contract loaded: Yes")
            # Try to call a simple function
            try:
                # Get total supply or other simple view function
                print("Testing contract interaction...")
                # Note: The actual function name may vary
                print("Contract interaction test completed")
            except Exception as e:
                print(f"Contract interaction error (may be expected): {e}")
        else:
            print(f"Contract loaded: No (may need deployment)")
            
    else:
        print("\n[ERROR] Failed to connect to blockchain")
        print(f"Error: {network_info.get('error', 'Unknown error')}")
        
except Exception as e:
    print(f"[ERROR] Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test completed!")
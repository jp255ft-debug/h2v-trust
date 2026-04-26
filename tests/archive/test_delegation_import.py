#!/usr/bin/env python3
"""Test DelegationService import."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import DelegationService
    from backend.services.delegation_service import DelegationService
    print("SUCCESS: DelegationService import successful!")
    
    # Try to import the delegation router
    from backend.api.routes.delegation import router
    print("SUCCESS: Delegation router import successful!")
    
except ImportError as e:
    print(f"ERROR: Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"ERROR: Unexpected error: {e}")
    import traceback
    traceback.print_exc()

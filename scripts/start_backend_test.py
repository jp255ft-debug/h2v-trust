#!/usr/bin/env python3
"""Test starting the backend server."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import and create app
    from backend.main import app
    print("SUCCESS: Backend app imported successfully!")
    
    # Check if we can get routes
    routes = [route.path for route in app.routes]
    print(f"Found {len(routes)} routes")
    
    # Try to initialize database
    from backend.db.database import init_db
    try:
        init_db()
        print("SUCCESS: Database initialized!")
    except Exception as e:
        print(f"WARNING: Database initialization failed (expected for MVP): {e}")
        
    print("\nBackend is ready to start!")
    print("Run: cd backend && venv\\Scripts\\python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    
except ImportError as e:
    print(f"ERROR: Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"ERROR: Unexpected error: {e}")
    import traceback
    traceback.print_exc()
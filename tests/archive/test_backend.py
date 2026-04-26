#!/usr/bin/env python3
"""Simple test to check if backend can be imported."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import main components
    from backend.main import app
    from backend.config import settings
    from backend.db.database import init_db
    
    print("SUCCESS: Backend imports successful!")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    # Try to initialize database
    try:
        init_db()
        print("SUCCESS: Database initialization successful!")
    except Exception as e:
        print(f"WARNING: Database initialization failed: {e}")
        
except ImportError as e:
    print(f"ERROR: Import error: {e}")
    print("Missing dependencies. Try installing with:")
    print("  pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv")
except Exception as e:
    print(f"ERROR: Unexpected error: {e}")

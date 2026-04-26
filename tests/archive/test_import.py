import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import main components
    from backend.main import app
    print("SUCCESS: Backend imports successful!")
    
    # Check database
    from backend.config import settings
    print(f"Database URL: {settings.DATABASE_URL}")
    
    # Try to initialize database
    from backend.db.database import init_db
    try:
        init_db()
        print("SUCCESS: Database initialization successful!")
    except Exception as e:
        print(f"WARNING: Database initialization failed: {e}")
        
except ImportError as e:
    print(f"ERROR: Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"ERROR: Unexpected error: {e}")
    import traceback
    traceback.print_exc()
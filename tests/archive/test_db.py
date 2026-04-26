import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import settings

print("Testing database connection...")
try:
    engine = create_engine(settings.DATABASE_URL)
    connection = engine.connect()
    print(f"Database connected successfully: {settings.DATABASE_URL}")
    connection.close()
except Exception as e:
    print(f"Error connecting to database: {e}")
    import traceback
    traceback.print_exc()
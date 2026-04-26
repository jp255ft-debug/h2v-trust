#!/usr/bin/env python3
"""
Test the API route directly.
"""

import sys
sys.path.append('.')

from backend.api.dependencies.db import get_db
from backend.api.routes.batches import list_batches
from fastapi import HTTPException
import asyncio

async def test_api_route():
    """Test the list_batches API route."""
    print('Testing list_batches API route...')
    try:
        # Create a mock request context
        class MockRequest:
            def __init__(self):
                self.headers = {"X-API-Key": "test-secret-key-for-local-development-12345"}
        
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Call the route function
            result = await list_batches(
                skip=0,
                limit=10,
                producer_id=None,
                compliant_only=False,
                db=db,
                api_key="test-secret-key-for-local-development-12345"
            )
            print(f'Success! Result: {result}')
            print(f'Number of batches: {len(result["batches"])}')
        except HTTPException as e:
            print(f'HTTPException: {e.status_code} - {e.detail}')
        except Exception as e:
            print(f'Error: {e}')
            import traceback
            traceback.print_exc()
        finally:
            # Close the database session
            try:
                next(db_gen)
            except StopIteration:
                pass
    except Exception as e:
        print(f'Error setting up test: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api_route())
#!/usr/bin/env python3
"""
Test the BatchService.
"""

import sys
sys.path.append('.')

from backend.db.database import SessionLocal
from backend.services.batch_service import BatchService

def test_batch_service():
    """Test the BatchService.get_batches() method."""
    db = SessionLocal()
    try:
        service = BatchService(db)
        print('Testing BatchService.get_batches()...')
        try:
            batches = service.get_batches(skip=0, limit=10, producer_id=None, compliant_only=False)
            print(f'Success! Got {len(batches)} batches')
            if batches:
                import json
                print(json.dumps(batches[0], indent=2))
        except Exception as e:
            print(f'Error in get_batches(): {e}')
            import traceback
            traceback.print_exc()
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_batch_service()
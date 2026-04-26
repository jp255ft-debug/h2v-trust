#!/usr/bin/env python3
"""
Test the API endpoints.
"""

import sys
sys.path.append('.')

from backend.db.database import SessionLocal
from backend.db.models import Batch
from sqlalchemy.orm import joinedload

def test_batch_to_dict():
    """Test the to_dict() method on a batch."""
    db = SessionLocal()
    try:
        batch = db.query(Batch).options(joinedload(Batch.telemetry)).first()
        if batch:
            print(f'Testing to_dict() on batch {batch.id}')
            try:
                result = batch.to_dict()
                print(f'Success! Result:')
                import json
                print(json.dumps(result, indent=2))
            except Exception as e:
                print(f'Error in to_dict(): {e}')
                import traceback
                traceback.print_exc()
        else:
            print('No batches found')
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_batch_to_dict()
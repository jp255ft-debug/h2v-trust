# DelegationService Fix Plan

## Root Cause Analysis
1. **File exists but is empty**: `backend/services/delegation_service.py` exists but contains 0 bytes (empty file).
2. **Missing class definition**: The `DelegationService` class is not defined in the file.
3. **Import failure**: `backend/api/routes/delegation.py` tries to import `DelegationService` from a file that doesn't contain the class.

## Files to Modify/Create

### 1. `backend/services/delegation_service.py` (CREATE/REWRITE)
- Create a proper `DelegationService` class with the following methods:
  - `__init__(self, db: Session)`: Constructor that stores database session
  - `create_delegation(self, producer_id: str, declarant_address: str, valid_until: str) -> dict`: Creates a new delegation record
  - `get_active_delegation(self, producer_id: str) -> dict`: Retrieves active delegation for a producer
  - `revoke_delegation(self, producer_id: str) -> dict`: Revokes an active delegation

### 2. `backend/api/routes/delegation.py` (VERIFY)
- Verify the import statement is correct: `from backend.services.delegation_service import DelegationService`
- No changes needed if import is already correct.

## Specific Changes

### For `delegation_service.py`:
```python
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from backend.db.models import Delegation as DelegationORM

logger = logging.getLogger(__name__)

class DelegationService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_delegation(self, producer_id: str, declarant_address: str, valid_until: str) -> dict:
        """Create a new CBAM delegation authorization."""
        # Mock implementation for MVP
        delegation = {
            "id": "deleg_123",
            "producer_id": producer_id,
            "declarant_address": declarant_address,
            "valid_until": valid_until,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        logger.info(f"Created delegation: {delegation}")
        return delegation
    
    def get_active_delegation(self, producer_id: str) -> dict:
        """Get active delegation for a producer."""
        # Mock implementation for MVP
        return {
            "producer_id": producer_id,
            "has_active_delegation": True,
            "declarant_address": "0xDeclarant123",
            "valid_until": "2026-12-31",
            "created_at": "2026-04-18T10:00:00"
        }
    
    async def revoke_delegation(self, producer_id: str) -> dict:
        """Revoke active delegation for a producer."""
        # Mock implementation for MVP
        return {
            "producer_id": producer_id,
            "status": "revoked",
            "revoked_at": datetime.now().isoformat(),
            "message": "Delegation revoked successfully"
        }
```

## Implementation Strategy
1. Create the `delegation_service.py` file with the above implementation
2. Test the import by running a simple test script
3. Start the backend server to verify the `/delegation` endpoints work
4. Document any assumptions or limitations

## Assumptions
- For MVP, using mock implementations that return hardcoded data
- No actual database persistence needed for initial testing
- The service methods match the expected signatures from `delegation.py`
import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from db.models.delegation import Delegation

logger = logging.getLogger(__name__)

class DelegationService:
    def __init__(self, db: Session):
        self.db = db

    async def create_delegation(self, producer_id: str, declarant_wallet: str, valid_until: str = None, tenant_id: str = "default") -> dict:
        """Create a new CBAM delegation authorization."""
        if not valid_until:
            valid_until = (datetime.utcnow() + timedelta(days=365)).isoformat()

        delegation = Delegation(
            delegation_id=f"deleg_{uuid.uuid4().hex[:12]}",
            producer_id=producer_id,
            declarant_address=declarant_wallet,
            valid_until=datetime.fromisoformat(valid_until.replace("Z", "")),
            status="active",
            tenant_id=tenant_id,
        )
        self.db.add(delegation)
        self.db.commit()
        self.db.refresh(delegation)

        logger.info(f"Created delegation: {delegation.delegation_id} for producer {producer_id}")
        return delegation.to_dict()

    def get_delegations(self, producer_id: str, tenant_id: Optional[str] = "default") -> dict:
        """
        Get all delegations for a producer with tenant isolation.
        
        Args:
            tenant_id: If None (auditor), can view any producer's delegations.
                       If string (producer), only returns delegations for that tenant.
        """
        query = self.db.query(Delegation).filter(
            Delegation.producer_id == producer_id,
        )
        
        # Apenas filtra por tenant se tenant_id não for None
        if tenant_id is not None:
            query = query.filter(Delegation.tenant_id == tenant_id)
        
        delegations = query.order_by(Delegation.created_at.desc()).all()

        return {
            "producer_id": producer_id,
            "delegations": [d.to_dict() for d in delegations]
        }

    def get_active_delegation(self, producer_id: str, tenant_id: Optional[str] = "default") -> dict:
        """
        Get active delegation for a producer with tenant isolation.
        
        Args:
            tenant_id: If None (auditor), can view any producer's active delegation.
                       If string (producer), only returns if belongs to that tenant.
        """
        query = self.db.query(Delegation).filter(
            Delegation.producer_id == producer_id,
            Delegation.status == "active",
        )
        
        # Apenas filtra por tenant se tenant_id não for None
        if tenant_id is not None:
            query = query.filter(Delegation.tenant_id == tenant_id)
        
        delegation = query.first()

        if delegation:
            return {
                "producer_id": producer_id,
                "has_active_delegation": True,
                "declarant_address": delegation.declarant_address,
                "valid_until": delegation.valid_until.isoformat() if delegation.valid_until else None,
                "created_at": delegation.created_at.isoformat() if delegation.created_at else None
            }

        return {
            "producer_id": producer_id,
            "has_active_delegation": False
        }

    async def revoke_delegation(self, producer_id: str, declarant_wallet: str = None, tenant_id: Optional[str] = "default") -> dict:
        """
        Revoke delegation(s) for a producer with tenant isolation.
        
        Args:
            tenant_id: If None (auditor), cannot revoke (will return not_found).
                       If string (producer), only revokes if belongs to that tenant.
        """
        query = self.db.query(Delegation).filter(
            Delegation.producer_id == producer_id,
            Delegation.status == "active",
        )
        
        # Apenas filtra por tenant se tenant_id não for None
        if tenant_id is not None:
            query = query.filter(Delegation.tenant_id == tenant_id)

        if declarant_wallet:
            query = query.filter(Delegation.declarant_address == declarant_wallet)

        delegations = query.all()

        if not delegations:
            return {
                "producer_id": producer_id,
                "status": "not_found",
                "message": "Nenhuma delegação ativa encontrada para revogar"
            }

        now = datetime.utcnow()
        for d in delegations:
            d.status = "revoked"
            d.revoked_at = now

        self.db.commit()

        logger.info(f"Revoked {len(delegations)} delegation(s) for producer {producer_id}")
        return {
            "producer_id": producer_id,
            "status": "revoked",
            "revoked_at": now.isoformat(),
            "message": f"{len(delegations)} delegação(ões) revogada(s) com sucesso"
        }

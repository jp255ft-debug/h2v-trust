"""
Seed script for initial users and tenants data.

Creates:
- Default tenant (for backward compatibility with existing API keys)
- Admin user (platform administrator)
- Operator user (for produtor-alfa tenant)
- Auditor user (cross-tenant read-only access)

Usage:
    docker compose exec backend python scripts/seed_users_tenants.py
"""

import sys
import os
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal, engine, Base
from db.models import Tenant, User, UserTenant
from api.dependencies.jwt_auth import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed():
    """Seed initial users and tenants data."""
    logger.info("Starting users/tenants seed...")
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # ─── Tenants ───────────────────────────────────────────────
        
        # Check if default tenant already exists
        default_tenant = db.query(Tenant).filter(Tenant.slug == "default").first()
        if not default_tenant:
            default_tenant = Tenant(
                name="Default Platform",
                slug="default",
                status="active",
                contact_email="admin@h2v-trust.com",
            )
            db.add(default_tenant)
            db.flush()
            logger.info(f"Created default tenant: id={default_tenant.id}")
        else:
            logger.info(f"Default tenant already exists: id={default_tenant.id}")
        
        # Create produtor-alfa tenant
        alfa_tenant = db.query(Tenant).filter(Tenant.slug == "produtor-alfa").first()
        if not alfa_tenant:
            alfa_tenant = Tenant(
                name="Produtor Alfa Ltda",
                slug="produtor-alfa",
                status="active",
                contact_email="admin@produtor-alfa.com",
            )
            db.add(alfa_tenant)
            db.flush()
            logger.info(f"Created produtor-alfa tenant: id={alfa_tenant.id}")
        else:
            logger.info(f"Produtor-alfa tenant already exists: id={alfa_tenant.id}")
        
        # Create produtor-beta tenant
        beta_tenant = db.query(Tenant).filter(Tenant.slug == "produtor-beta").first()
        if not beta_tenant:
            beta_tenant = Tenant(
                name="Produtor Beta S.A.",
                slug="produtor-beta",
                status="active",
                contact_email="admin@produtor-beta.com",
            )
            db.add(beta_tenant)
            db.flush()
            logger.info(f"Created produtor-beta tenant: id={beta_tenant.id}")
        else:
            logger.info(f"Produtor-beta tenant already exists: id={beta_tenant.id}")
        
        # ─── Users ─────────────────────────────────────────────────
        
        # Admin user
        admin_user = db.query(User).filter(User.email == "admin@h2v-trust.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@h2v-trust.com",
                password_hash=hash_password("H2v@Trust!2026"),
                full_name="Platform Administrator",
                is_active=True,
            )
            db.add(admin_user)
            db.flush()
            logger.info(f"Created admin user: id={admin_user.id}")
        else:
            logger.info(f"Admin user already exists: id={admin_user.id}")
        
        # Operator user for produtor-alfa
        operator_user = db.query(User).filter(User.email == "operator@produtor-alfa.com").first()
        if not operator_user:
            operator_user = User(
                email="operator@produtor-alfa.com",
                password_hash=hash_password("H2v@Trust!2026"),
                full_name="Alfa Operator",
                is_active=True,
            )
            db.add(operator_user)
            db.flush()
            logger.info(f"Created operator user: id={operator_user.id}")
        else:
            logger.info(f"Operator user already exists: id={operator_user.id}")
        
        # Auditor user
        auditor_user = db.query(User).filter(User.email == "auditor@h2v-trust.com").first()
        if not auditor_user:
            auditor_user = User(
                email="auditor@h2v-trust.com",
                password_hash=hash_password("H2v@Trust!2026"),
                full_name="Compliance Auditor",
                is_active=True,
            )
            db.add(auditor_user)
            db.flush()
            logger.info(f"Created auditor user: id={auditor_user.id}")
        else:
            logger.info(f"Auditor user already exists: id={auditor_user.id}")
        
        # ─── User-Tenant Associations ──────────────────────────────
        
        # Admin -> Default tenant (primary, role=admin)
        admin_ut = db.query(UserTenant).filter(
            UserTenant.user_id == admin_user.id,
            UserTenant.tenant_id == default_tenant.id,
        ).first()
        if not admin_ut:
            db.add(UserTenant(
                user_id=admin_user.id,
                tenant_id=default_tenant.id,
                role="admin",
                is_primary=True,
            ))
            logger.info("Linked admin user to default tenant (admin)")
        
        # Operator -> Produtor-Alfa (primary, role=operator)
        op_ut = db.query(UserTenant).filter(
            UserTenant.user_id == operator_user.id,
            UserTenant.tenant_id == alfa_tenant.id,
        ).first()
        if not op_ut:
            db.add(UserTenant(
                user_id=operator_user.id,
                tenant_id=alfa_tenant.id,
                role="operator",
                is_primary=True,
            ))
            logger.info("Linked operator user to produtor-alfa tenant (operator)")
        
        # Auditor -> Default tenant (primary, role=auditor)
        aud_ut = db.query(UserTenant).filter(
            UserTenant.user_id == auditor_user.id,
            UserTenant.tenant_id == default_tenant.id,
        ).first()
        if not aud_ut:
            db.add(UserTenant(
                user_id=auditor_user.id,
                tenant_id=default_tenant.id,
                role="auditor",
                is_primary=True,
            ))
            logger.info("Linked auditor user to default tenant (auditor)")
        
        db.commit()
        logger.info("Seed completed successfully!")
        
        # Print summary
        print("\n" + "="*60)
        print("USERS & TENANTS SEED SUMMARY")
        print("="*60)
        print(f"\nTenants:")
        for t in db.query(Tenant).all():
            print(f"  - {t.name} (slug={t.slug}, status={t.status})")
        
        print(f"\nUsers:")
        for u in db.query(User).all():
            print(f"  - {u.email} ({u.full_name})")
        
        print(f"\nAssociations:")
        for ut in db.query(UserTenant).all():
            user = db.query(User).filter(User.id == ut.user_id).first()
            tenant = db.query(Tenant).filter(Tenant.id == ut.tenant_id).first()
            print(f"  - {user.email} → {tenant.name} (role={ut.role}, primary={ut.is_primary})")
        
        print(f"\nLogin credentials (all users):")
        print(f"  Admin:    admin@h2v-trust.com / H2v@Trust!2026")
        print(f"  Operator: operator@produtor-alfa.com / H2v@Trust!2026")
        print(f"  Auditor:  auditor@h2v-trust.com / H2v@Trust!2026")
        print("="*60)
        
    except Exception as e:
        db.rollback()
        logger.error(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()

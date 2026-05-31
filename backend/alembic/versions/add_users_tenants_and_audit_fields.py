"""add users tenants and audit fields

Revision ID: add_users_tenants
Revises: 6b1464dad020
Create Date: 2026-05-11 11:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_users_tenants'
down_revision: Union[str, None] = '6b1464dad020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tenants table
    op.create_table(
        'tenants',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('slug', sa.String(100), nullable=False, unique=True),
        sa.Column('api_key_hash', sa.String(255), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='active'),
        sa.Column('contact_email', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_tenants_id', 'tenants', ['id'])
    op.create_index('ix_tenants_slug', 'tenants', ['slug'])
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'])
    
    # Create user_tenants association table
    op.create_table(
        'user_tenants',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tenant_id', sa.String(36), sa.ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(50), nullable=False, server_default='operator'),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('user_id', 'tenant_id', name='uq_user_tenant'),
    )
    op.create_index('ix_user_tenants_id', 'user_tenants', ['id'])
    op.create_index('ix_user_tenants_user_id', 'user_tenants', ['user_id'])
    op.create_index('ix_user_tenants_tenant_id', 'user_tenants', ['tenant_id'])
    
    # Add user_id and tenant_id columns to audit_logs
    op.add_column('audit_logs', sa.Column('user_id', sa.String(36), nullable=True))
    op.add_column('audit_logs', sa.Column('tenant_id', sa.String(36), nullable=True))
    op.create_index('ix_audit_logs_user_id', 'audit_logs', ['user_id'])
    op.create_index('ix_audit_logs_tenant_id', 'audit_logs', ['tenant_id'])


def downgrade() -> None:
    # Remove columns from audit_logs
    op.drop_index('ix_audit_logs_tenant_id', table_name='audit_logs')
    op.drop_index('ix_audit_logs_user_id', table_name='audit_logs')
    op.drop_column('audit_logs', 'tenant_id')
    op.drop_column('audit_logs', 'user_id')
    
    # Drop user_tenants table
    op.drop_index('ix_user_tenants_tenant_id', table_name='user_tenants')
    op.drop_index('ix_user_tenants_user_id', table_name='user_tenants')
    op.drop_index('ix_user_tenants_id', table_name='user_tenants')
    op.drop_table('user_tenants')
    
    # Drop users table
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    
    # Drop tenants table
    op.drop_index('ix_tenants_slug', table_name='tenants')
    op.drop_index('ix_tenants_id', table_name='tenants')
    op.drop_table('tenants')

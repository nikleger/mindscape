"""add mfa fields

Revision ID: add_mfa_fields
Revises: 
Create Date: 2024-04-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_mfa_fields'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add MFA fields to users table
    op.add_column('users', sa.Column('mfa_enabled', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('mfa_secret', sa.String(), nullable=True))
    op.add_column('users', sa.Column('mfa_backup_codes', postgresql.JSON(), nullable=True))

def downgrade() -> None:
    # Remove MFA fields from users table
    op.drop_column('users', 'mfa_backup_codes')
    op.drop_column('users', 'mfa_secret')
    op.drop_column('users', 'mfa_enabled') 
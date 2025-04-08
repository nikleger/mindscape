"""initial schema

Revision ID: initial_schema
Revises: 
Create Date: 2024-04-07 19:32:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create enum types
    op.execute("CREATE TYPE mindmapstatus AS ENUM ('draft', 'published', 'archived')")
    op.execute("CREATE TYPE collaborationrole AS ENUM ('viewer', 'editor', 'admin')")
    
    # Create users table
    op.create_table(
        'user',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, default=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('preferences', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create templates table
    op.create_table(
        'template',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('structure', postgresql.JSONB(), nullable=False),
        sa.Column('default_styles', postgresql.JSONB(), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=False, default=False),
        sa.Column('creator_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create mind_maps table
    op.create_table(
        'mind_map',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('status', postgresql.ENUM('draft', 'published', 'archived', name='mindmapstatus'), nullable=False),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('template_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('content', postgresql.JSONB(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id']),
        sa.ForeignKeyConstraint(['template_id'], ['template.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create nodes table
    op.create_table(
        'node',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('node_type', sa.String(50), nullable=False),
        sa.Column('x_position', sa.Integer(), nullable=False),
        sa.Column('y_position', sa.Integer(), nullable=False),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('mind_map_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('style', postgresql.JSONB(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['mind_map_id'], ['mind_map.id']),
        sa.ForeignKeyConstraint(['parent_id'], ['node.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create collaborations table
    op.create_table(
        'collaboration',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('mind_map_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', postgresql.ENUM('viewer', 'editor', 'admin', name='collaborationrole'), nullable=False),
        sa.Column('can_edit', sa.Boolean(), nullable=False),
        sa.Column('can_share', sa.Boolean(), nullable=False),
        sa.Column('can_delete', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['mind_map_id'], ['mind_map.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'mind_map_id', name='unique_collaboration')
    )

def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('collaboration')
    op.drop_table('node')
    op.drop_table('mind_map')
    op.drop_table('template')
    op.drop_table('user')
    
    # Drop enum types
    op.execute('DROP TYPE collaborationrole')
    op.execute('DROP TYPE mindmapstatus') 
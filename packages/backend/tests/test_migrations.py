import pytest
from alembic.command import upgrade, downgrade
from alembic.config import Config
from sqlalchemy import text
import os

def test_migrations_upgrade(alembic_config: Config, db_engine):
    # Run all migrations up
    upgrade(alembic_config, "head")
    
    # Verify tables exist
    with db_engine.connect() as conn:
        tables = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)).fetchall()
        
        table_names = [t[0] for t in tables]
        assert "users" in table_names
        assert "mind_maps" in table_names
        assert "nodes" in table_names
        assert "edges" in table_names
        assert "templates" in table_names

def test_migrations_downgrade(alembic_config: Config, db_engine):
    # First upgrade to head
    upgrade(alembic_config, "head")
    
    # Then downgrade to base
    downgrade(alembic_config, "base")
    
    # Verify tables are removed
    with db_engine.connect() as conn:
        tables = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)).fetchall()
        
        table_names = [t[0] for t in tables]
        assert "users" not in table_names
        assert "mind_maps" not in table_names
        assert "nodes" not in table_names
        assert "edges" not in table_names
        assert "templates" not in table_names

def test_migration_rollback(alembic_config: Config, db_engine):
    # Test that we can rollback migrations
    # Upgrade to head
    upgrade(alembic_config, "head")
    
    # Get current revision
    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT version_num FROM alembic_version")).fetchone()
        current_revision = result[0]
    
    # Downgrade one step
    downgrade(alembic_config, "-1")
    
    # Verify revision changed
    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT version_num FROM alembic_version")).fetchone()
        assert result[0] != current_revision

def test_migration_data_integrity(alembic_config: Config, db_engine):
    # Test that data is preserved during migrations
    # Upgrade to head
    upgrade(alembic_config, "head")
    
    # Insert test data
    with db_engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO users (email, password_hash, full_name)
            VALUES ('test@example.com', 'hash', 'Test User')
        """))
        conn.execute(text("""
            INSERT INTO mind_maps (title, description, user_id)
            VALUES ('Test Map', 'Description', 1)
        """))
    
    # Downgrade and upgrade
    downgrade(alembic_config, "base")
    upgrade(alembic_config, "head")
    
    # Verify data is preserved
    with db_engine.connect() as conn:
        users = conn.execute(text("SELECT * FROM users")).fetchall()
        mind_maps = conn.execute(text("SELECT * FROM mind_maps")).fetchall()
        assert len(users) == 1
        assert len(mind_maps) == 1

def test_migration_foreign_keys(alembic_config: Config, db_engine):
    # Test foreign key constraints
    upgrade(alembic_config, "head")
    
    # Try to insert data with invalid foreign key
    with db_engine.connect() as conn:
        with pytest.raises(Exception):
            conn.execute(text("""
                INSERT INTO mind_maps (title, description, user_id)
                VALUES ('Test Map', 'Description', 999)
            """))
    
    # Insert valid data
    with db_engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO users (email, password_hash, full_name)
            VALUES ('test@example.com', 'hash', 'Test User')
        """))
        conn.execute(text("""
            INSERT INTO mind_maps (title, description, user_id)
            VALUES ('Test Map', 'Description', 1)
        """))

def test_migration_indexes(alembic_config: Config, db_engine):
    # Test that indexes are created correctly
    upgrade(alembic_config, "head")
    
    with db_engine.connect() as conn:
        indexes = conn.execute(text("""
            SELECT indexname, tablename 
            FROM pg_indexes 
            WHERE schemaname = 'public'
        """)).fetchall()
        
        index_names = [i[0] for i in indexes]
        assert "ix_users_email" in index_names
        assert "ix_mind_maps_user_id" in index_names

def test_migration_constraints(alembic_config: Config, db_engine):
    # Test that constraints are created correctly
    upgrade(alembic_config, "head")
    
    with db_engine.connect() as conn:
        constraints = conn.execute(text("""
            SELECT constraint_name, table_name 
            FROM information_schema.table_constraints 
            WHERE constraint_schema = 'public'
        """)).fetchall()
        
        constraint_names = [c[0] for c in constraints]
        assert "users_email_key" in constraint_names
        assert "mind_maps_pkey" in constraint_names 
# Database Setup Script
# This script sets up the local development database for Mindscape

# Configuration
$POSTGRES_USER = "postgres"
$POSTGRES_PASSWORD = "postgres"
$POSTGRES_HOST = "localhost"
$POSTGRES_PORT = "5432"
$DEV_DB = "mindscape_dev"
$TEST_DB = "mindscape_test"
$PROJECT_ROOT = $PSScriptRoot | Split-Path -Parent
$BACKEND_PATH = "$PROJECT_ROOT\packages\backend"

# Function to check if PostgreSQL is running
function Test-PostgreSQLRunning {
    try {
        $env:PGPASSWORD = $POSTGRES_PASSWORD
        psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -c "SELECT 1" -d postgres -q
        return $true
    } catch {
        return $false
    }
}

# Function to check if a database exists
function Test-DatabaseExists {
    param($dbname)
    try {
        $env:PGPASSWORD = $POSTGRES_PASSWORD
        psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -c "SELECT 1" -d $dbname -q
        return $true
    } catch {
        return $false
    }
}

# Check if PostgreSQL is running
if (-not (Test-PostgreSQLRunning)) {
    Write-Host "PostgreSQL is not running. Please start PostgreSQL and try again." -ForegroundColor Red
    exit 1
}

# Create development database if it doesn't exist
if (-not (Test-DatabaseExists $DEV_DB)) {
    Write-Host "Creating development database..." -ForegroundColor Cyan
    $env:PGPASSWORD = $POSTGRES_PASSWORD
    psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -c "CREATE DATABASE $DEV_DB;"
    Write-Host "Development database created successfully" -ForegroundColor Green
}

# Create test database if it doesn't exist
if (-not (Test-DatabaseExists $TEST_DB)) {
    Write-Host "Creating test database..." -ForegroundColor Cyan
    $env:PGPASSWORD = $POSTGRES_PASSWORD
    psql -U $POSTGRES_USER -h $POSTGRES_HOST -p $POSTGRES_PORT -c "CREATE DATABASE $TEST_DB;"
    Write-Host "Test database created successfully" -ForegroundColor Green
}

# Run database migrations
Write-Host "Running database migrations..." -ForegroundColor Cyan
Set-Location $BACKEND_PATH
try {
    # Development database migrations
    $env:DATABASE_URL = "postgresql://$POSTGRES_USER`:$POSTGRES_PASSWORD@$POSTGRES_HOST`:$POSTGRES_PORT/$DEV_DB"
    alembic upgrade head
    Write-Host "Development database migrations completed successfully" -ForegroundColor Green

    # Test database migrations
    $env:DATABASE_URL = "postgresql://$POSTGRES_USER`:$POSTGRES_PASSWORD@$POSTGRES_HOST`:$POSTGRES_PORT/$TEST_DB"
    alembic upgrade head
    Write-Host "Test database migrations completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Error running migrations: $_" -ForegroundColor Red
    exit 1
}

# Seed development database
Write-Host "Seeding development database..." -ForegroundColor Cyan
try {
    $env:DATABASE_URL = "postgresql://$POSTGRES_USER`:$POSTGRES_PASSWORD@$POSTGRES_HOST`:$POSTGRES_PORT/$DEV_DB"
    python -c "
import asyncio
from app.db.session import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.models.mind_map import MindMap
from app.models.node import Node
from app.models.edge import Edge
from app.models.template import Template
from datetime import datetime
from uuid import uuid4

async def seed_database():
    db = SessionLocal()
    try:
        # Create test user
        user = User(
            id=uuid4(),
            email='test@example.com',
            name='Test User',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()

        # Create test mind map
        mind_map = MindMap(
            id=uuid4(),
            title='Sample Mind Map',
            owner_id=user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(mind_map)
        db.commit()

        # Create test nodes
        root_node = Node(
            id=uuid4(),
            mind_map_id=mind_map.id,
            content='Root Node',
            position={'x': 0, 'y': 0},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(root_node)

        child_node = Node(
            id=uuid4(),
            mind_map_id=mind_map.id,
            content='Child Node',
            position={'x': 100, 'y': 100},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(child_node)
        db.commit()

        # Create test edge
        edge = Edge(
            id=uuid4(),
            source_id=root_node.id,
            target_id=child_node.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(edge)
        db.commit()

        # Create test template
        template = Template(
            id=uuid4(),
            name='Basic Template',
            description='A basic mind map template',
            nodes=[{'content': 'Root', 'position': {'x': 0, 'y': 0}}],
            edges=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(template)
        db.commit()

    finally:
        db.close()

asyncio.run(seed_database())
"
    Write-Host "Development database seeded successfully" -ForegroundColor Green
} catch {
    Write-Host "Error seeding database: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`nDatabase setup complete!" -ForegroundColor Green
Write-Host "`nDevelopment database: $DEV_DB" -ForegroundColor Yellow
Write-Host "Test database: $TEST_DB" -ForegroundColor Yellow
Write-Host "`nYou can now run the application with the development database." -ForegroundColor Yellow 
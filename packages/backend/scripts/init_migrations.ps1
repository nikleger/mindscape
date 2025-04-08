# Create migrations directory if it doesn't exist
if (-not (Test-Path -Path "migrations")) {
    New-Item -ItemType Directory -Path "migrations"
}

# Initialize alembic
alembic init migrations

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

Write-Host "Migration files created successfully!" 
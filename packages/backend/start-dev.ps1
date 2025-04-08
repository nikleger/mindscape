# Development startup script for Mindscape backend
Write-Host "Starting Mindscape backend development environment..."

# Check if Python is installed
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python is not installed or not in PATH"
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
Write-Host "Initializing database..."
alembic upgrade head

# Start the development server
Write-Host "Starting development server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
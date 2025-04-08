# Activate virtual environment if it exists
if (Test-Path -Path "venv/Scripts/Activate.ps1") {
    . venv/Scripts/Activate.ps1
}

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
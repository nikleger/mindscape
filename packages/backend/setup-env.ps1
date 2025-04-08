# Required directories validation
$requiredDirs = @(
    "test_history",
    "archived_tests",
    "static/icons",
    "static/styles",
    "app/models",
    "app/routes",
    "app/services",
    "tests/unit",
    "tests/integration",
    "tests/e2e"
)

Write-Host "Validating directory structure..." -ForegroundColor Cyan

foreach ($dir in $requiredDirs) {
    if (-not (Test-Path $dir)) {
        Write-Host "Creating directory: $dir" -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "Directory structure validated." -ForegroundColor Green

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
.\venv\Scripts\activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Install Playwright browsers
Write-Host "Installing Playwright browsers..." -ForegroundColor Cyan
playwright install

Write-Host "Environment setup complete!" -ForegroundColor Green
Write-Host "You can now run 'start-dev.ps1' to start the development server." -ForegroundColor Yellow 
Write-Host "Environment setup complete!" 
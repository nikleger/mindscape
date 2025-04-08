# Test All Script
# This script runs all tests in the project

# Configuration
$PROJECT_ROOT = $PSScriptRoot | Split-Path -Parent
$VENV_PATH = "$PROJECT_ROOT\.venv"
$FRONTEND_PATH = "$PROJECT_ROOT\packages\frontend"
$BACKEND_PATH = "$PROJECT_ROOT\packages\backend"

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $command) { return $true }
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
}

# Check for required tools
Write-Host "Checking for required tools..." -ForegroundColor Cyan

# Check for Python
if (-not (Test-CommandExists "python")) {
    Write-Host "Python not found. Please install Python from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Check for Node.js
if (-not (Test-CommandExists "node")) {
    Write-Host "Node.js not found. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "$VENV_PATH\Scripts\Activate.ps1"

# Run backend tests
Write-Host "`nRunning backend tests..." -ForegroundColor Cyan
Set-Location $BACKEND_PATH
pytest --cov=app --cov-report=term-missing

# Run frontend tests
Write-Host "`nRunning frontend tests..." -ForegroundColor Cyan
Set-Location $FRONTEND_PATH
npm test

# Run E2E tests
Write-Host "`nRunning E2E tests..." -ForegroundColor Cyan
npm run test:e2e

# Run security tests
Write-Host "`nRunning security tests..." -ForegroundColor Cyan
Set-Location $BACKEND_PATH
safety check
npm audit

# Run linting
Write-Host "`nRunning linting..." -ForegroundColor Cyan
Set-Location $BACKEND_PATH
black --check .
flake8 .

Set-Location $FRONTEND_PATH
npm run lint

Write-Host "`nAll tests completed!" -ForegroundColor Green 
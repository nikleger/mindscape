# Development Environment Setup Script
# This script sets up the development environment for Mindscape

# Configuration
$PYTHON_VERSION = "3.12"
$NODE_VERSION = "20"
$POSTGRES_VERSION = "15"
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

# Function to check if running as administrator
function Test-Administrator {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to generate a secure random string
function Get-RandomSecureString {
    param([int]$Length = 32)
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?'
    $random = New-Object System.Random
    $string = -join (1..$Length | ForEach-Object { $chars[$random.Next($chars.Length)] })
    return $string
}

# Check if running as administrator
if (-not (Test-Administrator)) {
    Write-Host "Please run this script as Administrator" -ForegroundColor Red
    exit 1
}

# Check for required tools
Write-Host "Checking for required tools..." -ForegroundColor Cyan

# Check for Python
if (-not (Test-CommandExists "python")) {
    Write-Host "Python not found. Please install Python $PYTHON_VERSION from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Verify Python version
$pythonVersion = python --version
if (-not ($pythonVersion -match "Python 3\.(12|11)")) {
    Write-Host "Python version must be 3.12 or 3.11. Found: $pythonVersion" -ForegroundColor Red
    exit 1
}

# Check for Node.js
if (-not (Test-CommandExists "node")) {
    Write-Host "Node.js not found. Please install Node.js $NODE_VERSION from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check for Git
if (-not (Test-CommandExists "git")) {
    Write-Host "Git not found. Please install Git from https://git-scm.com/downloads" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
if (Test-Path $VENV_PATH) {
    Write-Host "Virtual environment already exists. Removing..." -ForegroundColor Yellow
    Remove-Item -Path $VENV_PATH -Recurse -Force
}
python -m venv $VENV_PATH

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "$VENV_PATH\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r "$BACKEND_PATH\requirements.txt"
pip install -r "$BACKEND_PATH\requirements-dev.txt"

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Cyan
Set-Location $FRONTEND_PATH
npm install

# Create local configuration files
Write-Host "Creating local configuration files..." -ForegroundColor Cyan

# Generate secure keys
$SECRET_KEY = Get-RandomSecureString
$JWT_SECRET_KEY = Get-RandomSecureString

# Backend .env file
@"
# Backend Configuration

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mindscape_dev
TEST_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mindscape_test

# Security
SECRET_KEY=$SECRET_KEY
JWT_SECRET_KEY=$JWT_SECRET_KEY
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
DEBUG=True
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=json

# External Services
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# Email (Development)
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USER=your-mailtrap-user
SMTP_PASSWORD=your-mailtrap-password
EMAIL_FROM=noreply@mindscape.dev

# Feature Flags
ENABLE_WEBSOCKETS=True
ENABLE_EMAIL_VERIFICATION=False
ENABLE_RATE_LIMITING=True
"@ | Out-File -FilePath "$BACKEND_PATH\.env" -Encoding utf8

# Frontend .env file
@"
# Frontend Configuration

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_API_VERSION=v1

# Authentication
NEXT_PUBLIC_AUTH_ENABLED=true
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
NEXT_PUBLIC_GITHUB_CLIENT_ID=your-github-client-id

# Feature Flags
NEXT_PUBLIC_ENABLE_WEBSOCKETS=true
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_OFFLINE_MODE=true

# Application
NEXT_PUBLIC_APP_NAME=Mindscape
NEXT_PUBLIC_APP_DESCRIPTION="Enterprise Mind Mapping Platform"
NEXT_PUBLIC_APP_VERSION=0.1.0

# Development
NEXT_PUBLIC_DEBUG=true
NEXT_PUBLIC_DEV_TOOLS=true

# External Services
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key

# Analytics (Development)
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
NEXT_PUBLIC_ANALYTICS_ENABLED=false

# Error Tracking
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
NEXT_PUBLIC_SENTRY_ENABLED=false
"@ | Out-File -FilePath "$FRONTEND_PATH\.env.local" -Encoding utf8

# Create local database
Write-Host "Setting up local database..." -ForegroundColor Cyan
try {
    $env:PGPASSWORD = "postgres"
    psql -U postgres -c "CREATE DATABASE mindscape_dev;" -ErrorAction Stop
    psql -U postgres -c "CREATE DATABASE mindscape_test;" -ErrorAction Stop
    Write-Host "Databases created successfully" -ForegroundColor Green
} catch {
    Write-Host "Error creating databases. Please ensure PostgreSQL is running and accessible." -ForegroundColor Red
    Write-Host "Error details: $_" -ForegroundColor Red
    exit 1
}

# Run database migrations
Write-Host "Running database migrations..." -ForegroundColor Cyan
Set-Location $BACKEND_PATH
try {
    alembic upgrade head
    Write-Host "Migrations completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Error running migrations. Please check the error message above." -ForegroundColor Red
    exit 1
}

# Build frontend
Write-Host "Building frontend..." -ForegroundColor Cyan
Set-Location $FRONTEND_PATH
try {
    npm run build
    Write-Host "Frontend build completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Error building frontend. Please check the error message above." -ForegroundColor Red
    exit 1
}

# Create development certificates
Write-Host "Creating development SSL certificates..." -ForegroundColor Cyan
$CERT_PATH = "$PROJECT_ROOT\certs"
if (-not (Test-Path $CERT_PATH)) {
    New-Item -ItemType Directory -Path $CERT_PATH
}
try {
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$CERT_PATH\key.pem" -out "$CERT_PATH\cert.pem" -subj "/CN=localhost"
    Write-Host "SSL certificates created successfully" -ForegroundColor Green
} catch {
    Write-Host "Error creating SSL certificates. Please ensure OpenSSL is installed." -ForegroundColor Red
    exit 1
}

# Create startup scripts
Write-Host "Creating startup scripts..." -ForegroundColor Cyan

# Backend startup script
@"
@echo off
call $VENV_PATH\Scripts\activate.bat
cd $BACKEND_PATH
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --ssl-keyfile $CERT_PATH\key.pem --ssl-certfile $CERT_PATH\cert.pem
"@ | Out-File -FilePath "$PROJECT_ROOT\start-backend.bat" -Encoding ascii

# Frontend startup script
@"
@echo off
cd $FRONTEND_PATH
npm run dev
"@ | Out-File -FilePath "$PROJECT_ROOT\start-frontend.bat" -Encoding ascii

Write-Host "`nDevelopment environment setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Update the following configuration files with your specific values:" -ForegroundColor Yellow
Write-Host "   - $BACKEND_PATH\.env" -ForegroundColor Yellow
Write-Host "   - $FRONTEND_PATH\.env.local" -ForegroundColor Yellow
Write-Host "2. To start the development servers:" -ForegroundColor Yellow
Write-Host "   a. Open a terminal and run: .\start-backend.bat" -ForegroundColor Yellow
Write-Host "   b. Open another terminal and run: .\start-frontend.bat" -ForegroundColor Yellow
Write-Host "`nThe application will be available at:" -ForegroundColor Yellow
Write-Host "Frontend: https://localhost:3000" -ForegroundColor Yellow
Write-Host "Backend: https://localhost:8000" -ForegroundColor Yellow
Write-Host "`nAPI Documentation: https://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "`nNote: Make sure to keep your .env files secure and never commit them to version control." -ForegroundColor Yellow 
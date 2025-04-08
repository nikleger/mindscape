# Function to run command and check for errors
function Invoke-CommandWithCheck {
    param(
        [string]$Command,
        [string]$ErrorMessage
    )
    
    try {
        Invoke-Expression $Command
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error: $ErrorMessage" -ForegroundColor Red
            exit 1
        }
    }
    catch {
        Write-Host "Error: $ErrorMessage" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
}

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm install --save-dev @testing-library/react @testing-library/jest-dom jest ts-jest cypress k6 pa11y @types/jest @types/testing-library__react" -ErrorMessage "Failed to install Node.js dependencies"

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "pip install pytest pytest-cov" -ErrorMessage "Failed to install Python dependencies"

# Install Go dependencies
Write-Host "Installing Go dependencies..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "go get github.com/gruntwork-io/terratest" -ErrorMessage "Failed to install Go dependencies"

# Install k6 (Windows)
Write-Host "Installing k6..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "choco install k6 -y" -ErrorMessage "Failed to install k6"

# Run tests
Write-Host "Running tests..." -ForegroundColor Green

# Frontend unit tests
Write-Host "Running frontend unit tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm run test:unit" -ErrorMessage "Frontend unit tests failed"

# Backend unit tests
Write-Host "Running backend unit tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "pytest tests/unit" -ErrorMessage "Backend unit tests failed"

# E2E tests
Write-Host "Running E2E tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm run test:e2e" -ErrorMessage "E2E tests failed"

# Performance tests
Write-Host "Running performance tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm run test:performance" -ErrorMessage "Performance tests failed"

# Accessibility tests
Write-Host "Running accessibility tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm run test:accessibility" -ErrorMessage "Accessibility tests failed"

# Documentation tests
Write-Host "Running documentation tests..." -ForegroundColor Green
$currentLocation = Get-Location
Set-Location -Path "docs"
Invoke-CommandWithCheck -Command "npm install" -ErrorMessage "Failed to install documentation dependencies"
Invoke-CommandWithCheck -Command "npx docusaurus check-links" -ErrorMessage "Found broken links"
Invoke-CommandWithCheck -Command "npx docusaurus check-content" -ErrorMessage "Found broken references"
Invoke-CommandWithCheck -Command "npm run build" -ErrorMessage "Documentation build failed"
Set-Location -Path $currentLocation

Write-Host "All tests completed successfully!" -ForegroundColor Green 
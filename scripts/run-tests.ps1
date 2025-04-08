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

# Run all tests
Write-Host "Running all tests..." -ForegroundColor Green

# Run frontend unit tests
Write-Host "Running frontend unit tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm run test:unit" -ErrorMessage "Frontend unit tests failed"

# Run backend unit tests
Write-Host "Running backend unit tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "pytest tests/unit" -ErrorMessage "Backend unit tests failed"

# Run E2E tests
Write-Host "Running E2E tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm run test:e2e" -ErrorMessage "E2E tests failed"

# Run performance tests
Write-Host "Running performance tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm run test:performance" -ErrorMessage "Performance tests failed"

# Run accessibility tests
Write-Host "Running accessibility tests..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm run test:accessibility" -ErrorMessage "Accessibility tests failed"

# Update and deploy test dashboard
Write-Host "Updating and deploying test dashboard..." -ForegroundColor Green
Set-Location -Path "docs"
Invoke-CommandWithCheck -Command "npm run build" -ErrorMessage "Documentation build failed"
Invoke-CommandWithCheck -Command "npm run deploy" -ErrorMessage "Documentation deployment failed"

Write-Host "All tests completed and dashboard deployed successfully!" -ForegroundColor Green 
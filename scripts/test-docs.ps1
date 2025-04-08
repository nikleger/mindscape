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

# Navigate to docs directory
Set-Location -Path "$PSScriptRoot\..\docs"

# Install Docusaurus dependencies
Write-Host "Installing Docusaurus dependencies..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm install" -ErrorMessage "Failed to install dependencies"

# Check for broken links
Write-Host "Checking for broken links..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npx docusaurus check-links" -ErrorMessage "Found broken links"

# Check for broken references
Write-Host "Checking for broken references..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npx docusaurus check-content" -ErrorMessage "Found broken references"

# Build documentation
Write-Host "Building documentation..." -ForegroundColor Green
Invoke-CommandWithCheck -Command "npm run build" -ErrorMessage "Documentation build failed"

Write-Host "Documentation tests completed successfully!" -ForegroundColor Green 
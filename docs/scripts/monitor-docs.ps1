# Documentation Monitoring Script
$ErrorActionPreference = "Stop"

# Configuration
$healthCheckUrl = "http://localhost:3001/health"
$alertThreshold = 3  # Number of consecutive failures before alerting
$failureCount = 0
$lastAlertTime = $null
$alertCooldownMinutes = 30

# Setup function
function Initialize-Monitoring {
    Write-Host "Setting up documentation monitoring..." -ForegroundColor Cyan
    
    # Check if Node.js is installed
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        Write-Host "Installing Node.js..." -ForegroundColor Yellow
        winget install OpenJS.NodeJS.LTS
    }
    
    # Check if npm dependencies are installed
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing npm dependencies..." -ForegroundColor Yellow
        npm install
    }
    
    # Start health check server if not running
    $healthServer = Get-Process -Name "node" -ErrorAction SilentlyContinue | 
        Where-Object { $_.CommandLine -like "*health.js*" }
    
    if (-not $healthServer) {
        Write-Host "Starting health check server..." -ForegroundColor Yellow
        Start-Process -FilePath "node" -ArgumentList "health.js" -WindowStyle Hidden
        Start-Sleep -Seconds 5  # Wait for server to start
    }
}

function Send-Alert {
    param (
        [string]$message
    )
    
    # TODO: Implement actual alerting (email, Slack, etc.)
    Write-Host "ALERT: $message" -ForegroundColor Red
    
    # Log alert
    $logMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'): $message"
    Add-Content -Path "monitoring.log" -Value $logMessage
}

function Test-HealthEndpoint {
    try {
        $response = Invoke-RestMethod -Uri $healthCheckUrl -Method Get
        return $response
    }
    catch {
        return @{
            status = "unhealthy"
            error = $_.Exception.Message
        }
    }
}

function Test-DocumentationFiles {
    param (
        [object]$healthResponse
    )
    
    if ($healthResponse.checks.documentation.status -eq $false) {
        $missingFiles = $healthResponse.checks.documentation.missingFiles -join ", "
        Send-Alert "Missing documentation files: $missingFiles"
    }
}

function Test-BuildProcess {
    param (
        [object]$healthResponse
    )
    
    if ($healthResponse.checks.build.status -eq $false) {
        Send-Alert "Build process failed: $($healthResponse.checks.build.error)"
    }
}

function Test-Links {
    param (
        [object]$healthResponse
    )
    
    if ($healthResponse.checks.links.status -eq $false) {
        $brokenLinks = $healthResponse.checks.links.brokenLinks -join ", "
        Send-Alert "Broken links detected: $brokenLinks"
    }
}

# Main script
try {
    # Initialize monitoring environment
    Initialize-Monitoring
    
    # Main monitoring loop
    while ($true) {
        try {
            $healthResponse = Test-HealthEndpoint
            
            if ($healthResponse.status -eq "healthy") {
                $failureCount = 0
                Write-Host "Documentation is healthy" -ForegroundColor Green
                
                # Check individual components
                Test-DocumentationFiles -healthResponse $healthResponse
                Test-BuildProcess -healthResponse $healthResponse
                Test-Links -healthResponse $healthResponse
            }
            else {
                $failureCount++
                Write-Host "Documentation check failed: $($healthResponse.error)" -ForegroundColor Yellow
                
                if ($failureCount -ge $alertThreshold) {
                    $timeSinceLastAlert = if ($lastAlertTime) {
                        (Get-Date) - $lastAlertTime
                    }
                    else {
                        [TimeSpan]::MaxValue
                    }
                    
                    if ($timeSinceLastAlert.TotalMinutes -ge $alertCooldownMinutes) {
                        Send-Alert "Documentation is unhealthy: $($healthResponse.error)"
                        $lastAlertTime = Get-Date
                    }
                }
            }
        }
        catch {
            Write-Host "Monitoring error: $_" -ForegroundColor Red
            Send-Alert "Monitoring script error: $_"
        }
        
        # Wait before next check
        Start-Sleep -Seconds 60
    }
}
catch {
    Write-Host "Fatal error: $_" -ForegroundColor Red
    exit 1
} 
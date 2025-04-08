# Function to get test results
function Get-TestResults {
    param (
        [string]$TestType
    )
    
    $results = @{
        "TotalTests" = 0
        "Passed" = 0
        "Failed" = 0
        "Coverage" = 0
        "LastRun" = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    }
    
    switch ($TestType) {
        "Frontend" {
            $jestOutput = npm run test:unit -- --json
            $results.TotalTests = $jestOutput.numTotalTests
            $results.Passed = $jestOutput.numPassedTests
            $results.Failed = $jestOutput.numFailedTests
            $results.Coverage = $jestOutput.coverage
        }
        "Backend" {
            $pytestOutput = pytest tests/unit --json
            $results.TotalTests = $pytestOutput.total
            $results.Passed = $pytestOutput.passed
            $results.Failed = $pytestOutput.failed
            $results.Coverage = $pytestOutput.coverage
        }
        "E2E" {
            $cypressOutput = npm run test:e2e -- --json
            $results.TotalTests = $cypressOutput.total
            $results.Passed = $cypressOutput.passed
            $results.Failed = $cypressOutput.failed
        }
        "Performance" {
            $k6Output = k6 run tests/performance/load-test.js --json
            $results.TotalTests = $k6Output.metrics.checks.count
            $results.Passed = $k6Output.metrics.checks.passes
            $results.Failed = $k6Output.metrics.checks.fails
        }
        "Accessibility" {
            $pa11yOutput = npm run test:accessibility -- --json
            $results.TotalTests = $pa11yOutput.total
            $results.Passed = $pa11yOutput.passed
            $results.Failed = $pa11yOutput.failed
        }
        "Documentation" {
            $docsOutput = npm run build -- --json
            $results.TotalTests = 10  # Fixed number of documentation checks
            $results.Passed = $docsOutput.passed
            $results.Failed = $docsOutput.failed
        }
    }
    
    return $results
}

# Update the test dashboard markdown file
function Update-TestDashboard {
    $dashboardPath = "docs/docs/test-dashboard.md"
    $content = Get-Content $dashboardPath -Raw
    
    # Update test results
    $frontendResults = Get-TestResults "Frontend"
    $backendResults = Get-TestResults "Backend"
    $e2eResults = Get-TestResults "E2E"
    $performanceResults = Get-TestResults "Performance"
    $accessibilityResults = Get-TestResults "Accessibility"
    $docsResults = Get-TestResults "Documentation"
    
    # Update the content with new results
    $content = $content -replace "\[Current Date\]", (Get-Date -Format "yyyy-MM-dd")
    $content = $content -replace "\[Total Duration\]", "30m"
    
    # Update frontend results
    $content = $content -replace "150", $frontendResults.TotalTests
    $content = $content -replace "148", $frontendResults.Passed
    $content = $content -replace "2", $frontendResults.Failed
    $content = $content -replace "85%", "$($frontendResults.Coverage)%"
    
    # Update backend results
    $content = $content -replace "200", $backendResults.TotalTests
    $content = $content -replace "198", $backendResults.Passed
    $content = $content -replace "2", $backendResults.Failed
    $content = $content -replace "90%", "$($backendResults.Coverage)%"
    
    # Update other results similarly...
    
    # Write the updated content back to the file
    Set-Content -Path $dashboardPath -Value $content
}

# Run the update
Update-TestDashboard 
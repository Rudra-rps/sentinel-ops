# 🐳 SentinelOps Docker Deployment Test Script
# Quick test script for Docker Compose deployment

Write-Host "`n" -NoNewline
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SentinelOps Docker Deployment Tests  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n"

$testsPassed = 0
$testsFailed = 0

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$ExpectedStatus = "200"
    )
    
    Write-Host "Testing: " -NoNewline
    Write-Host "$Name" -ForegroundColor Yellow
    Write-Host "  URL: $Url" -ForegroundColor Gray
    
    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq $ExpectedStatus) {
            Write-Host "  ✅ PASS" -ForegroundColor Green
            Write-Host "     Status: $($response.StatusCode)" -ForegroundColor Gray
            $script:testsPassed++
            return $true
        } else {
            Write-Host "  ❌ FAIL" -ForegroundColor Red
            Write-Host "     Expected: $ExpectedStatus, Got: $($response.StatusCode)" -ForegroundColor Red
            $script:testsFailed++
            return $false
        }
    } catch {
        Write-Host "  ❌ FAIL" -ForegroundColor Red
        Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Red
        $script:testsFailed++
        return $false
    }
    Write-Host ""
}

function Test-JsonEndpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$ExpectedKey
    )
    
    Write-Host "Testing: " -NoNewline
    Write-Host "$Name" -ForegroundColor Yellow
    Write-Host "  URL: $Url" -ForegroundColor Gray
    
    try {
        $response = Invoke-RestMethod -Uri $Url -UseBasicParsing -ErrorAction Stop
        if ($ExpectedKey -and $response.PSObject.Properties.Name -contains $ExpectedKey) {
            Write-Host "  ✅ PASS" -ForegroundColor Green
            Write-Host "     Found key: $ExpectedKey" -ForegroundColor Gray
            $script:testsPassed++
            return $response
        } elseif (-not $ExpectedKey) {
            Write-Host "  ✅ PASS" -ForegroundColor Green
            $script:testsPassed++
            return $response
        } else {
            Write-Host "  ❌ FAIL" -ForegroundColor Red
            Write-Host "     Missing key: $ExpectedKey" -ForegroundColor Red
            $script:testsFailed++
            return $null
        }
    } catch {
        Write-Host "  ❌ FAIL" -ForegroundColor Red
        Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Red
        $script:testsFailed++
        return $null
    }
    Write-Host ""
}

# Test 1: Check Docker containers are running
Write-Host "`n📦 Phase 1: Docker Container Status" -ForegroundColor Cyan
Write-Host "====================================`n" -ForegroundColor Cyan

$containers = docker-compose ps --format json | ConvertFrom-Json
foreach ($container in $containers) {
    $name = $container.Name
    $state = $container.State
    $health = $container.Health
    
    Write-Host "Container: " -NoNewline
    Write-Host "$name" -ForegroundColor Yellow
    
    if ($state -eq "running") {
        Write-Host "  ✅ State: $state" -ForegroundColor Green
        $script:testsPassed++
    } else {
        Write-Host "  ❌ State: $state" -ForegroundColor Red
        $script:testsFailed++
    }
    
    if ($health) {
        if ($health -eq "healthy") {
            Write-Host "  ✅ Health: $health" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  Health: $health" -ForegroundColor Yellow
        }
    }
    Write-Host ""
}

# Test 2: Backend API Tests
Write-Host "`n🔧 Phase 2: Backend API Tests" -ForegroundColor Cyan
Write-Host "==============================`n" -ForegroundColor Cyan

Test-Endpoint -Name "Frontend (HTML)" -Url "http://localhost"
Test-Endpoint -Name "Backend Health Check" -Url "http://localhost:8000/health"
Test-Endpoint -Name "API Documentation (Swagger)" -Url "http://localhost:8000/docs"

$healthData = Test-JsonEndpoint -Name "Health Endpoint (JSON)" -Url "http://localhost:8000/health" -ExpectedKey "status"
if ($healthData) {
    Write-Host "  📊 Health Details:" -ForegroundColor Cyan
    Write-Host "     Status: $($healthData.status)" -ForegroundColor Gray
    Write-Host "     Timestamp: $($healthData.timestamp)" -ForegroundColor Gray
    Write-Host ""
}

$metricsData = Test-JsonEndpoint -Name "Metrics Endpoint" -Url "http://localhost:8000/metrics" -ExpectedKey "success"
if ($metricsData) {
    Write-Host "  📊 Metrics Details:" -ForegroundColor Cyan
    Write-Host "     Success: $($metricsData.success)" -ForegroundColor Gray
    Write-Host "     Namespace: $($metricsData.namespace)" -ForegroundColor Gray
    Write-Host ""
}

# Test 3: Frontend Tests
Write-Host "`n🎨 Phase 3: Frontend Tests" -ForegroundColor Cyan
Write-Host "===========================`n" -ForegroundColor Cyan

Test-Endpoint -Name "Frontend Root" -Url "http://localhost"
Test-Endpoint -Name "Frontend Assets (should 404)" -Url "http://localhost/assets/index.js" -ExpectedStatus "404"

# Test 4: Container Logs Check
Write-Host "`n📝 Phase 4: Container Logs" -ForegroundColor Cyan
Write-Host "===========================`n" -ForegroundColor Cyan

Write-Host "Recent Backend Logs:" -ForegroundColor Yellow
docker-compose logs --tail=5 backend
Write-Host ""

Write-Host "Recent Frontend Logs:" -ForegroundColor Yellow
docker-compose logs --tail=5 frontend
Write-Host ""

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "           Test Summary                 " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Passed: " -NoNewline -ForegroundColor Green
Write-Host "$testsPassed" -ForegroundColor White
Write-Host "❌ Failed: " -NoNewline -ForegroundColor Red
Write-Host "$testsFailed" -ForegroundColor White
Write-Host "📊 Total:  " -NoNewline -ForegroundColor Cyan
Write-Host "$($testsPassed + $testsFailed)" -ForegroundColor White
Write-Host ""

if ($testsFailed -eq 0) {
    Write-Host "🎉 All tests passed! Your deployment is healthy!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some tests failed. Check the output above for details." -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "         Access Points                  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Frontend:    " -NoNewline
Write-Host "http://localhost" -ForegroundColor Cyan
Write-Host "🔧 Backend API: " -NoNewline
Write-Host "http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs:    " -NoNewline
Write-Host "http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

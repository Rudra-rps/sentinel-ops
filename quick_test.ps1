# SentinelOps Quick Test Script (PowerShell)
# Run this to verify your system is ready

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SentinelOps Quick Test Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Docker
Write-Host "[1/7] Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker OK: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker not found!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 2: Kubernetes
Write-Host "[2/7] Checking Kubernetes..." -ForegroundColor Yellow
try {
    kubectl cluster-info | Out-Null
    Write-Host "✓ Kubernetes cluster accessible" -ForegroundColor Green
} catch {
    Write-Host "✗ Kubernetes not accessible!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Test 3: Demo namespace
Write-Host "[3/7] Checking demo namespace..." -ForegroundColor Yellow
$demoPods = kubectl get pods -n demo --no-headers 2>$null
if ($demoPods) {
    Write-Host "✓ Demo namespace exists" -ForegroundColor Green
    Write-Host $demoPods
} else {
    Write-Host "⚠ Demo namespace empty or not found" -ForegroundColor Yellow
}
Write-Host ""

# Test 4: Prometheus
Write-Host "[4/7] Checking Prometheus..." -ForegroundColor Yellow
$promPods = kubectl get pods -n monitoring --no-headers 2>$null
if ($promPods) {
    Write-Host "✓ Prometheus namespace exists" -ForegroundColor Green
    Write-Host $promPods
} else {
    Write-Host "⚠ Prometheus not found" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: Backend
Write-Host "[5/7] Checking backend server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✓ Backend running on port 8000" -ForegroundColor Green
} catch {
    Write-Host "✗ Backend NOT running on port 8000" -ForegroundColor Red
    Write-Host "  To start: python -m uvicorn mcp_server.main:app --reload" -ForegroundColor Gray
}
Write-Host ""

# Test 6: Frontend
Write-Host "[6/7] Checking frontend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✓ Frontend running on port 5173" -ForegroundColor Green
} catch {
    Write-Host "✗ Frontend NOT running on port 5173" -ForegroundColor Red
    Write-Host "  To start: cd frontend; npm run dev" -ForegroundColor Gray
}
Write-Host ""

# Test 7: Python environment
Write-Host "[7/7] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python OK: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Start backend:  python -m uvicorn mcp_server.main:app --reload" -ForegroundColor White
Write-Host "2. Start frontend: cd frontend; npm run dev" -ForegroundColor White
Write-Host "3. Run full tests: python test_backend.py" -ForegroundColor White
Write-Host "4. Start AI brain:  python agents/decision_engine.py" -ForegroundColor White
Write-Host ""
Write-Host "For detailed testing guide, see TEST_GUIDE.md" -ForegroundColor Cyan
Write-Host ""

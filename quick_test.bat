@echo off
echo ========================================
echo SentinelOps Quick Test Script
echo ========================================
echo.

echo [1/5] Checking Docker...
docker --version
if %errorlevel% neq 0 (
    echo ERROR: Docker not found!
    pause
    exit /b 1
)
echo ✓ Docker OK
echo.

echo [2/5] Checking Kubernetes...
kubectl cluster-info
if %errorlevel% neq 0 (
    echo ERROR: Kubernetes not accessible!
    pause
    exit /b 1
)
echo ✓ Kubernetes OK
echo.

echo [3/5] Checking pods in demo namespace...
kubectl get pods -n demo
echo.

echo [4/5] Checking Prometheus...
kubectl get pods -n monitoring
echo.

echo [5/5] Checking if backend is running...
curl http://localhost:8000/health 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Backend not running on port 8000
    echo.
    echo To start backend, run:
    echo   .\venv\Scripts\Activate.ps1
    echo   python -m uvicorn mcp_server.main:app --reload
) else (
    echo ✓ Backend OK
)
echo.

echo ========================================
echo Test Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend: python -m uvicorn mcp_server.main:app --reload
echo 2. Start frontend: cd frontend ^&^& npm run dev
echo 3. Run tests: python test_backend.py
echo.
pause

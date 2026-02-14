@echo off
REM SentinelOps - Start Backend and Frontend
echo ================================================
echo   SentinelOps - Starting Backend + Frontend
echo ================================================
echo.

REM Start backend in a new window
echo [1/2] Starting Backend Server...
start "SentinelOps Backend" cmd /k "python test_backend.py"
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
echo [2/2] Starting Frontend Dashboard...
start "SentinelOps Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ================================================
echo   Both services are starting!
echo ================================================
echo.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo.
echo   Press any key to open the dashboard...
pause >nul

REM Open browser
start http://localhost:5173

echo.
echo   Dashboard opened in browser!
echo   Close this window anytime.
pause

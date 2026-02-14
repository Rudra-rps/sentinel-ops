# SentinelOps - Start Backend and Frontend

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  SentinelOps - Starting Backend + Frontend" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Start backend
Write-Host "[1/2] Starting Backend Server..." -ForegroundColor Yellow
$backend = Start-Process powershell -ArgumentList "-NoExit", "-Command", "python test_backend.py" -PassThru
Start-Sleep -Seconds 3

# Start frontend
Write-Host "[2/2] Starting Frontend Dashboard..." -ForegroundColor Yellow
$frontend = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -PassThru
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  Both services are running!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "  Backend PID:  $($backend.Id)" -ForegroundColor DarkGray
Write-Host "  Frontend PID: $($frontend.Id)" -ForegroundColor DarkGray
Write-Host ""

# Wait a bit then open browser
Start-Sleep -Seconds 5
Write-Host "Opening dashboard in browser..." -ForegroundColor Yellow
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "  Dashboard opened!" -ForegroundColor Green
Write-Host "  Close the Backend and Frontend windows to stop the services." -ForegroundColor Gray
Write-Host ""

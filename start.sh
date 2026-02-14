#!/bin/bash
# SentinelOps - Start Backend and Frontend

echo "================================================"
echo "  SentinelOps - Starting Backend + Frontend"
echo "================================================"
echo ""

# Start backend in background
echo "[1/2] Starting Backend Server..."
python test_backend.py &
BACKEND_PID=$!
sleep 3

# Start frontend in background
echo "[2/2] Starting Frontend Dashboard..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "================================================"
echo "  Both services are running!"
echo "================================================"
echo ""
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Backend PID:  $BACKEND_PID"
echo "  Frontend PID: $FRONTEND_PID"
echo ""
echo "  Press Ctrl+C to stop both services..."

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

# SentinelOps - Quick Reference

## 🚀 One-Command Start

```powershell
# Windows PowerShell (Recommended)
.\start.ps1

# Windows CMD
start.bat

# Linux/Mac
./start.sh
```

## ⚠️ Prerequisites Checklist

Before running SentinelOps, ensure:

- ✅ **Docker Desktop is running** (check system tray)
- ✅ **Minikube cluster is started** (`minikube start`)
- ✅ **Demo apps are deployed** (`kubectl get pods -n demo`)
- ✅ **Prometheus is running** (`kubectl get pods -n monitoring`)
- ✅ **Prometheus port-forward active** (port 9090)
- ✅ **Python venv activated** (`venv\Scripts\Activate.ps1`)

## 🌐 URLs

| Service | URL |
|---------|-----|
| Frontend Dashboard | http://localhost:8080/ or http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Prometheus UI | http://localhost:9090 |

## 📁 Project Structure

```
sentinel-ops/
├── frontend/              # React + TypeScript dashboard
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api-config.ts      # API configuration
│   │   │   ├── api-types.ts       # TypeScript types
│   │   │   ├── api-service.ts     # API service layer
│   │   │   └── api-hooks.ts       # React hooks
│   │   ├── components/dashboard/  # UI components
│   │   └── pages/Index.tsx        # Main dashboard page
│   └── .env.development           # Frontend config
├── agents/                # Backend AI agents
├── tools/                 # Kubernetes & Prometheus tools
├── mcp_server/           # FastAPI server
└── test_backend.py       # Backend launcher
```

## 🔑 Key Commands

### Start Services
```powershell
# Backend server
python -m uvicorn mcp_server.main:app --reload

# Frontend dashboard  
cd frontend
npm run dev

# Prometheus port forwarding (required)
kubectl port-forward -n monitoring svc/prometheus 9090:9090
```

### Test & Verify
```powershell
# Test all backend endpoints
python test_backend.py

# Check Kubernetes cluster
kubectl get pods -n demo
kubectl get pods -n monitoring

# Test API health
curl http://localhost:8000/health
```

### First Time Setup
```powershell
# Python environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
```

## 📡 API Quick Reference

### Dashboard Data
```bash
# Get everything
curl http://localhost:8000/dashboard/stats?hours=24

# Get quick summary
curl http://localhost:8000/stats/summary
```

### Chaos Testing
```bash
# CPU spike (120s)
curl -X POST "http://localhost:8000/simulate/cpu_spike?duration=120"

# Crash random pod
curl -X POST "http://localhost:8000/simulate/crash"

# Cascade failure
curl -X POST "http://localhost:8000/simulate/cascade"

# Cleanup
curl -X POST "http://localhost:8000/simulate/cleanup"
```

### Control Operations
```bash
# Scale deployment
curl -X POST "http://localhost:8000/scale?deployment=nginx-demo&replicas=5"

# Restart deployment
curl -X POST "http://localhost:8000/restart?deployment=nginx-demo"
```

## 🎨 Frontend API Usage

### Fetch Dashboard Data
```typescript
import { useDashboard } from '@/lib/api-hooks';

const { data, isLoading, error, refresh } = useDashboard({
  refreshInterval: 10000,  // 10 seconds
  hours: 24,
});
```

### Real-time Metrics
```typescript
import { useRealtimeMetrics } from '@/lib/api-hooks';

const { data: metrics } = useRealtimeMetrics(true);
// Updates every 3 seconds: cpu, memory, pods, daily_cost
```

### Chaos Simulations
```typescript
import { useChaosSimulation } from '@/lib/api-hooks';

const { simulateCPUSpike, simulateCrash, isSimulating } = useChaosSimulation();

// Trigger CPU spike
await simulateCPUSpike(120);
```

### Direct API Calls
```typescript
import { api } from '@/lib/api-service';

// Get health
const health = await api.getHealth();

// Get pods
const pods = await api.getPods('demo');

// Scale deployment
await api.scaleDeployment('nginx-demo', 5);
```

## ⚙️ Configuration

### Change Backend URL
Edit `frontend/.env.development`:
```bash
VITE_API_URL=http://localhost:8000
```

### Adjust Polling Rates
Edit `frontend/src/lib/api-config.ts`:
```typescript
POLLING_INTERVALS: {
  FAST: 3000,      // Real-time metrics
  NORMAL: 10000,   // Dashboard updates
  SLOW: 30000,     // Cost/recommendations
}
```

## 🐛 Troubleshooting

### Backend not starting?
```bash
# Check Python version
python --version  # Should be 3.11+

# Install dependencies
pip install -r requirements.txt

# Check Kubernetes
kubectl cluster-info
kubectl get pods -n demo
```

### Frontend "Request timeout" errors?
```powershell
# This usually means backend can't connect to Kubernetes

# 1. Check Docker Desktop is running (system tray icon)

# 2. Start/restart Minikube
minikube start

# 3. Verify cluster is accessible
kubectl cluster-info
# Should NOT show connection errors

# 4. Deploy demo apps if not present
kubectl apply -f demo/nginx-deploy.yaml
kubectl apply -f demo/prometheus-deploy.yaml

# 5. Setup Prometheus port forwarding
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Keep this running in background

# 6. Restart backend server
python -m uvicorn mcp_server.main:app --reload

# 7. Test backend health
curl http://localhost:8000/health
# Should return: {"status":"healthy","services":{"kubernetes":"healthy","prometheus":"healthy"}}

# 8. Hard refresh browser (Ctrl+Shift+R)
```

### Frontend not connecting to backend?
```powershell
# Verify backend is running
curl http://localhost:8000/health

# Check environment variables
cat frontend/.env.development
# Should show: VITE_API_URL=http://localhost:8000

# Check for port conflicts
netstat -ano | findstr :8080
netstat -ano | findstr :8000

# Restart frontend with cleared cache
cd frontend
npm run dev
```

### No data showing in dashboard?
```powershell
# Verify demo namespace exists
kubectl get ns demo

# Deploy test application
kubectl apply -f demo/nginx-deploy.yaml

# Check pods are running (should see 3 nginx pods)
kubectl get pods -n demo

# Test API endpoint directly
curl http://localhost:8000/dashboard/stats?hours=24
# Should return JSON with cluster data
```

### Minikube won't start?
```powershell
# Delete and recreate cluster
minikube delete
minikube start

# Or try with more resources
minikube start --cpus=4 --memory=8192
```

## 📊 Default Thresholds

| Metric | Scale Up | Scale Down |
|--------|----------|------------|
| CPU | > 80% | < 30% |
| Memory | > 85% | < 40% |
| Pod Restarts | > 5 | - |

## 🔥 Demo Scenario - Full Test Flow

```powershell
# 1. Ensure everything is running
minikube status                    # Should show "Running"
kubectl get pods -n demo           # Should show 3 nginx pods
kubectl get pods -n monitoring     # Should show 1 prometheus pod

# 2. Start services (if not already running)
# Terminal 1: Prometheus port forward
kubectl port-forward -n monitoring svc/prometheus 9090:9090

# Terminal 2: Backend server
python -m uvicorn mcp_server.main:app --reload

# Terminal 3: Frontend dashboard
cd frontend
npm run dev

# 3. Test backend is healthy
curl http://localhost:8000/health
# Expected: {"status":"healthy","services":{"kubernetes":"healthy","prometheus":"healthy"}}

# 4. Run automated test suite
python test_backend.py
# Expected: All tests pass (100% success rate)

# 5. Open dashboard in browser
# Navigate to: http://localhost:8080/ (or http://localhost:5173)
# You should see:
#   - Live metrics (CPU, Memory, Pods)
#   - Cost analysis
#   - Incident feed
#   - Recommendations

# 6. Trigger chaos test - CPU spike
curl -X POST "http://localhost:8000/simulate/cpu_spike?duration=120"

# 7. Watch auto-scaling in action
# Dashboard will show in real-time:
#   1. CPU spike detected (>80%)
#   2. Decision: Scale up
#   3. Action: Pods increased (3 → 5)
#   4. Result: CPU normalized
#   5. Later: Pods scaled back down (5 → 3)

# 8. View incident logs
curl http://localhost:8000/incidents?limit=10

# 9. Check cost savings
curl http://localhost:8000/cost/savings?hours=24

# 10. Get recommendations
curl http://localhost:8000/cost/recommendations
```

## ✅ Success Checklist

After setup, verify:
- [ ] Backend returns `{"status":"healthy"}` at http://localhost:8000/health
- [ ] Dashboard loads at http://localhost:8080/ without timeout errors
- [ ] Live metrics display in dashboard (CPU, memory, pods)
- [ ] `python test_backend.py` shows 100% pass rate
- [ ] Chaos tests trigger and auto-heal
- [ ] Incident feed shows recent events

## 📚 Documentation

| File | Purpose |
|------|---------|
| [README.md](README.md) | Main project overview |
| [FRONTEND.md](FRONTEND.md) | Frontend integration guide |
| [frontend/README.md](frontend/README.md) | Frontend-specific docs |
| [API.md](API.md) | Complete API reference |
| [INTEGRATION.md](INTEGRATION.md) | Integration details |
| [STATUS.md](STATUS.md) | Project status |

## 🎯 Common Tasks

### Add new API endpoint

1. Add to backend (FastAPI route)
2. Add to `frontend/src/lib/api-service.ts`
3. Add type to `frontend/src/lib/api-types.ts`
4. Create hook in `frontend/src/lib/api-hooks.ts` (optional)
5. Use in component

### Change polling interval

Edit `frontend/src/lib/api-config.ts`:
```typescript
POLLING_INTERVALS: {
  FAST: 5000,  // Change from 3000 to 5000
}
```

### Add new chaos test

1. Backend: Add route in `tools/chaos.py`
2. Frontend: Add to `useChaosSimulation()` hook
3. Frontend: Add button to `ChaosPanel.tsx`

## 💡 Pro Tips

- Use browser DevTools Network tab to debug API calls
- Check browser console for errors
- Use `--watch` flag in Kubernetes to see real-time changes
- The `test_backend.py` runs a complete backend server
- Frontend hot-reloads on file changes (Vite)

---

**Quick Links:**
- 📚 [Full Documentation](README.md)
- 🎨 [Frontend Guide](frontend/README.md)
- 🔌 [API Reference](API.md)
- 🚀 [Integration Details](INTEGRATION.md)

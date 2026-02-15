# 🧪 SentinelOps Testing Guide

**Complete step-by-step guide to test your entire system**

---

## 📋 Pre-Flight Checklist

Before testing, ensure you have:
- [ ] Docker Desktop installed and running
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] kubectl installed
- [ ] Minikube installed (or access to a K8s cluster)

---

## 🚀 Phase 1: Infrastructure Setup (15 minutes)

### Step 1.1: Start Docker Desktop
```powershell
# Verify Docker is running
docker --version
docker ps

# Expected: Docker version info and running containers list
```

### Step 1.2: Start Kubernetes Cluster
```powershell
# Start minikube
minikube start --cpus=4 --memory=8192

# Verify cluster is running
kubectl cluster-info
kubectl get nodes

# Expected: Cluster info and 1 node in "Ready" status
```

### Step 1.3: Create Demo Namespace
```powershell
# Create namespace
kubectl create namespace demo

# Verify
kubectl get namespaces

# Expected: "demo" namespace in the list
```

### Step 1.4: Deploy Test Application
```powershell
# Deploy nginx demo app
kubectl apply -f demo/nginx-deploy.yaml

# Wait for pods to be ready (may take 1-2 minutes)
kubectl get pods -n demo --watch

# Press Ctrl+C when all pods show "Running"
# Expected: 3 nginx-demo pods in "Running" status
```

### Step 1.5: Deploy Prometheus
```powershell
# Deploy Prometheus
kubectl apply -f demo/prometheus-deploy.yaml

# Wait for Prometheus to be ready
kubectl get pods -n monitoring --watch

# Press Ctrl+C when pod shows "Running"
# Expected: prometheus pod in "Running" status
```

### Step 1.6: Setup Prometheus Port Forwarding
```powershell
# Open a NEW terminal window and run:
kubectl port-forward -n monitoring svc/prometheus 9090:9090

# Keep this terminal open!
# Test in browser: http://localhost:9090
# Expected: Prometheus UI loads
```

**✅ Phase 1 Complete!** You now have:
- Kubernetes cluster running
- Demo app deployed (3 nginx pods)
- Prometheus monitoring running
- Prometheus accessible at localhost:9090

---

## 🐍 Phase 2: Backend Setup (10 minutes)

### Step 2.1: Setup Python Environment
```powershell
# Navigate to project root
cd c:\sentinel-ops

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Verify activation (you should see (venv) in prompt)
```

### Step 2.2: Install Dependencies
```powershell
# Install Python packages
pip install -r requirements.txt

# Expected: All packages installed successfully
```

### Step 2.3: Start Backend Server
```powershell
# Start the MCP server
python -m uvicorn mcp_server.main:app --reload

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
```

### Step 2.4: Test Backend Health (NEW TERMINAL)
```powershell
# Open a NEW terminal and test
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"...","services":{...}}
```

**✅ Phase 2 Complete!** Backend is running on http://localhost:8000

---

## 🧪 Phase 3: Backend API Testing (5 minutes)

### Step 3.1: Run Automated Test Suite
```powershell
# In a NEW terminal (keep backend running)
cd c:\sentinel-ops

# Activate venv
.\venv\Scripts\Activate.ps1

# Run test script
python test_backend.py

# Expected: All tests pass with 100% success rate
```

### Step 3.2: Manual Endpoint Tests
```powershell
# Test metrics endpoint
curl http://localhost:8000/metrics

# Test pods endpoint
curl http://localhost:8000/pods

# Test dashboard stats
curl http://localhost:8000/dashboard/stats?hours=24

# Test cost analysis
curl http://localhost:8000/cost/current

# Expected: JSON responses with cluster data
```

**✅ Phase 3 Complete!** All backend endpoints are working!

---

## 🎨 Phase 4: Frontend Setup (10 minutes)

### Step 4.1: Install Frontend Dependencies
```powershell
# Open a NEW terminal
cd c:\sentinel-ops\frontend

# Install dependencies (first time only)
npm install

# Expected: Dependencies installed successfully
```

### Step 4.2: Start Frontend Dev Server
```powershell
# Start Vite dev server
npm run dev

# Expected output:
# VITE v5.x.x  ready in xxx ms
# ➜  Local:   http://localhost:5173/
```

### Step 4.3: Open Dashboard in Browser
```powershell
# Open browser to:
http://localhost:5173

# Expected: SentinelOps dashboard loads with live data
```

### Step 4.4: Verify Dashboard Components
Check that you see:
- [ ] Header with "SentinelOps" title
- [ ] Scoreboard cards showing CPU, Memory, Pods, Cost
- [ ] Performance chart with metrics
- [ ] Cost analysis section
- [ ] Incident feed (may be empty initially)
- [ ] AI recommendations
- [ ] Chaos testing panel

**✅ Phase 4 Complete!** Frontend is running and connected!

---

## 🔥 Phase 5: Chaos Testing (10 minutes)

### Test 5.1: Simulate Pod Crash
```powershell
# Method 1: Via API
curl -X POST "http://localhost:8000/simulate/crash?deployment=nginx-demo"

# Method 2: Via Frontend
# Click "Crash Random Pod" button in Chaos Panel

# Watch in terminal:
kubectl get pods -n demo --watch

# Expected: 
# - One pod goes to "Terminating"
# - New pod is created automatically
# - All pods return to "Running" within 30 seconds
```

### Test 5.2: Simulate CPU Spike
```powershell
# Trigger CPU spike (2 minute duration)
curl -X POST "http://localhost:8000/simulate/cpu_spike?duration=120"

# Watch dashboard:
# - CPU metric should increase
# - Watch for auto-scaling (if decision engine is running)

# Check stress pod was created:
kubectl get pods -n demo

# Expected: stress-test pod appears
```

### Test 5.3: Manual Scaling Test
```powershell
# Scale up deployment
curl -X POST "http://localhost:8000/scale?deployment=nginx-demo&replicas=5&namespace=demo"

# Verify in dashboard and kubectl:
kubectl get pods -n demo

# Expected: 5 nginx-demo pods running

# Scale back down
curl -X POST "http://localhost:8000/scale?deployment=nginx-demo&replicas=3&namespace=demo"

# Expected: 3 nginx-demo pods running
```

### Test 5.4: Cleanup Chaos Tests
```powershell
# Clean up stress tests
curl -X POST "http://localhost:8000/simulate/cleanup"

# Expected: All stress-test pods removed
```

**✅ Phase 5 Complete!** Chaos testing works!

---

## 🤖 Phase 6: Decision Engine Testing (15 minutes)

### Step 6.1: Start Decision Engine
```powershell
# Open a NEW terminal
cd c:\sentinel-ops

# Activate venv
.\venv\Scripts\Activate.ps1

# Start decision engine
python agents/decision_engine.py

# Expected output:
# ======================================================================
# SENTINELOPS DECISION ENGINE
# ======================================================================
# Starting autonomous decision loop...
# Monitoring namespace: demo
# Loop interval: 60 seconds
```

### Step 6.2: Watch Autonomous Monitoring
```
# The decision engine will run every 60 seconds
# Watch the console output for:

CYCLE #1 - [timestamp]
======================================================================

📊 STEP 1: Collecting metrics...
   CPU: XX.X% | Memory: XX.X% | Pods: X

🔍 STEP 2: Analyzing for issues...
   ✓ No issues detected (or ⚠️ Found X issue(s))

🧠 STEP 3: Deciding on actions...
   📋 Planned X action(s) (or ✓ No actions needed)

⚡ STEP 4: Executing actions...
   (Actions will be listed here if any)

📝 STEP 5: Logging incidents...
   ✅ Success (or details of actions taken)

⏱️  Cycle completed in XXXXms
```

### Step 6.3: Trigger Auto-Scaling
```powershell
# In another terminal, trigger CPU spike
curl -X POST "http://localhost:8000/simulate/cpu_spike?duration=300"

# Watch decision engine console:
# Within 60 seconds, you should see:
# - CPU overload detected
# - Scale up action planned
# - Deployment scaled from 3 to 5 replicas
# - Incident logged

# Verify scaling happened:
kubectl get pods -n demo

# Expected: 5 nginx-demo pods running
```

### Step 6.4: Watch Auto-Healing
```powershell
# Delete a pod manually
kubectl delete pod -n demo $(kubectl get pods -n demo -l app=nginx -o jsonpath='{.items[0].metadata.name}')

# Watch decision engine console:
# Within 60 seconds, you should see:
# - Pod issue detected
# - Healing action planned
# - Pod restarted or recreated
# - Incident logged

# Kubernetes will auto-recreate the pod anyway, but decision engine will log it
```

### Step 6.5: Check Incident Logs
```powershell
# View incidents via API
curl http://localhost:8000/incidents?limit=10

# Or check log file directly
cat logs/incidents.log

# Expected: JSON entries for each incident with:
# - timestamp
# - issue type
# - action taken
# - result (success/failure)
```

**✅ Phase 6 Complete!** Autonomous decision engine is working!

---

## 📊 Phase 7: End-to-End Integration Test (10 minutes)

### Full System Test Scenario

**Scenario: Simulate Production Incident and Watch Full Auto-Remediation**

1. **Ensure all components are running:**
   - [ ] Kubernetes cluster (minikube)
   - [ ] Prometheus (port-forward on 9090)
   - [ ] Backend server (port 8000)
   - [ ] Frontend dashboard (port 5173)
   - [ ] Decision engine (autonomous loop)

2. **Open monitoring windows:**
   ```powershell
   # Terminal 1: Watch pods
   kubectl get pods -n demo --watch

   # Terminal 2: Watch decision engine output
   # (already running)

   # Browser: Open dashboard at http://localhost:5173
   ```

3. **Trigger cascade failure:**
   ```powershell
   # Terminal 3: Trigger multiple issues
   curl -X POST "http://localhost:8000/simulate/cascade?deployment=nginx-demo"
   ```

4. **Watch the magic happen:**
   - **Dashboard**: See metrics spike, incident feed updates
   - **Decision Engine**: See detection → decision → action
   - **kubectl**: See pods crash and recover
   - **Logs**: See incidents being logged

5. **Verify recovery:**
   ```powershell
   # Check all pods are healthy
   kubectl get pods -n demo

   # Check incidents were logged
   curl http://localhost:8000/incidents?limit=5

   # Check dashboard shows recovery
   # Open http://localhost:5173
   ```

**Expected Timeline:**
- 0s: Cascade failure triggered
- 10-30s: Pods crash
- 30-60s: Decision engine detects issues
- 60-90s: Auto-healing actions executed
- 90-120s: All pods back to healthy state
- Incidents logged in dashboard

**✅ Phase 7 Complete!** Full system integration verified!

---

## 📈 Phase 8: Performance Verification

### Check System Metrics

```powershell
# 1. Check backend health
curl http://localhost:8000/health

# 2. Get comprehensive stats
curl http://localhost:8000/dashboard/stats?hours=24

# 3. Check incident success rate
curl http://localhost:8000/incidents?limit=50

# 4. Verify cost calculations
curl http://localhost:8000/cost/breakdown?hours=24
```

### Expected Results:
- ✅ Health status: "healthy"
- ✅ All pods running
- ✅ Incident success rate: >90%
- ✅ MTTR (Mean Time To Recovery): <120 seconds
- ✅ Dashboard loads in <2 seconds
- ✅ API response time: <500ms

---

## 🐛 Troubleshooting Guide

### Problem: Backend won't start
```powershell
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F

# Restart backend
python -m uvicorn mcp_server.main:app --reload
```

### Problem: Prometheus not accessible
```powershell
# Check if Prometheus pod is running
kubectl get pods -n monitoring

# Restart port-forward
kubectl port-forward -n monitoring svc/prometheus 9090:9090
```

### Problem: Frontend shows "Connection Error"
```powershell
# 1. Verify backend is running
curl http://localhost:8000/health

# 2. Check CORS settings in mcp_server/main.py
# Should allow localhost:5173

# 3. Restart frontend
cd frontend
npm run dev
```

### Problem: Decision engine crashes
```powershell
# Check logs
cat logs/decision_engine.log

# Verify Kubernetes connection
kubectl cluster-info

# Restart decision engine
python agents/decision_engine.py
```

### Problem: No metrics showing
```powershell
# 1. Check if demo pods are running
kubectl get pods -n demo

# 2. Redeploy if needed
kubectl apply -f demo/nginx-deploy.yaml

# 3. Check Prometheus
curl http://localhost:9090/api/v1/query?query=up
```

---

## ✅ Final Verification Checklist

After completing all phases, verify:

### Infrastructure
- [ ] Minikube cluster running
- [ ] Demo namespace exists
- [ ] 3 nginx-demo pods running
- [ ] Prometheus pod running
- [ ] Port-forward active (9090)

### Backend
- [ ] MCP server running on port 8000
- [ ] Health endpoint returns "healthy"
- [ ] All API endpoints responding
- [ ] Test suite passes 100%

### Frontend
- [ ] Dev server running on port 5173
- [ ] Dashboard loads successfully
- [ ] Real-time metrics updating
- [ ] No console errors

### Autonomous Features
- [ ] Decision engine running
- [ ] Auto-monitoring every 60s
- [ ] Incidents being logged
- [ ] Auto-scaling works
- [ ] Auto-healing works

### Chaos Testing
- [ ] Pod crash simulation works
- [ ] CPU spike simulation works
- [ ] Cascade failure works
- [ ] Cleanup works

### Logs & Tracking
- [ ] logs/incidents.log has entries
- [ ] logs/actions.log has entries
- [ ] Incident API returns data
- [ ] Dashboard shows incidents

---

## 🎯 Success Criteria

Your system is **fully operational** if:

1. ✅ All 5 components are running simultaneously:
   - Kubernetes cluster
   - Prometheus (port-forward)
   - Backend (port 8000)
   - Frontend (port 5173)
   - Decision engine (autonomous loop)

2. ✅ You can trigger a pod crash and see:
   - Detection in decision engine (within 60s)
   - Auto-healing action executed
   - Incident logged
   - Dashboard updated

3. ✅ You can trigger CPU spike and see:
   - Auto-scaling from 3 to 5 pods
   - Cost analysis updated
   - Incident logged

4. ✅ Dashboard shows:
   - Live metrics (CPU, memory, pods)
   - Cost analysis with savings
   - Incident feed with recent events
   - AI recommendations

---

## 🚀 Quick Start Script

For future testing, use the automated startup script:

```powershell
# Windows
.\start.ps1

# This will:
# 1. Activate Python venv
# 2. Start backend server
# 3. Start frontend dev server
# 4. Open browser to dashboard
```

---

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review logs in `logs/` directory
3. Check backend logs in terminal
4. Verify all prerequisites are installed
5. Ensure Docker Desktop is running

---

## 🎉 Congratulations!

If you've completed all phases successfully, you have a **fully functional autonomous SRE system**! 

Your SentinelOps is now:
- ✅ Monitoring your cluster in real-time
- ✅ Auto-scaling based on load
- ✅ Auto-healing crashed pods
- ✅ Tracking costs and savings
- ✅ Logging all incidents
- ✅ Providing AI recommendations

**You're ready for the hackathon demo!** 🏆

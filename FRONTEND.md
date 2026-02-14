# 🎨 Frontend - SentinelOps Dashboard

## ✅ Status: FULLY INTEGRATED

The SentinelOps frontend is **fully integrated** with the backend API!

### Quick Launch

```bash
# Start backend (Terminal 1)
python test_backend.py

# Start frontend (Terminal 2)
cd frontend
npm install  # First time only
npm run dev
```

Visit:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📂 Frontend Location

The dashboard is located in the `frontend/` directory and is a fully-featured React + TypeScript application.

**Tech Stack:**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS + shadcn/ui
- Recharts (charts)
- Real-time API integration

See [frontend/README.md](frontend/README.md) for complete documentation.

---

## 🎯 Features

### ✨ What's Working

- ✅ **Real-time Metrics** - CPU, memory, pod counts update every 3 seconds
- ✅ **Live Dashboard** - Complete stats refresh every 10 seconds
- ✅ **Cost Analysis** - Hourly/daily/monthly costs with savings tracking
- ✅ **Incident Timeline** - Real-time log of all auto-healing actions
- ✅ **AI Recommendations** - Smart optimization suggestions
- ✅ **Chaos Engineering** - CPU spike, crash pod, cascade failure tests
- ✅ **Error Handling** - Graceful fallbacks and loading states
- ✅ **Responsive Design** - Works on desktop, tablet, mobile

### 🎨 UI Highlights

- Stadium scoreboard aesthetic (LED fonts, neon borders)
- Animated metrics and smooth transitions
- Real-time status indicators
- Toast notifications for events
- Color-coded severity levels

---

## 🚀 Quick Start for Development

### 1. Install Dependencies

```bash
cd frontend
npm install
# or use bun for faster installs
bun install
```

### 2. Configure Environment

The `.env` files are already set up:

```bash
# .env.development
VITE_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
# or
bun run dev
```

Frontend will be available at: http://localhost:5173

---

## 🔌 API Integration

### Architecture

The frontend uses a clean, typed API layer:

```
src/lib/
├── api-config.ts    # Configuration & endpoints
├── api-types.ts     # TypeScript interfaces
├── api-service.ts   # API service class
└── api-hooks.ts     # React hooks for data fetching
```

### Usage Examples

#### Fetch Dashboard Data

```typescript
import { useDashboard } from '@/lib/api-hooks';

const { data, isLoading, error } = useDashboard({
  refreshInterval: 10000,  // 10 seconds
  hours: 24,
});

// data contains: cluster, metrics, cost, savings, incidents, recommendations
```

#### Get Real-time Metrics

```typescript
import { useRealtimeMetrics } from '@/lib/api-hooks';

const { data: metrics } = useRealtimeMetrics(true);

// Updates every 3 seconds: cpu, memory, pods, daily_cost
```

#### Trigger Chaos Tests

```typescript
import { useChaosSimulation } from '@/lib/api-hooks';

const { simulateCPUSpike, isSimulating } = useChaosSimulation();

await simulateCPUSpike(120); // 120 second CPU spike
```

---

## 🎯 Key Endpoints

### Dashboard (⭐ Primary endpoints)
```
GET  /dashboard/stats?hours=24    - All-in-one comprehensive data
GET  /stats/summary               - Quick stats for real-time updates
```

### Cost Analysis 💰
```
GET  /cost/current                - Current infrastructure cost
GET  /cost/savings?hours=24       - Savings from auto-scaling
GET  /cost/recommendations         - Optimization suggestions
GET  /cost/breakdown?hours=24     - Detailed cost analysis
```

### Kubernetes Resources
```
GET  /pods                        - List all pods
GET  /deployments                 - List deployments
GET  /nodes                       - List nodes
```

### Control Actions
```
POST /scale?deployment=nginx-demo&replicas=5
POST /restart?deployment=nginx-demo
POST /delete_pod?pod_name=xyz
```

### Incidents
```
GET  /incidents?limit=50          - Get incident history
```

### Chaos Testing 🔥
```
POST /simulate/cpu_spike?duration=120
POST /simulate/crash
POST /simulate/cascade
POST /simulate/cleanup
GET  /chaos/status
```


---

## 📦 Sample Response Structure

### `/dashboard/stats` Response:
```typescript
{
  success: true,
  timestamp: "2026-02-13T...",
  cluster: {
    namespace: "demo",
    total_pods: 5,
    healthy_pods: 5,
    unhealthy_pods: 0
  },
  metrics: {
    cpu_usage: 45.2,      // Percentage
    memory_usage: 62.8,   // Percentage
    pod_count: 5
  },
  cost: {
    hourly: 0.12,         // $
    daily: 2.88,          // $
    monthly: 86.40        // $
  },
  savings: {
    total_saved: 1.25,           // $ saved in time period
    projected_monthly: 37.50,     // $ projected monthly savings
    scale_down_count: 3,
    scale_up_count: 2
  },
  incidents: {
    total: 15,
    successful: 14,
    success_rate: 93.3,
    recent: [              // Last 10 incidents
      {
        id: "inc-...",
        timestamp: "...",
        issue: {
          type: "cpu_overload",
          severity: "high",
          metric_value: 87.3
        },
        action: {
          type: "scale_up",
          target: "nginx-demo"
        },
        result: {
          success: true
        }
      }
    ]
  },
  recommendations: [
    {
      type: "reduce_baseline",
      severity: "medium",
      title: "Reduce baseline replica count",
      description: "...",
      potential_savings: "$15-30/month"
    }
  ],
  health: {
    status: "healthy",
    kubernetes: "connected",
    prometheus: "connected"
  }
}
```

---

## 🎨 UI Components to Build

### 1. Hero Metrics (Top Cards)
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ CPU Usage   │ Memory      │ Active Pods │ Daily Cost  │
│   45.2%     │   62.8%     │     5       │   $2.88     │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### 2. Savings Badge
```
💰 Saved $37.50/month through autonomous operations
```

### 3. Success Rate
```
✅ 93.3% incidents resolved automatically
```

### 4. Live Charts
- CPU & Memory usage over time (line chart)
- Pod count timeline (area chart)
- Cost breakdown (bar chart)

### 5. Incident Feed (Timeline)
```
🟢 15:42:18 - CPU Overload Detected
   ↳ Scaled nginx-demo: 3 → 5 replicas
   ✓ Resolved in 8.2s

🔵 14:30:10 - Pod Crash Detected
   ↳ Restarted pod nginx-demo-abc12
   ✓ Resolved in 12.5s
```

### 6. Recommendations Panel
```
💡 Optimization Opportunities

⚠️  Reduce baseline replica count
    System frequently scales down but rarely scales up
    Potential savings: $15-30/month
```

### 7. Demo Controls
```
🔥 Chaos Testing
[Trigger CPU Spike] [Crash Pod] [Cascade Failure]
```

---

## 🎬 Demo Scenario Flow

### Step 1: Show Normal State
```javascript
// Display baseline metrics
const baseline = await fetch('/dashboard/stats').then(r => r.json());
// CPU: 30%, Memory: 40%, Pods: 3, Cost: $2.16/day
```

### Step 2: Trigger Chaos
```javascript
// User clicks "Trigger CPU Spike"
await fetch('/simulate/cpu_spike?duration=120', { method: 'POST' });
// Show alert: "🔥 CPU spike simulation started..."
```

### Step 3: Watch Auto-Scaling
```javascript
// Poll every 3 seconds to show real-time changes
const interval = setInterval(async () => {
  const stats = await fetch('/stats/summary').then(r => r.json());
  
  // Show CPU rising: 30% → 65% → 85%
  // Show auto-scaler triggering
  // Show pods increasing: 3 → 5
  // Show CPU normalizing: 85% → 50%
  
  if (stats.cpu < 60) {
    clearInterval(interval);
    showSuccess('✅ Auto-scaling completed!');
  }
}, 3000);
```

### Step 4: Show Results
```javascript
// Display incident timeline
// Show cost impact
// Show savings calculation
```

---

## 🎨 Color Scheme Suggestions

```css
/* Status Colors */
--success: #3fb950;     /* Green for healthy, resolved */
--warning: #d29922;     /* Yellow for warnings */
--danger: #f85149;      /* Red for errors, high severity */
--info: #58a6ff;        /* Blue for info, normal events */

/* Backgrounds */
--bg-primary: #0d1117;  /* Dark background */
--bg-secondary: #161b22; /* Cards, panels */
--border: #30363d;      /* Borders */

/* Text */
--text-primary: #c9d1d9;    /* Main text */
--text-secondary: #8b949e;  /* Secondary text */
--text-accent: #58a6ff;     /* Links, highlights */
```

---

## 🔧 CORS & Local Development

**CORS is already enabled** on the backend for all origins, so you can develop locally without issues.

```javascript
// Fetch works directly, no proxy needed
fetch('http://127.0.0.1:8000/dashboard/stats')
  .then(r => r.json())
  .then(data => console.log(data));
```

---

## 📱 Responsive Layout Suggestion

### Desktop (1400px+)
```
┌─────────────────────────────────────────┐
│  Hero Metrics (4 cards inline)           │
├───────────────────┬─────────────────────┤
│  Charts (60%)     │  Incident Feed (40%) │
│                   │                      │
├───────────────────┴─────────────────────┤
│  Recommendations & Cost Breakdown        │
└─────────────────────────────────────────┘
```

### Mobile (< 768px)
```
┌─────────────┐
│ Hero Metrics│  (2x2 grid)
├─────────────┤
│ Charts      │  (full width)
├─────────────┤
│ Incidents   │  (list view)
├─────────────┤
│ Cost        │
└─────────────┘
```

---

## 🚀 Getting Started Checklist

- [x] Backend running on http://127.0.0.1:8000
- [ ] Test `/dashboard/stats` endpoint in browser
- [ ] Build hero metrics component
- [ ] Add real-time polling
- [ ] Create incident timeline
- [ ] Add cost visualization
- [ ] Implement chaos testing buttons
- [ ] Add charts (Chart.js, Recharts, or similar)
- [ ] Test full demo flow

---

## 📚 Additional Resources

- **Full API Documentation:** [API.md](API.md)
- **Interactive API Tester:** http://127.0.0.1:8000/docs
- **Backend Code:** `mcp_server/main.py`
- **Cost Logic:** `agents/cost_analyzer.py`

---

## 💡 Pro Tips

1. **Start with `/dashboard/stats`** - it has everything
2. **Poll `/stats/summary`** every 5-10s for real-time feel
3. **Use WebSocket alternative:** Simply poll frequently (FastAPI supports WebSockets if needed later)
4. **Error handling:** All endpoints return `{ success: boolean }` - check this first
5. **Loading states:** Show spinners during initial data load
6. **Demo mode:** Add a "Run Demo" button that automatically triggers chaos → watch healing

---

## 🎯 Minimum Viable Dashboard

**For a quick prototype, just build:**

1. **4 hero cards** (CPU, Memory, Pods, Cost)
2. **One chart** (CPU over time)
3. **Incident list** (last 5-10 events)
4. **"Trigger CPU Spike" button**

That's enough to wow people! 🚀

---

**Questions? Check [API.md](API.md) for complete documentation!**

Built with ❤️ by SentinelOps

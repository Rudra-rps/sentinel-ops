# 🔌 SentinelOps API Reference

**Base URL:** `http://localhost:8000`

Complete REST API documentation for building frontends and integrations.

---

## 🎯 Quick Start for Frontend

### Best Endpoint for Dashboards

**GET `/dashboard/stats?hours=24`**

This single endpoint provides everything needed for a complete dashboard:
- Cluster health & metrics
- Current costs
- Savings calculations
- Recent incidents
- Optimization recommendations

```bash
curl http://localhost:8000/dashboard/stats?hours=24
```

**Response Structure:**
```json
{
  "success": true,
  "timestamp": "2026-02-13T...",
  "cluster": {
    "namespace": "demo",
    "total_pods": 5,
    "healthy_pods": 5,
    "unhealthy_pods": 0
  },
  "metrics": {
    "cpu_usage": 45.2,
    "memory_usage": 62.8,
    "pod_count": 5
  },
  "cost": {
    "hourly": 0.12,
    "daily": 2.88,
    "monthly": 86.40
  },
  "savings": {
    "total_saved": 1.25,
    "projected_monthly": 37.50,
    "scale_down_count": 3,
    "scale_up_count": 2
  },
  "incidents": {
    "total": 15,
    "successful": 14,
    "success_rate": 93.3,
    "recent": [...]
  },
  "recommendations": [...]
}
```

### Lightweight Endpoint for Real-time Updates

**GET `/stats/summary`**

Minimal response for frequent polling (every 2-5 seconds):

```json
{
  "success": true,
  "pods": 5,
  "cpu": 45.2,
  "memory": 62.8,
  "daily_cost": 2.88,
  "status": "operational"
}
```

---

## 📊 Core Endpoints

### Health & Status

#### GET `/`
Root endpoint with API information and all available routes.

#### GET `/health`
Health check for monitoring.

```json
{
  "status": "healthy",
  "timestamp": "2026-02-13T...",
  "services": {
    "kubernetes": "healthy",
    "prometheus": "healthy"
  }
}
```

---

## 📈 Metrics Endpoints

### GET `/metrics`
Get all metrics for the namespace.

**Query Parameters:**
- `namespace` (optional): Kubernetes namespace, default: `demo`

**Response:**
```json
{
  "success": true,
  "namespace": "demo",
  "metrics": {
    "cpu_usage": 45.2,
    "memory_usage": 62.8,
    "pod_count": 5,
    "timestamp": "2026-02-13T..."
  }
}
```

### GET `/metrics/cpu`
Get CPU usage metrics.

**Query Parameters:**
- `namespace` (optional): default `demo`
- `deployment` (optional): specific deployment name

**Response:**
```json
{
  "success": true,
  "namespace": "demo",
  "deployment": null,
  "cpu_usage_percent": 45.2
}
```

### GET `/metrics/memory`
Get memory usage metrics (same structure as CPU).

---

## 🎛️ Kubernetes Resources

### GET `/pods`
List all pods in namespace.

**Response:**
```json
{
  "success": true,
  "namespace": "demo",
  "count": 5,
  "pods": [
    {
      "name": "nginx-demo-7d4c8f9b5-abc12",
      "status": "Running",
      "ready": "1/1",
      "restarts": 0,
      "age": "2h",
      "ip": "10.244.0.5",
      "node": "minikube",
      "resources": {
        "requests": {
          "cpu": "100m",
          "memory": "128Mi"
        }
      }
    }
  ]
}
```

### GET `/deployments`
List all deployments.

**Response:**
```json
{
  "success": true,
  "namespace": "demo",
  "count": 1,
  "deployments": [
    {
      "name": "nginx-demo",
      "replicas": 5,
      "ready_replicas": 5,
      "available_replicas": 5,
      "age": "3h"
    }
  ]
}
```

### GET `/nodes`
List all cluster nodes.

---

## 🎮 Control Endpoints

### POST `/scale`
Scale a deployment to specified replica count.

**Query Parameters:**
- `deployment` (required): deployment name
- `replicas` (required): desired replica count
- `namespace` (optional): default `demo`

**Example:**
```bash
curl -X POST "http://localhost:8000/scale?deployment=nginx-demo&replicas=7"
```

**Response:**
```json
{
  "success": true,
  "action": "scale",
  "deployment": "nginx-demo",
  "namespace": "demo",
  "replicas": 7,
  "timestamp": "2026-02-13T..."
}
```

### POST `/restart`
Rolling restart of a deployment.

**Query Parameters:**
- `deployment` (required)
- `namespace` (optional)

**Example:**
```bash
curl -X POST "http://localhost:8000/restart?deployment=nginx-demo"
```

### POST `/delete_pod`
Delete a specific pod (will be recreated by deployment).

**Query Parameters:**
- `pod_name` (required)
- `namespace` (optional)

### GET `/logs/{pod_name}`
Get logs from a pod.

**Query Parameters:**
- `tail` (optional): number of lines, default 100
- `namespace` (optional)

---

## 💰 Cost Analysis Endpoints

### GET `/cost/current`
Calculate current infrastructure cost.

**Response:**
```json
{
  "success": true,
  "timestamp": "2026-02-13T...",
  "cost": {
    "total_pods": 5,
    "total_cpu_cores": 0.5,
    "total_memory_gb": 0.625,
    "hourly_cost": 0.12,
    "daily_cost": 2.88,
    "weekly_cost": 20.16,
    "monthly_cost": 86.40,
    "yearly_cost": 1051.20,
    "pod_breakdown": [
      {
        "name": "nginx-demo-abc12",
        "cpu_cores": 0.1,
        "memory_gb": 0.125,
        "hourly_cost": 0.024
      }
    ]
  }
}
```

### GET `/cost/savings?hours=24`
Calculate savings from auto-scaling.

**Query Parameters:**
- `hours` (optional): time period, default 24

**Response:**
```json
{
  "success": true,
  "savings": {
    "time_period_hours": 24,
    "total_saved": 1.25,
    "scale_down_count": 3,
    "scale_up_count": 2,
    "projected_monthly_savings": 37.50,
    "projected_yearly_savings": 450.00,
    "efficiency_score": 87.5,
    "recommendation": "Excellent! On track to save ~$37.50/month...",
    "scale_down_details": [...]
  }
}
```

### GET `/cost/recommendations`
Get cost optimization recommendations.

**Response:**
```json
{
  "success": true,
  "timestamp": "2026-02-13T...",
  "recommendations": [
    {
      "type": "reduce_baseline",
      "severity": "medium",
      "title": "Reduce baseline replica count",
      "description": "System frequently scales down but rarely scales up",
      "action": "Consider reducing minimum replicas from current baseline",
      "potential_savings": "$15-30/month",
      "confidence": "high"
    }
  ],
  "count": 1
}
```

### GET `/cost/breakdown?hours=24`
Comprehensive cost analysis with all details.

**Response:** Combines current cost, savings, and recommendations.

---

## 📋 Incident Tracking

### GET `/incidents?limit=50`
Get recent incidents.

**Query Parameters:**
- `limit` (optional): max incidents to return, default 50

**Response:**
```json
{
  "success": true,
  "count": 15,
  "incidents": [
    {
      "id": "inc-2026-02-13-001",
      "timestamp": "2026-02-13T15:42:18Z",
      "issue": {
        "type": "cpu_overload",
        "severity": "high",
        "affected_resource": "nginx-demo",
        "metric_value": 87.3
      },
      "action": {
        "type": "scale_up",
        "target": "nginx-demo",
        "parameters": {"from": 3, "to": 5, "delta": 2}
      },
      "result": {
        "success": true,
        "new_state": "5 replicas running",
        "duration_ms": 8234
      }
    }
  ]
}
```

### POST `/incidents`
Log a new incident (used by decision engine).

**Body:**
```json
{
  "type": "cpu_overload",
  "severity": "high",
  "resource": "nginx-demo",
  "action_taken": "scale_up"
}
```

---

## 🔥 Chaos Engineering

### POST `/simulate/cpu_spike`
Simulate CPU load for testing auto-scaling.

**Query Parameters:**
- `deployment` (optional): default `nginx-demo`
- `duration` (optional): seconds, default 300

**Example:**
```bash
curl -X POST "http://localhost:8000/simulate/cpu_spike?duration=180"
```

**Response:**
```json
{
  "success": true,
  "action": "cpu_spike_started",
  "deployment": "nginx-demo",
  "duration": 180,
  "pod_name": "stress-test-cpu",
  "message": "CPU spike simulation started for 180 seconds"
}
```

### POST `/simulate/crash`
Crash a random pod to test auto-healing.

**Response:**
```json
{
  "success": true,
  "action": "pod_crashed",
  "pod_deleted": "nginx-demo-abc12",
  "message": "Pod crashed, Kubernetes will recreate it"
}
```

### POST `/simulate/cascade`
Crash multiple pods simultaneously.

### POST `/simulate/cleanup`
Clean up all stress test pods.

### GET `/chaos/status`
Get status of active chaos simulations.

**Response:**
```json
{
  "success": true,
  "active_simulations": ["stress-test-cpu"],
  "recent_events": [...]
}
```

---

## 🎨 Frontend Integration Guide

### Polling Strategy

**High-frequency updates (2-5 seconds):**
```javascript
setInterval(() => {
  fetch('http://localhost:8000/stats/summary')
    .then(r => r.json())
    .then(data => updateMetrics(data));
}, 5000);
```

**Dashboard updates (10-30 seconds):**
```javascript
setInterval(() => {
  fetch('http://localhost:8000/dashboard/stats?hours=24')
    .then(r => r.json())
    .then(data => updateDashboard(data));
}, 15000);
```

### Real-time Demo Flow

1. **Initial load:** `/dashboard/stats`
2. **Show CPU/Memory:** Display `metrics.cpu_usage` and `metrics.memory_usage`
3. **Show costs:** Display `cost.daily` and `savings.total_saved`
4. **Incident feed:** Map `incidents.recent` to timeline
5. **Trigger chaos:** POST to `/simulate/cpu_spike`
6. **Watch auto-scaling:** Poll `/stats/summary` to see metrics rise and pod count increase

### TypeScript Types

```typescript
interface DashboardStats {
  success: boolean;
  timestamp: string;
  cluster: {
    namespace: string;
    total_pods: number;
    healthy_pods: number;
    unhealthy_pods: number;
  };
  metrics: {
    cpu_usage: number;
    memory_usage: number;
    pod_count: number;
  };
  cost: {
    hourly: number;
    daily: number;
    monthly: number;
  };
  savings: {
    total_saved: number;
    projected_monthly: number;
    scale_down_count: number;
    scale_up_count: number;
  };
  incidents: {
    total: number;
    successful: number;
    success_rate: number;
    recent: Incident[];
  };
  recommendations: Recommendation[];
  health: {
    status: string;
    kubernetes: string;
    prometheus: string;
  };
}
```

---

## 🚀 Testing Endpoints

### Quick Test Sequence

```bash
# 1. Check health
curl http://localhost:8000/health

# 2. Get current stats
curl http://localhost:8000/dashboard/stats

# 3. Trigger CPU spike (auto-scaling test)
curl -X POST http://localhost:8000/simulate/cpu_spike?duration=120

# 4. Watch scaling in action (repeat every 5s)
curl http://localhost:8000/stats/summary

# 5. Check incidents
curl http://localhost:8000/incidents?limit=10

# 6. Check savings
curl http://localhost:8000/cost/savings?hours=1

# 7. Cleanup
curl -X POST http://localhost:8000/simulate/cleanup
```

---

## 📊 Response Codes

- `200` - Success
- `400` - Bad request (invalid parameters)
- `500` - Server error (check logs)

All endpoints return JSON with `success: true/false`.

---

## 🔧 CORS Configuration

CORS is enabled for all origins. Safe for local development.

---

## 📚 Interactive Documentation

FastAPI auto-generates interactive docs:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Test all endpoints directly in the browser!

---

## 💡 Frontend Tips

### Key Metrics to Display

1. **Hero metrics:** CPU %, Memory %, Pod count, Daily cost
2. **Savings badge:** "Saved $X.XX today"
3. **Success rate:** "98.5% incidents resolved"
4. **Charts:** CPU/Memory over time, Pod count timeline
5. **Incident feed:** Real-time log of actions taken

### Demo Scenario

```javascript
async function runDemo() {
  // 1. Show normal state
  const baseline = await fetch('/dashboard/stats').then(r => r.json());
  
  // 2. Trigger chaos
  await fetch('/simulate/cpu_spike?duration=120', { method: 'POST' });
  
  // 3. Watch auto-scaling (poll every 3 seconds for 2 minutes)
  const interval = setInterval(async () => {
    const stats = await fetch('/stats/summary').then(r => r.json());
    updateUI(stats);
    
    if (stats.cpu < 50) {
      clearInterval(interval);
      showSuccess('Auto-scaling completed!');
    }
  }, 3000);
}
```

---

Built with ❤️ by SentinelOps | [GitHub](https://github.com/yourusername/sentinelops)

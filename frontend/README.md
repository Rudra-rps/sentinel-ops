# SentinelOps Frontend Integration

## 🎯 Overview

This is the React + TypeScript dashboard for **SentinelOps** - a Kubernetes monitoring and auto-healing platform with chaos engineering capabilities.

The frontend is fully integrated with the backend API and provides:
- **Real-time metrics** (CPU, memory, pod counts)
- **Live cost analysis** with savings tracking
- **Incident timeline** showing auto-healing actions
- **AI-powered recommendations**
- **Chaos engineering controls** for testing resilience

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ or Bun
- SentinelOps backend running at `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
# or
bun install
```

### Development

```bash
npm run dev
# or
bun run dev
```

Visit `http://localhost:5173` (default Vite port)

### Production Build

```bash
npm run build
npm run preview
```

## 🔧 Configuration

### Environment Variables

Create `.env.development` for development:

```bash
VITE_API_URL=http://localhost:8000
```

Create `.env.production` for production:

```bash
VITE_API_URL=https://your-production-api.com
```

### API Configuration

Edit `src/lib/api-config.ts` to customize:

```typescript
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  POLLING_INTERVALS: {
    FAST: 3000,      // Real-time metrics
    NORMAL: 10000,   // Dashboard updates
    SLOW: 30000,     // Cost/recommendations
  },
  DEFAULT_NAMESPACE: 'demo',
  DEFAULT_TIME_WINDOW: 24,
  TIMEOUT: 10000,
};
```

## 📊 Architecture

### Key Files

```
src/
├── lib/
│   ├── api-config.ts      # API configuration
│   ├── api-types.ts       # TypeScript types
│   ├── api-service.ts     # API service layer
│   └── api-hooks.ts       # React hooks for data fetching
├── components/
│   └── dashboard/
│       ├── Header.tsx
│       ├── ScoreboardCards.tsx    # Hero metrics
│       ├── PerformanceChart.tsx   # Time-series charts
│       ├── CostAnalysis.tsx       # Cost breakdown
│       ├── IncidentFeed.tsx       # Real-time incidents
│       ├── Recommendations.tsx    # AI suggestions
│       └── ChaosPanel.tsx         # Chaos controls
└── pages/
    └── Index.tsx          # Main dashboard page
```

### Data Flow

1. **Dashboard Stats** (`/dashboard/stats?hours=24`)
   - Fetched every 10 seconds
   - Provides cluster health, cost, savings, incidents, recommendations

2. **Real-time Metrics** (`/stats/summary`)
   - Fetched every 3 seconds
   - Provides CPU, memory, pod count, cost

3. **Chaos Simulations** (`/simulate/*`)
   - Triggered by user actions
   - Executes CPU spike, crash, or cascade simulations

## 🎨 UI Components

Built with:
- **shadcn/ui** - High-quality React components
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Performance charts
- **Lucide React** - Icons
- **Sonner** - Toast notifications

Custom theme applies a "stadium scoreboard" aesthetic:
- LED-style fonts
- Neon border effects
- Real-time animations
- Dark mode optimized

## 🔥 Features

### Real-time Monitoring

- Live CPU and memory usage graphs
- Pod health status
- Instant alert notifications
- Auto-refreshing data

### Cost Analysis

- Current hourly/daily/monthly costs
- Savings from auto-scaling
- Monthly projections
- Efficiency scores

### Chaos Engineering

Three chaos tests available:
1. **CPU Spike** - Overload simulation
2. **Crash Pod** - Force pod failure
3. **Cascade** - Multi-service failure

Watch the system auto-heal in real-time!

### Incident Timeline

- Chronological log of all events
- Action details and resolution times
- Color-coded severity levels
- Success rate tracking

## 🛠️ API Integration

### Custom Hooks

```typescript
import { useDashboard, useRealtimeMetrics, useChaosSimulation } from '@/lib/api-hooks';

// Full dashboard data
const { data, isLoading, error, refresh } = useDashboard({
  refreshInterval: 10000,
  hours: 24,
});

// Fast polling for metrics
const { data: metrics } = useRealtimeMetrics(true);

// Chaos testing
const { simulateCPUSpike, simulateCrash, isSimulating } = useChaosSimulation();
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

## 🧪 Testing

```bash
npm run test
```

## 📦 Deployment

### Static Hosting (Vercel, Netlify, etc.)

```bash
npm run build
# Deploy the 'dist' folder
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run build
RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

## 🐛 Troubleshooting

### Backend Connection Issues

**Problem:** "Unable to connect to the SentinelOps backend"

**Solutions:**
1. Ensure backend is running: `cd .. && python test_backend.py`
2. Check backend URL in `.env`: `VITE_API_URL=http://localhost:8000`
3. Verify CORS is enabled in backend
4. Check browser console for errors

### Data Not Updating

**Problem:** Metrics appear frozen

**Solutions:**
1. Check browser Network tab for failed requests
2. Verify polling intervals in `api-config.ts`
3. Check backend health: `curl http://localhost:8000/health`
4. Look for JavaScript errors in console

## 📚 Learn More

- [Backend API Documentation](../API.md)
- [Project Status](../STATUS.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

---

**Built with ❤️ for DevOps engineers who want their clusters to be self-healing, cost-optimized, and chaos-proof.**

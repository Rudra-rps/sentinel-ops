# 🚀 SentinelOps Deployment Guide

Complete deployment instructions for all environments.

---

## 📋 Table of Contents

- [Quick Start (Docker Compose)](#-quick-start-docker-compose)
- [Cloud Deployment](#-cloud-deployment-vercel--railway)
- [Full Kubernetes Deployment](#-full-kubernetes-deployment)
- [Environment Variables](#-environment-variables)
- [Troubleshooting](#-troubleshooting)

---

## 🐳 Quick Start (Docker Compose)

**Best for**: Local testing, hackathon demos, judges running locally

### Prerequisites
- Docker Desktop installed and running
- 4GB RAM available
- Ports 80 and 8000 available

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sentinel-ops.git
cd sentinel-ops
```

2. **Start the application**
```bash
docker-compose up -d --build
```

3. **Access the dashboard**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

4. **Verify it's working**
```bash
# Check container status
docker-compose ps

# Test backend health
curl http://localhost:8000/health

# Test frontend (should return HTML)
curl http://localhost
```

### What's Included

✅ Frontend (React + Nginx)  
✅ Backend (FastAPI)  
✅ Reverse proxy configuration  
✅ Health checks  
✅ Auto-restart on failure

### Limitations

⚠️ No real Kubernetes cluster (mock data only)  
⚠️ Chaos testing shows appropriate messages  
⚠️ Some features require kubectl

### Stop the Application

```bash
docker-compose down
```

---

## ☁️ Cloud Deployment (Vercel + Railway)

**Best for**: Live demo URL, easy access for judges, no installation required

### Architecture

```
Frontend (Vercel) → Backend (Railway) → Mock Data
     ↓                    ↓
  HTTPS              HTTPS + CORS
```

### Part 1: Deploy Backend to Railway

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize project**
```bash
cd sentinel-ops
railway init
```

4. **Configure backend**

Create `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn mcp_server.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

5. **Deploy**
```bash
railway up
```

6. **Get your backend URL**
```bash
railway status
# Copy the URL (e.g., https://your-app.railway.app)
```

### Part 2: Deploy Frontend to Vercel

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Configure frontend**

Update `frontend/.env.production`:
```bash
VITE_API_URL=https://your-backend.railway.app
```

3. **Deploy**
```bash
cd frontend
vercel --prod
```

4. **Get your frontend URL**
```bash
# Vercel will output the URL
# e.g., https://sentinel-ops.vercel.app
```

### Part 3: Update CORS

Update `mcp_server/main.py` with your frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # For development
        "https://sentinel-ops.vercel.app",  # Your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Redeploy backend:
```bash
railway up
```

### Verify Cloud Deployment

1. Visit your Vercel URL
2. Dashboard should load
3. Check browser console for errors
4. Test API endpoints

### Cost

- **Vercel**: Free tier (100GB bandwidth/month)
- **Railway**: Free tier ($5 credit/month)
- **Total**: $0/month for demo purposes

---

## 🎯 Full Kubernetes Deployment

**Best for**: Complete feature demonstration, production-ready setup

### Prerequisites

- Kubernetes cluster (GKE, EKS, AKS, or Minikube)
- kubectl installed and configured
- Helm (optional)

### Option A: Minikube (Local)

1. **Start Minikube**
```bash
minikube start --cpus=4 --memory=8192 --driver=docker
```

2. **Deploy demo applications**
```bash
# Create namespace
kubectl create namespace demo

# Deploy nginx demo
kubectl apply -f demo/nginx-deploy.yaml

# Deploy Prometheus
kubectl apply -f demo/prometheus-deploy.yaml
```

3. **Verify pods**
```bash
kubectl get pods -n demo
kubectl get pods -n monitoring
```

4. **Start backend locally**
```bash
# Backend needs kubectl access
python -m uvicorn mcp_server.main:app --reload
```

5. **Start frontend locally**
```bash
cd frontend
npm run dev
```

6. **Access**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

### Option B: Cloud Kubernetes (GKE/EKS/AKS)

1. **Create cluster**
```bash
# GKE example
gcloud container clusters create sentinelops \
  --num-nodes=3 \
  --machine-type=e2-medium \
  --zone=us-central1-a
```

2. **Deploy applications**
```bash
kubectl apply -f demo/nginx-deploy.yaml
kubectl apply -f demo/prometheus-deploy.yaml
```

3. **Deploy backend to cluster**

Create `k8s/backend-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentinelops-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sentinelops-backend
  template:
    metadata:
      labels:
        app: sentinelops-backend
    spec:
      containers:
      - name: backend
        image: your-registry/sentinelops-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: PORT
          value: "8000"
---
apiVersion: v1
kind: Service
metadata:
  name: sentinelops-backend
spec:
  selector:
    app: sentinelops-backend
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

4. **Deploy frontend**

Update `VITE_API_URL` to backend service URL and deploy to Vercel.

---

## 🔐 Environment Variables

### Backend (.env)

```bash
# Kubernetes (optional - uses default kubeconfig)
# KUBECONFIG=~/.kube/config

# Prometheus (optional)
# PROMETHEUS_URL=http://localhost:9090

# Server
# PORT=8000
# HOST=0.0.0.0

# Logging
# LOG_LEVEL=INFO
```

### Frontend (.env)

```bash
# Backend API URL
# For Docker Compose (uses nginx proxy)
VITE_API_URL=

# For cloud deployment
# VITE_API_URL=https://your-backend.railway.app

# Timeout (milliseconds)
# VITE_API_TIMEOUT_MS=30000
```

---

## 🐛 Troubleshooting

### Docker Compose Issues

**Problem**: Containers won't start
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild
docker-compose down
docker-compose up -d --build
```

**Problem**: Frontend shows connection error
```bash
# Hard refresh browser
Ctrl + Shift + R

# Check backend is running
curl http://localhost:8000/health
```

### Cloud Deployment Issues

**Problem**: CORS errors
- Update `mcp_server/main.py` with correct frontend URL
- Redeploy backend
- Clear browser cache

**Problem**: 500 errors from backend
- Check Railway logs: `railway logs`
- Verify environment variables
- Check if kubectl is available (it won't be in cloud deployment)

### Kubernetes Issues

**Problem**: Pods not starting
```bash
# Check pod status
kubectl get pods -n demo
kubectl describe pod <pod-name> -n demo

# Check logs
kubectl logs <pod-name> -n demo
```

**Problem**: Backend can't connect to cluster
```bash
# Verify kubectl works
kubectl cluster-info

# Check kubeconfig
echo $KUBECONFIG

# Restart minikube
minikube stop
minikube start
```

---

## 📊 Deployment Comparison

| Feature | Docker Compose | Cloud (Vercel+Railway) | Full Kubernetes |
|---------|---------------|----------------------|-----------------|
| **Setup Time** | 5 minutes | 30 minutes | 1-2 hours |
| **Cost** | Free | Free (demo tier) | $10-50/month |
| **Kubernetes Features** | ❌ Mock data | ❌ Mock data | ✅ Full features |
| **Live URL** | ❌ Local only | ✅ Public URL | ✅ Public URL |
| **Best For** | Local testing | Hackathon demo | Production |

---

## 🎯 Recommended for Hackathon

**Best approach**: **Hybrid**

1. **Primary**: Deploy to Vercel + Railway for live demo URL
2. **Backup**: Provide Docker Compose for judges to run locally
3. **Documentation**: Include both deployment methods in README

This gives you:
- ✅ Easy access for judges (live URL)
- ✅ Backup if cloud has issues (Docker Compose)
- ✅ Professional presentation
- ✅ No cost

---

## 📞 Support

For issues or questions:
1. Check [README.md](README.md) for general documentation
2. Check [TEST_GUIDE.md](TEST_GUIDE.md) for testing instructions
3. Review error logs
4. Open an issue on GitHub

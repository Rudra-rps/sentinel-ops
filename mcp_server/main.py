"""
SentinelOps MCP Server - Main FastAPI application
Autonomous Kubernetes SRE powered by Model Context Protocol
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import logging
import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from tools.k8s_client import k8s_client
from tools.prometheus import prometheus_client
from tools.chaos import chaos_engine
from agents.cost_analyzer import cost_analyzer
from mcp_server.config import (
    K8S_NAMESPACE, PROMETHEUS_URL, LOG_LEVEL, 
    ACTIONS_LOG, INCIDENTS_LOG
)

# Initialize FastAPI app
app = FastAPI(
    title="SentinelOps MCP Server",
    description="Autonomous AI SRE for Kubernetes",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(ACTIONS_LOG),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "name": "SentinelOps MCP Server",
        "version": "1.0.0",
        "status": "running",
        "description": "Autonomous AI SRE for Kubernetes",
        "endpoints": {
            "core": {
                "health": "/health",
                "metrics": "/metrics",
                "pods": "/pods",
                "deployments": "/deployments",
                "nodes": "/nodes"
            },
            "dashboard": {
                "stats": "/dashboard/stats?hours=24",
                "summary": "/stats/summary"
            },
            "control": {
                "scale": "/scale",
                "restart": "/restart",
                "delete_pod": "/delete_pod"
            },
            "cost": {
                "current": "/cost/current",
                "savings": "/cost/savings?hours=24",
                "recommendations": "/cost/recommendations",
                "breakdown": "/cost/breakdown?hours=24"
            },
            "incidents": {
                "list": "/incidents?limit=50",
                "log": "/incidents (POST)"
            },
            "chaos": {
                "cpu_spike": "/simulate/cpu_spike",
                "crash": "/simulate/crash",
                "cascade": "/simulate/cascade",
                "cleanup": "/simulate/cleanup",
                "status": "/chaos/status"
            }
        },
        "docs": "/docs",
        "frontend_tips": {
            "best_endpoint": "/dashboard/stats - All data in one call",
            "quick_stats": "/stats/summary - Lightweight metrics",
            "real_time": "Poll /dashboard/stats every 5-10 seconds"
        }
    }


@app.get("/health")
def health():
    """Health check endpoint"""
    k8s_healthy = True
    prometheus_healthy = prometheus_client.is_healthy()
    
    return {
        "status": "healthy" if k8s_healthy and prometheus_healthy else "degraded",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "kubernetes": "healthy" if k8s_healthy else "unhealthy",
            "prometheus": "healthy" if prometheus_healthy else "unhealthy"
        }
    }


# ============================================================================
# METRICS ENDPOINTS
# ============================================================================

@app.get("/metrics")
def get_metrics(namespace: str = Query(default=K8S_NAMESPACE)):
    """Get all metrics for a namespace"""
    try:
        metrics = prometheus_client.get_all_metrics(namespace)
        logger.info(f"Retrieved metrics for namespace {namespace}")
        return {
            "success": True,
            "namespace": namespace,
            "metrics": metrics
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/cpu")
def get_cpu_metrics(
    namespace: str = Query(default=K8S_NAMESPACE),
    deployment: str = Query(default=None)
):
    """Get CPU usage metrics"""
    try:
        cpu_usage = prometheus_client.get_cpu_usage(namespace, deployment)
        return {
            "success": True,
            "namespace": namespace,
            "deployment": deployment,
            "cpu_usage_percent": round(cpu_usage, 2)
        }
    except Exception as e:
        logger.error(f"Error getting CPU metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics/memory")
def get_memory_metrics(
    namespace: str = Query(default=K8S_NAMESPACE),
    deployment: str = Query(default=None)
):
    """Get memory usage metrics"""
    try:
        memory_usage = prometheus_client.get_memory_usage(namespace, deployment)
        return {
            "success": True,
            "namespace": namespace,
            "deployment": deployment,
            "memory_usage_percent": round(memory_usage, 2)
        }
    except Exception as e:
        logger.error(f"Error getting memory metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# KUBERNETES RESOURCE ENDPOINTS
# ============================================================================

@app.get("/pods")
def get_pods(namespace: str = Query(default=K8S_NAMESPACE)):
    """Get all pods in namespace"""
    try:
        pods = k8s_client.get_pods(namespace)
        return {
            "success": True,
            "namespace": namespace,
            "count": len(pods),
            "pods": pods
        }
    except Exception as e:
        logger.error(f"Error getting pods: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/deployments")
def get_deployments(namespace: str = Query(default=K8S_NAMESPACE)):
    """Get all deployments in namespace"""
    try:
        deployments = k8s_client.get_deployments(namespace)
        return {
            "success": True,
            "namespace": namespace,
            "count": len(deployments),
            "deployments": deployments
        }
    except Exception as e:
        logger.error(f"Error getting deployments: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/nodes")
def get_nodes():
    """Get all nodes in cluster"""
    try:
        nodes = k8s_client.get_nodes()
        return {
            "success": True,
            "count": len(nodes),
            "nodes": nodes
        }
    except Exception as e:
        logger.error(f"Error getting nodes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CONTROL ENDPOINTS (Actions)
# ============================================================================

@app.post("/scale")
def scale_deployment(
    deployment: str,
    replicas: int,
    namespace: str = Query(default=K8S_NAMESPACE)
):
    """Scale a deployment to specified number of replicas"""
    try:
        success = k8s_client.scale_deployment(deployment, replicas, namespace)
        
        if success:
            logger.info(f"Scaled {deployment} to {replicas} replicas in {namespace}")
            log_action("scale", deployment, namespace, {"replicas": replicas})
            
            return {
                "success": True,
                "action": "scale",
                "deployment": deployment,
                "namespace": namespace,
                "replicas": replicas,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to scale deployment")
    
    except Exception as e:
        logger.error(f"Error scaling deployment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/restart")
def restart_deployment(
    deployment: str,
    namespace: str = Query(default=K8S_NAMESPACE)
):
    """Restart a deployment (rolling restart)"""
    try:
        success = k8s_client.restart_deployment(deployment, namespace)
        
        if success:
            logger.info(f"Restarted deployment {deployment} in {namespace}")
            log_action("restart", deployment, namespace, {})
            
            return {
                "success": True,
                "action": "restart",
                "deployment": deployment,
                "namespace": namespace,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to restart deployment")
    
    except Exception as e:
        logger.error(f"Error restarting deployment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/delete_pod")
def delete_pod(
    pod_name: str,
    namespace: str = Query(default=K8S_NAMESPACE)
):
    """Delete a pod (will be recreated by deployment)"""
    try:
        success = k8s_client.delete_pod(pod_name, namespace)
        
        if success:
            logger.info(f"Deleted pod {pod_name} in {namespace}")
            log_action("delete_pod", pod_name, namespace, {})
            
            return {
                "success": True,
                "action": "delete_pod",
                "pod": pod_name,
                "namespace": namespace,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to delete pod")
    
    except Exception as e:
        logger.error(f"Error deleting pod: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs/{pod_name}")
def get_pod_logs(
    pod_name: str,
    namespace: str = Query(default=K8S_NAMESPACE),
    tail: int = Query(default=100)
):
    """Get logs from a pod"""
    try:
        logs = k8s_client.get_pod_logs(pod_name, namespace, tail)
        return {
            "success": True,
            "pod": pod_name,
            "namespace": namespace,
            "logs": logs
        }
    except Exception as e:
        logger.error(f"Error getting pod logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# INCIDENT TRACKING
# ============================================================================

@app.get("/incidents")
def get_incidents(limit: int = Query(default=50)):
    """Get recent incidents from log file"""
    try:
        incidents = []
        incident_file = Path(INCIDENTS_LOG)
        
        if incident_file.exists():
            with open(incident_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    try:
                        incident = json.loads(line.strip())
                        incidents.append(incident)
                    except json.JSONDecodeError:
                        continue
        
        return {
            "success": True,
            "count": len(incidents),
            "incidents": incidents
        }
    except Exception as e:
        logger.error(f"Error getting incidents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/incidents")
def log_incident(incident: dict):
    """Log a new incident"""
    try:
        incident["timestamp"] = datetime.now().isoformat()
        
        with open(INCIDENTS_LOG, 'a') as f:
            f.write(json.dumps(incident) + '\n')
        
        logger.info(f"Logged incident: {incident.get('type', 'unknown')}")
        
        return {
            "success": True,
            "incident": incident
        }
    except Exception as e:
        logger.error(f"Error logging incident: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# COST ANALYSIS ENDPOINTS
# ============================================================================

@app.get("/cost/current")
def get_current_cost():
    """
    Get current infrastructure cost based on running resources
    """
    try:
        cost_data = cost_analyzer.calculate_current_cost()
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "cost": cost_data
        }
    except Exception as e:
        logger.error(f"Error calculating current cost: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cost/savings")
def get_savings(hours: int = Query(default=24)):
    """
    Calculate savings from auto-scaling over specified time period
    """
    try:
        savings_data = cost_analyzer.calculate_savings(hours)
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "savings": savings_data
        }
    except Exception as e:
        logger.error(f"Error calculating savings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cost/recommendations")
def get_cost_recommendations():
    """
    Get cost optimization recommendations
    """
    try:
        recommendations = cost_analyzer.get_optimization_recommendations()
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "recommendations": recommendations,
            "count": len(recommendations)
        }
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cost/breakdown")
def get_cost_breakdown(hours: int = Query(default=24)):
    """
    Get comprehensive cost breakdown with analysis
    """
    try:
        breakdown = cost_analyzer.get_cost_breakdown(hours)
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "breakdown": breakdown
        }
    except Exception as e:
        logger.error(f"Error getting cost breakdown: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DASHBOARD / STATS ENDPOINTS
# ============================================================================

@app.get("/dashboard/stats")
def get_dashboard_stats(hours: int = Query(default=24)):
    """
    Get comprehensive stats for dashboard (one-stop endpoint for frontend)
    Combines metrics, cost, incidents, and recommendations
    """
    try:
        # Gather all data
        pods = k8s_client.get_pods(K8S_NAMESPACE)
        deployments = k8s_client.get_deployments(K8S_NAMESPACE)
        metrics = prometheus_client.get_all_metrics(K8S_NAMESPACE)
        current_cost = cost_analyzer.calculate_current_cost()
        savings = cost_analyzer.calculate_savings(hours)
        recommendations = cost_analyzer.get_optimization_recommendations()
        
        # Get recent incidents
        incidents = []
        incident_file = Path(INCIDENTS_LOG)
        if incident_file.exists():
            with open(incident_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-20:]:  # Last 20 incidents
                    try:
                        incidents.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
        
        # Calculate success rate
        successful_incidents = len([i for i in incidents if i.get('result', {}).get('success', False)])
        success_rate = (successful_incidents / len(incidents) * 100) if len(incidents) > 0 else 100.0
        
        # Build comprehensive response
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "cluster": {
                "namespace": K8S_NAMESPACE,
                "total_pods": len(pods),
                "total_deployments": len(deployments),
                "healthy_pods": len([p for p in pods if p.get('status') == 'Running']),
                "unhealthy_pods": len([p for p in pods if p.get('status') != 'Running'])
            },
            "metrics": {
                "cpu_usage": round(metrics.get("cpu_usage", 0.0), 1),
                "memory_usage": round(metrics.get("memory_usage", 0.0), 1),
                "pod_count": metrics.get("pod_count", 0),
                "timestamp": metrics.get("timestamp", datetime.now().isoformat())
            },
            "cost": {
                "hourly": current_cost.get("hourly_cost", 0),
                "daily": current_cost.get("daily_cost", 0),
                "monthly": current_cost.get("monthly_cost", 0),
                "total_pods": current_cost.get("total_pods", 0),
                "total_cpu_cores": current_cost.get("total_cpu_cores", 0),
                "total_memory_gb": current_cost.get("total_memory_gb", 0)
            },
            "savings": {
                "total_saved": savings.get("total_saved", 0),
                "time_period_hours": hours,
                "projected_monthly": savings.get("projected_monthly_savings", 0),
                "projected_yearly": savings.get("projected_yearly_savings", 0),
                "scale_down_count": savings.get("scale_down_count", 0),
                "scale_up_count": savings.get("scale_up_count", 0)
            },
            "incidents": {
                "total": len(incidents),
                "successful": successful_incidents,
                "success_rate": round(success_rate, 1),
                "recent": incidents[-10:] if len(incidents) > 10 else incidents
            },
            "recommendations": recommendations[:5],  # Top 5 recommendations
            "health": {
                "status": "healthy" if success_rate > 80 else "degraded",
                "kubernetes": "connected",
                "prometheus": "connected" if prometheus_client.is_healthy() else "disconnected"
            }
        }
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats/summary")
def get_stats_summary():
    """
    Quick summary stats (lighter version of dashboard/stats)
    """
    try:
        pods = k8s_client.get_pods(K8S_NAMESPACE)
        metrics = prometheus_client.get_all_metrics(K8S_NAMESPACE)
        current_cost = cost_analyzer.calculate_current_cost()
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "pods": len(pods),
            "cpu": round(metrics.get("cpu_usage", 0.0), 1),
            "memory": round(metrics.get("memory_usage", 0.0), 1),
            "daily_cost": current_cost.get("daily_cost", 0),
            "status": "operational"
        }
    except Exception as e:
        logger.error(f"Error getting summary stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CHAOS / SIMULATION ENDPOINTS
# ============================================================================

@app.post("/simulate/cpu_spike")
def simulate_cpu_spike(
    deployment: str = Query(default="nginx-demo"),
    duration: int = Query(default=300)
):
    """
    Simulate CPU spike using stress container
    """
    try:
        result = chaos_engine.simulate_cpu_spike(deployment, duration)
        return result
    except Exception as e:
        logger.error(f"Error simulating CPU spike: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulate/crash")
def simulate_crash(deployment: str = Query(default="nginx-demo")):
    """
    Simulate pod crash by deleting a random pod
    """
    try:
        result = chaos_engine.simulate_pod_crash(deployment)
        return result
    except Exception as e:
        logger.error(f"Error simulating crash: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulate/cascade")
def simulate_cascade(deployment: str = Query(default="nginx-demo")):
    """
    Simulate cascade failure by crashing multiple pods
    """
    try:
        result = chaos_engine.simulate_cascade_failure(deployment)
        return result
    except Exception as e:
        logger.error(f"Error simulating cascade failure: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulate/cleanup")
def cleanup_simulations():
    """
    Clean up stress test pods
    """
    try:
        result = chaos_engine.cleanup_stress_tests()
        return result
    except Exception as e:
        logger.error(f"Error cleaning up simulations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chaos/status")
def chaos_status():
    """
    Get status of active chaos simulations
    """
    try:
        return {
            "success": True,
            "active_simulations": chaos_engine.get_active_simulations(),
            "recent_events": chaos_engine.get_recent_events()
        }
    except Exception as e:
        logger.error(f"Error getting chaos status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log_action(action_type: str, resource: str, namespace: str, details: dict):
    """Log an action to actions log"""
    action_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action_type,
        "resource": resource,
        "namespace": namespace,
        "details": details
    }
    logger.info(f"Action: {json.dumps(action_entry)}")


# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 60)
    logger.info("SentinelOps MCP Server Starting")
    logger.info(f"Kubernetes Namespace: {K8S_NAMESPACE}")
    logger.info(f"Prometheus URL: {PROMETHEUS_URL}")
    logger.info("=" * 60)
    
    # Ensure log directory exists
    Path(ACTIONS_LOG).parent.mkdir(parents=True, exist_ok=True)
    Path(INCIDENTS_LOG).parent.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

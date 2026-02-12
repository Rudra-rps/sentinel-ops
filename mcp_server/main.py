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
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "pods": "/pods",
            "deployments": "/deployments",
            "scale": "/scale",
            "restart": "/restart",
            "delete_pod": "/delete_pod"
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

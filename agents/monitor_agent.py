"""
Monitor Agent - Collects metrics and analyzes system health
"""
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from tools.k8s_client import k8s_client
from tools.prometheus import prometheus_client
from mcp_server.config import (
    CPU_HIGH_THRESHOLD,
    CPU_LOW_THRESHOLD,
    MEMORY_HIGH_THRESHOLD,
    K8S_NAMESPACE
)

logger = logging.getLogger(__name__)


class MonitorAgent:
    """
    Monitors Kubernetes cluster metrics and detects issues
    """
    
    def __init__(self, namespace: str = K8S_NAMESPACE):
        self.namespace = namespace
        self.last_metrics = {}
    
    def collect_metrics(self) -> Dict:
        """
        Collect all relevant metrics from Prometheus and Kubernetes
        """
        try:
            # Get Prometheus metrics
            prom_metrics = prometheus_client.get_all_metrics(self.namespace)
            
            # Get Kubernetes pod status
            pods = k8s_client.get_pods(self.namespace)
            deployments = k8s_client.get_deployments(self.namespace)
            
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "namespace": self.namespace,
                "cpu_usage": prom_metrics.get("cpu_usage", 0.0),
                "memory_usage": prom_metrics.get("memory_usage", 0.0),
                "pod_count": len(pods),
                "pod_status": self._analyze_pod_status(pods),
                "deployments": deployments,
                "container_restarts": prom_metrics.get("container_restarts", 0),
                "node_cpu": prom_metrics.get("node_cpu", 0.0),
                "node_memory": prom_metrics.get("node_memory", 0.0),
            }
            
            self.last_metrics = metrics
            logger.debug(f"Collected metrics: CPU={metrics['cpu_usage']:.1f}%, "
                        f"Memory={metrics['memory_usage']:.1f}%, "
                        f"Pods={metrics['pod_count']}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return self.last_metrics if self.last_metrics else {}
    
    def _analyze_pod_status(self, pods: List[Dict]) -> Dict:
        """
        Analyze pod status and categorize
        """
        status_counts = {
            "running": 0,
            "pending": 0,
            "failed": 0,
            "crashloopbackoff": 0,
            "unknown": 0
        }
        
        problematic_pods = []
        
        for pod in pods:
            status = pod.get("status", "Unknown").lower()
            
            if status == "running":
                status_counts["running"] += 1
            elif status == "pending":
                status_counts["pending"] += 1
                problematic_pods.append({
                    "name": pod["name"],
                    "issue": "pending",
                    "restarts": pod.get("restarts", 0)
                })
            elif "crash" in status.lower() or "backoff" in status.lower():
                status_counts["crashloopbackoff"] += 1
                problematic_pods.append({
                    "name": pod["name"],
                    "issue": "crashloop",
                    "restarts": pod.get("restarts", 0)
                })
            elif status == "failed":
                status_counts["failed"] += 1
                problematic_pods.append({
                    "name": pod["name"],
                    "issue": "failed",
                    "restarts": pod.get("restarts", 0)
                })
            else:
                status_counts["unknown"] += 1
        
        return {
            "counts": status_counts,
            "problematic_pods": problematic_pods
        }
    
    def analyze_metrics(self, metrics: Dict) -> List[Dict]:
        """
        Analyze metrics and identify issues based on thresholds
        """
        issues = []
        
        # CPU Analysis
        cpu_usage = metrics.get("cpu_usage", 0.0)
        if cpu_usage > CPU_HIGH_THRESHOLD:
            issues.append({
                "type": "cpu_overload",
                "severity": "high",
                "value": cpu_usage,
                "threshold": CPU_HIGH_THRESHOLD,
                "message": f"CPU usage ({cpu_usage:.1f}%) exceeds threshold ({CPU_HIGH_THRESHOLD}%)",
                "resource": self.namespace,
                "timestamp": datetime.now().isoformat()
            })
        elif cpu_usage < CPU_LOW_THRESHOLD:
            # Get deployment info to check if we can scale down
            deployments = metrics.get("deployments", [])
            for deployment in deployments:
                if deployment.get("replicas", 0) > 2:  # Don't suggest scale down if already at minimum
                    issues.append({
                        "type": "cpu_underutilized",
                        "severity": "low",
                        "value": cpu_usage,
                        "threshold": CPU_LOW_THRESHOLD,
                        "message": f"CPU usage ({cpu_usage:.1f}%) below threshold ({CPU_LOW_THRESHOLD}%), possible cost savings",
                        "resource": deployment["name"],
                        "timestamp": datetime.now().isoformat()
                    })
        
        # Memory Analysis
        memory_usage = metrics.get("memory_usage", 0.0)
        if memory_usage > MEMORY_HIGH_THRESHOLD:
            issues.append({
                "type": "memory_pressure",
                "severity": "medium",
                "value": memory_usage,
                "threshold": MEMORY_HIGH_THRESHOLD,
                "message": f"Memory usage ({memory_usage:.1f}%) exceeds threshold ({MEMORY_HIGH_THRESHOLD}%)",
                "resource": self.namespace,
                "timestamp": datetime.now().isoformat()
            })
        
        # Pod Status Analysis
        pod_status = metrics.get("pod_status", {})
        problematic_pods = pod_status.get("problematic_pods", [])
        
        for pod_info in problematic_pods:
            issue_type = pod_info["issue"]
            
            if issue_type == "crashloop":
                issues.append({
                    "type": "pod_crashloop",
                    "severity": "high",
                    "value": pod_info["restarts"],
                    "message": f"Pod {pod_info['name']} is in CrashLoopBackOff state",
                    "resource": pod_info["name"],
                    "timestamp": datetime.now().isoformat()
                })
            
            elif issue_type == "pending":
                issues.append({
                    "type": "pod_pending",
                    "severity": "medium",
                    "message": f"Pod {pod_info['name']} stuck in Pending state",
                    "resource": pod_info["name"],
                    "timestamp": datetime.now().isoformat()
                })
            
            elif issue_type == "failed":
                issues.append({
                    "type": "pod_failed",
                    "severity": "high",
                    "message": f"Pod {pod_info['name']} has failed",
                    "resource": pod_info["name"],
                    "timestamp": datetime.now().isoformat()
                })
        
        # High restart count analysis
        restart_count = metrics.get("container_restarts", 0)
        if restart_count > 10:
            issues.append({
                "type": "high_restart_count",
                "severity": "medium",
                "value": restart_count,
                "message": f"Total container restarts ({restart_count}) is high",
                "resource": self.namespace,
                "timestamp": datetime.now().isoformat()
            })
        
        if issues:
            logger.warning(f"Detected {len(issues)} issue(s): {[i['type'] for i in issues]}")
        else:
            logger.info("No issues detected - system healthy")
        
        return issues
    
    def get_health_summary(self) -> Dict:
        """
        Get overall health summary
        """
        metrics = self.collect_metrics()
        issues = self.analyze_metrics(metrics)
        
        # Determine overall health status
        if not issues:
            health_status = "healthy"
        elif any(i["severity"] == "high" for i in issues):
            health_status = "critical"
        elif any(i["severity"] == "medium" for i in issues):
            health_status = "degraded"
        else:
            health_status = "warning"
        
        return {
            "status": health_status,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "issues": issues,
            "issue_count": len(issues)
        }


# Create singleton instance
monitor_agent = MonitorAgent()


if __name__ == "__main__":
    # Test the monitor agent
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    print("=" * 60)
    print("Testing Monitor Agent")
    print("=" * 60)
    
    agent = MonitorAgent()
    
    # Collect metrics
    print("\n1. Collecting metrics...")
    metrics = agent.collect_metrics()
    print(f"   CPU: {metrics.get('cpu_usage', 0):.1f}%")
    print(f"   Memory: {metrics.get('memory_usage', 0):.1f}%")
    print(f"   Pods: {metrics.get('pod_count', 0)}")
    
    # Analyze for issues
    print("\n2. Analyzing for issues...")
    issues = agent.analyze_metrics(metrics)
    if issues:
        print(f"   Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"   - [{issue['severity'].upper()}] {issue['type']}: {issue['message']}")
    else:
        print("   ✓ No issues detected")
    
    # Get health summary
    print("\n3. Health Summary...")
    summary = agent.get_health_summary()
    print(f"   Overall Status: {summary['status'].upper()}")
    print("=" * 60)

"""
Healer Agent - Handles auto-healing of failed pods and deployments
"""
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from tools.k8s_client import k8s_client
from mcp_server.config import K8S_NAMESPACE

logger = logging.getLogger(__name__)


class HealerAgent:
    """
    Automatically heals failed or problematic pods
    """
    
    def __init__(self, namespace: str = K8S_NAMESPACE):
        self.namespace = namespace
        self.restart_threshold = 5  # Restart deployment if pod restarts exceed this
    
    def restart_pod(self, pod_name: str, reason: str = "") -> Dict:
        """
        Delete a pod (Kubernetes will recreate it)
        """
        try:
            success = k8s_client.delete_pod(pod_name, self.namespace)
            
            if success:
                logger.info(f"Restarted pod {pod_name}. Reason: {reason}")
                return {
                    "success": True,
                    "action": "restart_pod",
                    "pod": pod_name,
                    "reason": reason,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"success": False, "reason": "k8s_error"}
                
        except Exception as e:
            logger.error(f"Error restarting pod {pod_name}: {e}")
            return {"success": False, "reason": str(e)}
    
    def restart_deployment(self, deployment: str, reason: str = "") -> Dict:
        """
        Perform rolling restart of deployment
        """
        try:
            success = k8s_client.restart_deployment(deployment, self.namespace)
            
            if success:
                logger.info(f"Restarted deployment {deployment}. Reason: {reason}")
                return {
                    "success": True,
                    "action": "restart_deployment",
                    "deployment": deployment,
                    "reason": reason,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"success": False, "reason": "k8s_error"}
                
        except Exception as e:
            logger.error(f"Error restarting deployment {deployment}: {e}")
            return {"success": False, "reason": str(e)}
    
    def heal_crashloop(self, pod_info: Dict) -> Dict:
        """
        Handle pod in CrashLoopBackOff state
        """
        pod_name = pod_info.get("name")
        restarts = pod_info.get("restarts", 0)
        
        logger.warning(f"Healing CrashLoopBackOff pod: {pod_name} (restarts: {restarts})")
        
        if restarts > self.restart_threshold:
            # If many restarts, restart entire deployment
            deployment = pod_name.rsplit('-', 2)[0]  # Extract deployment name
            logger.info(f"High restart count ({restarts}), restarting deployment {deployment}")
            return self.restart_deployment(
                deployment, 
                reason=f"Pod {pod_name} has {restarts} restarts"
            )
        else:
            # Just restart the pod
            return self.restart_pod(
                pod_name,
                reason="CrashLoopBackOff detected"
            )
    
    def heal_pending(self, pod_info: Dict) -> Dict:
        """
        Handle pod stuck in Pending state
        """
        pod_name = pod_info.get("name")
        logger.warning(f"Healing Pending pod: {pod_name}")
        
        # Try restarting the pod
        return self.restart_pod(
            pod_name,
            reason="Pod stuck in Pending state"
        )
    
    def heal_failed(self, pod_info: Dict) -> Dict:
        """
        Handle failed pod
        """
        pod_name = pod_info.get("name")
        logger.warning(f"Healing Failed pod: {pod_name}")
        
        # Restart the pod
        return self.restart_pod(
            pod_name,
            reason="Pod in Failed state"
        )
    
    def check_and_heal(self) -> List[Dict]:
        """
        Check all pods and heal any issues found
        """
        actions_taken = []
        
        try:
            pods = k8s_client.get_pods(self.namespace)
            
            for pod in pods:
                pod_name = pod.get("name")
                status = pod.get("status", "").lower()
                restarts = pod.get("restarts", 0)
                
                # Check for CrashLoopBackOff
                if "crash" in status or "backoff" in status:
                    result = self.heal_crashloop(pod)
                    if result.get("success"):
                        actions_taken.append(result)
                
                # Check for Pending (stuck for more than 5 minutes would need age check)
                elif status == "pending":
                    result = self.heal_pending(pod)
                    if result.get("success"):
                        actions_taken.append(result)
                
                # Check for Failed
                elif status == "failed":
                    result = self.heal_failed(pod)
                    if result.get("success"):
                        actions_taken.append(result)
                
                # Check for high restart count even if running
                elif restarts > self.restart_threshold:
                    logger.warning(f"Pod {pod_name} has high restart count: {restarts}")
                    # Could take action here if needed
            
            if actions_taken:
                logger.info(f"Healing complete: {len(actions_taken)} action(s) taken")
            
            return actions_taken
            
        except Exception as e:
            logger.error(f"Error in check_and_heal: {e}")
            return actions_taken
    
    def get_problematic_pods(self) -> List[Dict]:
        """
        Get list of pods that need attention
        """
        problematic = []
        
        try:
            pods = k8s_client.get_pods(self.namespace)
            
            for pod in pods:
                status = pod.get("status", "").lower()
                restarts = pod.get("restarts", 0)
                
                if status != "running" or restarts > self.restart_threshold:
                    problematic.append({
                        "name": pod.get("name"),
                        "status": status,
                        "restarts": restarts,
                        "ready": pod.get("ready")
                    })
            
            return problematic
            
        except Exception as e:
            logger.error(f"Error getting problematic pods: {e}")
            return []


# Create singleton instance
healer_agent = HealerAgent()


if __name__ == "__main__":
    # Test the healer agent
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    print("=" * 60)
    print("Testing Healer Agent")
    print("=" * 60)
    
    agent = HealerAgent()
    
    # Check for problematic pods
    print("\nChecking for problematic pods...")
    problematic = agent.get_problematic_pods()
    
    if problematic:
        print(f"Found {len(problematic)} problematic pod(s):")
        for pod in problematic:
            print(f"  - {pod['name']}: {pod['status']} (restarts: {pod['restarts']})")
    else:
        print("✓ No problematic pods found")
    
    print("\n" + "=" * 60)

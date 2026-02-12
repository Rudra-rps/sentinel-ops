"""
Scaler Agent - Handles auto-scaling of deployments
"""
import sys
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from tools.k8s_client import k8s_client
from mcp_server.config import MIN_REPLICAS, MAX_REPLICAS, K8S_NAMESPACE

logger = logging.getLogger(__name__)


class ScalerAgent:
    """
    Automatically scales deployments based on metrics
    """
    
    def __init__(self, namespace: str = K8S_NAMESPACE):
        self.namespace = namespace
        self.min_replicas = MIN_REPLICAS
        self.max_replicas = MAX_REPLICAS
    
    def scale_up(self, deployment: str, delta: int = 2, reason: str = "") -> Dict:
        """
        Scale up a deployment by delta replicas
        """
        try:
            current = k8s_client.get_deployment_replicas(deployment, self.namespace)
            new_count = min(current + delta, self.max_replicas)
            
            if new_count == current:
                logger.info(f"Cannot scale up {deployment}: already at maximum ({self.max_replicas})")
                return {
                    "success": False,
                    "reason": "at_maximum",
                    "current": current,
                    "max": self.max_replicas
                }
            
            success = k8s_client.scale_deployment(deployment, new_count, self.namespace)
            
            if success:
                logger.info(f"Scaled up {deployment}: {current} → {new_count} replicas. Reason: {reason}")
                return {
                    "success": True,
                    "action": "scale_up",
                    "deployment": deployment,
                    "from": current,
                    "to": new_count,
                    "delta": new_count - current,
                    "reason": reason,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"success": False, "reason": "k8s_error"}
                
        except Exception as e:
            logger.error(f"Error scaling up {deployment}: {e}")
            return {"success": False, "reason": str(e)}
    
    def scale_down(self, deployment: str, delta: int = 1, reason: str = "") -> Dict:
        """
        Scale down a deployment by delta replicas
        """
        try:
            current = k8s_client.get_deployment_replicas(deployment, self.namespace)
            new_count = max(current - delta, self.min_replicas)
            
            if new_count == current:
                logger.info(f"Cannot scale down {deployment}: already at minimum ({self.min_replicas})")
                return {
                    "success": False,
                    "reason": "at_minimum",
                    "current": current,
                    "min": self.min_replicas
                }
            
            success = k8s_client.scale_deployment(deployment, new_count, self.namespace)
            
            if success:
                logger.info(f"Scaled down {deployment}: {current} → {new_count} replicas. Reason: {reason}")
                return {
                    "success": True,
                    "action": "scale_down",
                    "deployment": deployment,
                    "from": current,
                    "to": new_count,
                    "delta": current - new_count,
                    "reason": reason,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"success": False, "reason": "k8s_error"}
                
        except Exception as e:
            logger.error(f"Error scaling down {deployment}: {e}")
            return {"success": False, "reason": str(e)}
    
    def scale_to(self, deployment: str, target: int, reason: str = "") -> Dict:
        """
        Scale deployment to exact target replica count
        """
        try:
            current = k8s_client.get_deployment_replicas(deployment, self.namespace)
            target = max(self.min_replicas, min(target, self.max_replicas))
            
            if target == current:
                logger.info(f"{deployment} already at target ({target} replicas)")
                return {
                    "success": False,
                    "reason": "already_at_target",
                    "current": current
                }
            
            success = k8s_client.scale_deployment(deployment, target, self.namespace)
            
            if success:
                action = "scale_up" if target > current else "scale_down"
                logger.info(f"Scaled {deployment}: {current} → {target} replicas. Reason: {reason}")
                return {
                    "success": True,
                    "action": action,
                    "deployment": deployment,
                    "from": current,
                    "to": target,
                    "delta": abs(target - current),
                    "reason": reason,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"success": False, "reason": "k8s_error"}
                
        except Exception as e:
            logger.error(f"Error scaling {deployment} to {target}: {e}")
            return {"success": False, "reason": str(e)}
    
    def get_current_replicas(self, deployment: str) -> int:
        """
        Get current replica count for deployment
        """
        return k8s_client.get_deployment_replicas(deployment, self.namespace)
    
    def can_scale_up(self, deployment: str) -> bool:
        """
        Check if deployment can be scaled up
        """
        current = self.get_current_replicas(deployment)
        return current < self.max_replicas
    
    def can_scale_down(self, deployment: str) -> bool:
        """
        Check if deployment can be scaled down
        """
        current = self.get_current_replicas(deployment)
        return current > self.min_replicas


# Create singleton instance
scaler_agent = ScalerAgent()


if __name__ == "__main__":
    # Test the scaler agent
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    print("=" * 60)
    print("Testing Scaler Agent")
    print("=" * 60)
    
    agent = ScalerAgent()
    deployment = "nginx-demo"
    
    # Get current replicas
    current = agent.get_current_replicas(deployment)
    print(f"\nCurrent replicas for {deployment}: {current}")
    
    # Check scaling possibilities
    print(f"Can scale up: {agent.can_scale_up(deployment)}")
    print(f"Can scale down: {agent.can_scale_down(deployment)}")
    
    print("\n" + "=" * 60)

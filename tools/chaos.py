"""
Chaos Engineering Tools - Simulate failures and load
"""
import sys
import subprocess
import logging
import random
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import time

sys.path.append(str(Path(__file__).parent.parent))

from tools.k8s_client import k8s_client
from mcp_server.config import K8S_NAMESPACE

logger = logging.getLogger(__name__)


class ChaosEngine:
    """
    Simulate various failure scenarios for testing
    """
    
    def __init__(self, namespace: str = K8S_NAMESPACE):
        self.namespace = namespace
        self.active_simulations = []
    
    def simulate_cpu_spike(self, deployment: str = "nginx-demo", duration: int = 300) -> Dict:
        """
        Simulate CPU spike by deploying stress container
        """
        try:
            # Use a unique pod name to avoid forbidden updates to existing pods
            pod_name = f"stress-test-cpu-{int(time.time())}"

            # Use `kubectl run` to create a one-off pod (restart=Never)
            cmd = [
                "kubectl", "-n", self.namespace, "run", pod_name,
                "--image=polinux/stress",
                "--restart=Never",
                "--labels=app=stress-test",
                "--",
                "stress",
                "--cpu",
                "4",
                "--timeout",
                f"{duration}s",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"Started CPU spike simulation for {duration}s (pod: {pod_name})")
                self.active_simulations.append({
                    "type": "cpu_spike",
                    "started": datetime.now().isoformat(),
                    "duration": duration,
                    "pod": pod_name
                })

                return {
                    "success": True,
                    "type": "cpu_spike",
                    "duration": duration,
                    "message": f"CPU stress test started for {duration} seconds (pod: {pod_name})",
                    "pod": pod_name
                }
            else:
                logger.error(f"Failed to start CPU spike: {result.stderr}")
                return {
                    "success": False,
                    "error": result.stderr
                }

        except Exception as e:
            logger.error(f"Error simulating CPU spike: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def simulate_pod_crash(self, deployment: str = "nginx-demo") -> Dict:
        """
        Crash a random pod from deployment
        """
        try:
            pods = k8s_client.get_pods(self.namespace)
            deployment_pods = [p for p in pods if deployment in p["name"]]
            
            if not deployment_pods:
                return {
                    "success": False,
                    "error": f"No pods found for deployment {deployment}"
                }
            
            # Pick random pod
            target_pod = random.choice(deployment_pods)
            pod_name = target_pod["name"]
            
            # Delete the pod
            success = k8s_client.delete_pod(pod_name, self.namespace)
            
            if success:
                logger.info(f"Crashed pod: {pod_name}")
                self.active_simulations.append({
                    "type": "pod_crash",
                    "pod": pod_name,
                    "timestamp": datetime.now().isoformat()
                })
                
                return {
                    "success": True,
                    "type": "pod_crash",
                    "pod": pod_name,
                    "message": f"Pod {pod_name} crashed (deleted)"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to delete pod"
                }
                
        except Exception as e:
            logger.error(f"Error simulating pod crash: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def simulate_cascade_failure(self, deployment: str = "nginx-demo") -> Dict:
        """
        Delete multiple pods at once (cascade failure)
        """
        try:
            pods = k8s_client.get_pods(self.namespace)
            deployment_pods = [p for p in pods if deployment in p["name"]]
            
            if not deployment_pods:
                return {
                    "success": False,
                    "error": f"No pods found for deployment {deployment}"
                }
            
            # Delete half of the pods
            targets_count = max(1, len(deployment_pods) // 2)
            targets = random.sample(deployment_pods, k=targets_count)
            
            deleted = []
            for pod in targets:
                pod_name = pod["name"]
                if k8s_client.delete_pod(pod_name, self.namespace):
                    deleted.append(pod_name)
            
            logger.info(f"Cascade failure: deleted {len(deleted)} pods")
            self.active_simulations.append({
                "type": "cascade_failure",
                "pods_deleted": len(deleted),
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "type": "cascade_failure",
                "pods_deleted": len(deleted),
                "pods": deleted,
                "message": f"Cascade failure: {len(deleted)} pods crashed"
            }
            
        except Exception as e:
            logger.error(f"Error simulating cascade failure: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def cleanup_stress_tests(self) -> Dict:
        """
        Clean up stress test pods
        """
        try:
            cmd = ["kubectl", "delete", "pod", "-n", self.namespace, "-l", "app=stress-test", "--ignore-not-found=true"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            logger.info("Cleaned up stress test pods")
            return {
                "success": True,
                "message": "Stress test pods cleaned up"
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up stress tests: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_active_simulations(self) -> List[Dict]:
        """
        Get list of active simulations
        """
        return self.active_simulations
    
    def get_recent_events(self, count: int = 10) -> List[Dict]:
        """
        Get recent simulation events
        """
        return self.active_simulations[-count:]


# Create singleton instance
chaos_engine = ChaosEngine()


if __name__ == "__main__":
    # Test chaos engine
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    print("=" * 60)
    print("Testing Chaos Engine")
    print("=" * 60)
    
    engine = ChaosEngine()
    
    # Test pod crash
    print("\n1. Simulating pod crash...")
    result = engine.simulate_pod_crash()
    if result["success"]:
        print(f"   ✓ Crashed pod: {result['pod']}")
    else:
        print(f"   ✗ Failed: {result.get('error')}")
    
    print("\n" + "=" * 60)

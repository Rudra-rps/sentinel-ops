"""
Kubernetes client wrapper for managing cluster resources
"""
import subprocess
import json
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class K8sClient:
    def __init__(self, namespace: str = "demo"):
        self.namespace = namespace
    
    def _run_command(self, cmd: List[str]) -> Dict:
        """Execute kubectl command and return output"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout, "error": None}
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(cmd)} - {e.stderr}")
            return {"success": False, "output": None, "error": e.stderr}
    
    def get_pods(self, namespace: Optional[str] = None) -> List[Dict]:
        """Get all pods in namespace"""
        ns = namespace or self.namespace
        cmd = ["kubectl", "get", "pods", "-n", ns, "-o", "json"]
        result = self._run_command(cmd)
        
        if result["success"]:
            data = json.loads(result["output"])
            pods = []
            for item in data.get("items", []):
                pod_info = {
                    "name": item["metadata"]["name"],
                    "status": item["status"]["phase"],
                    "ready": self._get_ready_status(item),
                    "restarts": self._get_restart_count(item),
                    "age": item["metadata"]["creationTimestamp"],
                    "node": item["spec"].get("nodeName", ""),
                }
                pods.append(pod_info)
            return pods
        return []
    
    def _get_ready_status(self, pod: Dict) -> str:
        """Extract ready status from pod"""
        try:
            conditions = pod["status"].get("conditions", [])
            ready_condition = next((c for c in conditions if c["type"] == "Ready"), None)
            if ready_condition:
                return "True" if ready_condition["status"] == "True" else "False"
        except:
            pass
        return "Unknown"
    
    def _get_restart_count(self, pod: Dict) -> int:
        """Get total restart count for pod"""
        try:
            container_statuses = pod["status"].get("containerStatuses", [])
            return sum(cs.get("restartCount", 0) for cs in container_statuses)
        except:
            return 0
    
    def get_deployments(self, namespace: Optional[str] = None) -> List[Dict]:
        """Get all deployments in namespace"""
        ns = namespace or self.namespace
        cmd = ["kubectl", "get", "deployments", "-n", ns, "-o", "json"]
        result = self._run_command(cmd)
        
        if result["success"]:
            data = json.loads(result["output"])
            deployments = []
            for item in data.get("items", []):
                deployment_info = {
                    "name": item["metadata"]["name"],
                    "replicas": item["spec"]["replicas"],
                    "ready_replicas": item["status"].get("readyReplicas", 0),
                    "available_replicas": item["status"].get("availableReplicas", 0),
                }
                deployments.append(deployment_info)
            return deployments
        return []
    
    def scale_deployment(self, deployment: str, replicas: int, namespace: Optional[str] = None) -> bool:
        """Scale deployment to specified number of replicas"""
        ns = namespace or self.namespace
        cmd = ["kubectl", "scale", "deployment", deployment, "-n", ns, "--replicas", str(replicas)]
        result = self._run_command(cmd)
        
        if result["success"]:
            logger.info(f"Scaled {deployment} to {replicas} replicas in {ns}")
            return True
        return False
    
    def delete_pod(self, pod_name: str, namespace: Optional[str] = None) -> bool:
        """Delete a pod"""
        ns = namespace or self.namespace
        cmd = ["kubectl", "delete", "pod", pod_name, "-n", ns]
        result = self._run_command(cmd)
        
        if result["success"]:
            logger.info(f"Deleted pod {pod_name} in {ns}")
            return True
        return False
    
    def restart_deployment(self, deployment: str, namespace: Optional[str] = None) -> bool:
        """Restart deployment by rolling restart"""
        ns = namespace or self.namespace
        cmd = ["kubectl", "rollout", "restart", "deployment", deployment, "-n", ns]
        result = self._run_command(cmd)
        
        if result["success"]:
            logger.info(f"Restarted deployment {deployment} in {ns}")
            return True
        return False
    
    def get_pod_logs(self, pod_name: str, namespace: Optional[str] = None, tail: int = 100) -> str:
        """Get logs from a pod"""
        ns = namespace or self.namespace
        cmd = ["kubectl", "logs", pod_name, "-n", ns, "--tail", str(tail)]
        result = self._run_command(cmd)
        
        if result["success"]:
            return result["output"]
        return ""
    
    def get_nodes(self) -> List[Dict]:
        """Get all nodes in cluster"""
        cmd = ["kubectl", "get", "nodes", "-o", "json"]
        result = self._run_command(cmd)
        
        if result["success"]:
            data = json.loads(result["output"])
            nodes = []
            for item in data.get("items", []):
                node_info = {
                    "name": item["metadata"]["name"],
                    "status": self._get_node_status(item),
                    "roles": self._get_node_roles(item),
                    "version": item["status"]["nodeInfo"]["kubeletVersion"],
                }
                nodes.append(node_info)
            return nodes
        return []
    
    def _get_node_status(self, node: Dict) -> str:
        """Extract node status"""
        try:
            conditions = node["status"].get("conditions", [])
            ready_condition = next((c for c in conditions if c["type"] == "Ready"), None)
            if ready_condition:
                return "Ready" if ready_condition["status"] == "True" else "NotReady"
        except:
            pass
        return "Unknown"
    
    def _get_node_roles(self, node: Dict) -> List[str]:
        """Extract node roles from labels"""
        labels = node["metadata"].get("labels", {})
        roles = []
        for key, value in labels.items():
            if key.startswith("node-role.kubernetes.io/"):
                role = key.split("/")[1]
                if role:
                    roles.append(role)
        return roles if roles else ["<none>"]
    
    def get_deployment_replicas(self, deployment: str, namespace: Optional[str] = None) -> int:
        """Get current replica count for deployment"""
        ns = namespace or self.namespace
        deployments = self.get_deployments(ns)
        
        for dep in deployments:
            if dep["name"] == deployment:
                return dep["replicas"]
        return 0


# Create singleton instance
k8s_client = K8sClient()

"""
Prometheus client wrapper for querying metrics
"""
import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PrometheusClient:
    def __init__(self, base_url: str = "http://localhost:9090"):
        self.base_url = base_url
        self.query_url = f"{base_url}/api/v1/query"
        self.query_range_url = f"{base_url}/api/v1/query_range"
        # Keep API responses responsive even when Prometheus is unavailable.
        self.query_timeout = (0.5, 1.0)  # (connect, read) seconds
        self.health_timeout = (0.5, 1.0)
    
    def _query(self, query: str) -> Optional[Dict]:
        """Execute Prometheus query"""
        try:
            response = requests.get(
                self.query_url,
                params={"query": query},
                timeout=self.query_timeout
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                return data.get("data", {})
            else:
                logger.error(f"Query failed: {data}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Prometheus query error: {e}")
            return None
    
    def _extract_value(self, result: Optional[Dict]) -> float:
        """Extract numeric value from query result"""
        if not result:
            return 0.0
        
        results = result.get("result", [])
        if not results:
            return 0.0
        
        # Get the first result's value
        value = results[0].get("value", [None, "0"])
        try:
            return float(value[1])
        except (ValueError, IndexError, TypeError):
            return 0.0
    
    def get_cpu_usage(self, namespace: str = "demo", deployment: str = None) -> float:
        """Get CPU usage percentage for namespace or deployment"""
        if deployment:
            query = f'sum(rate(container_cpu_usage_seconds_total{{namespace="{namespace}", pod=~"{deployment}.*"}}[5m])) * 100'
        else:
            query = f'sum(rate(container_cpu_usage_seconds_total{{namespace="{namespace}"}}[5m])) * 100'
        
        result = self._query(query)
        return self._extract_value(result)
    
    def get_memory_usage(self, namespace: str = "demo", deployment: str = None) -> float:
        """Get memory usage percentage for namespace or deployment"""
        if deployment:
            query = f'sum(container_memory_usage_bytes{{namespace="{namespace}", pod=~"{deployment}.*"}}) / sum(container_spec_memory_limit_bytes{{namespace="{namespace}", pod=~"{deployment}.*"}}) * 100'
        else:
            query = f'sum(container_memory_usage_bytes{{namespace="{namespace}"}}) / sum(container_spec_memory_limit_bytes{{namespace="{namespace}"}}) * 100'
        
        result = self._query(query)
        return self._extract_value(result)
    
    def get_pod_count(self, namespace: str = "demo") -> int:
        """Get number of running pods in namespace"""
        query = f'count(kube_pod_info{{namespace="{namespace}"}})'
        result = self._query(query)
        return int(self._extract_value(result))
    
    def get_pod_status(self, namespace: str = "demo") -> Dict[str, int]:
        """Get pod status counts"""
        query = f'sum by (phase) (kube_pod_status_phase{{namespace="{namespace}"}})'
        result = self._query(query)
        
        if not result:
            return {"running": 0, "pending": 0, "failed": 0, "succeeded": 0}
        
        status_counts = {}
        for item in result.get("result", []):
            phase = item.get("metric", {}).get("phase", "unknown").lower()
            value = float(item.get("value", [None, "0"])[1])
            status_counts[phase] = int(value)
        
        return status_counts
    
    def get_container_restarts(self, namespace: str = "demo") -> int:
        """Get total container restart count"""
        query = f'sum(kube_pod_container_status_restarts_total{{namespace="{namespace}"}})'
        result = self._query(query)
        return int(self._extract_value(result))
    
    def get_node_cpu_usage(self) -> float:
        """Get overall node CPU usage"""
        query = 'sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) / sum(rate(node_cpu_seconds_total[5m])) * 100'
        result = self._query(query)
        return self._extract_value(result)
    
    def get_node_memory_usage(self) -> float:
        """Get overall node memory usage"""
        query = '(1 - sum(node_memory_MemAvailable_bytes) / sum(node_memory_MemTotal_bytes)) * 100'
        result = self._query(query)
        return self._extract_value(result)
    
    def get_all_metrics(self, namespace: str = "demo") -> Dict:
        """Get all key metrics at once"""
        if not self.is_healthy():
            return {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "pod_count": 0,
                "pod_status": {"running": 0, "pending": 0, "failed": 0, "succeeded": 0},
                "container_restarts": 0,
                "node_cpu": 0.0,
                "node_memory": 0.0,
                "timestamp": datetime.now().isoformat()
            }

        return {
            "cpu_usage": self.get_cpu_usage(namespace),
            "memory_usage": self.get_memory_usage(namespace),
            "pod_count": self.get_pod_count(namespace),
            "pod_status": self.get_pod_status(namespace),
            "container_restarts": self.get_container_restarts(namespace),
            "node_cpu": self.get_node_cpu_usage(),
            "node_memory": self.get_node_memory_usage(),
            "timestamp": datetime.now().isoformat()
        }
    
    def is_healthy(self) -> bool:
        """Check if Prometheus is accessible"""
        try:
            response = requests.get(f"{self.base_url}/-/healthy", timeout=self.health_timeout)
            return response.status_code == 200
        except:
            return False


# Create singleton instance
prometheus_client = PrometheusClient()

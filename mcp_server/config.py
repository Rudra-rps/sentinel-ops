"""
Configuration settings for SentinelOps MCP Server
"""
import os

# Kubernetes Configuration
K8S_NAMESPACE = os.getenv("K8S_NAMESPACE", "demo")
KUBECONFIG_PATH = os.getenv("KUBECONFIG", "~/.kube/config")

# Prometheus Configuration
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9090"))

# MCP Server Configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "logs")
ACTIONS_LOG = f"{LOG_DIR}/actions.log"
INCIDENTS_LOG = f"{LOG_DIR}/incidents.log"

# Thresholds for Auto-Scaling
CPU_HIGH_THRESHOLD = float(os.getenv("CPU_HIGH_THRESHOLD", "80.0"))
CPU_LOW_THRESHOLD = float(os.getenv("CPU_LOW_THRESHOLD", "30.0"))
MEMORY_HIGH_THRESHOLD = float(os.getenv("MEMORY_HIGH_THRESHOLD", "85.0"))

# Scaling Limits
MIN_REPLICAS = int(os.getenv("MIN_REPLICAS", "2"))
MAX_REPLICAS = int(os.getenv("MAX_REPLICAS", "10"))

# Decision Engine
DECISION_LOOP_INTERVAL = int(os.getenv("DECISION_LOOP_INTERVAL", "60"))  # seconds

# Cost Configuration (example rates in $/hour)
COST_PER_CPU_HOUR = float(os.getenv("COST_PER_CPU_HOUR", "0.0416"))
COST_PER_GB_HOUR = float(os.getenv("COST_PER_GB_HOUR", "0.0052"))

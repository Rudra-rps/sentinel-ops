"""
Decision Engine - The brain of SentinelOps
Monitors, analyzes, decides, and acts autonomously
"""
import sys
import time
import signal
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from agents.monitor_agent import monitor_agent
from agents.scaler_agent import scaler_agent
from agents.healer_agent import healer_agent
from agents.incident_tracker import incident_tracker
from mcp_server.config import DECISION_LOOP_INTERVAL, K8S_NAMESPACE

logger = logging.getLogger(__name__)


class DecisionEngine:
    """
    Autonomous decision engine that:
    1. Monitors cluster metrics
    2. Analyzes for issues
    3. Decides on actions
    4. Executes remediation
    5. Tracks outcomes
    """
    
    def __init__(self, namespace: str = K8S_NAMESPACE, interval: int = DECISION_LOOP_INTERVAL):
        self.namespace = namespace
        self.interval = interval
        self.running = False
        self.cycle_count = 0
        
        # Agents
        self.monitor = monitor_agent
        self.scaler = scaler_agent
        self.healer = healer_agent
        self.tracker = incident_tracker
        
        logger.info(f"Decision Engine initialized (interval: {interval}s, namespace: {namespace})")
    
    def start(self):
        """
        Start the decision loop
        """
        self.running = True
        logger.info("=" * 70)
        logger.info("SENTINELOPS DECISION ENGINE STARTED")
        logger.info("=" * 70)
        logger.info(f"Monitoring namespace: {self.namespace}")
        logger.info(f"Decision interval: {self.interval} seconds")
        logger.info(f"Press Ctrl+C to stop")
        logger.info("=" * 70)
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            while self.running:
                self.cycle_count += 1
                logger.info(f"\n{'='*70}")
                logger.info(f"CYCLE #{self.cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'='*70}")
                
                self.run_cycle()
                
                if self.running:
                    logger.info(f"\n[SLEEP] Sleeping for {self.interval} seconds...")
                    time.sleep(self.interval)
                    
        except Exception as e:
            logger.error(f"Fatal error in decision loop: {e}", exc_info=True)
        finally:
            logger.info("\n" + "=" * 70)
            logger.info("SENTINELOPS DECISION ENGINE STOPPED")
            logger.info("=" * 70)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info("\n\nShutdown signal received...")
        self.running = False
    
    def run_cycle(self):
        """
        Execute one complete decision cycle
        """
        start_time = time.time()
        
        try:
            # STEP 1: Monitor
            logger.info("\n[STEP 1] Collecting metrics...")
            metrics = self.monitor.collect_metrics()
            logger.info(f"   CPU: {metrics.get('cpu_usage', 0):.1f}% | "
                       f"Memory: {metrics.get('memory_usage', 0):.1f}% | "
                       f"Pods: {metrics.get('pod_count', 0)}")
            
            # STEP 2: Analyze
            logger.info("\n[STEP 2] Analyzing for issues...")
            issues = self.monitor.analyze_metrics(metrics)
            
            if not issues:
                logger.info("   [OK] No issues detected - system healthy")
                return
            
            logger.info(f"   [WARN] Found {len(issues)} issue(s):")
            for issue in issues:
                logger.info(f"      - [{issue['severity'].upper()}] {issue['type']}: {issue['message']}")
            
            # STEP 3: Decide
            logger.info("\n[STEP 3] Deciding on actions...")
            actions = self.decide_actions(issues, metrics)
            
            if not actions:
                logger.info("   [INFO] No actions needed")
                # Still log incidents even if no action taken
                for issue in issues:
                    self.tracker.log_incident(issue)
                return
            
            logger.info(f"   [PLAN] Planned {len(actions)} action(s):")
            for action in actions:
                logger.info(f"      - {action['type']}: {action.get('description', '')}")
            
            # STEP 4: Act
            logger.info("\n[STEP 4] Executing actions...")
            results = self.execute_actions(actions, issues)
            
            # STEP 5: Log
            logger.info("\n[STEP 5] Logging incidents...")
            for i, issue in enumerate(issues):
                if i < len(results):
                    action = actions[i]
                    result = results[i]
                    self.tracker.log_incident(issue, action, result)
                    
                    status = "[SUCCESS]" if result.get("success") else "[FAILED]"
                    logger.info(f"   {status}: {action['type']} for {issue['type']}")
            
            # STEP 6: Summary
            duration_ms = (time.time() - start_time) * 1000
            logger.info(f"\n[TIMING] Cycle completed in {duration_ms:.0f}ms")
            
        except Exception as e:
            logger.error(f"Error in decision cycle: {e}", exc_info=True)
    
    def decide_actions(self, issues: List[Dict], metrics: Dict) -> List[Dict]:
        """
        Decide what actions to take based on issues
        """
        actions = []
        deployments = metrics.get("deployments", [])
        
        for issue in issues:
            issue_type = issue["type"]
            resource = issue.get("resource", "")
            
            # CPU Overload → Scale Up
            if issue_type == "cpu_overload":
                # Find the deployment to scale
                deployment = deployments[0]["name"] if deployments else "nginx-demo"
                
                if self.scaler.can_scale_up(deployment):
                    actions.append({
                        "type": "scale_up",
                        "deployment": deployment,
                        "delta": 2,
                        "reason": issue["message"],
                        "description": f"Scale up {deployment} by 2 replicas"
                    })
            
            # CPU Underutilized → Scale Down
            elif issue_type == "cpu_underutilized":
                deployment = resource
                
                if self.scaler.can_scale_down(deployment):
                    actions.append({
                        "type": "scale_down",
                        "deployment": deployment,
                        "delta": 1,
                        "reason": issue["message"],
                        "description": f"Scale down {deployment} by 1 replica"
                    })
            
            # Memory Pressure → Scale Up
            elif issue_type == "memory_pressure":
                deployment = deployments[0]["name"] if deployments else "nginx-demo"
                
                if self.scaler.can_scale_up(deployment):
                    actions.append({
                        "type": "scale_up",
                        "deployment": deployment,
                        "delta": 1,
                        "reason": issue["message"],
                        "description": f"Scale up {deployment} due to memory pressure"
                    })
            
            # Pod CrashLoop → Heal
            elif issue_type == "pod_crashloop":
                pod_name = resource
                actions.append({
                    "type": "heal_crashloop",
                    "pod": pod_name,
                    "restarts": issue.get("value", 0),
                    "reason": issue["message"],
                    "description": f"Heal pod {pod_name} in CrashLoopBackOff"
                })
            
            # Pod Pending → Heal
            elif issue_type == "pod_pending":
                pod_name = resource
                actions.append({
                    "type": "heal_pending",
                    "pod": pod_name,
                    "reason": issue["message"],
                    "description": f"Restart pending pod {pod_name}"
                })
            
            # Pod Failed → Heal
            elif issue_type == "pod_failed":
                pod_name = resource
                actions.append({
                    "type": "heal_failed",
                    "pod": pod_name,
                    "reason": issue["message"],
                    "description": f"Restart failed pod {pod_name}"
                })
        
        return actions
    
    def execute_actions(self, actions: List[Dict], issues: List[Dict]) -> List[Dict]:
        """
        Execute all planned actions
        """
        results = []
        
        for action in actions:
            action_type = action["type"]
            start_time = time.time()
            
            try:
                # Scaling actions
                if action_type == "scale_up":
                    result = self.scaler.scale_up(
                        action["deployment"],
                        action.get("delta", 2),
                        action.get("reason", "")
                    )
                
                elif action_type == "scale_down":
                    result = self.scaler.scale_down(
                        action["deployment"],
                        action.get("delta", 1),
                        action.get("reason", "")
                    )
                
                # Healing actions
                elif action_type == "heal_crashloop":
                    pod_info = {
                        "name": action["pod"],
                        "restarts": action.get("restarts", 0)
                    }
                    result = self.healer.heal_crashloop(pod_info)
                
                elif action_type == "heal_pending":
                    pod_info = {"name": action["pod"]}
                    result = self.healer.heal_pending(pod_info)
                
                elif action_type == "heal_failed":
                    pod_info = {"name": action["pod"]}
                    result = self.healer.heal_failed(pod_info)
                
                else:
                    result = {
                        "success": False,
                        "reason": f"Unknown action type: {action_type}"
                    }
                
                # Add timing information
                duration_ms = (time.time() - start_time) * 1000
                result["duration_ms"] = duration_ms
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error executing action {action_type}: {e}")
                results.append({
                    "success": False,
                    "reason": str(e),
                    "duration_ms": (time.time() - start_time) * 1000
                })
        
        return results
    
    def get_status(self) -> Dict:
        """
        Get current status of the decision engine
        """
        return {
            "running": self.running,
            "cycle_count": self.cycle_count,
            "interval": self.interval,
            "namespace": self.namespace,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """
    Main entry point for running the decision engine
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/decision_engine.log"),
            logging.StreamHandler()
        ]
    )
    
    # Create and start engine
    engine = DecisionEngine()
    engine.start()


if __name__ == "__main__":
    main()

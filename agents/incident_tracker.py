"""
Incident Tracker - Logs and tracks all incidents and remediation actions
"""
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid

sys.path.append(str(Path(__file__).parent.parent))

from mcp_server.config import INCIDENTS_LOG

logger = logging.getLogger(__name__)


class IncidentTracker:
    """
    Tracks incidents, actions taken, and results
    """
    
    def __init__(self, log_file: str = INCIDENTS_LOG):
        self.log_file = Path(log_file)
        self.incidents = []
        self._ensure_log_file()
        self._load_recent_incidents()
    
    def _ensure_log_file(self):
        """Ensure log file and directory exist"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.touch()
    
    def _load_recent_incidents(self, hours: int = 24):
        """Load recent incidents from file"""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()
                    cutoff = datetime.now() - timedelta(hours=hours)
                    
                    for line in lines:
                        try:
                            incident = json.loads(line.strip())
                            incident_time = datetime.fromisoformat(incident.get("timestamp", ""))
                            if incident_time > cutoff:
                                self.incidents.append(incident)
                        except (json.JSONDecodeError, ValueError):
                            continue
        except Exception as e:
            logger.error(f"Error loading incidents: {e}")
    
    def log_incident(
        self,
        issue: Dict,
        action: Optional[Dict] = None,
        result: Optional[Dict] = None
    ) -> Dict:
        """
        Log a new incident with optional action and result
        """
        incident_id = str(uuid.uuid4())[:8]
        
        incident = {
            "id": incident_id,
            "timestamp": datetime.now().isoformat(),
            "issue": {
                "type": issue.get("type", "unknown"),
                "severity": issue.get("severity", "medium"),
                "message": issue.get("message", ""),
                "resource": issue.get("resource", ""),
                "value": issue.get("value"),
                "threshold": issue.get("threshold")
            }
        }
        
        if action:
            incident["action"] = {
                "type": action.get("action", "none"),
                "target": action.get("deployment") or action.get("pod") or action.get("resource", ""),
                "details": {
                    k: v for k, v in action.items() 
                    if k not in ["action", "deployment", "pod", "resource", "success", "timestamp"]
                }
            }
        
        if result:
            incident["result"] = {
                "success": result.get("success", False),
                "message": result.get("message", ""),
                "duration_ms": result.get("duration_ms"),
                "new_state": result.get("new_state")
            }
        else:
            # If no result provided but action exists, mark as pending
            if action:
                incident["result"] = {
                    "success": None,
                    "message": "pending",
                    "duration_ms": None
                }
        
        # Save to file
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(incident) + '\n')
            
            self.incidents.append(incident)
            logger.info(f"Logged incident {incident_id}: {issue.get('type')}")
            
        except Exception as e:
            logger.error(f"Error writing incident to file: {e}")
        
        return incident
    
    def update_incident(self, incident_id: str, result: Dict) -> bool:
        """
        Update an existing incident with results
        """
        try:
            # Find incident in memory
            for incident in self.incidents:
                if incident.get("id") == incident_id:
                    incident["result"] = {
                        "success": result.get("success", False),
                        "message": result.get("message", ""),
                        "duration_ms": result.get("duration_ms"),
                        "new_state": result.get("new_state")
                    }
                    incident["updated_at"] = datetime.now().isoformat()
                    
                    # Re-write the log file with updated incident
                    self._rewrite_log_file()
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating incident {incident_id}: {e}")
            return False
    
    def _rewrite_log_file(self):
        """Rewrite entire log file with current incidents"""
        try:
            with open(self.log_file, 'w') as f:
                for incident in self.incidents:
                    f.write(json.dumps(incident) + '\n')
        except Exception as e:
            logger.error(f"Error rewriting log file: {e}")
    
    def get_incidents(
        self,
        hours: Optional[int] = None,
        severity: Optional[str] = None,
        issue_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get incidents with optional filters
        """
        filtered = self.incidents.copy()
        
        # Filter by time
        if hours:
            cutoff = datetime.now() - timedelta(hours=hours)
            filtered = [
                i for i in filtered
                if datetime.fromisoformat(i["timestamp"]) > cutoff
            ]
        
        # Filter by severity
        if severity:
            filtered = [
                i for i in filtered
                if i.get("issue", {}).get("severity") == severity
            ]
        
        # Filter by type
        if issue_type:
            filtered = [
                i for i in filtered
                if i.get("issue", {}).get("type") == issue_type
            ]
        
        # Sort by timestamp (newest first)
        filtered.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Limit results
        if limit:
            filtered = filtered[:limit]
        
        return filtered
    
    def get_stats(self, hours: int = 24) -> Dict:
        """
        Get incident statistics
        """
        incidents = self.get_incidents(hours=hours)
        
        if not incidents:
            return {
                "total_incidents": 0,
                "by_severity": {},
                "by_type": {},
                "success_rate": 0.0,
                "avg_resolution_time_ms": 0.0
            }
        
        # Count by severity
        by_severity = {}
        for incident in incidents:
            severity = incident.get("issue", {}).get("severity", "unknown")
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        # Count by type
        by_type = {}
        for incident in incidents:
            issue_type = incident.get("issue", {}).get("type", "unknown")
            by_type[issue_type] = by_type.get(issue_type, 0) + 1
        
        # Calculate success rate
        resolved = [i for i in incidents if i.get("result", {}).get("success") is not None]
        successful = [i for i in resolved if i.get("result", {}).get("success") is True]
        success_rate = (len(successful) / len(resolved) * 100) if resolved else 0.0
        
        # Calculate average resolution time
        durations = [
            i.get("result", {}).get("duration_ms", 0)
            for i in incidents
            if i.get("result", {}).get("duration_ms") is not None
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0.0
        
        return {
            "total_incidents": len(incidents),
            "by_severity": by_severity,
            "by_type": by_type,
            "success_rate": round(success_rate, 2),
            "avg_resolution_time_ms": round(avg_duration, 2),
            "period_hours": hours
        }
    
    def get_recent_timeline(self, count: int = 10) -> List[Dict]:
        """
        Get recent incident timeline
        """
        return self.get_incidents(limit=count)


# Create singleton instance
incident_tracker = IncidentTracker()


if __name__ == "__main__":
    # Test the incident tracker
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    print("=" * 60)
    print("Testing Incident Tracker")
    print("=" * 60)
    
    tracker = IncidentTracker()
    
    # Log a test incident
    print("\n1. Logging test incident...")
    issue = {
        "type": "cpu_overload",
        "severity": "high",
        "message": "CPU usage exceeds threshold",
        "resource": "nginx-demo",
        "value": 85.5,
        "threshold": 80.0
    }
    
    action = {
        "action": "scale_up",
        "deployment": "nginx-demo",
        "from": 3,
        "to": 5
    }
    
    result = {
        "success": True,
        "message": "Scaled successfully",
        "duration_ms": 2500
    }
    
    incident = tracker.log_incident(issue, action, result)
    print(f"   Logged incident: {incident['id']}")
    
    # Get statistics
    print("\n2. Getting statistics...")
    stats = tracker.get_stats()
    print(f"   Total incidents (24h): {stats['total_incidents']}")
    print(f"   Success rate: {stats['success_rate']}%")
    
    # Get recent timeline
    print("\n3. Recent timeline...")
    timeline = tracker.get_recent_timeline(count=5)
    print(f"   Got {len(timeline)} recent incident(s)")
    
    print("\n" + "=" * 60)

"""
Cost Analyzer - Calculate infrastructure costs and savings from auto-scaling
"""
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

sys.path.append(str(Path(__file__).parent.parent))

from tools.k8s_client import k8s_client
from agents.incident_tracker import incident_tracker
from mcp_server.config import K8S_NAMESPACE

logger = logging.getLogger(__name__)


class CostAnalyzer:
    """
    Analyzes infrastructure costs and calculates savings from autonomous operations
    """
    
    # AWS-like pricing (simplified, can be customized per cloud provider)
    COST_PER_CPU_HOUR = 0.0416  # ~$30/month per vCPU
    COST_PER_GB_HOUR = 0.0052   # ~$4/month per GB RAM
    
    def __init__(self, namespace: str = K8S_NAMESPACE):
        self.namespace = namespace
        self.baseline_cost = None
    
    def calculate_current_cost(self) -> Dict:
        """
        Calculate current infrastructure cost based on running pods
        """
        try:
            pods = k8s_client.get_pods(self.namespace)
            
            total_cpu = 0.0
            total_memory_gb = 0.0
            pod_details = []
            
            for pod in pods:
                # Extract resource requests (fallback to limits or defaults)
                cpu_cores = self._parse_cpu(pod.get('resources', {}).get('requests', {}).get('cpu', '100m'))
                memory_gb = self._parse_memory(pod.get('resources', {}).get('requests', {}).get('memory', '128Mi'))
                
                total_cpu += cpu_cores
                total_memory_gb += memory_gb
                
                pod_details.append({
                    'name': pod['name'],
                    'cpu_cores': cpu_cores,
                    'memory_gb': memory_gb,
                    'hourly_cost': (cpu_cores * self.COST_PER_CPU_HOUR) + (memory_gb * self.COST_PER_GB_HOUR)
                })
            
            hourly_cost = (total_cpu * self.COST_PER_CPU_HOUR) + (total_memory_gb * self.COST_PER_GB_HOUR)
            
            return {
                'total_pods': len(pods),
                'total_cpu_cores': round(total_cpu, 2),
                'total_memory_gb': round(total_memory_gb, 2),
                'hourly_cost': round(hourly_cost, 2),
                'daily_cost': round(hourly_cost * 24, 2),
                'weekly_cost': round(hourly_cost * 24 * 7, 2),
                'monthly_cost': round(hourly_cost * 24 * 30, 2),
                'yearly_cost': round(hourly_cost * 24 * 365, 2),
                'pod_breakdown': pod_details
            }
        except Exception as e:
            logger.error(f"Error calculating current cost: {e}")
            return {
                'error': str(e),
                'hourly_cost': 0,
                'daily_cost': 0,
                'monthly_cost': 0
            }
    
    def calculate_savings(self, hours: int = 24) -> Dict:
        """
        Calculate savings from auto-scaling actions over specified time period
        """
        try:
            incidents = incident_tracker.get_timeline(hours=hours)
            
            total_saved = 0.0
            scale_downs = []
            scale_ups = []
            
            for incident in incidents:
                action_type = incident.get('action', {}).get('type', '')
                
                if action_type == 'scale_down':
                    # Calculate savings from scaling down
                    params = incident.get('action', {}).get('parameters', {})
                    pods_removed = abs(params.get('delta', 0))
                    
                    # Estimate duration until next scaling action
                    duration_hours = self._estimate_duration(incident, incidents)
                    
                    # Assume average pod cost (0.5 CPU, 0.25 GB RAM)
                    pod_cost_per_hour = (0.5 * self.COST_PER_CPU_HOUR) + (0.25 * self.COST_PER_GB_HOUR)
                    saved = pods_removed * pod_cost_per_hour * duration_hours
                    
                    total_saved += saved
                    scale_downs.append({
                        'timestamp': incident.get('timestamp'),
                        'pods_removed': pods_removed,
                        'duration_hours': duration_hours,
                        'saved': round(saved, 2)
                    })
                
                elif action_type == 'scale_up':
                    params = incident.get('action', {}).get('parameters', {})
                    scale_ups.append({
                        'timestamp': incident.get('timestamp'),
                        'pods_added': params.get('delta', 0)
                    })
            
            # Calculate average utilization efficiency
            efficiency_score = self._calculate_efficiency_score(hours)
            
            # Project savings
            hours_in_month = 24 * 30
            monthly_projection = (total_saved / hours) * hours_in_month if hours > 0 else 0
            
            return {
                'time_period_hours': hours,
                'total_saved': round(total_saved, 2),
                'scale_down_count': len(scale_downs),
                'scale_up_count': len(scale_ups),
                'projected_monthly_savings': round(monthly_projection, 2),
                'projected_yearly_savings': round(monthly_projection * 12, 2),
                'efficiency_score': efficiency_score,
                'scale_down_details': scale_downs,
                'recommendation': self._get_savings_recommendation(total_saved, hours)
            }
        except Exception as e:
            logger.error(f"Error calculating savings: {e}")
            return {
                'error': str(e),
                'total_saved': 0,
                'projected_monthly_savings': 0
            }
    
    def get_optimization_recommendations(self) -> List[Dict]:
        """
        Provide cost optimization recommendations based on current usage
        """
        recommendations = []
        
        try:
            # Get current metrics
            pods = k8s_client.get_pods(self.namespace)
            deployments = k8s_client.get_deployments(self.namespace)
            
            # Get recent incidents to understand patterns
            incidents = incident_tracker.get_timeline(hours=24)
            
            # Check for over-provisioning
            scale_down_frequency = len([i for i in incidents if i.get('action', {}).get('type') == 'scale_down'])
            scale_up_frequency = len([i for i in incidents if i.get('action', {}).get('type') == 'scale_up'])
            
            if scale_down_frequency > scale_up_frequency * 2:
                recommendations.append({
                    'type': 'reduce_baseline',
                    'severity': 'medium',
                    'title': 'Reduce baseline replica count',
                    'description': 'System frequently scales down but rarely scales up',
                    'action': 'Consider reducing minimum replicas from current baseline',
                    'potential_savings': '$15-30/month',
                    'confidence': 'high'
                })
            
            # Check for resource over-allocation
            for deployment in deployments:
                if deployment.get('replicas', 0) > 5:
                    recommendations.append({
                        'type': 'review_scaling',
                        'severity': 'low',
                        'title': f'Review {deployment["name"]} scaling',
                        'description': f'Deployment has {deployment["replicas"]} replicas running',
                        'action': 'Verify this scaling level is necessary during normal operations',
                        'potential_savings': '$20-50/month',
                        'confidence': 'medium'
                    })
            
            # Check incident patterns for optimization
            if len(incidents) == 0:
                recommendations.append({
                    'type': 'no_activity',
                    'severity': 'info',
                    'title': 'Low activity detected',
                    'description': 'No auto-scaling events in the last 24 hours',
                    'action': 'System is stable; consider lowering thresholds for more aggressive savings',
                    'potential_savings': '$10-20/month',
                    'confidence': 'low'
                })
            
            # Add general recommendations
            if len(recommendations) == 0:
                recommendations.append({
                    'type': 'optimized',
                    'severity': 'success',
                    'title': 'System is well-optimized',
                    'description': 'SentinelOps is actively managing resources efficiently',
                    'action': 'Continue monitoring; no immediate actions needed',
                    'potential_savings': 'N/A',
                    'confidence': 'high'
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return [{
                'type': 'error',
                'severity': 'error',
                'title': 'Unable to generate recommendations',
                'description': str(e),
                'action': 'Check logs for details',
                'potential_savings': 'Unknown',
                'confidence': 'low'
            }]
    
    def get_cost_breakdown(self, hours: int = 24) -> Dict:
        """
        Get detailed cost breakdown over time period
        """
        try:
            current = self.calculate_current_cost()
            savings = self.calculate_savings(hours)
            recommendations = self.get_optimization_recommendations()
            
            # Calculate baseline (what it would cost without auto-scaling)
            incidents = incident_tracker.get_timeline(hours=hours)
            avg_pods = self._calculate_average_pods(incidents, hours)
            
            baseline_hourly = avg_pods * 0.5 * self.COST_PER_CPU_HOUR
            baseline_cost = baseline_hourly * hours
            
            actual_cost = current['hourly_cost'] * hours
            
            return {
                'current_state': current,
                'time_period': f'{hours} hours',
                'baseline_cost': round(baseline_cost, 2),
                'actual_cost': round(actual_cost, 2),
                'total_saved': savings['total_saved'],
                'savings_percentage': round((savings['total_saved'] / baseline_cost * 100), 1) if baseline_cost > 0 else 0,
                'optimization_score': savings['efficiency_score'],
                'recommendations': recommendations,
                'summary': {
                    'status': 'optimized' if savings['total_saved'] > 0 else 'stable',
                    'message': f"Saved ${savings['total_saved']} in the last {hours} hours through autonomous scaling"
                }
            }
        except Exception as e:
            logger.error(f"Error generating cost breakdown: {e}")
            return {'error': str(e)}
    
    # Helper methods
    
    def _parse_cpu(self, cpu_str: str) -> float:
        """Parse Kubernetes CPU format (e.g., '100m', '0.5', '1')"""
        if not cpu_str:
            return 0.1  # Default 100m
        
        cpu_str = str(cpu_str).lower()
        if 'm' in cpu_str:
            return float(cpu_str.replace('m', '')) / 1000
        return float(cpu_str)
    
    def _parse_memory(self, mem_str: str) -> float:
        """Parse Kubernetes memory format (e.g., '128Mi', '1Gi', '256M')"""
        if not mem_str:
            return 0.128  # Default 128Mi
        
        mem_str = str(mem_str).upper()
        
        if 'GI' in mem_str:
            return float(mem_str.replace('GI', '').replace('G', ''))
        elif 'MI' in mem_str:
            return float(mem_str.replace('MI', '').replace('M', '')) / 1024
        elif 'KI' in mem_str:
            return float(mem_str.replace('KI', '').replace('K', '')) / (1024 * 1024)
        elif 'G' in mem_str:
            return float(mem_str.replace('G', ''))
        elif 'M' in mem_str:
            return float(mem_str.replace('M', '')) / 1024
        
        # Assume bytes
        return float(mem_str) / (1024 ** 3)
    
    def _estimate_duration(self, incident: Dict, all_incidents: List[Dict]) -> float:
        """Estimate how long a scaling action's effect lasted"""
        try:
            incident_time = datetime.fromisoformat(incident['timestamp'])
            
            # Find next incident after this one
            future_incidents = [
                i for i in all_incidents 
                if datetime.fromisoformat(i['timestamp']) > incident_time
            ]
            
            if future_incidents:
                next_incident = min(future_incidents, key=lambda x: x['timestamp'])
                next_time = datetime.fromisoformat(next_incident['timestamp'])
                duration = (next_time - incident_time).total_seconds() / 3600
                return min(duration, 24)  # Cap at 24 hours
            else:
                # Assume effect lasted until now
                duration = (datetime.now() - incident_time).total_seconds() / 3600
                return min(duration, 24)
        except Exception:
            return 1.0  # Default 1 hour
    
    def _calculate_efficiency_score(self, hours: int) -> float:
        """Calculate overall efficiency score (0-100)"""
        try:
            incidents = incident_tracker.get_timeline(hours=hours)
            
            if not incidents:
                return 75.0  # Neutral score if no activity
            
            successful = len([i for i in incidents if i.get('result', {}).get('success', False)])
            total = len(incidents)
            
            success_rate = (successful / total * 100) if total > 0 else 0
            
            # Factor in activity level (more activity = more optimization)
            activity_bonus = min(len(incidents) * 2, 15)
            
            score = min(success_rate + activity_bonus, 100)
            return round(score, 1)
        except Exception:
            return 75.0
    
    def _calculate_average_pods(self, incidents: List[Dict], hours: int) -> float:
        """Calculate average pod count over time period"""
        try:
            current_pods = len(k8s_client.get_pods(self.namespace))
            
            if not incidents:
                return float(current_pods)
            
            # Simple average based on scaling events
            total_pod_hours = current_pods * hours
            
            for incident in incidents:
                if incident.get('action', {}).get('type') in ['scale_up', 'scale_down']:
                    delta = incident.get('action', {}).get('parameters', {}).get('delta', 0)
                    duration = self._estimate_duration(incident, incidents)
                    total_pod_hours += delta * duration
            
            return max(total_pod_hours / hours, 1.0)
        except Exception:
            return 3.0  # Default average
    
    def _get_savings_recommendation(self, saved: float, hours: int) -> str:
        """Generate recommendation message based on savings"""
        if saved == 0:
            return "No scaling events yet. System is monitoring for optimization opportunities."
        elif saved < 0.10:
            return "Minimal savings so far. Continue monitoring for more data."
        elif saved < 1.0:
            return "Good start! Auto-scaling is actively optimizing costs."
        else:
            monthly = (saved / hours) * 24 * 30
            return f"Excellent! On track to save ~${monthly:.2f}/month through autonomous operations."


# Singleton instance
cost_analyzer = CostAnalyzer()

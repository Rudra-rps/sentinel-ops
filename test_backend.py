"""
Backend Test Script - Verify all SentinelOps endpoints are working
"""
import requests
import time
import json
from typing import Dict, List

BASE_URL = "http://localhost:8000"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def test_endpoint(method: str, endpoint: str, description: str, **kwargs) -> bool:
    """Test a single endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, **kwargs)
        elif method == "POST":
            response = requests.post(url, **kwargs)
        else:
            print(f"{RED}✗{RESET} {description} - Invalid method")
            return False
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success', True):  # Some endpoints don't have 'success' field
                print(f"{GREEN}✓{RESET} {description}")
                return True
            else:
                print(f"{RED}✗{RESET} {description} - Success=false")
                return False
        else:
            print(f"{RED}✗{RESET} {description} - Status {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗{RESET} {description} - Connection failed (Is server running?)")
        return False
    except Exception as e:
        print(f"{RED}✗{RESET} {description} - Error: {str(e)}")
        return False


def test_all_endpoints():
    """Test all backend endpoints"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}SentinelOps Backend Test Suite{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    results = []
    
    # Health & Core Endpoints
    print(f"{YELLOW}Testing Health & Core Endpoints...{RESET}")
    results.append(test_endpoint("GET", "/", "Root endpoint"))
    results.append(test_endpoint("GET", "/health", "Health check"))
    print()
    
    # Metrics Endpoints
    print(f"{YELLOW}Testing Metrics Endpoints...{RESET}")
    results.append(test_endpoint("GET", "/metrics", "Get all metrics"))
    results.append(test_endpoint("GET", "/metrics/cpu", "Get CPU metrics"))
    results.append(test_endpoint("GET", "/metrics/memory", "Get memory metrics"))
    print()
    
    # Kubernetes Resources
    print(f"{YELLOW}Testing Kubernetes Resources...{RESET}")
    results.append(test_endpoint("GET", "/pods", "Get pods"))
    results.append(test_endpoint("GET", "/deployments", "Get deployments"))
    results.append(test_endpoint("GET", "/nodes", "Get nodes"))
    print()
    
    # Dashboard Endpoints
    print(f"{YELLOW}Testing Dashboard Endpoints...{RESET}")
    results.append(test_endpoint("GET", "/dashboard/stats?hours=24", "Dashboard stats (comprehensive)"))
    results.append(test_endpoint("GET", "/stats/summary", "Quick summary stats"))
    print()
    
    # Cost Analysis
    print(f"{YELLOW}Testing Cost Analysis Endpoints...{RESET}")
    results.append(test_endpoint("GET", "/cost/current", "Current cost calculation"))
    results.append(test_endpoint("GET", "/cost/savings?hours=24", "Savings calculation"))
    results.append(test_endpoint("GET", "/cost/recommendations", "Cost recommendations"))
    results.append(test_endpoint("GET", "/cost/breakdown?hours=24", "Cost breakdown"))
    print()
    
    # Incidents
    print(f"{YELLOW}Testing Incident Tracking...{RESET}")
    results.append(test_endpoint("GET", "/incidents?limit=10", "Get incidents"))
    print()
    
    # Chaos Engineering
    print(f"{YELLOW}Testing Chaos Engineering Endpoints...{RESET}")
    results.append(test_endpoint("GET", "/chaos/status", "Chaos status"))
    # Note: Not testing POST chaos endpoints to avoid actually disrupting the cluster
    print(f"{BLUE}ℹ{RESET}  Skipping POST chaos endpoints (would disrupt cluster)")
    print()
    
    # Summary
    total = len(results)
    passed = sum(results)
    failed = total - passed
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Results:{RESET}")
    print(f"  {GREEN}Passed:{RESET} {passed}/{total}")
    print(f"  {RED}Failed:{RESET} {failed}/{total}")
    print(f"  Success Rate: {success_rate:.1f}%")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    if success_rate == 100:
        print(f"{GREEN}✓ All tests passed! Backend is fully operational.{RESET}\n")
    elif success_rate >= 80:
        print(f"{YELLOW}⚠ Most tests passed. Check failed endpoints.{RESET}\n")
    else:
        print(f"{RED}✗ Multiple failures detected. Check server logs.{RESET}\n")
    
    return success_rate == 100


def demo_dashboard_response():
    """Show sample dashboard response for frontend developers"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Sample Dashboard Response (for frontend development){RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    try:
        response = requests.get(f"{BASE_URL}/dashboard/stats?hours=24")
        if response.status_code == 200:
            data = response.json()
            
            print(f"{GREEN}Cluster Status:{RESET}")
            cluster = data.get('cluster', {})
            print(f"  Total Pods: {cluster.get('total_pods', 0)}")
            print(f"  Healthy: {cluster.get('healthy_pods', 0)}")
            print(f"  Unhealthy: {cluster.get('unhealthy_pods', 0)}")
            print()
            
            print(f"{GREEN}Current Metrics:{RESET}")
            metrics = data.get('metrics', {})
            print(f"  CPU: {metrics.get('cpu_usage', 0)}%")
            print(f"  Memory: {metrics.get('memory_usage', 0)}%")
            print()
            
            print(f"{GREEN}Cost:{RESET}")
            cost = data.get('cost', {})
            print(f"  Hourly: ${cost.get('hourly', 0):.2f}")
            print(f"  Daily: ${cost.get('daily', 0):.2f}")
            print(f"  Monthly: ${cost.get('monthly', 0):.2f}")
            print()
            
            print(f"{GREEN}Savings:{RESET}")
            savings = data.get('savings', {})
            print(f"  Saved (24h): ${savings.get('total_saved', 0):.2f}")
            print(f"  Projected Monthly: ${savings.get('projected_monthly', 0):.2f}")
            print(f"  Scale Ups: {savings.get('scale_up_count', 0)}")
            print(f"  Scale Downs: {savings.get('scale_down_count', 0)}")
            print()
            
            print(f"{GREEN}Incidents:{RESET}")
            incidents = data.get('incidents', {})
            print(f"  Total: {incidents.get('total', 0)}")
            print(f"  Successful: {incidents.get('successful', 0)}")
            print(f"  Success Rate: {incidents.get('success_rate', 0)}%")
            print()
            
            print(f"{GREEN}Recommendations:{RESET}")
            recommendations = data.get('recommendations', [])
            if recommendations:
                for rec in recommendations[:3]:  # Show first 3
                    print(f"  • {rec.get('title', 'N/A')}")
                    print(f"    {rec.get('description', '')}")
            else:
                print(f"  No recommendations")
            print()
            
            print(f"{BLUE}Full JSON Response:{RESET}")
            print(json.dumps(data, indent=2))
            
        else:
            print(f"{RED}Failed to get dashboard stats{RESET}")
    
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")


def interactive_menu():
    """Interactive menu for testing"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}SentinelOps Backend Test Menu{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    print("1. Run all endpoint tests")
    print("2. Show sample dashboard response")
    print("3. Test single endpoint")
    print("4. Monitor real-time stats (5s interval)")
    print("5. Exit")
    print()


def monitor_realtime():
    """Monitor real-time stats"""
    print(f"\n{BLUE}Monitoring real-time stats (Ctrl+C to stop)...{RESET}\n")
    
    try:
        while True:
            response = requests.get(f"{BASE_URL}/stats/summary")
            if response.status_code == 200:
                data = response.json()
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] Pods: {data.get('pods', 0)} | "
                      f"CPU: {data.get('cpu', 0):.1f}% | "
                      f"Memory: {data.get('memory', 0):.1f}% | "
                      f"Cost: ${data.get('daily_cost', 0):.2f}/day")
            time.sleep(5)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Monitoring stopped{RESET}\n")


if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print(f"{RED}Server is not healthy. Please start the server first.{RESET}")
            print(f"Run: {BLUE}python -m uvicorn mcp_server.main:app --reload{RESET}")
            exit(1)
    except:
        print(f"{RED}Cannot connect to server at {BASE_URL}{RESET}")
        print(f"Please start the server first:")
        print(f"  {BLUE}cd mcp_server{RESET}")
        print(f"  {BLUE}python -m uvicorn main:app --reload{RESET}")
        exit(1)
    
    # Run tests by default
    if test_all_endpoints():
        demo_dashboard_response()
    
    # Interactive mode (optional)
    # while True:
    #     interactive_menu()
    #     choice = input("Select option: ").strip()
    #     
    #     if choice == "1":
    #         test_all_endpoints()
    #     elif choice == "2":
    #         demo_dashboard_response()
    #     elif choice == "4":
    #         monitor_realtime()
    #     elif choice == "5":
    #         break

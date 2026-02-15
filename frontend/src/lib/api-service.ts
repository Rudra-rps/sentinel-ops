// SentinelOps API Service
import { API_CONFIG, API_ENDPOINTS } from './api-config';
import type {
  DashboardStats,
  StatsSummary,
  HealthResponse,
  ResourceMetrics,
  Pod,
  Deployment,
  CostMetrics,
  SavingsMetrics,
  Recommendation,
  Incident,
  ScaleResponse,
  SimulationResponse,
  ChaosStatus,
} from './api-types';

class APIError extends Error {
  constructor(
    message: string,
    public status?: number,
    public response?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

class SentinelOpsAPI {
  private baseURL: string;
  private timeout: number;

  constructor() {
    this.baseURL = API_CONFIG.BASE_URL;
    this.timeout = API_CONFIG.TIMEOUT;
  }

  /**
   * Generic fetch wrapper with error handling
   */
  private async fetch<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const url = `${this.baseURL}${endpoint}`;
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new APIError(
          `API request failed: ${response.statusText}`,
          response.status
        );
      }

      const data = await response.json();
      return data as T;
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error instanceof APIError) {
        throw error;
      }
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new APIError('Request timeout');
        }
        throw new APIError(`Network error: ${error.message}`);
      }
      
      throw new APIError('Unknown error occurred');
    }
  }

  // ============================================================
  // DASHBOARD & SUMMARY ENDPOINTS
  // ============================================================

  /**
   * Get complete dashboard statistics
   * @param hours - Time window in hours (default: 24)
   */
  async getDashboardStats(hours: number = API_CONFIG.DEFAULT_TIME_WINDOW): Promise<DashboardStats> {
    return this.fetch<DashboardStats>(`${API_ENDPOINTS.DASHBOARD_STATS}?hours=${hours}`);
  }

  /**
   * Get lightweight summary for real-time updates
   */
  async getStatsSummary(): Promise<StatsSummary> {
    return this.fetch<StatsSummary>(API_ENDPOINTS.STATS_SUMMARY);
  }

  /**
   * Health check
   */
  async getHealth(): Promise<HealthResponse> {
    return this.fetch<HealthResponse>(API_ENDPOINTS.HEALTH);
  }

  // ============================================================
  // METRICS ENDPOINTS
  // ============================================================

  /**
   * Get all metrics for namespace
   */
  async getMetrics(namespace: string = API_CONFIG.DEFAULT_NAMESPACE): Promise<ResourceMetrics> {
    const response = await this.fetch<{ success: boolean; metrics: ResourceMetrics }>(
      `${API_ENDPOINTS.METRICS}?namespace=${namespace}`
    );
    return response.metrics;
  }

  /**
   * Get CPU usage
   */
  async getCPUMetrics(
    namespace: string = API_CONFIG.DEFAULT_NAMESPACE,
    deployment?: string
  ): Promise<number> {
    const params = new URLSearchParams({ namespace });
    if (deployment) params.append('deployment', deployment);
    
    const response = await this.fetch<{ cpu_usage_percent: number }>(
      `${API_ENDPOINTS.METRICS_CPU}?${params}`
    );
    return response.cpu_usage_percent;
  }

  /**
   * Get memory usage
   */
  async getMemoryMetrics(
    namespace: string = API_CONFIG.DEFAULT_NAMESPACE,
    deployment?: string
  ): Promise<number> {
    const params = new URLSearchParams({ namespace });
    if (deployment) params.append('deployment', deployment);
    
    const response = await this.fetch<{ memory_usage_percent: number }>(
      `${API_ENDPOINTS.METRICS_MEMORY}?${params}`
    );
    return response.memory_usage_percent;
  }

  // ============================================================
  // KUBERNETES RESOURCES
  // ============================================================

  /**
   * Get all pods
   */
  async getPods(namespace: string = API_CONFIG.DEFAULT_NAMESPACE): Promise<Pod[]> {
    const response = await this.fetch<{ pods: Pod[] }>(
      `${API_ENDPOINTS.PODS}?namespace=${namespace}`
    );
    return response.pods;
  }

  /**
   * Get all deployments
   */
  async getDeployments(namespace: string = API_CONFIG.DEFAULT_NAMESPACE): Promise<Deployment[]> {
    const response = await this.fetch<{ deployments: Deployment[] }>(
      `${API_ENDPOINTS.DEPLOYMENTS}?namespace=${namespace}`
    );
    return response.deployments;
  }

  /**
   * Get pod logs
   */
  async getPodLogs(
    podName: string,
    namespace: string = API_CONFIG.DEFAULT_NAMESPACE,
    tail: number = 100
  ): Promise<string> {
    const response = await this.fetch<{ logs: string }>(
      `/logs/${podName}?namespace=${namespace}&tail=${tail}`
    );
    return response.logs;
  }

  // ============================================================
  // CONTROL OPERATIONS
  // ============================================================

  /**
   * Scale a deployment
   */
  async scaleDeployment(
    deployment: string,
    replicas: number,
    namespace: string = API_CONFIG.DEFAULT_NAMESPACE
  ): Promise<ScaleResponse> {
    return this.fetch<ScaleResponse>(
      `${API_ENDPOINTS.SCALE}?deployment=${deployment}&replicas=${replicas}&namespace=${namespace}`,
      { method: 'POST' }
    );
  }

  /**
   * Restart a deployment
   */
  async restartDeployment(
    deployment: string,
    namespace: string = API_CONFIG.DEFAULT_NAMESPACE
  ): Promise<any> {
    return this.fetch(
      `${API_ENDPOINTS.RESTART}?deployment=${deployment}&namespace=${namespace}`,
      { method: 'POST' }
    );
  }

  /**
   * Delete a pod
   */
  async deletePod(
    podName: string,
    namespace: string = API_CONFIG.DEFAULT_NAMESPACE
  ): Promise<any> {
    return this.fetch(
      `${API_ENDPOINTS.DELETE_POD}?pod_name=${podName}&namespace=${namespace}`,
      { method: 'POST' }
    );
  }

  // ============================================================
  // COST ANALYSIS
  // ============================================================

  /**
   * Get current cost
   */
  async getCurrentCost(namespace: string = API_CONFIG.DEFAULT_NAMESPACE): Promise<any> {
    return this.fetch(`${API_ENDPOINTS.COST_CURRENT}?namespace=${namespace}`);
  }

  /**
   * Get savings data
   */
  async getSavings(hours: number = API_CONFIG.DEFAULT_TIME_WINDOW): Promise<any> {
    return this.fetch(`${API_ENDPOINTS.COST_SAVINGS}?hours=${hours}`);
  }

  /**
   * Get cost recommendations
   */
  async getRecommendations(): Promise<{ recommendations: Recommendation[] }> {
    return this.fetch(`${API_ENDPOINTS.COST_RECOMMENDATIONS}`);
  }

  /**
   * Get comprehensive cost breakdown
   */
  async getCostBreakdown(hours: number = API_CONFIG.DEFAULT_TIME_WINDOW): Promise<any> {
    return this.fetch(`${API_ENDPOINTS.COST_BREAKDOWN}?hours=${hours}`);
  }

  // ============================================================
  // INCIDENTS
  // ============================================================

  /**
   * Get recent incidents
   */
  async getIncidents(limit: number = 50): Promise<{ incidents: Incident[]; count: number }> {
    return this.fetch(`${API_ENDPOINTS.INCIDENTS}?limit=${limit}`);
  }

  /**
   * Log a new incident
   */
  async logIncident(incident: {
    type: string;
    severity: string;
    resource: string;
    action_taken: string;
  }): Promise<any> {
    return this.fetch(API_ENDPOINTS.INCIDENTS, {
      method: 'POST',
      body: JSON.stringify(incident),
    });
  }

  // ============================================================
  // CHAOS ENGINEERING
  // ============================================================

  /**
   * Simulate CPU spike
   */
  async simulateCPUSpike(
    deployment: string = 'nginx-demo',
    duration: number = 300
  ): Promise<SimulationResponse> {
    return this.fetch<SimulationResponse>(
      `${API_ENDPOINTS.SIMULATE_CPU_SPIKE}?deployment=${deployment}&duration=${duration}`,
      { method: 'POST' }
    );
  }

  /**
   * Simulate pod crash
   */
  async simulateCrash(): Promise<SimulationResponse> {
    return this.fetch<SimulationResponse>(
      API_ENDPOINTS.SIMULATE_CRASH,
      { method: 'POST' }
    );
  }

  /**
   * Simulate cascade failure
   */
  async simulateCascade(): Promise<SimulationResponse> {
    return this.fetch<SimulationResponse>(
      API_ENDPOINTS.SIMULATE_CASCADE,
      { method: 'POST' }
    );
  }

  /**
   * Cleanup chaos simulations
   */
  async cleanupSimulations(): Promise<SimulationResponse> {
    return this.fetch<SimulationResponse>(
      API_ENDPOINTS.SIMULATE_CLEANUP,
      { method: 'POST' }
    );
  }

  /**
   * Get chaos status
   */
  async getChaosStatus(): Promise<ChaosStatus> {
    return this.fetch<ChaosStatus>(API_ENDPOINTS.CHAOS_STATUS);
  }
}

// Export singleton instance
export const api = new SentinelOpsAPI();

// Export class for testing
export { SentinelOpsAPI, APIError };

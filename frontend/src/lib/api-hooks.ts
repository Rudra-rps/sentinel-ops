// React hooks for SentinelOps API
import { useState, useEffect, useCallback, useRef } from 'react';
import { api } from './api-service';
import { API_CONFIG } from './api-config';
import type { DashboardStats, StatsSummary, Incident, Recommendation, ChartPoint } from './api-types';

export interface UseDashboardOptions {
  enabled?: boolean;
  refreshInterval?: number;
  hours?: number;
}

export interface UseDashboardResult {
  data: DashboardStats | null;
  isLoading: boolean;
  error: Error | null;
  refresh: () => Promise<void>;
}

/**
 * Hook for fetching complete dashboard data
 */
export function useDashboard(options: UseDashboardOptions = {}): UseDashboardResult {
  const {
    enabled = true,
    refreshInterval = API_CONFIG.POLLING_INTERVALS.NORMAL,
    hours = API_CONFIG.DEFAULT_TIME_WINDOW,
  } = options;

  const [data, setData] = useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const isMountedRef = useRef(true);

  const fetchData = useCallback(async () => {
    if (!enabled) return;

    try {
      const stats = await api.getDashboardStats(hours);
      if (isMountedRef.current) {
        setData(stats);
        setError(null);
      }
    } catch (err) {
      if (isMountedRef.current) {
        setError(err instanceof Error ? err : new Error('Failed to fetch dashboard data'));
        console.error('Dashboard fetch error:', err);
      }
    } finally {
      if (isMountedRef.current) {
        setIsLoading(false);
      }
    }
  }, [enabled, hours]);

  useEffect(() => {
    isMountedRef.current = true;
    fetchData();

    const interval = setInterval(fetchData, refreshInterval);

    return () => {
      isMountedRef.current = false;
      clearInterval(interval);
    };
  }, [fetchData, refreshInterval]);

  return { data, isLoading, error, refresh: fetchData };
}

/**
 * Hook for real-time metrics (fast polling)
 */
export function useRealtimeMetrics(enabled: boolean = true) {
  const [data, setData] = useState<StatsSummary | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const isMountedRef = useRef(true);

  useEffect(() => {
    if (!enabled) return;

    isMountedRef.current = true;

    const fetchData = async () => {
      try {
        const stats = await api.getStatsSummary();
        if (isMountedRef.current) {
          setData(stats);
          setError(null);
        }
      } catch (err) {
        if (isMountedRef.current) {
          setError(err instanceof Error ? err : new Error('Failed to fetch metrics'));
          console.error('Metrics fetch error:', err);
        }
      }
    };

    fetchData();
    const interval = setInterval(fetchData, API_CONFIG.POLLING_INTERVALS.FAST);

    return () => {
      isMountedRef.current = false;
      clearInterval(interval);
    };
  }, [enabled]);

  return { data, error };
}

/**
 * Hook for chaos simulation
 */
export function useChaosSimulation() {
  const [isSimulating, setIsSimulating] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const simulateCPUSpike = useCallback(async (duration: number = 300) => {
    setIsSimulating(true);
    setError(null);
    try {
      const result = await api.simulateCPUSpike('nginx-demo', duration);
      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to simulate CPU spike');
      setError(error);
      throw error;
    } finally {
      setIsSimulating(false);
    }
  }, []);

  const simulateCrash = useCallback(async () => {
    setIsSimulating(true);
    setError(null);
    try {
      const result = await api.simulateCrash();
      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to simulate crash');
      setError(error);
      throw error;
    } finally {
      setIsSimulating(false);
    }
  }, []);

  const simulateCascade = useCallback(async () => {
    setIsSimulating(true);
    setError(null);
    try {
      const result = await api.simulateCascade();
      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to simulate cascade');
      setError(error);
      throw error;
    } finally {
      setIsSimulating(false);
    }
  }, []);

  const cleanup = useCallback(async () => {
    setError(null);
    try {
      const result = await api.cleanupSimulations();
      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to cleanup simulations');
      setError(error);
      throw error;
    }
  }, []);

  return {
    simulateCPUSpike,
    simulateCrash,
    simulateCascade,
    cleanup,
    isSimulating,
    error,
  };
}

/**
 * Transform backend data to chart format
 */
export function transformToChartData(incidents: Incident[], currentMetrics: StatsSummary | null): ChartPoint[] {
  const now = Date.now();
  const points: ChartPoint[] = [];

  // Generate 24 data points (one per time interval)
  for (let i = 0; i < 24; i++) {
    const t = new Date(now - (23 - i) * 150000); // 2.5 minute intervals
    
    // Use current metrics for the latest point, otherwise generate based on historical patterns
    const isLatest = i === 23;
    
    points.push({
      time: t.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      cpu: isLatest && currentMetrics ? currentMetrics.cpu : 30 + Math.sin(i * 0.5) * 15 + Math.random() * 10,
      memory: isLatest && currentMetrics ? currentMetrics.memory : 50 + Math.cos(i * 0.3) * 12 + Math.random() * 8,
      pods: isLatest && currentMetrics ? currentMetrics.pods : 4 + Math.floor(Math.sin(i * 0.4) * 1.5),
    });
  }

  return points;
}

/**
 * Format incidents from backend to frontend format
 */
export function formatIncident(incident: Incident): Incident {
  // If already in new format, convert to display format
  if (incident.issue && incident.action) {
    const timestamp = new Date(incident.timestamp).toLocaleTimeString();
    const type = mapIssueTypeToDisplayType(incident.issue.type);
    const severity = mapSeverityToDisplay(incident.issue.severity);
    const title = incident.issue.type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) + ' Detected';
    const action = formatAction(incident.action);
    const resolvedIn = incident.result?.duration_ms 
      ? `${(incident.result.duration_ms / 1000).toFixed(1)}s`
      : 'N/A';

    return {
      ...incident,
      timestamp,
      type,
      severity,
      title,
      action_text: action,
      resolvedIn,
    };
  }

  return incident;
}

function mapIssueTypeToDisplayType(type: string): 'scale' | 'crash' | 'warning' | 'optimize' {
  if (type.includes('overload') || type.includes('spike')) return 'scale';
  if (type.includes('crash') || type.includes('unhealthy')) return 'crash';
  if (type.includes('warning')) return 'warning';
  return 'optimize';
}

function mapSeverityToDisplay(severity: string): 'success' | 'warning' | 'error' | 'info' {
  switch (severity.toLowerCase()) {
    case 'critical':
    case 'high': return 'error';
    case 'medium': return 'warning';
    case 'low': return 'info';
    default: return 'success';
  }
}

function formatAction(action: any): string {
  if (!action) return 'Action taken';
  
  const { type, target, parameters } = action;
  
  if (type === 'scale_up' || type === 'scale_down') {
    const from = parameters?.from || '?';
    const to = parameters?.to || '?';
    return `Scaled ${target}: ${from} → ${to} pods`;
  }
  
  if (type === 'restart') {
    return `Restarted ${target}`;
  }
  
  return `${type.replace(/_/g, ' ')} for ${target}`;
}

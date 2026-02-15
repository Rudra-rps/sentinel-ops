import { useState, useEffect, useMemo } from "react";
import Header from "@/components/dashboard/Header";
import ScoreboardCards from "@/components/dashboard/ScoreboardCards";
import PerformanceChart from "@/components/dashboard/PerformanceChart";
import CostAnalysis from "@/components/dashboard/CostAnalysis";
import IncidentFeed from "@/components/dashboard/IncidentFeed";
import Recommendations from "@/components/dashboard/Recommendations";
import ChaosPanel from "@/components/dashboard/ChaosPanel";
import Footer from "@/components/dashboard/Footer";
import { useDashboard, useRealtimeMetrics, transformToChartData, formatIncident } from "@/lib/api-hooks.ts";
import type { ChartPoint } from "@/lib/api-types";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2 } from "lucide-react";

const Index = () => {
  // Fetch dashboard data with 10-second refresh
  const { data: dashboardData, isLoading, error } = useDashboard({
    refreshInterval: 10000,
    hours: 24,
  });

  // Fetch real-time metrics with 3-second refresh
  const { data: realtimeMetrics } = useRealtimeMetrics(true);

  // Generate chart data from real-time metrics
  const [chartData, setChartData] = useState<ChartPoint[]>([]);

  useEffect(() => {
    if (realtimeMetrics || dashboardData) {
      const newChartData = transformToChartData(
        dashboardData?.incidents?.recent || [],
        realtimeMetrics
      );
      setChartData(newChartData);
    }
  }, [realtimeMetrics, dashboardData]);

  // Transform backend data to component format
  const metrics = useMemo(() => {
    if (!dashboardData) return null;

    return {
      cpu: realtimeMetrics?.cpu || dashboardData.metrics.cpu_usage,
      memory: realtimeMetrics?.memory || dashboardData.metrics.memory_usage,
      pods: {
        total: realtimeMetrics?.pods || dashboardData.cluster.total_pods,
        healthy: dashboardData.cluster.healthy_pods,
        unhealthy: dashboardData.cluster.unhealthy_pods,
      },
      cost: {
        daily: realtimeMetrics?.daily_cost || dashboardData.cost.daily,
        savedToday: dashboardData.savings.total_saved,
        monthlyProjection: dashboardData.cost.monthly,
        monthlySavings: dashboardData.savings.projected_monthly,
        savingsPercent: dashboardData.savings.efficiency_score ||
          ((dashboardData.savings.projected_monthly / dashboardData.cost.monthly) * 100),
      },
    };
  }, [dashboardData, realtimeMetrics]);

  const incidents = useMemo(() => {
    return dashboardData?.incidents?.recent?.map(formatIncident) || [];
  }, [dashboardData?.incidents]);

  const recommendations = useMemo(() => {
    return dashboardData?.recommendations?.map(rec => ({
      ...rec,
      potentialSavings: rec.potential_savings || rec.potentialSavings || 'N/A',
    })) || [];
  }, [dashboardData?.recommendations]);

  // Loading state
  if (isLoading && !dashboardData) {
    return (
      <div className="min-h-screen stadium-bg flex items-center justify-center">
        <div className="text-center space-y-4">
          <Loader2 className="h-12 w-12 animate-spin mx-auto text-primary" />
          <p className="text-lg text-muted-foreground">Connecting to SentinelOps...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error && !dashboardData) {
    return (
      <div className="min-h-screen stadium-bg flex items-center justify-center p-4">
        <Alert variant="destructive" className="max-w-md">
          <AlertDescription>
            <strong>Connection Error</strong>
            <p className="mt-2">Unable to connect to the SentinelOps backend.</p>
            <p className="text-sm mt-2">Please ensure the backend is running at http://localhost:8000</p>
            <p className="text-sm text-muted-foreground mt-2">{error.message}</p>
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="min-h-screen stadium-bg flex flex-col">
      <Header />

      <main className="flex-1 p-4 md:p-6 space-y-4 md:space-y-6 max-w-[1400px] mx-auto w-full">
        {/* Connection warning banner */}
        {error && (
          <Alert variant="destructive">
            <AlertDescription>
              Connection issues detected. Displaying cached data. {error.message}
            </AlertDescription>
          </Alert>
        )}

        {/* Hero Metrics */}
        {metrics && <ScoreboardCards metrics={metrics} />}

        {/* Two-column layout on desktop */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-4 md:gap-6">
          {/* Left column - 60% */}
          <div className="lg:col-span-3 space-y-4 md:space-y-6">
            <PerformanceChart data={chartData} />
            {metrics && <CostAnalysis metrics={metrics} />}
          </div>

          {/* Right column - 40% */}
          <div className="lg:col-span-2 space-y-4 md:space-y-6">
            <IncidentFeed incidents={incidents} />
            <Recommendations recommendations={recommendations} />
          </div>
        </div>

        {/* Chaos Testing Panel */}
        <ChaosPanel />
      </main>

      <Footer />
    </div>
  );
};

export default Index;

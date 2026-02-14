import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import type { ChartPoint } from "@/lib/mock-data";

interface PerformanceChartProps {
  data: ChartPoint[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="scoreboard-card p-3 border border-border text-xs">
      <p className="font-scoreboard text-muted-foreground mb-1">{label}</p>
      {payload.map((entry: any) => (
        <p key={entry.name} className="font-led" style={{ color: entry.color }}>
          {entry.name.toUpperCase()}: {typeof entry.value === "number" ? entry.value.toFixed(1) : entry.value}
          {entry.name !== "pods" ? "%" : ""}
        </p>
      ))}
    </div>
  );
};

const PerformanceChart = ({ data }: PerformanceChartProps) => (
  <div className="scoreboard-card neon-border-green p-4 md:p-5">
    <div className="flex items-center justify-between mb-4">
      <h3 className="font-scoreboard text-xs md:text-sm tracking-widest text-foreground">
        📊 GAME STATS — SYSTEM PERFORMANCE
      </h3>
      <span className="font-led text-[10px] text-muted-foreground">LAST HOUR</span>
    </div>
    <div className="h-[220px] md:h-[280px]">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: -20 }}>
          <defs>
            <linearGradient id="cpuGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="hsl(190, 85%, 50%)" stopOpacity={0.3} />
              <stop offset="100%" stopColor="hsl(190, 85%, 50%)" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="memGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="hsl(270, 70%, 60%)" stopOpacity={0.3} />
              <stop offset="100%" stopColor="hsl(270, 70%, 60%)" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="podGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="hsl(160, 80%, 45%)" stopOpacity={0.3} />
              <stop offset="100%" stopColor="hsl(160, 80%, 45%)" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 15%, 18%)" />
          <XAxis dataKey="time" tick={{ fontSize: 10, fill: "hsl(215, 15%, 55%)", fontFamily: "Share Tech Mono" }} interval="preserveStartEnd" />
          <YAxis tick={{ fontSize: 10, fill: "hsl(215, 15%, 55%)", fontFamily: "Share Tech Mono" }} />
          <Tooltip content={<CustomTooltip />} />
          <Area type="monotone" dataKey="cpu" stroke="hsl(190, 85%, 50%)" fill="url(#cpuGrad)" strokeWidth={2} name="cpu" dot={false} />
          <Area type="monotone" dataKey="memory" stroke="hsl(270, 70%, 60%)" fill="url(#memGrad)" strokeWidth={2} name="memory" dot={false} />
          <Area type="monotone" dataKey="pods" stroke="hsl(160, 80%, 45%)" fill="url(#podGrad)" strokeWidth={2} name="pods" dot={false} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
    <div className="flex gap-4 mt-3">
      {[
        { label: "CPU", color: "hsl(190, 85%, 50%)" },
        { label: "MEMORY", color: "hsl(270, 70%, 60%)" },
        { label: "PODS", color: "hsl(160, 80%, 45%)" },
      ].map((item) => (
        <div key={item.label} className="flex items-center gap-1.5">
          <div className="h-2 w-2 rounded-full" style={{ backgroundColor: item.color }} />
          <span className="font-scoreboard text-[9px] tracking-wider text-muted-foreground">{item.label}</span>
        </div>
      ))}
    </div>
  </div>
);

export default PerformanceChart;

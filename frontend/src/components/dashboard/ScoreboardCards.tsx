import { useEffect, useState } from "react";
import { Cpu, MemoryStick, Box, DollarSign, TrendingDown } from "lucide-react";
import type { MetricData } from "@/lib/mock-data";

interface ScoreboardCardsProps {
  metrics: MetricData;
}

const useAnimatedNumber = (target: number, decimals = 1) => {
  const [value, setValue] = useState(0);
  useEffect(() => {
    const duration = 800;
    const start = value;
    const diff = target - start;
    const startTime = Date.now();
    const tick = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setValue(start + diff * eased);
      if (progress < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [target]);
  return Number(value.toFixed(decimals));
};

const getStatusColor = (value: number, thresholds: [number, number]) => {
  if (value < thresholds[0]) return "green";
  if (value < thresholds[1]) return "amber";
  return "red";
};

const ScoreboardCards = ({ metrics }: ScoreboardCardsProps) => {
  const cpu = useAnimatedNumber(metrics.cpu);
  const memory = useAnimatedNumber(metrics.memory);
  const cost = useAnimatedNumber(metrics.cost.daily, 2);
  const saved = useAnimatedNumber(metrics.cost.savedToday, 2);

  const cpuColor = getStatusColor(metrics.cpu, [60, 80]);
  const memColor = getStatusColor(metrics.memory, [70, 85]);

  const cards = [
    {
      icon: Cpu,
      label: "CPU USAGE",
      value: `${cpu}%`,
      bar: metrics.cpu,
      color: cpuColor,
      status: cpuColor === "green" ? "NORMAL" : cpuColor === "amber" ? "ELEVATED" : "CRITICAL",
    },
    {
      icon: MemoryStick,
      label: "MEMORY",
      value: `${memory}%`,
      bar: metrics.memory,
      color: memColor,
      status: memColor === "green" ? "OPTIMAL" : memColor === "amber" ? "MODERATE" : "HIGH",
    },
    {
      icon: Box,
      label: "ACTIVE PODS",
      value: `${metrics.pods.total}`,
      bar: (metrics.pods.healthy / metrics.pods.total) * 100,
      color: metrics.pods.unhealthy > 0 ? "red" : "green",
      status: metrics.pods.unhealthy > 0 ? `${metrics.pods.unhealthy} UNHEALTHY` : "ALL HEALTHY",
    },
    {
      icon: DollarSign,
      label: "COST / DAY",
      value: `$${cost}`,
      bar: null,
      color: "cyan",
      status: null,
      extra: { saved, savingsPercent: metrics.cost.savingsPercent },
    },
  ];

  const colorClasses: Record<string, { text: string; border: string; bg: string; bar: string }> = {
    green: { text: "led-text-green", border: "neon-border-green", bg: "bg-primary/10", bar: "bg-primary" },
    amber: { text: "led-text-amber", border: "neon-border-amber", bg: "bg-accent/10", bar: "bg-accent" },
    red: { text: "led-text-red", border: "neon-border-red", bg: "bg-destructive/10", bar: "bg-destructive" },
    cyan: { text: "led-text-cyan", border: "border-info/40", bg: "bg-info/10", bar: "bg-info" },
  };

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
      {cards.map((card, i) => {
        const c = colorClasses[card.color];
        return (
          <div
            key={card.label}
            className={`scoreboard-card ${c.border} p-4 md:p-5 transition-all duration-300 cursor-default`}
            style={{ animationDelay: `${i * 100}ms` }}
          >
            <div className="flex items-center gap-2 mb-3">
              <div className={`p-1.5 rounded ${c.bg}`}>
                <card.icon className={`h-4 w-4 ${c.text.replace('led-text-', 'text-').replace('green', 'primary').replace('amber', 'accent').replace('red', 'destructive').replace('cyan', 'info')}`} />
              </div>
              <span className="font-scoreboard text-[10px] md:text-xs text-muted-foreground tracking-widest">
                {card.label}
              </span>
            </div>

            <div className={`font-led text-2xl md:text-4xl font-bold ${c.text} mb-2`}>
              {card.value}
            </div>

            {card.bar !== null && (
              <div className="w-full h-1.5 bg-secondary rounded-full overflow-hidden mb-2">
                <div
                  className={`h-full ${c.bar} rounded-full transition-all duration-700`}
                  style={{ width: `${Math.min(card.bar, 100)}%` }}
                />
              </div>
            )}

            {card.status && (
              <span className={`font-scoreboard text-[9px] tracking-widest ${c.text} opacity-80`}>
                {card.status}
              </span>
            )}

            {card.extra && (
              <div className="flex items-center gap-1.5 mt-1">
                <TrendingDown className="h-3 w-3 text-primary" />
                <span className="font-led text-xs text-primary">
                  -${card.extra.saved.toFixed(2)} saved
                </span>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default ScoreboardCards;

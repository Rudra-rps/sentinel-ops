import { TrendingDown, Trophy, Target } from "lucide-react";
import type { MetricData } from "@/lib/mock-data";

interface CostAnalysisProps {
  metrics: MetricData;
}

const CostAnalysis = ({ metrics }: CostAnalysisProps) => {
  const { cost } = metrics;

  return (
    <div className="scoreboard-card neon-border-amber p-4 md:p-5">
      <h3 className="font-scoreboard text-xs md:text-sm tracking-widest text-foreground mb-4">
        💰 SEASON STATS — COST ANALYSIS
      </h3>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <span className="font-scoreboard text-[9px] tracking-widest text-muted-foreground">DAILY COST</span>
          <p className="font-led text-2xl led-text-cyan mt-1">${cost.daily.toFixed(2)}</p>
        </div>
        <div>
          <span className="font-scoreboard text-[9px] tracking-widest text-muted-foreground">MONTHLY PROJ.</span>
          <p className="font-led text-2xl text-foreground mt-1">${cost.monthlyProjection.toFixed(0)}</p>
        </div>
      </div>

      <div className="border-t border-border pt-4 space-y-3">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded bg-primary/10">
            <TrendingDown className="h-4 w-4 text-primary" />
          </div>
          <div>
            <span className="font-scoreboard text-[9px] tracking-widest text-muted-foreground">SAVED TODAY</span>
            <p className="font-led text-lg led-text-green">${cost.savedToday.toFixed(2)}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded bg-accent/10">
            <Trophy className="h-4 w-4 text-accent" />
          </div>
          <div>
            <span className="font-scoreboard text-[9px] tracking-widest text-muted-foreground">MONTHLY SAVINGS</span>
            <p className="font-led text-lg led-text-amber">${cost.monthlySavings.toFixed(0)}</p>
          </div>
        </div>

        {/* Savings bar */}
        <div>
          <div className="flex justify-between mb-1">
            <span className="font-scoreboard text-[9px] tracking-widest text-muted-foreground">SAVINGS RATE</span>
            <span className="font-led text-xs text-primary">{cost.savingsPercent.toFixed(0)}%</span>
          </div>
          <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-primary to-accent rounded-full transition-all duration-700"
              style={{ width: `${cost.savingsPercent}%` }}
            />
          </div>
        </div>

        <div className="flex items-center gap-2 p-2 rounded bg-primary/5 border border-primary/20">
          <Target className="h-4 w-4 text-primary" />
          <span className="font-body text-sm text-primary font-semibold">
            Saving {cost.savingsPercent.toFixed(0)}% vs baseline!
          </span>
        </div>
      </div>
    </div>
  );
};

export default CostAnalysis;

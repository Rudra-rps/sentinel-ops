import { Lightbulb, ArrowRight, Sparkles } from "lucide-react";
import type { Recommendation } from "@/lib/api-types";
import { toast } from "sonner";

interface RecommendationsProps {
  recommendations: Recommendation[];
}

const severityBadge: Record<string, string> = {
  high: "bg-destructive/15 text-destructive border-destructive/30",
  medium: "bg-accent/15 text-accent border-accent/30",
  low: "bg-info/15 text-info border-info/30",
};

const Recommendations = ({ recommendations }: RecommendationsProps) => (
  <div className="scoreboard-card p-4 md:p-5">
    <h3 className="font-scoreboard text-xs md:text-sm tracking-widest text-foreground mb-4">
      💡 COACH&apos;S CORNER — RECOMMENDATIONS
    </h3>

    <div className="space-y-3">
      {recommendations.map((rec) => (
        <div key={rec.id} className="bg-secondary/30 rounded-md p-3 border border-border hover:border-primary/20 transition-colors">
          <div className="flex items-start justify-between gap-2 mb-2">
            <div className="flex items-center gap-2">
              <Lightbulb className="h-4 w-4 text-accent shrink-0" />
              <span className="font-body text-sm font-semibold text-foreground">{rec.title}</span>
            </div>
            <span className={`font-scoreboard text-[9px] tracking-wider px-2 py-0.5 rounded-full border ${severityBadge[rec.severity]}`}>
              {rec.severity.toUpperCase()}
            </span>
          </div>
          <p className="font-body text-xs text-muted-foreground mb-2">{rec.description}</p>
          <div className="flex items-center justify-between">
            <span className="font-led text-xs text-primary">Saves {rec.potentialSavings || rec.potential_savings || 'N/A'}</span>
            <button
              onClick={() => toast.success(`Applied: ${rec.title}`)}
              className="flex items-center gap-1 font-scoreboard text-[10px] tracking-wider text-primary hover:text-primary/80 transition-colors"
            >
              APPLY <ArrowRight className="h-3 w-3" />
            </button>
          </div>
        </div>
      ))}

      <div className="flex items-center gap-2 p-3 rounded-md bg-primary/5 border border-primary/20">
        <Sparkles className="h-4 w-4 text-primary" />
        <span className="font-body text-sm text-primary font-semibold">System is well-optimized overall!</span>
      </div>
    </div>
  </div>
);

export default Recommendations;

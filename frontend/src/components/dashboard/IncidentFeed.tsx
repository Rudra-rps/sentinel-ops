import { CheckCircle, AlertTriangle, XCircle, Info } from "lucide-react";
import type { Incident } from "@/lib/api-types";

interface IncidentFeedProps {
  incidents: Incident[];
}

const severityConfig = {
  success: { icon: CheckCircle, border: "border-l-primary", iconClass: "text-primary" },
  warning: { icon: AlertTriangle, border: "border-l-accent", iconClass: "text-accent" },
  error: { icon: XCircle, border: "border-l-destructive", iconClass: "text-destructive" },
  info: { icon: Info, border: "border-l-info", iconClass: "text-info" },
};

const IncidentFeed = ({ incidents }: IncidentFeedProps) => (
  <div className="scoreboard-card neon-border-green p-4 md:p-5">
    <div className="flex items-center justify-between mb-4">
      <h3 className="font-scoreboard text-xs md:text-sm tracking-widest text-foreground">
        🔄 PLAY-BY-PLAY — LIVE ACTIONS
      </h3>
      <span className="font-led text-[10px] text-primary animate-pulse-glow">● RECORDING</span>
    </div>

    <div className="space-y-2 max-h-[400px] overflow-y-auto pr-1 scrollbar-thin">
      {incidents.map((incident, i) => {
        const config = severityConfig[incident.severity];
        const Icon = config.icon;
        return (
          <div
            key={incident.id}
            className={`border-l-2 ${config.border} bg-secondary/30 rounded-r-md p-3 transition-all duration-200 hover:bg-secondary/50 animate-fade-in`}
            style={{ animationDelay: `${i * 80}ms` }}
          >
            <div className="flex items-start gap-2">
              <Icon className={`h-4 w-4 mt-0.5 shrink-0 ${config.iconClass}`} />
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="font-body text-sm font-semibold text-foreground truncate">
                    {incident.title}
                  </span>
                  <span className="font-led text-[10px] text-muted-foreground shrink-0">
                    {incident.timestamp}
                  </span>
                </div>
                <p className="font-body text-xs text-muted-foreground mt-0.5">
                  ↳ {incident.action_text || (incident.action ? `${incident.action.type}: ${incident.action.target}` : incident.title || 'Action taken')}
                </p>
                <p className="font-led text-[10px] text-primary mt-1">
                  ✓ {incident.resolvedIn || (incident.result?.duration_ms ? `Resolved in ${incident.result.duration_ms}ms` : 'Completed')}
                </p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  </div>
);

export default IncidentFeed;

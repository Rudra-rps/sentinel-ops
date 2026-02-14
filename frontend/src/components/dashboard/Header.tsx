import { useState } from "react";
import { Shield, Radio, Wifi } from "lucide-react";
import { tickerMessages } from "@/lib/mock-data";

const Header = () => {
  const [logoClicks, setLogoClicks] = useState(0);
  const [matrixMode, setMatrixMode] = useState(false);

  const handleLogoClick = () => {
    const next = logoClicks + 1;
    setLogoClicks(next);
    if (next >= 5) {
      setMatrixMode(!matrixMode);
      setLogoClicks(0);
    }
  };

  return (
    <header className="scoreboard-card border-b border-border px-4 py-3 md:px-6">
      <div className="flex items-center justify-between">
        {/* Logo */}
        <button onClick={handleLogoClick} className="flex items-center gap-2 group">
          <div className="relative">
            <Shield className="h-7 w-7 text-primary transition-all group-hover:drop-shadow-[0_0_8px_hsl(var(--primary)/0.6)]" />
          </div>
          <span className="font-scoreboard text-lg font-bold tracking-wider text-foreground">
            SENTINEL<span className="text-primary">OPS</span>
          </span>
        </button>

        {/* Live Badge + Status */}
        <div className="flex items-center gap-4">
          <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-destructive/10 border border-destructive/30">
            <Radio className="h-3 w-3 text-destructive animate-pulse-glow" />
            <span className="font-led text-xs text-destructive tracking-wider">LIVE</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30">
            <Wifi className="h-3 w-3 text-primary" />
            <span className="font-led text-xs text-primary tracking-wider">CONNECTED</span>
          </div>
        </div>
      </div>

      {/* Ticker */}
      <div className="mt-2 overflow-hidden border-t border-border pt-2">
        <div className="ticker-scroll whitespace-nowrap">
          <span className="font-led text-xs text-muted-foreground tracking-wider">
            {tickerMessages.join("   •   ")}
          </span>
        </div>
      </div>

      {/* Matrix Rain Easter Egg */}
      {matrixMode && (
        <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden opacity-20">
          {Array.from({ length: 20 }).map((_, i) => (
            <div
              key={i}
              className="absolute font-led text-primary text-xs animate-fade-in"
              style={{
                left: `${i * 5}%`,
                animation: `fade-in ${1 + Math.random() * 2}s ease-in-out infinite`,
                animationDelay: `${Math.random() * 2}s`,
                top: `${Math.random() * 100}%`,
              }}
            >
              {Array.from({ length: 15 }).map((_, j) => (
                <div key={j}>{String.fromCharCode(0x30A0 + Math.random() * 96)}</div>
              ))}
            </div>
          ))}
        </div>
      )}
    </header>
  );
};

export default Header;

import { useEffect, useState } from "react";

const Footer = () => {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <footer className="border-t border-border px-4 py-3 md:px-6 flex items-center justify-between text-muted-foreground">
      <span className="font-body text-xs">
        Built with ❤️ by <span className="font-scoreboard tracking-wider text-foreground">SentinelOps</span>
      </span>
      <div className="flex items-center gap-4">
        <span className="font-led text-[10px]">REFRESH: {seconds}s ago</span>
        <div className="flex items-center gap-1.5">
          <div className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse-glow" />
          <span className="font-led text-[10px] text-primary">API OK</span>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

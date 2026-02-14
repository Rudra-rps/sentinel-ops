import { useState } from "react";
import { Zap, Bomb, Waves, Timer, AlertTriangle } from "lucide-react";
import { toast } from "sonner";
import { useChaosSimulation } from "@/lib/api-hooks";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface ChaosTest {
  id: string;
  icon: typeof Zap;
  label: string;
  description: string;
  duration: number;
}

const tests: ChaosTest[] = [
  { id: "cpu", icon: Zap, label: "CPU SPIKE", description: "Trigger a 120s CPU overload simulation", duration: 120 },
  { id: "crash", icon: Bomb, label: "CRASH POD", description: "Force-kill a random pod to test auto-heal", duration: 30 },
  { id: "cascade", icon: Waves, label: "CASCADE", description: "Simulate cascading failure across services", duration: 180 },
];

const ChaosPanel = () => {
  const [activeTest, setActiveTest] = useState<string | null>(null);
  const [confirmTest, setConfirmTest] = useState<ChaosTest | null>(null);
  const [countdown, setCountdown] = useState(0);
  
  const { simulateCPUSpike, simulateCrash, simulateCascade, isSimulating, error } = useChaosSimulation();

  const runTest = async (test: ChaosTest) => {
    setConfirmTest(null);
    setActiveTest(test.id);
    setCountdown(test.duration);
    
    try {
      let result;
      
      switch (test.id) {
        case "cpu":
          result = await simulateCPUSpike(test.duration);
          break;
        case "crash":
          result = await simulateCrash();
          break;
        case "cascade":
          result = await simulateCascade();
          break;
      }
      
      toast.success(`${test.label} simulation started!`, {
        description: result?.message || 'Watch the dashboard for real-time updates',
      });

      const interval = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            clearInterval(interval);
            setActiveTest(null);
            toast.success(`${test.label} completed — system auto-healed!`);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } catch (err) {
      setActiveTest(null);
      setCountdown(0);
      toast.error(`Failed to start ${test.label}`, {
        description: error?.message || 'Could not connect to backend',
      });
    }
  };

  return (
    <div className="scoreboard-card neon-border-red p-4 md:p-5">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle className="h-4 w-4 text-destructive" />
        <h3 className="font-scoreboard text-xs md:text-sm tracking-widest text-destructive">
          🔥 OVERTIME MODE — CHAOS ENGINEERING
        </h3>
      </div>

      <p className="font-body text-xs text-muted-foreground mb-4">
        Test autonomous healing capabilities with controlled chaos simulations.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {tests.map((test) => {
          const isActive = activeTest === test.id;
          const isDisabled = !!activeTest || isSimulating;
          
          return (
            <button
              key={test.id}
              onClick={() => !isDisabled && setConfirmTest(test)}
              disabled={isDisabled}
              className={`relative p-4 rounded-lg border transition-all duration-300 text-left group
                ${isActive
                  ? "border-destructive/50 bg-destructive/10"
                  : "border-border hover:border-destructive/40 hover:bg-destructive/5 disabled:opacity-40 disabled:cursor-not-allowed"
                }`}
            >
              <test.icon className={`h-6 w-6 mb-2 ${isActive ? "text-destructive animate-pulse" : "text-muted-foreground group-hover:text-destructive"} transition-colors`} />
              <p className="font-scoreboard text-xs tracking-wider text-foreground">{test.label}</p>
              <p className="font-body text-[10px] text-muted-foreground mt-1">{test.description}</p>
              {isActive && (
                <div className="flex items-center gap-1 mt-2">
                  <Timer className="h-3 w-3 text-destructive" />
                  <span className="font-led text-xs text-destructive">{countdown}s</span>
                </div>
              )}
            </button>
          );
        })}
      </div>

      <AlertDialog open={!!confirmTest} onOpenChange={() => setConfirmTest(null)}>
        <AlertDialogContent className="bg-card border-destructive/30">
          <AlertDialogHeader>
            <AlertDialogTitle className="font-scoreboard tracking-wider text-destructive">
              ⚠️ CONFIRM CHAOS TEST
            </AlertDialogTitle>
            <AlertDialogDescription className="font-body text-muted-foreground">
              You are about to run <strong className="text-foreground">{confirmTest?.label}</strong>.{" "}
              {confirmTest?.description}. Duration: {confirmTest?.duration}s.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel className="font-scoreboard text-xs tracking-wider">ABORT</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => confirmTest && runTest(confirmTest)}
              className="bg-destructive text-destructive-foreground font-scoreboard text-xs tracking-wider hover:bg-destructive/90"
            >
              EXECUTE
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default ChaosPanel;

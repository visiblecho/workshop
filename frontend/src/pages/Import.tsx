import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const WEBER_FIRM_ID = "10000000-0000-0000-0000-000000000001";

interface Step {
  label: string;
  detail: string;
  duration: number;
}

const STEPS: Step[] = [
  { label: "Kundendaten", detail: "23 Kunden gefunden", duration: 800 },
  { label: "Projekte", detail: "5 abgeschlossene, 3 aktive Projekte", duration: 900 },
  { label: "Angebote", detail: "8 Angebote, 147 Positionen", duration: 1000 },
  { label: "Betriebsvergleich", detail: "wird berechnet...", duration: 1200 },
];

export default function Import() {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(-1);
  const [done, setDone] = useState(false);

  useEffect(() => {
    let timeout: number;

    function runStep(index: number) {
      if (index >= STEPS.length) {
        setTimeout(() => setDone(true), 400);
        return;
      }
      setCurrentStep(index);
      timeout = window.setTimeout(() => runStep(index + 1), STEPS[index].duration);
    }

    // Small initial delay
    timeout = window.setTimeout(() => runStep(0), 500);
    return () => clearTimeout(timeout);
  }, []);

  useEffect(() => {
    if (done) {
      const t = setTimeout(() => {
        navigate(`/dashboard?firm=${WEBER_FIRM_ID}&imported=true`);
      }, 600);
      return () => clearTimeout(t);
    }
  }, [done, navigate]);

  return (
    <div className="min-h-screen bg-[#1F1B1C] flex items-center justify-center px-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-2xl font-bold text-white">Taifun-Import</h1>
          <p className="text-white/50">Ihre Daten werden übernommen...</p>
        </div>

        <div className="space-y-4">
          {STEPS.map((step, i) => {
            const isActive = i === currentStep;
            const isComplete = i < currentStep || done;
            const isPending = i > currentStep;

            return (
              <div
                key={i}
                className={`flex items-center gap-4 p-4 rounded-lg transition-all duration-300 ${
                  isActive
                    ? "bg-amber-500/10 border border-amber-500/30"
                    : isComplete
                    ? "bg-green-500/5 border border-green-500/20"
                    : "bg-white/[0.02] border border-white/5"
                }`}
              >
                {/* Status indicator */}
                <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0">
                  {isComplete ? (
                    <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center">
                      <svg className="w-4 h-4 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  ) : isActive ? (
                    <div className="w-8 h-8 rounded-full border-2 border-amber-400 border-t-transparent animate-spin" />
                  ) : (
                    <div className="w-8 h-8 rounded-full border-2 border-white/10" />
                  )}
                </div>

                {/* Text */}
                <div className="min-w-0">
                  <div className={`font-medium text-sm ${
                    isPending ? "text-white/30" : "text-white"
                  }`}>
                    {step.label}
                  </div>
                  {(isActive || isComplete) && (
                    <div className={`text-xs mt-0.5 ${
                      isComplete ? "text-green-400/70" : "text-amber-400/70"
                    }`}>
                      {isComplete && i === 3 ? "Betriebsvergleich bereit" : step.detail}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {done && (
          <div className="text-center animate-pulse">
            <p className="text-green-400 font-medium">Import abgeschlossen</p>
          </div>
        )}
      </div>
    </div>
  );
}

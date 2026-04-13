import { useEffect, useState } from "react";
import { getHealth, type HealthResponse } from "./api";

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch(() => setHealth({ status: "error", db: "unreachable", firm_count: 0 }));
  }, []);

  return (
    <div className="min-h-screen bg-[#1F1B1C] text-white font-['Inter',sans-serif]">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-3 border-b border-white/10">
        <h1 className="text-lg font-semibold tracking-tight">Workshop</h1>
        <div className="text-sm text-white/50">Rolle wählen...</div>
      </header>

      {/* Main */}
      <main className="max-w-2xl mx-auto px-4 py-8">
        <div className="text-center space-y-4">
          <h2 className="text-2xl font-semibold">AI-Native Handwerkersoftware</h2>
          <p className="text-white/60">Prototype wird geladen...</p>

          {/* Health status (dev aid) */}
          {health && (
            <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm ${
              health.status === "ok"
                ? "bg-green-900/30 text-green-400"
                : "bg-red-900/30 text-red-400"
            }`}>
              <span className={`w-2 h-2 rounded-full ${
                health.status === "ok" ? "bg-green-400" : "bg-red-400"
              }`} />
              API: {health.db} | Betriebe: {health.firm_count}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;

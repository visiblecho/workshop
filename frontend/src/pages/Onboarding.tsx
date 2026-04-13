import { useNavigate } from "react-router-dom";

export default function Onboarding() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#1F1B1C] flex items-center justify-center px-4">
      <div className="max-w-2xl w-full space-y-8">
        {/* Logo / Title */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-white tracking-tight">
            Workshop
          </h1>
          <p className="text-white/50 text-lg">
            Intelligente Handwerkersoftware
          </p>
        </div>

        {/* Two paths */}
        <div className="grid gap-4 sm:grid-cols-2">
          {/* Path 1: Taifun Import */}
          <button
            onClick={() => navigate("/import")}
            className="group text-left p-6 rounded-xl border-2 border-amber-500/30 bg-amber-500/5 hover:bg-amber-500/10 hover:border-amber-500/60 transition-all"
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 rounded-lg bg-amber-500/20 flex items-center justify-center text-amber-400">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-white">
                Daten importieren
              </h2>
            </div>
            <p className="text-sm text-white/60 leading-relaxed">
              Ihre Taifun- oder SmartHandwerk-Daten werden importiert. Sofortiger Zugriff auf Ihren Betriebsvergleich.
            </p>
          </button>

          {/* Path 2: Fresh start */}
          <button
            onClick={() => navigate("/new")}
            className="group text-left p-6 rounded-xl border-2 border-white/10 bg-white/[0.02] hover:bg-white/[0.05] hover:border-white/20 transition-all"
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center text-white/70">
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                </svg>
              </div>
              <h2 className="text-lg font-semibold text-white">
                Neu starten
              </h2>
            </div>
            <p className="text-sm text-white/60 leading-relaxed">
              Starten Sie ohne historische Daten. Der Plattform-Vergleich steht sofort zur Verfügung.
            </p>
          </button>
        </div>
      </div>
    </div>
  );
}

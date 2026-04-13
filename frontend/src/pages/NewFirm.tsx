import { useNavigate } from "react-router-dom";

const NEUER_FIRM_ID = "10000000-0000-0000-0000-000000000002";

export default function NewFirm() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#1F1B1C] flex items-center justify-center px-4">
      <div className="max-w-md w-full space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-2xl font-bold text-white">Neuer Betrieb</h1>
          <p className="text-white/50 text-sm">
            Keine historischen Daten? Kein Problem.
          </p>
        </div>

        <div className="space-y-4 p-6 rounded-xl bg-white/[0.03] border border-white/10">
          <div>
            <label className="block text-xs text-white/40 mb-1">Gewerk</label>
            <div className="px-3 py-2 rounded-lg bg-white/5 text-white/80 text-sm">SHK</div>
          </div>
          <div>
            <label className="block text-xs text-white/40 mb-1">Betriebsgröße</label>
            <div className="px-3 py-2 rounded-lg bg-white/5 text-white/80 text-sm">Mikro (1 Meister, 2 Gesellen)</div>
          </div>
          <div>
            <label className="block text-xs text-white/40 mb-1">Betriebsname</label>
            <div className="px-3 py-2 rounded-lg bg-white/5 text-white/80 text-sm">Neuer Betrieb</div>
          </div>
        </div>

        <button
          onClick={() => navigate(`/dashboard?firm=${NEUER_FIRM_ID}`)}
          className="w-full px-6 py-3 bg-amber-500 hover:bg-amber-400 text-[#1F1B1C] font-semibold rounded-lg transition-colors"
        >
          Betrieb anlegen
        </button>

        <button
          onClick={() => navigate("/")}
          className="w-full text-center text-sm text-white/30 hover:text-white/50 transition-colors"
        >
          Zurück
        </button>
      </div>
    </div>
  );
}

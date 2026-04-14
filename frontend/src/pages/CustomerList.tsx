import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getCustomers, type CustomerSummary } from "../api";
import AppLayout from "../components/AppLayout";
import { showPhase2Toast } from "../components/Phase2Toast";

const WEBER_FIRM_ID = "10000000-0000-0000-0000-000000000001";

const TYPE_LABELS: Record<string, string> = {
  residential: "Privat",
  commercial: "Gewerbe",
  public: "Öffentlich",
};

export default function CustomerList() {
  const [searchParams] = useSearchParams();
  const firmId = searchParams.get("firm") || WEBER_FIRM_ID;
  const [customers, setCustomers] = useState<CustomerSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCustomers(firmId).then((c) => {
      setCustomers(c);
      setLoading(false);
    });
  }, [firmId]);

  return (
    <AppLayout title="Kunden">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold">Kunden</h1>
          <button
            onClick={() => showPhase2Toast("Neuer Kunde — verfügbar in Phase 2.")}
            className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-[#1F1B1C] font-semibold rounded-lg text-sm transition-colors"
          >
            + Neuer Kunde
          </button>
        </div>

        {loading ? (
          <div className="text-white/50">Laden...</div>
        ) : customers.length === 0 ? (
          <div className="text-white/40 text-sm">Keine Kunden vorhanden.</div>
        ) : (
          <div className="rounded-lg border border-white/10 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/10 text-left text-xs text-white/40">
                  <th className="px-4 py-2">Name</th>
                  <th className="px-4 py-2">Typ</th>
                  <th className="px-4 py-2 text-right">Aktionen</th>
                </tr>
              </thead>
              <tbody>
                {customers.map((c) => (
                  <tr key={c.id} className="border-b border-white/5 hover:bg-white/[0.02]">
                    <td className="px-4 py-2.5 text-white/80">{c.name}</td>
                    <td className="px-4 py-2.5 text-white/50">{TYPE_LABELS[c.type] || c.type}</td>
                    <td className="px-4 py-2.5 text-right">
                      <div className="flex gap-2 justify-end">
                        <button
                          onClick={() => showPhase2Toast("Kundendetail — verfügbar in Phase 2.")}
                          className="px-2 py-1 bg-white/5 hover:bg-white/10 text-white/40 hover:text-white/70 rounded text-xs transition-colors"
                        >
                          Details
                        </button>
                        <button
                          onClick={() => showPhase2Toast("Kunde bearbeiten — verfügbar in Phase 2.")}
                          className="px-2 py-1 bg-white/5 hover:bg-white/10 text-white/40 hover:text-white/70 rounded text-xs transition-colors"
                        >
                          Bearbeiten
                        </button>
                        <button
                          onClick={() => showPhase2Toast("Kunde deaktivieren — verfügbar in Phase 2.")}
                          className="px-2 py-1 bg-white/5 hover:bg-red-500/10 text-white/40 hover:text-red-400/70 rounded text-xs transition-colors"
                        >
                          Deaktivieren
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </AppLayout>
  );
}

import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import {
  getDashboard,
  getFirmUsers,
  type DashboardData,
  type UserSummary,
} from "../api";

const WEBER_FIRM_ID = "10000000-0000-0000-0000-000000000001";
const NEUER_FIRM_ID = "10000000-0000-0000-0000-000000000002";

const ROLE_LABELS: Record<string, string> = {
  meister: "Meister",
  geselle: "Geselle",
  buero: "Bürokraft",
};

const STATUS_LABELS: Record<string, string> = {
  draft: "Entwurf",
  sent: "Gesendet",
  accepted: "Angenommen",
  rejected: "Abgelehnt",
  expired: "Abgelaufen",
  planned: "Geplant",
  active: "Aktiv",
  completed: "Abgeschlossen",
  cancelled: "Storniert",
};

function formatEUR(val: number | null): string {
  if (val === null) return "–";
  return new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(val);
}

function formatDate(iso: string | null): string {
  if (!iso) return "–";
  return new Date(iso).toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" });
}

function MarginBadge({ pct }: { pct: number | null }) {
  if (pct === null) return <span className="text-white/30">–</span>;
  const color = pct >= 25 ? "text-green-400 bg-green-400/10" : pct >= 18 ? "text-amber-400 bg-amber-400/10" : "text-red-400 bg-red-400/10";
  return <span className={`px-2 py-0.5 rounded text-xs font-medium ${color}`}>{pct.toFixed(0)}%</span>;
}

export default function Dashboard() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const firmId = searchParams.get("firm") || WEBER_FIRM_ID;
  const imported = searchParams.get("imported") === "true";

  const [data, setData] = useState<DashboardData | null>(null);
  const [users, setUsers] = useState<UserSummary[]>([]);
  const [activeUser, setActiveUser] = useState<UserSummary | null>(null);
  const [showBanner, setShowBanner] = useState(imported);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([getDashboard(firmId), getFirmUsers(firmId)]).then(([d, u]) => {
      setData(d);
      setUsers(u);
      setActiveUser(u.find((x) => x.role === "meister") || u[0] || null);
      setLoading(false);
    });
  }, [firmId]);

  if (loading || !data) {
    return (
      <div className="min-h-screen bg-[#1F1B1C] flex items-center justify-center">
        <div className="text-white/50">Laden...</div>
      </div>
    );
  }

  const isMeister = activeUser?.role === "meister";
  const isNewFirm = firmId === NEUER_FIRM_ID;

  return (
    <div className="min-h-screen bg-[#1F1B1C] text-white font-['Inter',sans-serif]">
      {/* Header */}
      <header className="border-b border-white/10 px-4 py-3">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={() => navigate("/")} className="text-lg font-semibold tracking-tight hover:text-amber-400 transition-colors">
              Workshop
            </button>
            <span className="text-white/20">|</span>
            <span className="text-sm text-white/50">{data.firm.name}</span>
          </div>

          {/* Role switcher */}
          {users.length > 0 && (
            <div className="flex items-center gap-1 bg-white/5 rounded-lg p-1">
              {users.map((u) => (
                <button
                  key={u.id}
                  onClick={() => setActiveUser(u)}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                    activeUser?.id === u.id
                      ? "bg-amber-500/20 text-amber-400"
                      : "text-white/40 hover:text-white/70"
                  }`}
                >
                  {ROLE_LABELS[u.role] || u.role}
                </button>
              ))}
            </div>
          )}
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6 space-y-6">
        {/* Import banner (E1-S4) */}
        {showBanner && !isNewFirm && (
          <div className="flex items-start justify-between gap-4 p-4 rounded-lg bg-amber-500/10 border border-amber-500/20">
            <div>
              <p className="text-sm font-medium text-amber-400">
                Diese Daten stammen aus Ihrem Taifun-Export.
              </p>
              <p className="text-xs text-white/50 mt-1">
                {data.counts.completed_projects} Projekte, {data.counts.customers} Kunden, {data.counts.positions} Positionen importiert.
              </p>
            </div>
            <button onClick={() => setShowBanner(false)} className="text-white/30 hover:text-white/60 shrink-0 mt-0.5">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        )}

        {/* Welcome for new firm */}
        {isNewFirm && (
          <div className="p-4 rounded-lg bg-teal-500/10 border border-teal-500/20">
            <p className="text-sm font-medium text-teal-400">
              Willkommen. Sie haben noch keine Projekte.
            </p>
            <p className="text-xs text-white/50 mt-1">
              Der Plattform-Vergleich steht Ihnen ab sofort zur Verfügung.
            </p>
          </div>
        )}

        {/* Summary cards */}
        <div className="grid grid-cols-3 gap-4">
          <SummaryCard label="Offene Angebote" value={data.counts.open_quotes} />
          <SummaryCard label="Aktive Projekte" value={data.counts.active_projects} />
          <SummaryCard label="Abgeschlossen" value={data.counts.completed_projects} />
        </div>

        {/* CL Insights (visible to Meister only) */}
        {isMeister && data.cl_insights.length > 0 && (
          <div className="p-4 rounded-lg bg-white/[0.03] border border-white/10 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-white/80">Ihr Betriebsvergleich</h3>
              {!isNewFirm && showBanner && (
                <span className="text-xs text-amber-400/60">Berechnet aus Ihren importierten Daten</span>
              )}
            </div>
            <div className="space-y-2">
              {data.cl_insights.map((insight) => (
                <div key={insight.job_type} className="flex items-center justify-between text-sm">
                  <span className="text-white/60">{insight.job_type}</span>
                  <div className="flex items-center gap-4 text-xs">
                    {insight.firm_median !== null && (
                      <span className="text-white/80">
                        Ihr Betrieb: <strong>Ø {insight.firm_median}h</strong>
                      </span>
                    )}
                    <span className="text-white/40">
                      Plattform: Ø {insight.platform_median}h
                      <span className="text-white/20 ml-1">(n={insight.platform_sample_size})</span>
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* New Quote CTA */}
        <button
          onClick={() => navigate(`/quote/new?firm=${firmId}`)}
          className="w-full sm:w-auto px-6 py-3 bg-amber-500 hover:bg-amber-400 text-[#1F1B1C] font-semibold rounded-lg transition-colors"
        >
          + Neues Angebot
        </button>

        {/* Recent Quotes */}
        {data.recent_quotes.length > 0 && (
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-white/60">Angebote</h3>
            <div className="rounded-lg border border-white/10 overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/10 text-left text-xs text-white/40">
                    <th className="px-4 py-2">Kunde</th>
                    <th className="px-4 py-2">Auftragstyp</th>
                    <th className="px-4 py-2">Status</th>
                    {isMeister && <th className="px-4 py-2 text-right">Netto</th>}
                    <th className="px-4 py-2 text-right">Datum</th>
                  </tr>
                </thead>
                <tbody>
                  {data.recent_quotes.map((q) => (
                    <tr key={q.id} className="border-b border-white/5 hover:bg-white/[0.02]">
                      <td className="px-4 py-2.5 text-white/80">{q.customer_name}</td>
                      <td className="px-4 py-2.5 text-white/50">{q.job_type}</td>
                      <td className="px-4 py-2.5">
                        <span className="text-xs px-2 py-0.5 rounded bg-white/5 text-white/50">
                          {STATUS_LABELS[q.status] || q.status}
                          {imported && !isNewFirm && (
                            <span className="ml-1.5 text-amber-400/60">Importiert</span>
                          )}
                        </span>
                      </td>
                      {isMeister && <td className="px-4 py-2.5 text-right text-white/60">{formatEUR(q.total_net)}</td>}
                      <td className="px-4 py-2.5 text-right text-white/40">{formatDate(q.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Recent Projects */}
        {data.recent_projects.length > 0 && (
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-white/60">Projekte</h3>
            <div className="rounded-lg border border-white/10 overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/10 text-left text-xs text-white/40">
                    <th className="px-4 py-2">Kunde</th>
                    <th className="px-4 py-2">Auftragstyp</th>
                    <th className="px-4 py-2">Status</th>
                    <th className="px-4 py-2 text-right">Stunden (Plan/Ist)</th>
                    {isMeister && <th className="px-4 py-2 text-right">Marge</th>}
                  </tr>
                </thead>
                <tbody>
                  {data.recent_projects.map((p) => (
                    <tr
                      key={p.id}
                      onClick={() => navigate(`/project/${p.id}?firm=${firmId}`)}
                      className="border-b border-white/5 hover:bg-white/[0.02] cursor-pointer"
                    >
                      <td className="px-4 py-2.5 text-white/80">{p.customer_name}</td>
                      <td className="px-4 py-2.5 text-white/50">{p.job_type}</td>
                      <td className="px-4 py-2.5">
                        <span className="text-xs px-2 py-0.5 rounded bg-white/5 text-white/50">
                          {STATUS_LABELS[p.status] || p.status}
                        </span>
                      </td>
                      <td className="px-4 py-2.5 text-right text-white/50">
                        {p.planned_hours ?? "–"} / {p.actual_hours ?? "–"}
                      </td>
                      {isMeister && (
                        <td className="px-4 py-2.5 text-right">
                          <MarginBadge pct={p.margin_pct} />
                        </td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

function SummaryCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="p-4 rounded-lg bg-white/[0.03] border border-white/10">
      <div className="text-2xl font-bold text-white">{value}</div>
      <div className="text-xs text-white/40 mt-1">{label}</div>
    </div>
  );
}

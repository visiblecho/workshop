import { useEffect, useState } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import { getProject, getEvents, type ProjectDetail as ProjectDetailData, type EventRecord } from "../api";

const STATUS_LABELS: Record<string, string> = {
  planned: "Geplant", active: "Aktiv", completed: "Abgeschlossen", cancelled: "Storniert",
};
const STATUS_LABELS_LOWER: Record<string, string> = {
  draft: "Entwurf", sent: "Gesendet", accepted: "Angenommen",
  planned: "Geplant", active: "Aktiv", completed: "Abgeschlossen",
};
const ROLE_LABELS: Record<string, string> = {
  meister: "Meister", geselle: "Geselle", buero: "Bürokraft",
};

function formatEUR(val: number): string {
  return new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(val);
}

function formatDateTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("de-DE", { day: "2-digit", month: "short", year: "numeric" }) +
    ", " + d.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" });
}

function DeltaText({ quoted, actual, unit, currency }: { quoted: number; actual: number; unit?: string; currency?: boolean }) {
  const diff = actual - quoted;
  const pct = quoted > 0 ? (diff / quoted) * 100 : 0;
  const isOver = diff > 0;
  const sign = isOver ? "+" : "";
  const diffStr = currency
    ? `${sign}${formatEUR(Math.abs(diff))}`
    : `${sign}${diff.toFixed(diff % 1 === 0 ? 0 : 1)}${unit ? ` ${unit}` : ""}`;
  return (
    <span className={`font-medium ${isOver ? "text-red-400" : "text-green-400"}`}>
      {diffStr} ({sign}{pct.toFixed(0)}%)
    </span>
  );
}

export default function ProjectDetailPage() {
  const { projectId } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const firmId = searchParams.get("firm") || "";

  const [project, setProject] = useState<ProjectDetailData | null>(null);
  const [events, setEvents] = useState<EventRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!projectId) return;
    Promise.all([
      getProject(projectId),
      getEvents("project", projectId),
    ]).then(([p, e]) => {
      setProject(p);
      setEvents(e);
      setLoading(false);
    });
  }, [projectId]);

  if (loading || !project) {
    return (
      <div className="min-h-screen bg-[#1F1B1C] flex items-center justify-center">
        <div className="text-white/50">Laden...</div>
      </div>
    );
  }

  const laborItems = project.line_items.filter((li) => li.category === "labor");
  const materialItems = project.line_items.filter((li) => li.category !== "labor");

  const totalQuoted = project.line_items.reduce((s, li) => s + (li.quoted?.total ?? 0), 0);
  const totalActual = project.line_items.reduce((s, li) => s + li.actual_total, 0);

  const laborQuoted = laborItems.reduce((s, li) => s + (li.quoted?.total ?? 0), 0);
  const laborActual = laborItems.reduce((s, li) => s + li.actual_total, 0);
  const materialQuoted = materialItems.reduce((s, li) => s + (li.quoted?.total ?? 0), 0);
  const materialActual = materialItems.reduce((s, li) => s + li.actual_total, 0);

  return (
    <div className="min-h-screen bg-[#1F1B1C] text-white">
      <header className="border-b border-white/10 px-4 py-3">
        <div className="max-w-5xl mx-auto flex items-center gap-3">
          <button onClick={() => navigate(`/dashboard?firm=${firmId}`)} className="text-lg font-semibold tracking-tight hover:text-amber-400 transition-colors">
            Workshop
          </button>
          <span className="text-white/20">|</span>
          <span className="text-sm text-white/50">Projektdetail</span>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6 space-y-6">
        {/* Project header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <div>
            <h2 className="text-xl font-bold">{project.job_type}</h2>
            <p className="text-sm text-white/50">{project.customer_name}</p>
          </div>
          <div className="flex items-center gap-3">
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
              project.status === "completed" ? "bg-green-500/10 text-green-400" :
              project.status === "active" ? "bg-amber-500/10 text-amber-400" :
              "bg-white/5 text-white/50"
            }`}>
              {STATUS_LABELS[project.status]}
            </span>
          </div>
        </div>

        {/* ===== Section 1: Arbeitszeit (Labor time) ===== */}
        <div className="p-4 rounded-lg bg-white/[0.03] border border-white/10 space-y-4">
          <h3 className="text-sm font-semibold text-white/80">Arbeitszeit</h3>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <StatCard label="Kalkuliert" value={project.planned_hours ? `${project.planned_hours}h` : "–"} />
            <StatCard label="Tatsächlich" value={project.actual_hours ? `${project.actual_hours}h` : "–"} />
            <StatCard
              label="Abweichung"
              value={project.planned_hours && project.actual_hours
                ? <DeltaText quoted={project.planned_hours} actual={project.actual_hours} unit="h" />
                : "–"
              }
            />
            <StatCard
              label="Plattform-Vergleich"
              value={project.cl_benchmark_duration ? `Ø ${project.cl_benchmark_duration}h` : "–"}
              sub={project.cl_sample_size ? `(${project.cl_sample_size} Betriebe)` : undefined}
            />
          </div>

          {/* Firm vs platform context */}
          {project.firm_benchmark_duration && project.cl_benchmark_duration && (
            <div className="text-xs text-white/40 pt-2 border-t border-white/5">
              Ihr Durchschnitt bei {project.job_type}: Ø {project.firm_benchmark_duration}h · Plattform: Ø {project.cl_benchmark_duration}h
            </div>
          )}
        </div>

        {/* ===== Section 2: Kosten (Costs) ===== */}
        <div className="p-4 rounded-lg bg-white/[0.03] border border-white/10 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white/80">Kosten — Kalkuliert vs. Tatsächlich</h3>
            {project.margin_pct !== null && (
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                project.margin_pct >= 25 ? "bg-green-500/10 text-green-400" :
                project.margin_pct >= 18 ? "bg-amber-500/10 text-amber-400" :
                "bg-red-500/10 text-red-400"
              }`}>
                Marge: {project.margin_pct.toFixed(0)}%
              </span>
            )}
          </div>

          {/* Summary row */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <StatCard label="Kalkuliert gesamt" value={formatEUR(totalQuoted)} />
            <StatCard label="Tatsächlich gesamt" value={formatEUR(totalActual)} />
            <StatCard
              label="Differenz"
              value={totalQuoted > 0 ? <DeltaText quoted={totalQuoted} actual={totalActual} currency /> : "–"}
            />
          </div>

          {/* Breakdown: labor vs material */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-white/5">
            <div className="text-sm">
              <div className="text-white/40 text-xs mb-1">Arbeit</div>
              <div className="flex justify-between">
                <span className="text-white/50">{formatEUR(laborQuoted)}</span>
                <span className="text-white/30">→</span>
                <span className="text-white/80">{formatEUR(laborActual)}</span>
                {laborQuoted > 0 && <DeltaText quoted={laborQuoted} actual={laborActual} currency />}
              </div>
            </div>
            <div className="text-sm">
              <div className="text-white/40 text-xs mb-1">Material</div>
              <div className="flex justify-between">
                <span className="text-white/50">{formatEUR(materialQuoted)}</span>
                <span className="text-white/30">→</span>
                <span className="text-white/80">{formatEUR(materialActual)}</span>
                {materialQuoted > 0 && <DeltaText quoted={materialQuoted} actual={materialActual} currency />}
              </div>
            </div>
          </div>

          {/* Detailed line items */}
          <details className="pt-2 border-t border-white/5">
            <summary className="text-xs text-white/40 cursor-pointer hover:text-white/60">
              Einzelpositionen anzeigen
            </summary>
            <div className="mt-2 rounded-lg border border-white/5 overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/5 text-left text-xs text-white/30">
                    <th className="px-3 py-1.5">Position</th>
                    <th className="px-3 py-1.5 text-right">Kalkuliert</th>
                    <th className="px-3 py-1.5 text-right">Tatsächlich</th>
                    <th className="px-3 py-1.5 text-right">Δ</th>
                  </tr>
                </thead>
                <tbody>
                  {project.line_items.map((li) => {
                    const quoted = li.quoted?.total ?? 0;
                    return (
                      <tr key={li.id} className="border-b border-white/[0.03]">
                        <td className="px-3 py-1.5">
                          <span className="text-white/60">{li.description}</span>
                          {li.notes && <span className="text-xs text-amber-400/60 ml-2">{li.notes}</span>}
                        </td>
                        <td className="px-3 py-1.5 text-right text-white/30">{li.quoted ? formatEUR(quoted) : "–"}</td>
                        <td className="px-3 py-1.5 text-right text-white/60">{formatEUR(li.actual_total)}</td>
                        <td className="px-3 py-1.5 text-right">
                          {li.quoted && quoted > 0 ? <DeltaText quoted={quoted} actual={li.actual_total} currency /> : "–"}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </details>
        </div>

        {/* Learning signal */}
        {project.status === "completed" && project.planned_hours && project.actual_hours && (
          (() => {
            const hoursDelta = ((project.actual_hours! - project.planned_hours!) / project.planned_hours!) * 100;
            const costDelta = totalQuoted > 0 ? ((totalActual - totalQuoted) / totalQuoted) * 100 : 0;
            if (hoursDelta <= 5 && costDelta <= 5) return null;
            return (
              <div className="p-4 rounded-lg bg-amber-500/5 border border-amber-500/20">
                <p className="text-sm text-amber-400/90">
                  {hoursDelta > 5 && <>Arbeitszeit lag {hoursDelta.toFixed(0)}% über der Kalkulation. </>}
                  {costDelta > 5 && <>Kosten lagen {costDelta.toFixed(0)}% über dem Angebot. </>}
                  Bei Ihrem nächsten {project.job_type}-Angebot wird dieser Erfahrungswert berücksichtigt.
                </p>
              </div>
            );
          })()
        )}

        {/* Event trail */}
        {events.length > 0 && (
          <details>
            <summary className="text-sm font-semibold text-white/60 cursor-pointer hover:text-white/80">
              Änderungsverlauf ({events.length})
            </summary>
            <div className="mt-2 space-y-1">
              {events.map((evt) => (
                <div key={evt.id} className="flex items-start gap-3 px-4 py-2 rounded-lg bg-white/[0.02]">
                  <div className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${
                    evt.event_type === "status_changed" ? "bg-amber-400" :
                    evt.event_type === "updated" ? "bg-blue-400" : "bg-white/20"
                  }`} />
                  <div className="min-w-0">
                    <div className="text-xs text-white/60">
                      <span className="text-white/80">{evt.actor_name}</span>
                      <span className="text-white/30 ml-1">({ROLE_LABELS[evt.actor_role]})</span>
                      <span className="text-white/20 mx-1">·</span>
                      <span>{formatDateTime(evt.created_at)}</span>
                    </div>
                    <div className="text-xs text-white/40 mt-0.5">
                      {formatEventPayload(evt)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </details>
        )}

        <button
          onClick={() => navigate(`/dashboard?firm=${firmId}`)}
          className="px-4 py-2 bg-white/5 hover:bg-white/10 text-white/60 rounded-lg text-sm transition-colors"
        >
          Zurück zum Dashboard
        </button>
      </main>
    </div>
  );
}

function StatCard({ label, value, sub }: { label: string; value: React.ReactNode; sub?: string }) {
  return (
    <div className="p-3 rounded-lg bg-white/[0.02]">
      <div className="text-lg font-bold text-white">{value}</div>
      <div className="text-xs text-white/40 mt-0.5">{label}</div>
      {sub && <div className="text-xs text-white/20">{sub}</div>}
    </div>
  );
}

function formatEventPayload(evt: EventRecord): string {
  const p = evt.payload;
  if (evt.event_type === "status_changed" && p.status) {
    const s = p.status as { old: string; new: string };
    return `Status: ${STATUS_LABELS_LOWER[s.old] || s.old} → ${STATUS_LABELS_LOWER[s.new] || s.new}`;
  }
  if (evt.event_type === "created") return "Erstellt";
  if (evt.event_type === "updated") {
    const parts: string[] = [];
    for (const [key, val] of Object.entries(p)) {
      if (typeof val === "object" && val && "old" in val && "new" in val) {
        parts.push(`${key}: ${(val as any).old} → ${(val as any).new}`);
      }
    }
    return parts.join(", ") || "Geändert";
  }
  return evt.event_type;
}

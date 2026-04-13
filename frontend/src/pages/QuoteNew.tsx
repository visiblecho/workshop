import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import {
  getCustomers,
  getJobTypes,
  generateQuote,
  getBenchmarks,
  getArticlePriceHistory,
  type CustomerSummary,
  type JobTypeSummary,
  type GenerateQuoteResponse,
  type BenchmarkData,
  type PriceHistoryRecord,
} from "../api";

const UNIT_LABELS: Record<string, string> = {
  hours: "Std", pieces: "Stk", meters: "m", kg: "kg",
  liters: "L", sqm: "m²", flat_rate: "pauschal",
};

const CATEGORY_LABELS: Record<string, string> = {
  labor: "Arbeit", material: "Material", other: "Sonstig",
};

function formatEUR(val: number): string {
  return new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(val);
}

export default function QuoteNew() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const firmId = searchParams.get("firm") || "";

  const [customers, setCustomers] = useState<CustomerSummary[]>([]);
  const [jobTypes, setJobTypes] = useState<JobTypeSummary[]>([]);
  const [customerId, setCustomerId] = useState("");
  const [jobTypeId, setJobTypeId] = useState("");
  const [description, setDescription] = useState("");
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<GenerateQuoteResponse | null>(null);
  const [benchmarks, setBenchmarks] = useState<BenchmarkData | null>(null);
  const [priceAlerts, setPriceAlerts] = useState<Record<string, { pct: number; current: number; previous: number }>>({});

  // Speech recognition
  const [listening, setListening] = useState(false);
  const [speechSupported] = useState(() =>
    typeof window !== "undefined" && ("SpeechRecognition" in window || "webkitSpeechRecognition" in window)
  );

  useEffect(() => {
    if (!firmId) return;
    Promise.all([getCustomers(firmId), getJobTypes(firmId)]).then(([c, j]) => {
      setCustomers(c);
      setJobTypes(j);
      if (c.length) setCustomerId(c[0].id);
      if (j.length) setJobTypeId(j[0].id);
    });
  }, [firmId]);

  async function handleGenerate() {
    if (!customerId || !jobTypeId || !description.trim()) return;
    setGenerating(true);
    setError(null);
    setResult(null);
    setBenchmarks(null);

    // Hardcode meister as creator
    const createdBy = "20000000-0000-0000-0000-000000000001";

    try {
      const [quoteRes, benchRes] = await Promise.all([
        generateQuote({ firm_id: firmId, customer_id: customerId, job_type_id: jobTypeId, description, created_by: createdBy }),
        getBenchmarks(jobTypeId, firmId),
      ]);
      setResult(quoteRes);
      setBenchmarks(benchRes);

      // Fetch price history for articles in the quote
      const articleIds = quoteRes.line_items
        .map((li) => li.article_id)
        .filter((id): id is string => !!id);
      const uniqueIds = [...new Set(articleIds)];

      const alerts: Record<string, { pct: number; current: number; previous: number }> = {};
      await Promise.all(
        uniqueIds.map(async (artId) => {
          const history = await getArticlePriceHistory(artId);
          if (history.length >= 2) {
            const current = history[0].price;
            const prev = history[1].price;
            const pct = ((current - prev) / prev) * 100;
            if (Math.abs(pct) > 2) {
              alerts[artId] = { pct: Math.round(pct * 10) / 10, current, previous: prev };
            }
          }
        })
      );
      setPriceAlerts(alerts);
    } catch (e) {
      setError("Angebot konnte nicht erstellt werden. Bitte versuchen Sie es erneut.");
      console.error("Quote generation failed:", e);
    } finally {
      setGenerating(false);
    }
  }

  function toggleSpeech() {
    if (!speechSupported) return;
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (listening) {
      setListening(false);
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = "de-DE";
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.onresult = (event: any) => {
      let transcript = "";
      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      setDescription(transcript);
    };
    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);
    recognition.start();
    setListening(true);
    // Store for cleanup
    (window as any).__recognition = recognition;
  }

  // Cleanup speech on unmount
  useEffect(() => {
    return () => {
      if ((window as any).__recognition) {
        (window as any).__recognition.stop();
      }
    };
  }, []);

  const totalNet = result?.total_net ?? 0;
  const mwst = totalNet * 0.19;
  const totalGross = totalNet + mwst;

  // Margin forecast
  const firmMargin = benchmarks?.firm_benchmarks?.margin_pct?.p50;
  const clMargin = benchmarks?.cl_benchmarks?.margin_pct?.p50;
  const firmDuration = benchmarks?.firm_benchmarks?.duration_h?.p50;
  const clDuration = benchmarks?.cl_benchmarks?.duration_h?.p50;
  const clQuoteTotal = benchmarks?.cl_benchmarks?.quote_total?.p50;
  const clSampleSize = benchmarks?.cl_benchmarks?.duration_h?.sample_size;

  // Estimate margin from CL data
  let estimatedMargin: number | null = null;
  if (result && clMargin !== undefined) {
    // Use firm margin if available, otherwise platform
    estimatedMargin = firmMargin ?? clMargin;
  }

  return (
    <div className="min-h-screen bg-[#1F1B1C] text-white font-['Inter',sans-serif]">
      <header className="border-b border-white/10 px-4 py-3">
        <div className="max-w-5xl mx-auto flex items-center gap-3">
          <button onClick={() => navigate(`/dashboard?firm=${firmId}`)} className="text-lg font-semibold tracking-tight hover:text-amber-400 transition-colors">
            Workshop
          </button>
          <span className="text-white/20">|</span>
          <span className="text-sm text-white/50">Neues Angebot</span>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6 space-y-6">
        {/* Input form */}
        {!result && (
          <div className="space-y-4 max-w-2xl">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs text-white/40 mb-1">Kunde</label>
                <select
                  value={customerId}
                  onChange={(e) => setCustomerId(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:border-amber-500/50 focus:outline-none"
                >
                  {customers.map((c) => (
                    <option key={c.id} value={c.id} className="bg-[#1F1B1C]">{c.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs text-white/40 mb-1">Auftragstyp</label>
                <select
                  value={jobTypeId}
                  onChange={(e) => setJobTypeId(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm focus:border-amber-500/50 focus:outline-none"
                >
                  {jobTypes.map((j) => (
                    <option key={j.id} value={j.id} className="bg-[#1F1B1C]">{j.name}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs text-white/40 mb-1">Auftragsbeschreibung</label>
              <div className="relative">
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={4}
                  placeholder="Heizungstausch Einfamilienhaus, Altbau 1965, Keller, 24kW Gasbrennwert raus, Wärmepumpe rein..."
                  className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm placeholder:text-white/20 focus:border-amber-500/50 focus:outline-none resize-none"
                />
                {speechSupported && (
                  <button
                    onClick={toggleSpeech}
                    className={`absolute right-2 bottom-2 w-9 h-9 rounded-full flex items-center justify-center transition-colors ${
                      listening
                        ? "bg-red-500/20 text-red-400 animate-pulse"
                        : "bg-white/5 text-white/30 hover:text-white/60"
                    }`}
                    title={listening ? "Aufnahme stoppen" : "Spracheingabe"}
                  >
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5zm6 6c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                    </svg>
                  </button>
                )}
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleGenerate}
                disabled={generating || !description.trim()}
                className="px-6 py-3 bg-amber-500 hover:bg-amber-400 disabled:bg-white/10 disabled:text-white/30 text-[#1F1B1C] font-semibold rounded-lg transition-colors"
              >
                {generating ? "Angebot wird erstellt..." : "Angebot erstellen"}
              </button>
              <button
                onClick={() => navigate(`/dashboard?firm=${firmId}`)}
                className="px-4 py-3 bg-white/5 hover:bg-white/10 text-white/60 rounded-lg text-sm transition-colors"
              >
                Abbrechen
              </button>
            </div>

            {error && (
              <div className="px-3 py-2 rounded-lg bg-red-500/10 border border-red-500/20 text-sm text-red-400">
                {error}
              </div>
            )}

            {generating && (
              <div className="flex items-center gap-3 text-sm text-white/50">
                <div className="w-5 h-5 border-2 border-amber-400 border-t-transparent rounded-full animate-spin" />
                KI erstellt Ihr Leistungsverzeichnis...
              </div>
            )}
          </div>
        )}

        {/* Quote result */}
        {result && (
          <div className="space-y-6">
            {result.is_fallback && (
              <div className="px-3 py-2 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-400">
                Demo-Modus: Beispielangebot geladen
              </div>
            )}

            {/* Line items table */}
            <div className="rounded-lg border border-white/10 overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/10 text-left text-xs text-white/40">
                    <th className="px-4 py-2 w-12">#</th>
                    <th className="px-4 py-2">Beschreibung</th>
                    <th className="px-4 py-2">Typ</th>
                    <th className="px-4 py-2 text-right">Menge</th>
                    <th className="px-4 py-2 text-right">Einheit</th>
                    <th className="px-4 py-2 text-right">EP</th>
                    <th className="px-4 py-2 text-right">Gesamt</th>
                  </tr>
                </thead>
                <tbody>
                  {result.line_items.map((li) => (
                    <tr key={li.id} className="border-b border-white/5">
                      <td className="px-4 py-2.5 text-white/30">{li.position}</td>
                      <td className="px-4 py-2.5 text-white/80">
                        {li.description}
                        {li.article_id && priceAlerts[li.article_id] && (
                          <span className={`ml-2 text-xs px-1.5 py-0.5 rounded ${
                            priceAlerts[li.article_id].pct > 0
                              ? "bg-red-500/10 text-red-400"
                              : "bg-green-500/10 text-green-400"
                          }`}>
                            {priceAlerts[li.article_id].pct > 0 ? "↑" : "↓"} {Math.abs(priceAlerts[li.article_id].pct)}% (30 Tage)
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-2.5 text-white/40">{CATEGORY_LABELS[li.category]}</td>
                      <td className="px-4 py-2.5 text-right text-white/60">{li.quantity}</td>
                      <td className="px-4 py-2.5 text-right text-white/40">{UNIT_LABELS[li.unit] || li.unit}</td>
                      <td className="px-4 py-2.5 text-right text-white/60">{formatEUR(li.unit_price)}</td>
                      <td className="px-4 py-2.5 text-right text-white/80">{formatEUR(li.total)}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr className="border-t border-white/10">
                    <td colSpan={6} className="px-4 py-2 text-right text-white/40">Netto</td>
                    <td className="px-4 py-2 text-right font-medium">{formatEUR(totalNet)}</td>
                  </tr>
                  <tr>
                    <td colSpan={6} className="px-4 py-1.5 text-right text-white/30 text-xs">MwSt. 19%</td>
                    <td className="px-4 py-1.5 text-right text-white/40 text-xs">{formatEUR(mwst)}</td>
                  </tr>
                  <tr className="border-t border-white/10">
                    <td colSpan={6} className="px-4 py-2 text-right font-semibold">Brutto</td>
                    <td className="px-4 py-2 text-right font-bold text-amber-400">{formatEUR(totalGross)}</td>
                  </tr>
                </tfoot>
              </table>
            </div>

            {/* CL Overlay Panel */}
            {benchmarks && (
              <div className="p-4 rounded-lg bg-white/[0.03] border border-white/10 space-y-4">
                <h3 className="text-sm font-semibold text-white/80">Crowd Learning — Ihr Vergleich</h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Firm benchmark */}
                  {Object.keys(benchmarks.firm_benchmarks).length > 0 && (
                    <div className="space-y-2">
                      <div className="text-xs text-white/40">Ihr Betrieb (letzte 12 Monate)</div>
                      {firmDuration !== undefined && (
                        <MetricRow label="Ø Dauer" value={`${firmDuration}h`} />
                      )}
                      {firmMargin !== undefined && (
                        <MetricRow label="Ø Marge" value={`${firmMargin}%`} />
                      )}
                    </div>
                  )}

                  {/* Platform benchmark */}
                  <div className="space-y-2">
                    <div className="text-xs text-white/40">
                      Plattform ({clSampleSize ? `${clSampleSize} Betriebe` : "–"})
                    </div>
                    {clDuration !== undefined && (
                      <MetricRow label="Ø Dauer" value={`${clDuration}h`} />
                    )}
                    {clMargin !== undefined && (
                      <MetricRow label="Ø Marge" value={`${clMargin}%`} />
                    )}
                    {clQuoteTotal !== undefined && (
                      <MetricRow label="Ø Angebotssumme" value={formatEUR(clQuoteTotal)} />
                    )}
                  </div>
                </div>

                {/* Margin forecast */}
                {estimatedMargin !== null && (
                  <div className="pt-3 border-t border-white/5">
                    <div className="text-sm">
                      <span className="text-white/50">Bei diesen Preisen: erwartete Marge </span>
                      <span className={`font-semibold ${
                        estimatedMargin >= 25 ? "text-green-400" : estimatedMargin >= 20 ? "text-amber-400" : "text-red-400"
                      }`}>
                        {estimatedMargin}%
                      </span>
                      <span className="text-white/30 ml-2">Ziel: 25% · Plattform: {clMargin}%</span>
                    </div>
                  </div>
                )}

                {Object.keys(benchmarks.firm_benchmarks).length === 0 && (
                  <p className="text-xs text-white/30">
                    Keine Betriebsdaten für diesen Auftragstyp. Plattform-Vergleich verfügbar.
                  </p>
                )}
              </div>
            )}

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={() => {
                  setResult(null);
                  setBenchmarks(null);
                  setPriceAlerts({});
                  setDescription("");
                }}
                className="px-4 py-2 bg-white/5 hover:bg-white/10 text-white/60 rounded-lg text-sm transition-colors"
              >
                Neues Angebot
              </button>
              <button
                onClick={() => navigate(`/dashboard?firm=${firmId}`)}
                className="px-4 py-2 bg-white/5 hover:bg-white/10 text-white/60 rounded-lg text-sm transition-colors"
              >
                Zurück zum Dashboard
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

function MetricRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between text-sm">
      <span className="text-white/50">{label}</span>
      <span className="text-white/80 font-medium">{value}</span>
    </div>
  );
}

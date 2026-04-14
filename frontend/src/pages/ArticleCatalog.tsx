import { useState } from "react";
import AppLayout from "../components/AppLayout";
import { showPhase2Toast } from "../components/Phase2Toast";

// Static article data for the shell — matches seed data structure
const SAMPLE_ARTICLES = [
  { id: "1", name: "Viessmann Vitocal 250-A Wärmepumpe", datanorm: "VIT-250A", unit: "Stk", price: 8500 },
  { id: "2", name: "Kupferrohr 22mm (pro Meter)", datanorm: "CU-22-M", unit: "m", price: 12.50 },
  { id: "3", name: "Fußbodenheizung Rohr 16mm", datanorm: "FBH-16", unit: "m", price: 3.20 },
  { id: "4", name: "Heizkörper Typ 22, 600x1000mm", datanorm: "HK-22-600", unit: "Stk", price: 320 },
  { id: "5", name: "Monteurstunde", datanorm: "ARB-STD", unit: "Std", price: 62 },
  { id: "6", name: "Meisterstunde", datanorm: "ARB-MST", unit: "Std", price: 78 },
  { id: "7", name: "Pressfitting 22mm T-Stück", datanorm: "PF-22-T", unit: "Stk", price: 8.90 },
  { id: "8", name: "Isolierung Rohrleitungen 22mm", datanorm: "ISO-22", unit: "m", price: 4.50 },
];

function formatEUR(val: number): string {
  return new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(val);
}

export default function ArticleCatalog() {
  const [search, setSearch] = useState("");

  const filtered = SAMPLE_ARTICLES.filter(
    (a) =>
      a.name.toLowerCase().includes(search.toLowerCase()) ||
      a.datanorm.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <AppLayout title="Artikelkatalog">
      <div className="space-y-6">
        <div className="flex items-center justify-between gap-4">
          <h1 className="text-xl font-bold">Artikelkatalog</h1>
          <button
            onClick={() => showPhase2Toast("Artikel hinzufügen — verfügbar in Phase 2.")}
            className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-[#1F1B1C] font-semibold rounded-lg text-sm transition-colors shrink-0"
          >
            + Artikel hinzufügen
          </button>
        </div>

        {/* Search */}
        <input
          type="text"
          placeholder="Artikel suchen (Name oder DATANORM-Nr.)..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full max-w-md px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-white text-sm placeholder:text-white/20 focus:border-amber-500/50 focus:outline-none"
        />

        {/* Table */}
        <div className="rounded-lg border border-white/10 overflow-x-auto">
          <table className="w-full text-sm min-w-[500px]">
            <thead>
              <tr className="border-b border-white/10 text-left text-xs text-white/40">
                <th className="px-4 py-2">DATANORM</th>
                <th className="px-4 py-2">Bezeichnung</th>
                <th className="px-4 py-2">Einheit</th>
                <th className="px-4 py-2 text-right">Listenpreis</th>
                <th className="px-4 py-2 text-right">Aktionen</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((a) => (
                <tr key={a.id} className="border-b border-white/5 hover:bg-white/[0.02]">
                  <td className="px-4 py-2.5 text-white/40 font-mono text-xs">{a.datanorm}</td>
                  <td className="px-4 py-2.5 text-white/80">{a.name}</td>
                  <td className="px-4 py-2.5 text-white/50">{a.unit}</td>
                  <td className="px-4 py-2.5 text-right text-white/60">{formatEUR(a.price)}</td>
                  <td className="px-4 py-2.5 text-right">
                    <div className="flex gap-2 justify-end">
                      <button
                        onClick={() => showPhase2Toast("Preis anpassen — verfügbar in Phase 2.")}
                        className="px-2 py-1 bg-white/5 hover:bg-white/10 text-white/40 hover:text-white/70 rounded text-xs transition-colors"
                      >
                        Preis anpassen
                      </button>
                      <button
                        onClick={() => showPhase2Toast("Artikel deaktivieren — verfügbar in Phase 2.")}
                        className="px-2 py-1 bg-white/5 hover:bg-red-500/10 text-white/40 hover:text-red-400/70 rounded text-xs transition-colors"
                      >
                        Deaktivieren
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-6 text-center text-white/30">
                    Kein Artikel gefunden.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <p className="text-xs text-white/20">
          {SAMPLE_ARTICLES.length} Artikel im Katalog (Demo-Daten)
        </p>
      </div>
    </AppLayout>
  );
}

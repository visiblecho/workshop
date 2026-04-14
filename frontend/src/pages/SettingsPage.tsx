import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getDashboard, type DashboardData } from "../api";
import AppLayout from "../components/AppLayout";
import { showPhase2Toast } from "../components/Phase2Toast";

const WEBER_FIRM_ID = "10000000-0000-0000-0000-000000000001";

export default function SettingsPage() {
  const [searchParams] = useSearchParams();
  const firmId = searchParams.get("firm") || WEBER_FIRM_ID;
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    getDashboard(firmId).then(setData);
  }, [firmId]);

  return (
    <AppLayout title="Einstellungen">
      <div className="space-y-6 max-w-2xl">
        <h1 className="text-xl font-bold">Einstellungen</h1>

        {/* Firm profile */}
        <div className="p-4 rounded-lg bg-white/[0.03] border border-white/10 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-white/80">Firmenprofil</h2>
            <button
              onClick={() => showPhase2Toast("Firmendaten bearbeiten — verfügbar in Phase 2.")}
              className="px-3 py-1.5 bg-white/5 hover:bg-white/10 text-white/50 hover:text-white/70 rounded-lg text-xs transition-colors"
            >
              Bearbeiten
            </button>
          </div>
          {data ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
              <Field label="Firmenname" value={data.firm.name} />
              <Field label="Segment" value={data.firm.segment} />
              <Field label="Region" value={data.firm.region} />
              <Field label="Bankverbindung" value="•••• •••• •••• 4821" />
              <Field label="Steuernummer" value="123/456/78901" />
              <Field label="USt-IdNr." value="DE123456789" />
            </div>
          ) : (
            <div className="text-white/50 text-sm">Laden...</div>
          )}
        </div>

        {/* Integrations */}
        <div className="p-4 rounded-lg bg-white/[0.03] border border-white/10 space-y-4">
          <h2 className="text-sm font-semibold text-white/80">Schnittstellen</h2>
          <div className="space-y-2">
            <IntegrationRow
              name="DATEV-Export"
              description="Buchungen automatisch an DATEV übertragen"
              onClick={() => showPhase2Toast("DATEV-Schnittstelle — verfügbar in Phase 2.")}
            />
            <IntegrationRow
              name="Großhandel (DATANORM)"
              description="Artikelkatalog und Preise synchronisieren"
              onClick={() => showPhase2Toast("DATANORM-Schnittstelle — verfügbar in Phase 2.")}
            />
            <IntegrationRow
              name="ZUGFeRD / XRechnung"
              description="E-Rechnungen im Standard-Format"
              onClick={() => showPhase2Toast("E-Rechnung — verfügbar in Phase 2.")}
            />
          </div>
        </div>

        {/* Users */}
        <div className="p-4 rounded-lg bg-white/[0.03] border border-white/10 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-white/80">Benutzer</h2>
            <button
              onClick={() => showPhase2Toast("Benutzer hinzufügen — verfügbar in Phase 2.")}
              className="px-3 py-1.5 bg-white/5 hover:bg-white/10 text-white/50 hover:text-white/70 rounded-lg text-xs transition-colors"
            >
              + Benutzer
            </button>
          </div>
          <p className="text-xs text-white/30">
            Benutzerverwaltung mit Rollen und Zugriffsrechten.
          </p>
        </div>
      </div>
    </AppLayout>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-xs text-white/40">{label}</div>
      <div className="text-white/70">{value}</div>
    </div>
  );
}

function IntegrationRow({ name, description, onClick }: { name: string; description: string; onClick: () => void }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-white/5 last:border-0">
      <div>
        <div className="text-sm text-white/70">{name}</div>
        <div className="text-xs text-white/30">{description}</div>
      </div>
      <button
        onClick={onClick}
        className="px-3 py-1.5 bg-white/5 hover:bg-white/10 text-white/50 hover:text-white/70 rounded-lg text-xs transition-colors shrink-0"
      >
        Einrichten
      </button>
    </div>
  );
}

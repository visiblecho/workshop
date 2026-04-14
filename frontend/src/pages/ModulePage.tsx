import { useParams, useNavigate } from "react-router-dom";
import PlaceholderPage, { type WaveContent } from "../components/PlaceholderPage";
import AppLayout from "../components/AppLayout";

interface ModuleContent {
  title: string;
  description: string;
  waves: WaveContent;
  clTeaser: string;
}

const MODULES: Record<string, ModuleContent> = {
  kunden: {
    title: "Kunden",
    description: "Kundenanfragen erfassen, Kontakte verwalten, Auftragshistorie einsehen.",
    waves: {
      w1: "Kunde ruft an, Bürokraft notiert Daten, legt Akte an.",
      w2: "Lead-Formular auf der Website erstellt automatisch einen Kundendatensatz.",
      w3: "KI beantwortet Erstanfragen, qualifiziert Leads und bucht den Aufmaßtermin.",
    },
    clTeaser: "CL-Signal: \"Betriebe in Ihrer Region, die innerhalb von 2h antworten, gewinnen 3x mehr Aufträge.\"",
  },
  aufnahme: {
    title: "Aufnahme",
    description: "Vor-Ort-Bewertung, Maße erfassen, Fotos dokumentieren.",
    waves: {
      w1: "Geselle nimmt Maße auf Papier, fährt zurück ins Büro.",
      w2: "Geselle erfasst Maße auf dem Tablet, synchronisiert ins Büro. Fotos werden dem Auftrag zugeordnet.",
      w3: "KI liest Fotos und Maße, füllt das Angebotstemplate automatisch vor.",
    },
    clTeaser: "CL-Signal: \"Aufträge mit Fotodokumentation haben 30% weniger Angebotsfehler.\"",
  },
  versand: {
    title: "Versand",
    description: "Angebot an den Kunden senden, Nachverfolgung, Online-Annahme.",
    waves: {
      w1: "Angebot als PDF drucken oder per E-Mail senden.",
      w2: "Kundenportal: Kunde sieht Angebot online und nimmt an.",
      w3: "KI-Nachverfolgung: \"Kunde hat seit 5 Tagen nicht geantwortet. Vorschlag: anrufen oder Preis anpassen.\"",
    },
    clTeaser: "CL-Signal: \"Betriebe, die Angebote innerhalb von 24h versenden, konvertieren 40% mehr.\"",
  },
  plantafel: {
    title: "Plantafel",
    description: "Aufträge planen, Teams koordinieren, Materiallieferungen abstimmen.",
    waves: {
      w1: "Meister verteilt Aufträge manuell, Kalender im Kopf.",
      w2: "Drag-and-Drop Plantafel, Teamkalender, Sync mit Gesellen-App.",
      w3: "KI-Routenoptimierung, Skill-Matching, automatische Materialbestellung.",
    },
    clTeaser: "CL-Signal: \"Ihre durchschnittliche Fahrzeit zwischen Aufträgen: 45min. Top 25%: 28min.\"",
  },
  zeiterfassung: {
    title: "Zeiterfassung",
    description: "Arbeitszeiten pro Auftrag erfassen, Soll/Ist vergleichen.",
    waves: {
      w1: "Stundenzettel auf Papier, Eingabe am Wochenende.",
      w2: "Mobile Zeiterfassung pro Auftrag, Echtzeit-Synchronisation.",
      w3: "Auto-Tracking (GPS/standortbasierter Start/Stopp).",
    },
    clTeaser: "CL-Signal: \"Ihre Gesellen erfassen 78% der Stunden. Top-Betriebe: 95%. Die Lücke kostet Sie €X/Jahr an unsichtbaren Kosten.\"",
  },
  dokumentation: {
    title: "Dokumentation",
    description: "Aufträge dokumentieren, Abnahmeprotokolle, Gewährleistungsnachweise.",
    waves: {
      w1: "Geselle schreibt Fertigstellungsvermerk, Meister zeichnet ab.",
      w2: "Fotodokumentation vor Ort, synchronisiert zum Auftrag.",
      w3: "KI erstellt Abnahmebericht aus Fotos und Zeitprotokollen.",
    },
    clTeaser: "CL-Signal: \"Betriebe mit lückenloser Dokumentation haben 60% weniger Gewährleistungsstreitigkeiten.\"",
  },
  rechnungen: {
    title: "Rechnungen",
    description: "Rechnungen erstellen, GoBD-konform, DATEV-Export.",
    waves: {
      w1: "Bürokraft erstellt Rechnung aus Angebot, exportiert an DATEV. ZUGFeRD/XRechnung.",
      w2: "Auto-Rechnung aus abgeschlossenem Projekt (Angebot → Ist-Werte → Rechnung).",
      w3: "KI passt Rechnung anhand Soll/Ist an, markiert Abweichungen.",
    },
    clTeaser: "CL-Signal: \"Ihre durchschnittliche Rechnungsstellung: 8 Tage nach Abschluss. Top-Betriebe: 2 Tage.\"",
  },
  zahlungen: {
    title: "Zahlungen",
    description: "Zahlungsstatus verfolgen, Mahnwesen, Cashflow-Überblick.",
    waves: {
      w1: "Zahlungsstatus manuell nachverfolgen.",
      w2: "Automatische Zahlungserinnerungen.",
      w3: "KI-Cashflow-Prognose.",
    },
    clTeaser: "CL-Signal: \"Ihr durchschnittlicher Zahlungseingang: 38 Tage. Branche: 28 Tage.\"",
  },
  einstellungen: {
    title: "Einstellungen",
    description: "Firmenprofil, Benutzer, Integrationen, Datenexport.",
    waves: {
      w1: "Firmenadresse und Bankdaten pflegen, Briefkopf anpassen.",
      w2: "Benutzerverwaltung, Rollenrechte, Schnittstellen zu Buchhaltung und Großhandel.",
      w3: "KI-gestützte Konfiguration: System lernt Ihre Präferenzen und schlägt Optimierungen vor.",
    },
    clTeaser: "CL-Signal: \"86% der Betriebe Ihrer Größe nutzen die DATEV-Schnittstelle. Einrichten?\"",
  },
  betriebsvergleich: {
    title: "Betriebsvergleich",
    description: "Anonymisierter Vergleich Ihrer Kennzahlen mit der Plattform.",
    waves: {
      w1: "Steuerberater erstellt jährlichen BWA-Vergleich — oft Monate zu spät.",
      w2: "Echtzeit-Dashboard mit eigenen Kennzahlen.",
      w3: "Anonymisierter Quervergleich über tausende Betriebe: Wo stehen Sie wirklich?",
    },
    clTeaser: "CL-Signal: \"Ihre Marge liegt 4% unter dem Plattform-Median für Betriebe Ihrer Größe.\"",
  },
};

export default function ModulePage() {
  const { moduleId } = useParams();
  const navigate = useNavigate();
  const content = moduleId ? MODULES[moduleId] : undefined;

  if (!content) {
    return (
      <AppLayout title="Nicht gefunden">
        <div className="text-center py-20 space-y-4">
          <p className="text-white/50">Modul nicht gefunden.</p>
          <button
            onClick={() => navigate("/dashboard")}
            className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-[#1F1B1C] font-semibold rounded-lg transition-colors"
          >
            Zum Dashboard
          </button>
        </div>
      </AppLayout>
    );
  }

  return <PlaceholderPage {...content} />;
}

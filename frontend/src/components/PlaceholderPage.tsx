import { CheckCircle2, Timer, Sparkles, BarChart3 } from "lucide-react";
import AppLayout from "./AppLayout";

export interface WaveContent {
  w1: string;
  w2: string;
  w3: string;
}

export interface PlaceholderAction {
  label: string;
  onClick: () => void;
}

interface PlaceholderPageProps {
  title: string;
  description: string;
  waves: WaveContent;
  clTeaser: string;
  actions?: PlaceholderAction[];
}

export default function PlaceholderPage({ title, description, waves, clTeaser, actions }: PlaceholderPageProps) {
  return (
    <AppLayout title={title}>
      <div className="max-w-2xl space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold">{title}</h1>
          <p className="text-white/50 mt-1">{description}</p>
        </div>

        {/* W1/W2/W3 progression cards */}
        <div className="space-y-3">
          {/* W1 — Legacy */}
          <div className="p-4 rounded-lg bg-white/[0.03] border border-white/10">
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 text-white/20 shrink-0 mt-0.5" />
              <div>
                <div className="text-[10px] uppercase tracking-wider text-white/25 mb-1">
                  Was Handwerkersoftware heute kann
                </div>
                <p className="text-sm text-white/40">{waves.w1}</p>
              </div>
            </div>
          </div>

          {/* W2 — Modern */}
          <div className="p-4 rounded-lg bg-amber-500/5 border border-amber-500/15">
            <div className="flex items-start gap-3">
              <Timer className="w-5 h-5 text-amber-400/60 shrink-0 mt-0.5" />
              <div>
                <div className="text-[10px] uppercase tracking-wider text-amber-400/50 mb-1">
                  Was moderne Tools hinzufügen
                </div>
                <p className="text-sm text-amber-400/70">{waves.w2}</p>
              </div>
            </div>
          </div>

          {/* W3 — AI-native */}
          <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/25">
            <div className="flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <div className="text-[10px] uppercase tracking-wider text-amber-400/80 mb-1">
                  Was KI-native Plattformen ermöglichen
                </div>
                <p className="text-sm text-white/80">{waves.w3}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        {actions && actions.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {actions.map((action) => (
              <button
                key={action.label}
                onClick={action.onClick}
                className="px-4 py-2 bg-white/5 hover:bg-white/10 text-white/60 hover:text-white/80 rounded-lg text-sm transition-colors"
              >
                {action.label}
              </button>
            ))}
          </div>
        )}

        {/* CL teaser */}
        <div className="p-4 rounded-lg bg-white/[0.02] border border-white/5">
          <div className="flex items-start gap-3">
            <BarChart3 className="w-4 h-4 text-teal-400/60 shrink-0 mt-0.5" />
            <p className="text-xs text-white/40 italic">{clTeaser}</p>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}

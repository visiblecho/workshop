import { useLocation, useNavigate, useSearchParams } from "react-router-dom";
import {
  LayoutGrid, Users, ClipboardList, FileText, Send, Calendar,
  Clock, FileCheck, Receipt, CreditCard, TrendingUp, BarChart3,
  Settings,
} from "lucide-react";

const WEBER_FIRM_ID = "10000000-0000-0000-0000-000000000001";
const NEUER_FIRM_ID = "10000000-0000-0000-0000-000000000002";

interface NavItem {
  label: string;
  icon: React.ElementType;
  path: string;
  active: boolean; // true = links to existing screen, false = placeholder
}

interface NavGroup {
  title: string;
  items: NavItem[];
}

const NAV_GROUPS: NavGroup[] = [
  {
    title: "Tagesgeschäft",
    items: [
      { label: "Dashboard", icon: LayoutGrid, path: "/dashboard", active: true },
      { label: "Kunden", icon: Users, path: "/module/kunden", active: false },
      { label: "Aufnahme", icon: ClipboardList, path: "/module/aufnahme", active: false },
      { label: "Angebote", icon: FileText, path: "/quote/new", active: true },
      { label: "Versand", icon: Send, path: "/module/versand", active: false },
      { label: "Plantafel", icon: Calendar, path: "/module/plantafel", active: false },
      { label: "Zeiterfassung", icon: Clock, path: "/module/zeiterfassung", active: false },
      { label: "Dokumentation", icon: FileCheck, path: "/module/dokumentation", active: false },
      { label: "Rechnungen", icon: Receipt, path: "/module/rechnungen", active: false },
      { label: "Zahlungen", icon: CreditCard, path: "/module/zahlungen", active: false },
    ],
  },
  {
    title: "Analyse",
    items: [
      { label: "Nachkalkulation", icon: TrendingUp, path: "/dashboard", active: true },
      { label: "Betriebsvergleich", icon: BarChart3, path: "/dashboard", active: true },
    ],
  },
  {
    title: "System",
    items: [
      { label: "Einstellungen", icon: Settings, path: "/module/einstellungen", active: false },
    ],
  },
];

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

export default function Sidebar({ open, onClose }: SidebarProps) {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const firmId = searchParams.get("firm") || WEBER_FIRM_ID;

  function handleNav(item: NavItem) {
    const separator = item.path.includes("?") ? "&" : "?";
    const target = item.path.startsWith("/module/")
      ? item.path
      : `${item.path}${separator}firm=${firmId}`;
    navigate(target);
    onClose();
  }

  function isCurrent(item: NavItem): boolean {
    if (item.path.startsWith("/module/")) {
      return location.pathname === item.path;
    }
    return location.pathname === item.path;
  }

  return (
    <>
      {/* Overlay on mobile */}
      {open && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed top-0 left-0 h-full w-60 bg-[#171314] border-r border-white/10 z-50 flex flex-col transition-transform duration-200 ${
          open ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        {/* Brand */}
        <div className="px-4 py-4 border-b border-white/10">
          <span className="text-lg font-semibold tracking-tight text-white">Workshop</span>
        </div>

        {/* Nav groups */}
        <nav className="flex-1 overflow-y-auto py-2">
          {NAV_GROUPS.map((group) => (
            <div key={group.title} className="mb-2">
              <div className="px-4 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-white/25">
                {group.title}
              </div>
              {group.items.map((item) => {
                const current = isCurrent(item);
                const Icon = item.icon;
                return (
                  <button
                    key={item.label}
                    onClick={() => handleNav(item)}
                    className={`w-full flex items-center gap-3 px-4 py-2 text-sm transition-colors ${
                      current
                        ? "bg-amber-500/10 text-amber-400"
                        : item.active
                        ? "text-white/80 hover:bg-white/5 hover:text-white"
                        : "text-white/35 hover:bg-white/5 hover:text-white/50"
                    }`}
                  >
                    <Icon className="w-4 h-4 shrink-0" strokeWidth={current || item.active ? 2 : 1.5} />
                    <span className={item.active ? "" : ""}>{item.label}</span>
                    {!item.active && (
                      <span className="ml-auto text-[9px] text-white/15 uppercase tracking-wide">Bald</span>
                    )}
                  </button>
                );
              })}
            </div>
          ))}
        </nav>

        {/* Firm switcher in footer */}
        <div className="border-t border-white/10 p-3 space-y-2">
          <div className="text-[10px] text-white/25 uppercase tracking-wider">Betrieb</div>
          <div className="flex gap-1">
            <button
              onClick={() => { navigate(`/dashboard?firm=${WEBER_FIRM_ID}`); onClose(); }}
              className={`flex-1 px-2 py-1.5 rounded text-xs font-medium transition-all ${
                firmId === WEBER_FIRM_ID ? "bg-amber-500/20 text-amber-400" : "text-white/40 hover:text-white/70 bg-white/5"
              }`}
            >
              Weber
            </button>
            <button
              onClick={() => { navigate(`/dashboard?firm=${NEUER_FIRM_ID}`); onClose(); }}
              className={`flex-1 px-2 py-1.5 rounded text-xs font-medium transition-all ${
                firmId === NEUER_FIRM_ID ? "bg-amber-500/20 text-amber-400" : "text-white/40 hover:text-white/70 bg-white/5"
              }`}
            >
              Neuer Betrieb
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}

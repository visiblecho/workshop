import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Menu } from "lucide-react";
import Sidebar from "./Sidebar";

const WEBER_FIRM_ID = "10000000-0000-0000-0000-000000000001";

interface AppLayoutProps {
  children: React.ReactNode;
  title?: string;
}

export default function AppLayout({ children, title }: AppLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchParams] = useSearchParams();
  const firmId = searchParams.get("firm") || WEBER_FIRM_ID;

  return (
    <div className="min-h-screen bg-[#1F1B1C] text-white">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main content area — offset by sidebar width on desktop */}
      <div className="lg:ml-60">
        {/* Top bar */}
        <header className="border-b border-white/10 px-4 py-3">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden text-white/50 hover:text-white"
            >
              <Menu className="w-5 h-5" />
            </button>
            {title && <span className="text-sm text-white/50">{title}</span>}
          </div>
        </header>

        <main className="max-w-5xl mx-auto px-4 py-6">
          {children}
        </main>
      </div>
    </div>
  );
}

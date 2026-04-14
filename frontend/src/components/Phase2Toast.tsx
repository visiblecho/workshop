import { useState, useEffect, useCallback } from "react";

interface ToastState {
  visible: boolean;
  message: string;
}

let showToastGlobal: ((msg?: string) => void) | null = null;

/** Call from anywhere to show the Phase 2 toast */
export function showPhase2Toast(message?: string) {
  showToastGlobal?.(message);
}

/**
 * Mount this once in AppLayout. Shows a toast notification for Phase 2 features.
 */
export default function Phase2Toast() {
  const [toast, setToast] = useState<ToastState>({ visible: false, message: "" });

  const show = useCallback((msg?: string) => {
    setToast({
      visible: true,
      message: msg || "Diese Funktion ist in Phase 2 verfügbar. Das Datenmodell ist vorbereitet.",
    });
  }, []);

  // Register global trigger
  useEffect(() => {
    showToastGlobal = show;
    return () => { showToastGlobal = null; };
  }, [show]);

  // Auto-dismiss after 3 seconds
  useEffect(() => {
    if (!toast.visible) return;
    const timer = setTimeout(() => setToast((t) => ({ ...t, visible: false })), 3000);
    return () => clearTimeout(timer);
  }, [toast.visible]);

  if (!toast.visible) return null;

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-[60] lg:left-[calc(50%+7.5rem)]">
      <div
        onClick={() => setToast((t) => ({ ...t, visible: false }))}
        className="px-5 py-3 rounded-lg bg-[#2a2426] border border-amber-500/20 shadow-lg shadow-black/30 cursor-pointer animate-fade-in"
      >
        <p className="text-sm text-amber-400/90">{toast.message}</p>
      </div>
    </div>
  );
}

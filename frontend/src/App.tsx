import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import Onboarding from "./pages/Onboarding";
import Import from "./pages/Import";
import NewFirm from "./pages/NewFirm";
import Dashboard from "./pages/Dashboard";
import QuoteNew from "./pages/QuoteNew";
import ProjectDetail from "./pages/ProjectDetail";

function NotFound() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-[#1F1B1C] flex items-center justify-center px-4">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-white">404</h1>
        <p className="text-white/50">Seite nicht gefunden</p>
        <button
          onClick={() => navigate("/")}
          className="px-6 py-3 bg-amber-500 hover:bg-amber-400 text-[#1F1B1C] font-semibold rounded-lg transition-colors"
        >
          Zur Startseite
        </button>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Onboarding />} />
        <Route path="/import" element={<Import />} />
        <Route path="/new" element={<NewFirm />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/quote/new" element={<QuoteNew />} />
        <Route path="/project/:projectId" element={<ProjectDetail />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

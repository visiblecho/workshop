import { BrowserRouter, Routes, Route } from "react-router-dom";
import Onboarding from "./pages/Onboarding";
import Import from "./pages/Import";
import NewFirm from "./pages/NewFirm";
import Dashboard from "./pages/Dashboard";
import QuoteNew from "./pages/QuoteNew";
import ProjectDetail from "./pages/ProjectDetail";

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
      </Routes>
    </BrowserRouter>
  );
}

export default App;

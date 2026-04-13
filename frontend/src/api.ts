const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

export interface HealthResponse {
  status: string;
  db: string;
  firm_count: number;
}

export interface FirmSummary {
  id: string;
  name: string;
  segment: string;
  region: string;
  employee_count: number | null;
}

export interface UserSummary {
  id: string;
  firm_id: string;
  name: string;
  role: "meister" | "geselle" | "buero";
  email: string | null;
  language: string;
}

export interface DashboardCLInsight {
  job_type: string;
  firm_median: number | null;
  platform_median: number | null;
  platform_sample_size: number | null;
}

export interface DashboardQuote {
  id: string;
  customer_name: string;
  job_type: string;
  status: string;
  total_net: number | null;
  created_at: string | null;
}

export interface DashboardProject {
  id: string;
  customer_name: string;
  job_type: string;
  status: string;
  planned_hours: number | null;
  actual_hours: number | null;
  margin_pct: number | null;
  completed_at: string | null;
}

export interface DashboardData {
  firm: { id: string; name: string; segment: string; region: string };
  counts: {
    open_quotes: number;
    active_projects: number;
    completed_projects: number;
    customers: number;
    positions: number;
  };
  recent_quotes: DashboardQuote[];
  recent_projects: DashboardProject[];
  cl_insights: DashboardCLInsight[];
}

export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export function getFirms(): Promise<FirmSummary[]> {
  return request<FirmSummary[]>("/api/firms");
}

export function getFirmUsers(firmId: string): Promise<UserSummary[]> {
  return request<UserSummary[]>(`/api/firms/${firmId}/users`);
}

export function getDashboard(firmId: string): Promise<DashboardData> {
  return request<DashboardData>(`/api/firms/${firmId}/dashboard`);
}

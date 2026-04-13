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

// --- Quote ---

export interface QuoteLineItemData {
  id: string;
  position: number;
  description: string;
  category: "labor" | "material" | "other";
  quantity: number;
  unit: string;
  unit_price: number;
  total: number;
  article_id: string | null;
}

export interface GenerateQuoteResponse {
  quote_id: string;
  is_fallback: boolean;
  total_net: number;
  total_gross: number;
  line_items: QuoteLineItemData[];
}

export function generateQuote(data: {
  firm_id: string;
  customer_id: string;
  job_type_id: string;
  description: string;
  created_by: string;
}): Promise<GenerateQuoteResponse> {
  return request<GenerateQuoteResponse>("/api/quotes/generate", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export interface CustomerSummary {
  id: string;
  name: string;
  type: string;
}

export interface JobTypeSummary {
  id: string;
  name: string;
  description: string | null;
}

export function getCustomers(firmId: string): Promise<CustomerSummary[]> {
  return request<CustomerSummary[]>(`/api/firms/${firmId}/customers`);
}

export function getJobTypes(firmId: string): Promise<JobTypeSummary[]> {
  return request<JobTypeSummary[]>(`/api/firms/${firmId}/job-types`);
}

// --- Benchmarks ---

export interface BenchmarkMetric {
  p25?: number;
  p50: number;
  p75?: number;
  mean: number;
  sample_size?: number;
}

export interface BenchmarkData {
  job_type_id: string;
  firm_id: string;
  cl_benchmarks: Record<string, BenchmarkMetric>;
  firm_benchmarks: Record<string, BenchmarkMetric>;
}

export function getBenchmarks(jobTypeId: string, firmId: string): Promise<BenchmarkData> {
  return request<BenchmarkData>(`/api/benchmarks/${jobTypeId}?firm_id=${firmId}`);
}

// --- Price History ---

export interface PriceHistoryRecord {
  price: number;
  currency: string;
  source: string | null;
  recorded_at: string;
}

export function getArticlePriceHistory(articleId: string): Promise<PriceHistoryRecord[]> {
  return request<PriceHistoryRecord[]>(`/api/articles/${articleId}/price-history`);
}

// --- Events ---

export interface EventRecord {
  id: string;
  event_type: string;
  actor_name: string;
  actor_role: string;
  payload: Record<string, unknown>;
  created_at: string;
}

export function getEvents(entityType: string, entityId: string): Promise<EventRecord[]> {
  return request<EventRecord[]>(`/api/events?entity_type=${entityType}&entity_id=${entityId}`);
}

// --- Project Detail ---

export interface ProjectLineItemDetail {
  id: string;
  description: string;
  category: string;
  actual_quantity: number;
  actual_unit_price: number;
  actual_total: number;
  notes: string | null;
  quoted: {
    description: string;
    quantity: number;
    unit_price: number;
    total: number;
  } | null;
}

export interface ProjectDetail {
  id: string;
  customer_name: string;
  job_type: string;
  status: string;
  planned_hours: number | null;
  actual_hours: number | null;
  planned_cost: number | null;
  actual_cost: number | null;
  margin_pct: number | null;
  started_at: string | null;
  completed_at: string | null;
  line_items: ProjectLineItemDetail[];
  firm_benchmark_duration: number | null;
  cl_benchmark_duration: number | null;
  cl_sample_size: number | null;
}

export function getProject(projectId: string): Promise<ProjectDetail> {
  return request<ProjectDetail>(`/api/projects/${projectId}`);
}

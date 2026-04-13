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

export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export default { getHealth };

export interface Firm {
  id: string;
  name: string;
  segment: string;
  country: string;
  currency: string;
  region: string;
  postal_code: string;
  employee_count: number | null;
}

export interface User {
  id: string;
  firm_id: string;
  name: string;
  role: "meister" | "geselle" | "buero";
  email: string | null;
  language: string;
}

export interface Customer {
  id: string;
  firm_id: string;
  name: string;
  type: "residential" | "commercial" | "public";
  address: string | null;
  postal_code: string | null;
  phone: string | null;
  email: string | null;
}

export interface JobType {
  id: string;
  segment: string;
  name: string;
  description: string | null;
  avg_duration_h: number | null;
  avg_margin_pct: number | null;
  sample_size: number | null;
}

export interface QuoteLineItem {
  id: string;
  quote_id: string;
  position: number;
  description: string;
  category: "labor" | "material" | "other";
  quantity: number;
  unit: string;
  unit_price: number;
  total: number;
  article_id: string | null;
  cl_price_flag: string | null;
}

export interface Quote {
  id: string;
  firm_id: string;
  customer_id: string;
  job_type_id: string;
  created_by: string;
  status: "draft" | "sent" | "accepted" | "rejected" | "expired";
  total_net: number | null;
  total_gross: number | null;
  margin_target: number | null;
  cl_margin_pred: number | null;
  cl_price_bench: number | null;
  created_at: string;
  line_items?: QuoteLineItem[];
}

export interface ProjectLineItem {
  id: string;
  project_id: string;
  quote_line_id: string | null;
  description: string;
  category: "labor" | "material" | "other";
  actual_quantity: number;
  actual_unit_price: number;
  actual_total: number;
  notes: string | null;
}

export interface Project {
  id: string;
  firm_id: string;
  customer_id: string;
  quote_id: string | null;
  job_type_id: string;
  assigned_to: string | null;
  status: "planned" | "active" | "completed" | "cancelled";
  planned_hours: number | null;
  actual_hours: number | null;
  planned_cost: number | null;
  actual_cost: number | null;
  margin_pct: number | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  line_items?: ProjectLineItem[];
}

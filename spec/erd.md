# Entity-Relationship Model -- AI-Native Trade Software Prototype

**Updated:** April 12, 2026
**Scope:** Full backbone (A0-A9) data model. Prototype implements A2 (Quote) + A9 (Post-calculate) + CL layer.
**Principle:** Segment-agnostic core. SHK-specific data injected as configuration, not hardcoded.

---

## Design Principles

1. **Every entity that generates CL data has a `segment` and `region` field.** This enables crowd benchmarking by trade and geography.
2. **Quotes and actuals are separate but linked.** Quote line items predict; project line items record actuals. The delta is the learning signal.
3. **Auth-ready, not auth-required.** The model supports roles (Meister/Geselle/Buero) and trust boundaries from day one. Prototype: 3 hardcoded users, role switcher, no user management.
4. **Timestamps everywhere.** CL benchmarks depend on time-series data. No entity without `created_at` and `updated_at`.
5. **Soft deletes.** Nothing is truly deleted -- `deleted_at` on every entity. Historical data feeds the CL layer.
6. **Event-sourced learning.** Quote, QuoteLineItem, Project, ProjectLineItem changes are tracked via an Events table. Customer/Firm get `updated_by` but no event trail. Events power audit + per-firm learning (FirmBenchmark).
7. **i18n-ready from day one.** Firm carries `country` and `currency`. All monetary fields are bare decimals; currency context comes from the firm. Benchmarks are currency-scoped. Display strings go through an i18n layer, not hardcoded. Adding Swiss/Austrian support later should be config, not migration.

---

## DBML Schema

```dbml
// ============================================================
// ENUMS
// ============================================================

Enum segment {
  shk
  elektro
  dach_holz
  metallbau
  geruestbau
  landschaftsbau
  general
}

Enum role {
  meister
  geselle
  buero
}

Enum customer_type {
  residential
  commercial
  public
}

Enum quote_status {
  draft
  sent
  accepted
  rejected
  expired
}

Enum project_status {
  planned
  active
  completed
  cancelled
}

Enum line_category {
  labor
  material
  other
}

Enum unit {
  hours
  pieces
  meters
  kg
  liters
  sqm
  flat_rate
}

Enum cl_metric {
  duration_h
  margin_pct
  material_cost
  quote_total
  conversion_rate
}

Enum event_type {
  created
  updated
  status_changed
  deleted
}

Enum event_entity_type {
  quote
  quote_line_item
  project
  project_line_item
}

// ============================================================
// CORE ENTITIES
// ============================================================

Table firm {
  id uuid [pk]
  name varchar [not null]
  segment segment [not null]
  country varchar(2) [not null, default: 'DE', note: 'ISO 3166-1 alpha-2. Drives currency, tax, locale.']
  currency varchar(3) [not null, default: 'EUR', note: 'ISO 4217. All monetary fields on this firm are in this currency.']
  region varchar [not null]
  postal_code varchar [not null]
  employee_count int
  updated_by uuid [ref: > user.id, note: 'Last editor. No event trail.']
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`]
  deleted_at timestamptz
}

Table user {
  id uuid [pk]
  firm_id uuid [ref: > firm.id, not null]
  name varchar [not null]
  role role [not null, note: 'meister / geselle / buero']
  email varchar
  language varchar(5) [not null, default: 'de', note: 'IETF BCP 47. UI display language. de / de-CH / en / tr / ...']
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`]
  deleted_at timestamptz

  Note: 'Prototype: 3 hardcoded users (master, journeyman, office). Role switcher in header. No auth flows. Language defaults to de.'
}

Table customer {
  id uuid [pk]
  firm_id uuid [ref: > firm.id, not null]
  name varchar [not null]
  type customer_type [not null]
  address text
  postal_code varchar
  phone varchar
  email varchar
  notes text
  updated_by uuid [ref: > user.id, note: 'Last editor. No event trail.']
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`]
  deleted_at timestamptz
}

// ============================================================
// QUOTE (predicted)
// ============================================================

Table quote {
  id uuid [pk]
  firm_id uuid [ref: > firm.id, not null]
  customer_id uuid [ref: > customer.id, not null]
  job_type_id uuid [ref: > job_type.id, not null]
  created_by uuid [ref: > user.id, not null]
  status quote_status [not null, default: 'draft']
  total_net decimal
  total_gross decimal
  margin_target decimal
  cl_margin_pred decimal [note: 'CL prediction at time of quote creation']
  cl_price_bench decimal [note: 'CL platform benchmark at time of quote creation']
  sent_at timestamptz
  accepted_at timestamptz
  rejected_at timestamptz
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`]
  deleted_at timestamptz

  Note: 'Event-tracked. All changes logged to events table.'
}

Table quote_line_item {
  id uuid [pk]
  quote_id uuid [ref: > quote.id, not null]
  position int [not null, note: 'Display ordering']
  description text [not null]
  category line_category [not null]
  quantity decimal [not null]
  unit unit [not null]
  unit_price decimal [not null]
  total decimal [not null]
  article_id uuid [ref: > article.id, note: 'Optional, from catalogue']
  cl_price_flag varchar [note: 'e.g. "12% below platform median"']
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`]
  deleted_at timestamptz

  Note: 'Event-tracked. All changes logged to events table.'
}

// ============================================================
// PROJECT (actual)
// ============================================================

Table project {
  id uuid [pk]
  firm_id uuid [ref: > firm.id, not null]
  customer_id uuid [ref: > customer.id, not null]
  quote_id uuid [ref: - quote.id, note: 'A project is born from an accepted quote']
  job_type_id uuid [ref: > job_type.id, not null]
  assigned_to uuid [ref: > user.id]
  status project_status [not null, default: 'planned']
  planned_hours decimal
  actual_hours decimal
  planned_cost decimal
  actual_cost decimal
  margin_pct decimal [note: 'Calculated on project close']
  started_at timestamptz
  completed_at timestamptz
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`]
  deleted_at timestamptz

  Note: 'Event-tracked. All changes logged to events table.'
}

Table project_line_item {
  id uuid [pk]
  project_id uuid [ref: > project.id, not null]
  quote_line_id uuid [ref: > quote_line_item.id, note: 'Links actual to predicted -- the CL learning signal']
  description text [not null]
  category line_category [not null]
  actual_quantity decimal [not null]
  actual_unit_price decimal [not null]
  actual_total decimal [not null]
  notes text
  logged_by uuid [ref: > user.id]
  logged_at timestamptz [not null]
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`]
  deleted_at timestamptz

  Note: 'Event-tracked. All changes logged to events table.'
}

// ============================================================
// REFERENCE DATA
// ============================================================

Table job_type {
  id uuid [pk]
  segment segment [not null]
  name varchar [not null]
  description text
  parent_id uuid [ref: > job_type.id, note: 'Hierarchical job types']
  avg_duration_h decimal [note: 'CL-derived']
  avg_margin_pct decimal [note: 'CL-derived']
  sample_size int [note: 'CL sample count']
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`]
  deleted_at timestamptz
}

Table article {
  id uuid [pk]
  segment segment [not null]
  name varchar [not null]
  datanorm_id varchar [note: 'External reference (DATANORM catalogue)']
  unit unit [not null]
  default_price decimal [not null]
  wholesaler varchar
  last_price_date date
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`]
  deleted_at timestamptz
}

// ============================================================
// EVENT SOURCING (audit + per-firm learning)
// ============================================================

Table event {
  id uuid [pk]
  entity_type event_entity_type [not null, note: 'quote / quote_line_item / project / project_line_item']
  entity_id uuid [not null, note: 'FK to the changed entity']
  event_type event_type [not null, note: 'created / updated / status_changed / deleted']
  actor_id uuid [ref: > user.id, not null, note: 'Who made the change']
  payload jsonb [not null, note: 'Full diff: {field: {old: x, new: y}}']
  created_at timestamptz [not null, default: `now()`]

  indexes {
    (entity_type, entity_id) [name: 'idx_event_entity']
    actor_id [name: 'idx_event_actor']
    created_at [name: 'idx_event_time']
  }

  Note: 'Append-only. Application reads from projected state tables (quote, project, etc.), not from events. Events power audit trail UI + FirmBenchmark computation.'
}

// ============================================================
// CROWD LEARNING (CL) LAYER
// ============================================================

Table cl_benchmark {
  id uuid [pk]
  job_type_id uuid [ref: > job_type.id, not null]
  segment segment [not null]
  region varchar [not null]
  metric cl_metric [not null]
  currency varchar(3) [not null, note: 'ISO 4217. Monetary metrics must be currency-scoped.']
  period_start date [not null]
  period_end date [not null]
  sample_size int [not null]
  p25 decimal [not null]
  p50 decimal [not null, note: 'Median']
  p75 decimal [not null]
  mean decimal [not null]
  updated_at timestamptz [not null, default: `now()`]

  indexes {
    (job_type_id, segment, region, metric, currency) [name: 'idx_cl_benchmark_lookup']
  }

  Note: 'Platform-level benchmarks. Seeded for demo, not computed. Currency-scoped.'
}

Table firm_benchmark {
  id uuid [pk]
  firm_id uuid [ref: > firm.id, not null]
  job_type_id uuid [ref: > job_type.id, not null]
  metric cl_metric [not null]
  currency varchar(3) [not null, note: 'ISO 4217. Inherited from firm.currency at computation time.']
  period_start date [not null]
  period_end date [not null]
  sample_size int [not null]
  p25 decimal
  p50 decimal [note: 'Median']
  p75 decimal
  mean decimal [not null]
  updated_at timestamptz [not null, default: `now()`]

  indexes {
    (firm_id, job_type_id, metric) [name: 'idx_firm_benchmark_lookup']
  }

  Note: 'Per-firm benchmarks. Layer 2 of CL. Scheduled update (weekly/monthly), manual trigger option. Seeded for demo.'
}

Table article_price_history {
  id uuid [pk]
  article_id uuid [ref: > article.id, not null]
  price decimal [not null]
  currency varchar(3) [not null, note: 'ISO 4217.']
  source varchar [note: 'DATANORM, wholesaler name, manual']
  recorded_at date [not null]
  created_at timestamptz [not null, default: `now()`]

  indexes {
    (article_id, recorded_at) [name: 'idx_article_price_history_lookup']
  }

  Note: 'Separate from events -- price changes come from external sources (DATANORM, wholesalers), not user actions. Powers material cost trend signals in quotes.'
}
```

---

## Key Relationships

```
Firm 1:N User
Firm 1:N Customer
Firm 1:N Quote
Firm 1:N Project
Firm 1:N FirmBenchmark

Customer 1:N Quote
Customer 1:N Project

Quote 1:N QuoteLineItem
Quote 1:1 Project            (a project is born from an accepted quote)

Project 1:N ProjectLineItem
ProjectLineItem N:1 QuoteLineItem   (actual vs. predicted, the CL learning signal)

JobType 1:N Quote
JobType 1:N Project
JobType 1:N CLBenchmark      (benchmarks are per job type + segment + region)
JobType 1:N FirmBenchmark    (per-firm benchmarks, same dimensions)

Article 1:N QuoteLineItem    (optional -- articles from catalogue)
Article 1:N ArticlePriceHistory  (external price changes over time)

User 1:N Event               (actor_id -- who made the change)
Event N:1 {Quote, QuoteLineItem, Project, ProjectLineItem}  (polymorphic via entity_type + entity_id)
```

---

## The CL Learning Signal

```
QuoteLineItem (predicted)
        |
        |  project completes
        v
ProjectLineItem (actual)
        |
        |  delta = actual - predicted
        v
Event log: full history of revisions, corrections, status changes
        |
        |  aggregate per firm
        v
FirmBenchmark: "Your bathroom renovations take 14h, not 10h."
        |
        |  aggregate across firms (anonymized)
        v
CLBenchmark: "Platform median for bathroom reno in region X: 12h, margin 26%"
        |
        |  feed back into next quote
        v
QuoteLineItem.cl_price_flag: "12% below platform median"
Quote.cl_margin_pred / cl_price_bench
```

---

## What the Prototype Implements

| Entity | In prototype? | Notes |
|--------|--------------|-------|
| Firm | Yes | Two firms seeded: (1) "Weber Haustechnik GmbH" -- micro, populated with historical data; (2) "Neuer Betrieb" -- micro, empty/fresh. Country: DE, currency: EUR. |
| User | Yes | 3 hardcoded users (master, journeyman, office roles). Role switcher in header. No auth flows. |
| Customer | Yes | 3-5 seed customers in different German regions. |
| Quote | Yes | Core feature. AI-generated from text input. Event-tracked. |
| QuoteLineItem | Yes | AI populates from job description + article catalogue. Event-tracked. |
| Project | Seed x5 | 5 completed projects for Weber firm with actuals. Powers post-calc view and FirmBenchmark demo. Event-tracked. |
| ProjectLineItem | Seed data | Pre-populated actuals for 5 past projects. Actuals differ from quoted (realistic variance). The delta vs. QuoteLineItem is the CL learning signal. Event-tracked. |
| JobType | Yes | SHK job types. Segment = "shk". Names stored as i18n keys. |
| Article | Seed data | 20-30 common SHK articles with prices. Simulates DATANORM catalogue. |
| Event | Yes | Append-only log. UI shows audit trail on quotes/projects. |
| CLBenchmark | Seed data | Pre-calculated benchmarks for demo. Seeded, not computed. |
| FirmBenchmark | Seed data | Pre-calculated for migrated demo firm. CL overlay shows both layers. |
| ArticlePriceHistory | Seed data | Copper pipe price trend in quote view. "+8% in 30 days." |

---

## Extension Points (not in prototype, but the model supports them)

| Future capability | Which entities | What's needed |
|-------------------|---------------|---------------|
| Auth + permissions | User.role + new: Permission | Auth layer, permission matrix, trust boundaries |
| Scheduling (Plantafel) | New: Schedule, TimeSlot | Link to Project + User |
| Time tracking | New: TimeEntry | Link to Project + User, powers A5 |
| Material ordering | Article + New: Order, OrderLine | IDS/OCI integration |
| Invoice generation | New: Invoice, InvoiceLine | Link to Project, DATEV/ZUGFeRD export |
| Segment extension | Segment enum + JobType + Article | Add enum values, seed segment-specific data |
| MCP external interface | All entities | Expose as MCP resources (read) and tools (write). Trust boundary per consumer type. |
| FirmBenchmark auto-compute | event + project_line_item -> firm_benchmark | Scheduled job, manual trigger endpoint |
| i18n / multi-country | Firm.country/currency, User.language | Translation tables, currency conversion for cross-currency CL benchmarks |

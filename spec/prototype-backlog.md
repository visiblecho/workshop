# Prototype Backlog -- AI-Native Trade Software

**Source:** prototype-scope.md (locked), erd.md, user-story-map.md, design-rationale.md
**Build day:** Monday April 13, 2026
**Time budget:** 5 hours
**Builder:** Claude Code (fresh instance in prototype repo)

---

## How to Read This Document

**Structure:** Epics > Stories > Tasks. Epics map to the scope doc. Stories follow "As a [role], when [context], I want [action] so that [outcome]." Tasks are engineer-level actions for the builder.

**Tags on every story:**

| Tag | Purpose |
|-----|---------|
| **Kano** | `must-be` (missing = broken), `performance` (more = better, linear), `excitement` (unexpected delight), `indifferent` (nobody cares) |
| **Product area** | Maps to user story map backbone: `onboarding`, `quotes` (A2), `post-calc` (A9), `dashboard`, `infrastructure` |
| **JTBD outcome** | Desired outcome from user-story-map.md, or `[not applicable -- infrastructure]` / `[not applicable -- business model]` |
| **Act** | Demo act: `Act 1 (retain)`, `Act 2 (product)`, `Act 3 (acquire)`, `Setup` |

**Priority:** Stories are ordered within epics by build dependency, not importance. The sorted backlog (Section 2) shows the global build sequence.

**Tasks:** Written for E0 (procedural setup). E1-E4 stories have acceptance criteria only -- the builder decomposes into tasks using CLAUDE.md conventions and the ERD.

---

## 1. Epic Overview

| Epic | Name | Act | Stories | Time est. |
|------|------|-----|---------|-----------|
| **E0** | Foundation | Setup | 6 | 1h |
| **E1** | Migration Onboarding | Act 1 (retain) | 4 | 45 min |
| **E2** | AI Quote + Crowd Learning | Act 2 (product) | 8 | 2h |
| **E3** | New User Onboarding | Act 3 (acquire) | 3 | 30 min |
| **E4** | Polish + Hardening | All | 4 | 45 min |
| | | | **25 stories** | **5h** |

---

## 2. Sorted Backlog (Build Sequence)

The builder works top to bottom. Each story is independently committable and deployable.

| # | ID | Story (one-liner) | Epic | Kano | Area | Time |
|---|----|--------------------|------|------|------|------|
| 1 | E0-S1 | Scaffold project structure (frontend + backend + repo) | E0 | must-be | infrastructure | 10 min |
| 2 | E0-S2 | Database schema + Neon connection | E0 | must-be | infrastructure | 15 min |
| 3 | E0-S5 | API health + frontend shell + CORS | E0 | must-be | infrastructure | 5 min |
| 4 | E0-S6 | Deploy to Render (frontend + backend) | E0 | must-be | infrastructure | 10 min |
| 5 | E0-S3 | Seed data: reference tables (firms, users, customers, job types, articles) | E0 | must-be | infrastructure | 15 min |
| 6 | E0-S4 | Seed data: historical (projects, line items, events, benchmarks, price history) | E0 | must-be | infrastructure | 15 min |
| 7 | E1-S1 | Onboarding screen with two paths | E1 | must-be | onboarding | 15 min |
| 8 | E1-S2 | Taifun import flow (simulated) | E1 | performance | onboarding | 15 min |
| 9 | E1-S3 | Dashboard: populated state (post-import) | E1 | must-be | dashboard | 10 min |
| 10 | E1-S4 | Migration narrative in UI | E1 | excitement | onboarding | 5 min |
| 11 | E2-S1 | Quote creation: text input -> AI -> structured quote + cached fallback | E2 | must-be | quotes | 30 min |
| 12 | E2-S2 | CL overlay: FirmBenchmark + CLBenchmark on quote | E2 | performance | quotes | 20 min |
| 13 | E2-S3 | Margin forecast on quote | E2 | performance | quotes | 10 min |
| 14 | E2-S4 | Material cost trend signal | E2 | excitement | quotes | 10 min |
| 15 | E2-S5 | Role switcher + role-differentiated views | E2 | must-be | quotes | 15 min |
| 16 | E2-S6 | Event trail (audit log) on quotes | E2 | performance | quotes | 10 min |
| 17 | E2-S7 | Project detail: post-calculation view | E2 | performance | post-calc | 15 min |
| 18 | E2-S8 | Voice input for quote creation | E2 | excitement | quotes | 10 min |
| 19 | E3-S1 | New user onboarding path (no legacy data) | E3 | performance | onboarding | 15 min |
| 20 | E3-S2 | Dashboard: sparse state (new firm) | E3 | must-be | dashboard | 10 min |
| 21 | E3-S3 | CL-only overlay for new firm (no FirmBenchmark) | E3 | performance | quotes | 5 min |
| 22 | E4-S1 | Navigation hardening (no dead ends) | E4 | must-be | infrastructure | 15 min |
| 23 | E4-S2 | Visual polish (Tailwind) | E4 | performance | infrastructure | 15 min |
| 24 | E4-S3 | German UI text audit | E4 | must-be | infrastructure | 10 min |
| 25 | E4-S4 | Responsive layout check | E4 | indifferent | infrastructure | 5 min |

**Cut line:** If running over time, cut from bottom up. E4-S4 goes first, then E2-S8 (voice), then E3-S3.

---

## 3. Full Story Details

---

### Epic E0: Foundation

**Goal:** A deployed, empty shell on Render. Frontend talks to backend, backend talks to database. Seed data loaded. Health endpoint returns 200 from the live URL. Every subsequent epic builds on something that's already live.

**Time budget:** 1 hour

---

#### E0-S1: Scaffold project structure

**As a** builder, **when** starting the prototype, **I want** a working project structure with frontend (React+Vite+TS+Tailwind), backend (FastAPI+Python), and git repo **so that** I can build features on a stable foundation.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- infrastructure] |
| Act | Setup |

**Acceptance criteria:**
- [ ] `frontend/` directory with React + Vite + TypeScript, Tailwind CSS v4 via @tailwindcss/vite plugin
- [ ] `backend/` directory with FastAPI, uvicorn, anthropic, psycopg2-binary, sqlalchemy, alembic, python-dotenv
- [ ] Root `CLAUDE.md`, `frontend/CLAUDE.md`, `backend/CLAUDE.md` with build/run conventions
- [ ] `.gitignore` excludes node_modules, venv, .env, __pycache__, dist
- [ ] `npm run dev` starts frontend on :5173
- [ ] `uvicorn main:app --reload` starts backend on :8000
- [ ] Git initialized, first commit

**Tasks:**
1. Create project directory
2. Run `npm create vite@latest frontend -- --template react-ts` inside it
3. `cd frontend && npm install && npm install tailwindcss @tailwindcss/vite`
4. Configure `vite.config.ts` with tailwindcss plugin, `index.css` with `@import "tailwindcss"`
5. Create `backend/` with `main.py` (FastAPI skeleton + CORS), `requirements.txt`
6. Create Python venv, install deps
7. Write 3 CLAUDE.md files (root, frontend, backend)
8. Write `.gitignore`
9. `git init && git add . && git commit`

---

#### E0-S2: Database schema + Neon connection

**As a** builder, **when** the project is scaffolded, **I want** all tables from the ERD created in Neon Postgres **so that** seed data and API endpoints have a working database.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- infrastructure] |
| Act | Setup |

**Acceptance criteria:**
- [ ] Neon database provisioned (eu-central-1)
- [ ] `DATABASE_URL` in `backend/.env`
- [ ] All 13 tables from ERD created: firm, user, customer, quote, quote_line_item, project, project_line_item, job_type, article, event, cl_benchmark, firm_benchmark, article_price_history
- [ ] All enums created: segment, role, customer_type, quote_status, project_status, line_category, unit, cl_metric, event_type, event_entity_type
- [ ] All indexes created per ERD
- [ ] SQLAlchemy models match DBML schema (field names, types, nullable, defaults)
- [ ] Alembic initial migration generated and applied
- [ ] `backend/main.py` connects to DB on startup (health endpoint returns DB status)

**Tasks:**
1. Provision Neon project and obtain connection string
2. Create `backend/.env` with DATABASE_URL and ANTHROPIC_API_KEY
3. Create SQLAlchemy models in `backend/models/` -- one file per logical group (core.py, quote.py, project.py, reference.py, event.py, cl.py)
4. Create enum types matching DBML
5. Configure Alembic
6. Generate and apply initial migration
7. Update health endpoint to test DB connection
8. Commit

---

#### E0-S5: API health + frontend shell + CORS

**As a** builder, **when** database and seed data exist, **I want** the frontend to successfully call the backend API **so that** I can verify the full stack works end-to-end before deploying.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- infrastructure] |
| Act | Setup |

**Acceptance criteria:**
- [ ] Backend `/health` endpoint returns `{"status": "ok", "db": "connected", "firm_count": 2}`
- [ ] Frontend has `api.ts` with base URL config (localhost:8000 for dev, production URL for deploy)
- [ ] Frontend App.tsx renders a shell: header with app name + role switcher placeholder, main content area, minimal Tailwind styling
- [ ] Frontend calls `/health` on mount and displays connection status (dev aid, can be removed later)
- [ ] CORS configured: allow frontend origin
- [ ] pytest installed, one test: `test_health_returns_ok`
- [ ] Both dev servers start without errors

**Tasks:**
1. Update `backend/main.py` health endpoint to query DB
2. Create `frontend/src/api.ts` with fetch wrapper and base URL config
3. Create minimal `App.tsx` shell with Tailwind
4. Add pytest to requirements.txt, create `backend/tests/test_health.py`
5. Verify frontend -> backend communication
6. Commit

---

#### E0-S6: Deploy to Render (EARLY -- before seed data)

**As a** builder, **when** the API health and frontend shell work locally, **I want** to deploy immediately to Render **so that** every subsequent epic builds on something already live and I never debug infrastructure in hour 4.

**Build order note:** Moved ahead of E0-S3/S4 (seed data). Deploy a working hello-world first. Seed data deploys via auto-deploy on next push.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- infrastructure] |
| Act | Setup |

**Acceptance criteria:**
- [ ] GitHub repo created and code pushed
- [ ] Render Static Site configured for frontend (build: `cd frontend && npm install && npm run build`, publish: `frontend/dist`)
- [ ] Render Web Service configured for backend (build: `cd backend && pip install -r requirements.txt`, start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`)
- [ ] Environment variables set on Render: DATABASE_URL, ANTHROPIC_API_KEY
- [ ] Frontend `api.ts` base URL points to Render backend URL in production
- [ ] Live URL returns health check OK
- [ ] Seed data is accessible via API (at minimum: `/api/firms` or health endpoint shows firm_count=2)

**Tasks:**
1. Create GitHub repo
2. Push code
3. Create Render Static Site for frontend
4. Create Render Web Service for backend
5. Set env vars on Render
6. Update frontend api.ts with production backend URL
7. Verify live deployment
8. Commit any config changes

---

#### E0-S3: Seed data -- reference tables

**As a** builder, **when** the database schema exists, **I want** reference and identity data seeded (firms, users, customers, job types, articles) **so that** the application has a working context for all features.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- infrastructure] |
| Act | Setup |

**Acceptance criteria:**
- [ ] 2 firms seeded: (1) "Weber Haustechnik GmbH" -- micro, segment=shk, region=Niedersachsen, country=DE, currency=EUR, employee_count=4; (2) "Neuer Betrieb" -- micro, segment=shk, empty/fresh, same country/currency
- [ ] 3 users for Weber firm: Meister Weber (role=meister), Geselle Hoffmann (role=geselle), Burokraft Yilmaz (role=buero). Language=de for all.
- [ ] 3-5 customers for Weber firm: residential and commercial, different German postal codes (Hannover 30xxx, Hamburg 20xxx, Braunschweig 38xxx)
- [ ] 5+ SHK job types: Heizungstausch, Badsanierung, Wartung, Rohrbruch, Waermepumpe-Installation. Segment=shk. avg_duration_h and avg_margin_pct populated.
- [ ] 20-30 SHK articles: copper pipe 15mm, copper pipe 22mm, radiator type 22, thermostatic valve, circulation pump, gas condensing boiler, heat pump unit, etc. Realistic prices in EUR. Unit types correct (meters, pieces, etc.)
- [ ] Seed is idempotent (re-runnable without duplicates)
- [ ] Seed runs as a script or management command: `python seed.py` or similar

**Tasks:**
1. Create `backend/seed.py`
2. Define firm records (2 firms with all ERD fields)
3. Define user records (3 users, all linked to Weber firm)
4. Define customer records (3-5, various regions)
5. Define job_type records (5+ SHK types with CL-derived fields populated)
6. Define article records (20-30 realistic SHK materials with prices, units, datanorm_id placeholders)
7. Use SQLAlchemy sessions with merge-on-conflict for idempotency
8. Run seed, verify data
9. Commit

---

#### E0-S4: Seed data -- historical (projects, events, benchmarks, price history)

**As a** builder, **when** reference tables are seeded, **I want** historical project data, events, benchmarks, and price history seeded **so that** the CL overlay and post-calc views have realistic data to display.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- infrastructure] |
| Act | Setup |

**Acceptance criteria:**
- [ ] 3 active projects (status=planned or active, with planned_hours/planned_cost but no actuals yet) and 5 completed projects (status=completed, actual_hours and actual_cost populated) for Weber firm, linked to customers and job types. Each has a linked quote (status=accepted).
- [ ] QuoteLineItems for each quote (3-6 line items per quote, mix of labor and material, articles from catalog)
- [ ] ProjectLineItems for each project, linked to corresponding QuoteLineItems. Actuals differ from quoted (some over, some under -- realistic variance)
- [ ] At least one project shows significant margin gap (hours exceeded by 20%+ or material cost exceeded by 15%+) -- this is the key insight moment.
- [ ] Event records for all 5 projects: at minimum created and status_changed events. At least one quote has an "updated" event showing a price change (the audit trail demo).
- [ ] FirmBenchmark records for Weber firm: at least 3 job types, metrics duration_h and margin_pct. Currency=EUR. Period covers last 12 months.
- [ ] CLBenchmark records: same 3+ job types, same metrics. p25/p50/p75/mean populated with realistic values. Region=Niedersachsen. Currency=EUR. Sample sizes in hundreds/thousands.
- [ ] ArticlePriceHistory: copper pipe 15mm with 6 monthly data points showing upward trend (+8% over 30 days). 2-3 other articles with mild fluctuations.
- [ ] All seed data tells a coherent story: Weber firm is slightly slower than platform median on bathroom renovations, on par for heating, and underquotes materials.

**Tasks:**
1. Extend `backend/seed.py` with historical data section
2. Create 5 quotes with line items (use article IDs from E0-S3)
3. Create 5 projects linked to quotes, with line items showing actuals
4. Generate event records for quote creation, updates, status transitions
5. Create FirmBenchmark records (Weber firm, 3-4 job types, 2 metrics each)
6. Create CLBenchmark records (platform-wide, same job types, broader sample sizes)
7. Create ArticlePriceHistory records (copper pipe hero, 2-3 supporting articles)
8. Verify the narrative is coherent: run a quick query to compare firm vs. platform medians
9. Commit

---

### Epic E1: Migration Onboarding

**Goal:** An existing customer clicks "Import" and their historical data becomes day-one intelligence. The demo opens here -- this is Act 1. The viewer sees that existing customers are safe and their data is MORE valuable in the new system.

**Time budget:** 45 minutes

**Depends on:** E0 complete (deployed, seeded shell)

---

#### E1-S1: Onboarding screen with two paths

**As a** new user, **when** I open the application for the first time, **I want** to choose between importing my existing data or starting fresh **so that** I can get started in the way that matches my situation.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | onboarding |
| JTBD outcome | [not applicable -- business model] |
| Act | Act 1 (retain) + Act 3 (acquire) |

**Acceptance criteria:**
- [ ] Full-screen onboarding view with two clear paths
- [ ] Path 1: "Daten aus Taifun importieren" -- prominent, primary action (this is the common case for existing customers)
- [ ] Path 2: "Neu starten -- ohne bestehende Daten" -- secondary action
- [ ] Clean, professional design. Not a form -- a choice. Two cards or two buttons with brief descriptions.
- [ ] Path 1 description: "Ihre Taifun- oder SmartHandwerk-Daten werden importiert. Sofortiger Zugriff auf Ihren Betriebsvergleich."
- [ ] Path 2 description: "Starten Sie ohne historische Daten. Der Plattform-Vergleich steht sofort zur Verfuegung."
- [ ] Selecting a path navigates to the appropriate flow (E1-S2 or E3-S1)
- [ ] No authentication UI. The onboarding is the entry point.

---

#### E1-S2: Taifun import flow (simulated)

**As an** existing customer, **when** I choose "Taifun importieren," **I want** to see my historical data loading into the new system **so that** I trust that my business data is safe and immediately useful.

| Tag | Value |
|-----|-------|
| Kano | performance |
| Product area | onboarding |
| JTBD outcome | [not applicable -- business model: retention] |
| Act | Act 1 (retain) |

**Acceptance criteria:**
- [ ] After selecting "Taifun importieren," a simulated import sequence plays:
  - Step indicator or progress animation (not a spinner -- show what's happening)
  - "Kundendaten werden importiert... 23 Kunden gefunden"
  - "Projekte werden importiert... 5 abgeschlossene Projekte"
  - "Angebote werden importiert... 147 Positionen"
  - "Betriebsvergleich wird berechnet..."
- [ ] Animation takes 3-5 seconds total (not instant -- the wait builds trust that something real is happening)
- [ ] On completion, navigates to Dashboard (E1-S3) with Weber firm context active
- [ ] Backend: `/api/onboarding/import` endpoint switches the active firm context to the pre-seeded Weber firm (no actual import logic -- the data is already seeded)
- [ ] The import is a simulation. Under the hood it activates the pre-seeded Weber firm data. This is fine for a prototype.

---

#### E1-S3: Dashboard -- populated state

**As a** Meister, **when** my data has been imported, **I want** to see an overview of my business with immediate CL insights **so that** I understand the value of the new system from the first screen.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | dashboard |
| JTBD outcome | Minimize the time it takes to know whether a job was profitable before accepting the next one [A9, the gap] |
| Act | Act 1 (retain) |

**Acceptance criteria:**
- [ ] Header: firm name ("Weber Haustechnik GmbH"), active user + role, role switcher control
- [ ] Summary cards: Offene Angebote (count), Aktive Projekte (count), Abgeschlossene Projekte (count)
- [ ] CL insight panel: "Ihr Betriebsvergleich" showing FirmBenchmark vs. CLBenchmark for 2-3 job types. E.g.: "Badsanierung: Ihr Betrieb Ø 14h / Plattform Ø 12h" and "Heizungstausch: Ihr Betrieb Ø 18h / Plattform Ø 16h"
- [ ] Recent quotes list (from seed data): quote number, customer name, job type, status, total
- [ ] Recent projects list: project, customer, status, margin indicator (green/yellow/red)
- [ ] Navigation: "Neues Angebot" button (prominent) links to quote creation (E2-S1)
- [ ] Clicking a project navigates to Project Detail (E2-S7)
- [ ] Data loads from backend API endpoints: `/api/firms/{id}/dashboard` or similar aggregation endpoint

---

#### E1-S4: Migration narrative in UI

**As a** demo viewer, **when** seeing the populated dashboard, **I want** a clear indicator that this data came from a legacy system **so that** I understand the migration value proposition.

| Tag | Value |
|-----|-------|
| Kano | excitement |
| Product area | onboarding |
| JTBD outcome | [not applicable -- business model: "install base as asset"] |
| Act | Act 1 (retain) |

**Acceptance criteria:**
- [ ] A banner or subtle indicator on the dashboard after import: "Diese Daten stammen aus Ihrem Taifun-Export. 5 Projekte, 23 Kunden, 147 Positionen."
- [ ] The banner is dismissible (X button)
- [ ] Past projects and quotes in lists show a small "Importiert" badge or tag
- [ ] The CL insight panel shows: "Betriebsvergleich berechnet aus Ihren importierten Daten." -- making explicit that historical data powers day-one intelligence
- [ ] This narrative is only visible for the migrated firm, not for the new firm (E3)

---

### Epic E2: AI Quote + Crowd Learning

**Goal:** The hero flow. A craftsman describes a job, AI generates a structured quote, CL intelligence overlays pricing and margin context. Role-differentiated views. Audit trail. Post-calculation on past projects. Voice input.

**Time budget:** 2 hours

**Depends on:** E0 complete, E1-S3 (dashboard provides navigation entry point)

---

#### E2-S1: Quote creation -- text input to AI-generated structured quote

**As a** Meister, **when** I need to create a quote for a customer, **I want** to describe the job in plain German and get a structured Leistungsverzeichnis **so that** I save hours of manual data entry and never miss a line item.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | quotes (A2) |
| JTBD outcome | Minimize the time it takes to create and send a quote including materials from wholesaler catalogues [A2] |
| Act | Act 2 (product) |

**Acceptance criteria:**
- [ ] "Neues Angebot" screen with: customer selector (dropdown from seeded customers), job type selector (from seeded job types), and free-text input area
- [ ] Text input placeholder: "Beschreiben Sie den Auftrag..." with example: "Heizungstausch Einfamilienhaus, Altbau 1965, Keller, 24kW Gasbrennwert raus, Waermepumpe rein"
- [ ] "Angebot erstellen" button sends job description to backend
- [ ] Backend `/api/quotes/generate` endpoint: sends job description + customer context + article catalog (names + prices from DB) to Claude API
- [ ] Claude API system prompt instructs: generate a structured quote as JSON with line items (description, category, quantity, unit, unit_price, total), linking to articles from the catalog where possible
- [ ] Response parsed into QuoteLineItem structure and displayed as an editable table
- [ ] Line items show: position #, description, category (Arbeit/Material), quantity, unit, unit price, total
- [ ] Totals calculated: Netto, MwSt (19%), Brutto
- [ ] Quote saved to DB as draft (status=draft) with all line items
- [ ] Event created: type=created, entity_type=quote
- [ ] Loading state while AI generates (skeleton or spinner with "Angebot wird erstellt...")
- [ ] **Cached fallback quote:** Pre-generate a complete Heizungstausch quote JSON (line items, articles, totals) stored in `backend/fallback_quotes/`. If Claude API response takes >5 seconds or fails, load the fallback and display with a subtle "Demo-Modus" indicator. This is the single biggest demo risk -- non-negotiable.
- [ ] If AI call fails, fall back to cached quote (not an error screen)

---

#### E2-S2: CL overlay -- FirmBenchmark + CLBenchmark on quote

**As a** Meister, **when** viewing a generated quote, **I want** to see how my pricing compares to my own history and the platform **so that** I can make informed pricing decisions and stop leaving money on the table.

| Tag | Value |
|-----|-------|
| Kano | performance |
| Product area | quotes (A2) |
| JTBD outcome | Minimize the gap between estimated and actual costs on complex SHK projects [A2] |
| Act | Act 2 (product) |

**Acceptance criteria:**
- [ ] CL panel appears alongside or below the quote line items (not a modal -- always visible)
- [ ] Panel title: "Crowd Learning -- Ihr Vergleich"
- [ ] FirmBenchmark row: "Ihr Betrieb (letzte 12 Monate)" with metric values for this job type. E.g.: "Ø Dauer: 18h, Ø Angebotssumme: EUR 12.400, Ø Marge: 21%"
- [ ] CLBenchmark row: "Plattform (1.247 Betriebe)" with p50 values. E.g.: "Ø Dauer: 16h, Ø Angebotssumme: EUR 11.800, Ø Marge: 26%"
- [ ] Visual indicator for each metric: green (at or above platform), yellow (within 10%), red (>10% below)
- [ ] Sample size displayed for platform benchmark ("basierend auf 1.247 Betrieben in Ihrer Region")
- [ ] Data loaded from backend: `/api/benchmarks/{job_type_id}?firm_id={id}` returning both FirmBenchmark and CLBenchmark for the selected job type
- [ ] If FirmBenchmark doesn't exist for this job type (new job type for the firm), show only platform benchmark with note: "Keine Betriebsdaten fuer diesen Auftragstyp. Plattform-Vergleich verfuegbar."

---

#### E2-S3: Margin forecast on quote

**As a** Meister, **when** reviewing a quote before sending, **I want** a margin prediction based on my history and platform data **so that** I know whether this quote will be profitable before I commit.

| Tag | Value |
|-----|-------|
| Kano | performance |
| Product area | quotes (A2) |
| JTBD outcome | Minimize the gap between estimated and actual costs [A2] |
| Act | Act 2 (product) |

**Acceptance criteria:**
- [ ] Margin forecast section within or adjacent to CL panel
- [ ] Calculation: (quote total - estimated cost) / quote total * 100
- [ ] Estimated cost derived from FirmBenchmark actuals (if available) or CLBenchmark p50
- [ ] Display: "Bei diesen Preisen: erwartete Marge 19%. Ihr Ziel: 25%. Plattform-Median: 26%."
- [ ] Color coding: green (>= target), yellow (within 5% of target), red (>5% below target)
- [ ] Margin target defaults to firm average or 25% if no firm data
- [ ] If no FirmBenchmark, forecast uses platform median only

---

#### E2-S4: Material cost trend signal

**As a** Meister, **when** creating a quote with materials, **I want** to see price trend warnings for volatile articles **so that** I don't underquote because I used last month's prices.

| Tag | Value |
|-----|-------|
| Kano | excitement |
| Product area | quotes (A2) |
| JTBD outcome | Reduce the effort required to compare supplier prices at point of ordering [A2] |
| Act | Act 2 (product) |

**Acceptance criteria:**
- [ ] For quote line items linked to articles that have ArticlePriceHistory, show a trend indicator
- [ ] Indicator format: small badge or icon on the line item row. E.g.: "up-arrow +8% (30 Tage)" in orange/red, or "arrow-right stabil" in green
- [ ] Clicking/hovering the indicator shows: article name, current price, price 30 days ago, % change, mini sparkline (optional -- nice to have)
- [ ] Hero example: "Kupferrohr 15mm: EUR 4,85/m -> EUR 5,24/m (+8% in 30 Tagen)"
- [ ] Data from backend: `/api/articles/{id}/price-history` returning last 6 months of price records
- [ ] Only shown for articles with price history. No indicator if no history exists.

---

#### E2-S5: Role switcher + role-differentiated views

**As a** demo presenter, **when** showing the product, **I want** to switch between Meister/Geselle/Burokraft roles **so that** I can demonstrate that different users see different perspectives on the same data.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | quotes (A2) |
| JTBD outcome | [not applicable -- multi-user coordination] |
| Act | Act 2 (product) |

**Acceptance criteria:**
- [ ] Role switcher in application header: dropdown or segmented control showing current user name + role
- [ ] 3 options: "Meister Weber", "Geselle Hoffmann", "Burokraft Yilmaz"
- [ ] Switching role updates a client-side context (stored in React state or context provider). No backend auth.
- [ ] **Meister view:** Full access. All CL data, margins, pricing, benchmarks visible. Can create/edit quotes.
- [ ] **Geselle view:** Sees quote scope (line items, quantities, materials) but NOT margin data, NOT pricing benchmarks, NOT FirmBenchmark financials. Can view assigned projects. The message: "The Geselle sees the job, not the margin."
- [ ] **Burokraft view:** Sees quote status, customer info, event trail (audit). Focus on compliance and admin. Can see totals but not CL benchmarks.
- [ ] Role switching on quote detail immediately hides/shows the appropriate panels (no page reload)
- [ ] Header shows current role context: name, role label, and firm name

---

#### E2-S6: Event trail (audit log) on quotes

**As a** Meister or Burokraft, **when** viewing a quote, **I want** to see a chronological trail of all changes **so that** I have an audit-ready record of who changed what and when (GoBD-relevant).

| Tag | Value |
|-----|-------|
| Kano | performance |
| Product area | quotes (A2) |
| JTBD outcome | Increase the share of invoices that are audit-ready without extra effort [A7] |
| Act | Act 2 (product) |

**Acceptance criteria:**
- [ ] Event trail section on quote detail view (collapsible panel or sidebar)
- [ ] Each event shows: timestamp (German format), actor name + role, event type, and change description
- [ ] Example: "12. Apr 2026, 14:33 -- Meister Weber: Preis geaendert von EUR 3.600 auf EUR 4.200"
- [ ] Events ordered newest-first (most recent at top)
- [ ] Data from backend: `/api/events?entity_type=quote&entity_id={id}` returning all events for this quote
- [ ] At least one seeded quote has multiple events (created + updated) so the trail is not empty
- [ ] Visual distinction between event types (e.g., status change vs. price change)

---

#### E2-S7: Project detail -- post-calculation view

**As a** Meister, **when** a project is completed, **I want** to compare quoted vs. actual numbers **so that** I learn from every job and improve my next quote.

| Tag | Value |
|-----|-------|
| Kano | performance |
| Product area | post-calc (A9) |
| JTBD outcome | Minimize the time it takes to know whether a job was profitable before accepting the next one [A9, the gap -- nobody solves this] |
| Act | Act 2 (product) |

**Acceptance criteria:**
- [ ] Project detail screen accessible from dashboard (clicking a completed project)
- [ ] Header: project name/number, customer, job type, status badge ("Abgeschlossen"), dates
- [ ] **Quoted vs. Actual comparison table:** side-by-side for each line item
  - Columns: Position, Beschreibung, Geplant (qty, price, total), Tatsaechlich (qty, price, total), Differenz (absolute + %)
  - Line items color-coded: green (actual <= quoted), red (actual > quoted)
- [ ] **Summary row:** total quoted vs. total actual, overall margin
- [ ] **Hours comparison:** planned_hours vs. actual_hours, with delta. "Geplant: 10h, Tatsaechlich: 14h (+40%)"
- [ ] **CL context panel:** FirmBenchmark for this job type ("Ihr Durchschnitt ueber alle Badsanierungen: Ø 14h") + CLBenchmark ("Plattform: Ø 12h"). Same layout as E2-S2.
- [ ] **The learning signal:** explicit text like "Dieses Projekt lag 22% ueber Ihrer Kalkulation. Bei Ihrem naechsten Badsanierungs-Angebot wird dieser Erfahrungswert beruecksichtigt."
- [ ] Event trail for this project (same component as E2-S6, reused)
- [ ] Data from backend: `/api/projects/{id}` with line items, linked quote line items, events, benchmarks

---

#### E2-S8: Voice input for quote creation

**As a** Meister on a job site, **when** I want to create a quote quickly, **I want** to describe the job by speaking into my phone **so that** I can send a quote from the site without typing.

| Tag | Value |
|-----|-------|
| Kano | excitement |
| Product area | quotes (A2) |
| JTBD outcome | Minimize the time it takes to create and send a quote including materials from wholesaler catalogues [A2] |
| Act | Act 2 (product) |

**Acceptance criteria:**
- [ ] Microphone button next to the text input on quote creation screen
- [ ] Clicking starts browser SpeechRecognition API (Web Speech API)
- [ ] Visual indicator that recording is active (pulsing icon, red dot, or similar)
- [ ] Speech transcribed to German text in real-time, populating the text input field
- [ ] Clicking again (or silence timeout) stops recording
- [ ] Transcribed text can be edited before submitting
- [ ] Same "Angebot erstellen" flow as E2-S1 -- voice is just an input method, not a separate pipeline
- [ ] **Browser gating:** Check for SpeechRecognition API support on mount. If unsupported (Firefox, Safari), hide the microphone button entirely -- text input remains prominent. Do NOT show a broken or greyed-out mic. Chrome-only feature; don't let it become the thing that breaks.
- [ ] Language set to 'de-DE' for recognition
- [ ] **Cut priority:** This is the first excitement-tier story to cut if running over time. Text-to-quote is the must-be; voice is the delight.

---

### Epic E3: New User Onboarding

**Goal:** A firm that was never a customer signs up in a browser and gets instant value from platform CL. No install, no migration, no legacy history. This is the PLG pitch -- Act 3.

**Time budget:** 30 minutes

**Depends on:** E0 complete, E1-S1 (shared onboarding screen), E2 (quote flow exists to reuse)

---

#### E3-S1: New user onboarding path

**As a** craftsperson without existing legacy products, **when** I choose "Neu starten," **I want** to set up my firm in under a minute with no install **so that** I can start using the product immediately.

| Tag | Value |
|-----|-------|
| Kano | performance |
| Product area | onboarding |
| JTBD outcome | [not applicable -- business model: acquisition/PLG] |
| Act | Act 3 (acquire) |

**Acceptance criteria:**
- [ ] After selecting "Neu starten" on onboarding screen, a simple setup form:
  - Firm name (text input)
  - Trade/Segment (dropdown: SHK, Elektro, ...) -- preselect SHK for demo
  - Firm size (radio: "1 Person", "2-4 Personen", "5-12 Personen") -- preselect "2-4 Personen" for Micro
  - Region (dropdown or text: Bundesland) -- preselect Niedersachsen
- [ ] "Loslegen" button creates firm context (activates pre-seeded empty firm with updated name/segment/size)
- [ ] No email, no password, no verification. This is SaaS onboarding at its simplest.
- [ ] Completion navigates to Dashboard in new-firm context (E3-S2)
- [ ] Backend: `/api/onboarding/new` endpoint activates the pre-seeded empty firm, updates display name

---

#### E3-S2: Dashboard -- sparse state (new firm)

**As a** new user, **when** I complete onboarding without historical data, **I want** to see a useful dashboard that isn't empty **so that** I feel the product is already valuable without my own data.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | dashboard |
| JTBD outcome | [not applicable -- business model: PLG first impression] |
| Act | Act 3 (acquire) |

**Acceptance criteria:**
- [ ] Same dashboard layout as E1-S3 but adapted for empty firm state
- [ ] Summary cards show zeros: "0 Angebote", "0 Projekte"
- [ ] **CL panel is NOT empty.** Shows platform benchmarks: "Plattform-Vergleich fuer SHK-Betriebe in Niedersachsen" with CLBenchmark data for key job types
- [ ] Welcome message: "Willkommen. Sie haben noch keine Projekte. Der Plattform-Vergleich mit [sample_size] Betrieben steht Ihnen ab sofort zur Verfuegung."
- [ ] "Neues Angebot" button is prominent -- the CTA is to create the first quote
- [ ] Future state teaser: "Nach Ihren ersten 5 abgeschlossenen Auftraegen berechnen wir Ihren individuellen Betriebsvergleich."
- [ ] No "Importiert" badges, no migration banner. Clean state.
- [ ] No empty-state sadness (no sad illustrations, no "nothing here yet" -- the CL data IS the value)

---

#### E3-S3: CL-only overlay for new firm

**As a** new user without firm history, **when** I create a quote, **I want** to see platform benchmarks **so that** I get intelligent pricing guidance from day one, even without my own data.

| Tag | Value |
|-----|-------|
| Kano | performance |
| Product area | quotes (A2) |
| JTBD outcome | Minimize the gap between estimated and actual costs on complex SHK projects [A2] |
| Act | Act 3 (acquire) |

**Acceptance criteria:**
- [ ] Same CL panel as E2-S2 but shows only CLBenchmark (platform) row
- [ ] FirmBenchmark row replaced with: "Noch keine Betriebsdaten -- Plattform-Vergleich aktiv"
- [ ] Platform data displays normally: "Plattform (1.247 Betriebe): Ø Dauer 16h, Ø Angebotssumme EUR 11.800, Ø Marge 26%"
- [ ] Margin forecast (E2-S3) still works using platform data as reference: "Erwartete Marge: 22%. Plattform-Median: 26%."
- [ ] The CL panel explicitly states: "Nach Ihren ersten 5 Auftraegen vergleichen wir Ihre Werte mit der Plattform."
- [ ] This is the same CL component as E2-S2 with a conditional: if FirmBenchmark exists, show both; if not, show platform only with guidance text.

---

### Epic E4: Polish + Hardening

**Goal:** A viewer can navigate the live product without hitting dead ends or broken states. All text is German. Visual design is clean and professional.

**Time budget:** 45 minutes

**Depends on:** E0-E3 functionally complete

---

#### E4-S1: Navigation hardening

**As a** user, **when** clicking through the prototype during a demo, **I want** every click to lead somewhere meaningful **so that** the product feels real and trustworthy.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- demo quality] |
| Act | All |

**Acceptance criteria:**
- [ ] Every visible link/button leads to a real screen or shows a clear "Kommt bald" placeholder
- [ ] Back navigation works (browser back button doesn't break state)
- [ ] Switching between migrated firm and new firm doesn't corrupt state (firm context is clean)
- [ ] Switching roles doesn't break the current view
- [ ] API errors show a German error message, not a stack trace
- [ ] Empty states have meaningful messages (no blank screens, no "undefined")
- [ ] App header with firm name + role is present on every screen
- [ ] Navigation is consistent: back to dashboard from any detail view

---

#### E4-S2: Visual polish

**As a** viewer, **when** seeing the prototype, **I want** it to look clean and professional **so that** the product vision is taken seriously.

| Tag | Value |
|-----|-------|
| Kano | performance |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- demo quality] |
| Act | All |

**Acceptance criteria:**
- [ ] Consistent color scheme (Tailwind defaults are fine -- blue primary, gray secondary, green/yellow/red for CL indicators)
- [ ] Typography hierarchy: clear headings, readable body text, data tables with good contrast
- [ ] Cards/panels have consistent spacing and borders
- [ ] CL panel is visually distinct (highlighted background, different border) -- it's the special thing
- [ ] Quote line item table is readable and well-aligned
- [ ] Loading states are smooth (no layout jumping)
- [ ] Mobile-responsive: content doesn't overflow on smaller viewports (not optimized, just not broken)

---

#### E4-S3: German UI text audit

**As a** German-speaking user, **when** using the product, **I want** all text to be in natural, professional German **so that** the product feels native, not translated.

| Tag | Value |
|-----|-------|
| Kano | must-be |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- localization quality] |
| Act | All |

**Acceptance criteria:**
- [ ] All UI labels, buttons, headings, placeholders in German
- [ ] No English text visible in the UI (variable names in code are English, but nothing user-facing)
- [ ] Professional register: "Sie" (formal), not "du." This is business software.
- [ ] Currency formatted correctly: "EUR 4.200,00" (German: dot for thousands, comma for decimals)
- [ ] Date formatted correctly: "12. Apr 2026" or "12.04.2026"
- [ ] Numbers formatted: "1.247 Betriebe" (German: dot for thousands)
- [ ] CL-specific terms consistent: "Betriebsvergleich" (firm benchmark), "Plattform-Median" (platform benchmark), "Crowd Learning" (keep English -- it's the product term)

---

#### E4-S4: Responsive layout check

**As a** viewer on mobile, **when** pulling out a phone, **I want** the app to be usable on a mobile screen **so that** the "mobile-first for craftsmen" narrative is credible.

| Tag | Value |
|-----|-------|
| Kano | indifferent |
| Product area | infrastructure |
| JTBD outcome | [not applicable -- demo quality] |
| Act | All |

**Acceptance criteria:**
- [ ] All 4 screens render without horizontal overflow on 375px width (iPhone SE)
- [ ] Text is readable without zooming
- [ ] Buttons/links are tappable (min 44px touch targets)
- [ ] Tables scroll horizontally if too wide (not broken layout)
- [ ] Role switcher is accessible on mobile (not hidden behind a desktop-only menu)

---

## 4. Cross-Cutting Concerns

These apply to ALL stories and should be in the prototype CLAUDE.md:

| Concern | Rule |
|---------|------|
| **Language** | All UI text in German. "Sie" register. Code in English. |
| **Database** | Every write creates an Event record for tracked entities (quote, quote_line_item, project, project_line_item) |
| **Firm context** | Active firm_id is stored client-side (React context). All API calls include firm_id. |
| **Role context** | Active user_id/role is stored client-side. API calls include user_id for created_by/actor_id. Role affects UI visibility. |
| **Testing** | One pytest per API endpoint. Assert status code + response structure. No frontend tests. |
| **Error handling** | API returns German error messages. Frontend shows them in a toast/alert. No stack traces in UI. |
| **Commits** | One commit per story. Message: "E{n}-S{m}: {story title}" |

---

## 5. Seed Data Summary

Detailed fixture design for E0-S3 and E0-S4. The builder should generate exact values, but here are the constraints:

### Firms

| Firm | Segment | Region | Employees | Country | Currency | Purpose |
|------|---------|--------|-----------|---------|----------|---------|
| Weber Haustechnik GmbH | shk | Niedersachsen | 4 | DE | EUR | Migrated (Act 1). Has history. |
| [entered by user at onboarding] | shk | [entered] | [entered] | DE | EUR | New (Act 3). Empty. |

### Users (Weber firm)

| Name | Role | Language |
|------|------|----------|
| Stefan Weber | meister | de |
| Jan Hoffmann | geselle | de |
| Elif Yilmaz | buero | de |

### Customers (Weber firm)

| Name | Type | Postal code | City |
|------|------|-------------|------|
| Familie Mueller | residential | 30159 | Hannover |
| Hausverwaltung Schmidt GmbH | commercial | 20095 | Hamburg |
| Familie Braun | residential | 38100 | Braunschweig |
| Gemeinde Langenhagen | public | 30853 | Langenhagen |

### Job Types (SHK)

| Name | Avg duration (from CL) | Avg margin (from CL) |
|------|----------------------|---------------------|
| Heizungstausch | 16h | 26% |
| Badsanierung | 12h | 24% |
| Wartung Heizungsanlage | 3h | 35% |
| Rohrbruch-Reparatur | 4h | 30% |
| Waermepumpe-Installation | 24h | 22% |

### Projects (Weber firm -- the narrative)

| # | Customer | Job type | Quoted total | Actual total | Quoted hours | Actual hours | Key story point |
|---|----------|----------|-------------|-------------|-------------|-------------|----------------|
| 1 | Mueller | Badsanierung | EUR 8.500 | EUR 9.200 | 10h | 14h | Hours exceeded by 40%. Material cost +8%. Key insight moment. |
| 2 | Schmidt GmbH | Heizungstausch | EUR 12.400 | EUR 12.100 | 18h | 17h | On par. Slight profit. |
| 3 | Braun | Badsanierung | EUR 7.200 | EUR 8.400 | 11h | 13h | Another bathroom overrun. Pattern visible. |
| 4 | Langenhagen | Wartung | EUR 1.800 | EUR 1.750 | 3h | 2.5h | Profitable. Maintenance is Weber's sweet spot. |
| 5 | Mueller | Rohrbruch | EUR 2.200 | EUR 2.600 | 4h | 5.5h | Emergency job. Underquoted time. |

**Narrative this tells:** Weber consistently underquotes bathroom renovations (pattern). Maintenance and heating are on track. The CL system flags this: "Ihre Badsanierungen liegen 22% ueber der Kalkulation. Plattform-Median: 12h. Ihr Durchschnitt: 13.5h."

### FirmBenchmark (Weber)

| Job type | Metric | Mean | Period |
|----------|--------|------|--------|
| Badsanierung | duration_h | 13.5 | Last 12 months |
| Badsanierung | margin_pct | 16 | Last 12 months |
| Heizungstausch | duration_h | 17 | Last 12 months |
| Heizungstausch | margin_pct | 24 | Last 12 months |
| Wartung | duration_h | 2.5 | Last 12 months |
| Wartung | margin_pct | 38 | Last 12 months |

### CLBenchmark (Platform)

| Job type | Metric | p25 | p50 | p75 | Mean | Sample size |
|----------|--------|-----|-----|-----|------|-------------|
| Badsanierung | duration_h | 10 | 12 | 15 | 12.3 | 3,420 |
| Badsanierung | margin_pct | 18 | 24 | 30 | 23.8 | 3,420 |
| Heizungstausch | duration_h | 14 | 16 | 20 | 16.8 | 2,890 |
| Heizungstausch | margin_pct | 20 | 26 | 32 | 25.4 | 2,890 |
| Wartung | duration_h | 2 | 3 | 4 | 3.1 | 8,120 |
| Wartung | margin_pct | 28 | 35 | 42 | 34.7 | 8,120 |
| Rohrbruch | duration_h | 3 | 4 | 6 | 4.3 | 1,670 |
| Rohrbruch | margin_pct | 22 | 30 | 36 | 29.1 | 1,670 |
| Waermepumpe | duration_h | 20 | 24 | 30 | 24.6 | 890 |
| Waermepumpe | margin_pct | 16 | 22 | 28 | 21.5 | 890 |

### ArticlePriceHistory (copper pipe hero)

| Article | Month | Price (EUR/m) |
|---------|-------|--------------|
| Kupferrohr 15mm | Oct 2025 | EUR 4.42 |
| Kupferrohr 15mm | Nov 2025 | EUR 4.51 |
| Kupferrohr 15mm | Dec 2025 | EUR 4.58 |
| Kupferrohr 15mm | Jan 2026 | EUR 4.72 |
| Kupferrohr 15mm | Feb 2026 | EUR 4.85 |
| Kupferrohr 15mm | Mar 2026 | EUR 5.24 |

---

*Backlog created April 12, 2026.*
*Reference docs: prototype-scope.md, erd.md, user-story-map.md, design-rationale.md*

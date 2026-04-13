# Prototype Scope -- AI-Native Trade Software

**Status:** LOCKED
**Build day:** Monday April 13, 2026
**Time budget:** 5 hours
**Stack:** React + Vite + TypeScript + Tailwind (frontend), FastAPI + Python (backend), Neon Postgres (DB), Anthropic Claude API (AI), Render (deploy)

---

## What the Demo Proves

The product addresses three problems for a trade software company with ~22,000 customers on legacy ERP systems:

| Problem | What it means | What the demo shows |
|---------|--------------|-------------------|
| **(b) Retain** | Existing customers on aging software. Any reset risks losing them. | **Act 1:** Migration. Legacy data imports in one click. History becomes day-one intelligence. The install base is an asset, not a liability. |
| **Product** | Competitors are AI-native. Legacy products cannot evolve fast enough. | **Act 2:** The product. Voice-to-quote, CL overlay, audit trail. A new generation of trade software. |
| **(a) Acquire** | Current products don't reach firms that aren't already customers. PLG is impossible on legacy software. | **Act 3:** New user onboarding. No install, no legacy history, instant value from platform CL. PLG for the Micro segment. |

**(c) Margin** is not demoed -- it's argued verbally. "This took one person one day. The new stack is fundamentally cheaper to build on. Now imagine what a team of five does in a quarter."

---

## Demo Script (Three Acts)

### Act 1: Migration -- "Your data, instantly more valuable"

1. Onboarding screen. Two paths visible: "Daten aus Taifun importieren" and "Neu starten."
2. Click "Taifun importieren." Select firm. Animated import (simulated -- loads seed data).
3. Dashboard populates:
   - "5 Projekte importiert. 23 Kunden. 147 Positionen."
   - FirmBenchmark appears immediately: "Ihr Betrieb: Ø 14h Badezimmer-Sanierung. Plattform-Median: 12h."
   - "Diese Daten stammen aus Ihrem Taifun-Export."

### Act 2: The Product -- "Revolution, not evolution"

1. "Neues Angebot." Meister Weber describes a job -- by voice (browser Speech API) or text: "Heizungstausch Einfamilienhaus, Altbau 1965, Keller, 24kW Gasbrennwert raus, Wärmepumpe rein."
2. AI generates structured quote: line items, quantities, articles from catalog, pricing.
3. CL overlay lights up:
   - "Ihr Betrieb: letzte 3 Heizungswechsel Ø €12.400, Ø 18h"
   - "Plattform: Ø €11.800, Ø 16h. Ihr Materialanteil liegt 8% über Median."
   - "Kupferrohr 15mm: +8% in 30 Tagen. Preistrend beachten."
   - Margin forecast: "Bei diesen Preisen: erwartete Marge 19%. Ihr Ziel: 25%. Plattform-Median: 26%."
4. Role switcher: switch to Geselle Hoffmann. Same quote, but margin data hidden. Scope and materials visible.
5. Event trail: click on a past quote. "Angebot geändert: Preis von €3.600 auf €4.200 -- Meister Weber, 11. Apr 14:33." Audit-ready, GoBD-relevant.
6. Project detail: a completed past project. Actuals vs. quoted. Hours exceeded by 22%.

### Act 3: Acquisition -- "New users without our history"

1. Back to onboarding. Click "Neu starten -- kein Taifun."
2. Pick trade: SHK. Pick firm size: Micro (1 Meister, 2 Gesellen). Enter firm name.
3. Dashboard: empty of firm-specific data, but CL is live.
   - "Willkommen. Sie haben noch keine Projekte. Der Plattform-Vergleich steht Ihnen ab sofort zur Verfügung."
4. Create a quote. Same voice/text flow. CL overlay shows platform benchmarks only:
   - "Plattform-Median für Heizungstausch: €11.800, Ø 16h."
   - No FirmBenchmark yet -- "Nach Ihren ersten 5 Aufträgen berechnen wir Ihren Betriebsvergleich."

### Coda: Verbal mentions (not built)

- i18n: "The data model is i18n-ready. Currency and language on every entity. Switzerland is config, not code."
- MCP: "When Google's AI agent searches for a plumber in Hannover, this is what it finds." Verbal only.

**Demo emphasis order:** Lead with FirmBenchmark overlay on a real quote ("Ihr Betrieb: 14h, Plattform: 12h") -- that's the defensible moat. MCP stubs are secondary.

---

## Screens

| # | Screen | Primary act | Key elements |
|---|--------|------------|-------------|
| 1 | **Onboarding** | Acts 1 + 3 | Two paths: "Taifun importieren" / "Neu starten." Trade + firm size picker for new. Import animation for existing. |
| 2 | **Dashboard** | Acts 1 + 3 | Firm overview. Active quotes, past projects, CL summary metrics. Populated (post-import) vs. sparse (new firm). Role context in header. |
| 3 | **New Quote** | Act 2 | Hero screen. Voice/text input -> AI generation -> structured Leistungsverzeichnis -> CL overlay -> margin forecast. Role switcher. Article catalog. |
| 4 | **Project Detail** | Act 2 | Past completed project. Actuals vs. quoted. Hours, materials, margin delta. Event trail. FirmBenchmark vs. CLBenchmark. |

---

## Data Model (what's active in prototype)

See erd.md for full schema.

| Entity | Status | Notes |
|--------|--------|-------|
| Firm | Seed x2 | Two firms: one migrated (Meister Weber), one new (empty). Country: DE, currency: EUR. |
| User | Hardcoded x3 | Meister Weber, Geselle Hoffmann, Burokraft Yilmaz. Role switcher. No auth. |
| Customer | Seed x3-5 | Different German regions. Linked to migrated firm. |
| Quote | Active | Core feature. AI-generated. Event-tracked. |
| QuoteLineItem | Active | AI populates from description + article catalog. Event-tracked. |
| Project | Seed x5 | Past completed projects for migrated firm. Powers post-calc view. |
| ProjectLineItem | Seed | Actuals for past projects. The delta vs. QuoteLineItem is the learning signal. |
| JobType | Seed | SHK types (Heizungstausch, Badsanierung, Wartung, Rohrbruch, Wärmepumpe-Installation). Segment = "shk." |
| Article | Seed x20-30 | Common SHK materials with prices. Simulates DATANORM catalog. |
| Event | Active | Append-only. UI shows audit trail on quotes. |
| CLBenchmark | Seed | Platform-wide. p25/p50/p75 per job type. Currency: EUR. Available to both firms. |
| FirmBenchmark | Seed | Per-firm. Only for migrated firm. New firm has none (yet). |
| ArticlePriceHistory | Seed | Copper pipe price trend. 6 months. Currency: EUR. |

**Two firms in seed data.** The migrated firm (Weber, populated) and the new firm (empty, CL-only). This enables switching between Act 1 and Act 3 contexts.

---

## What's IN

1. Two onboarding paths (Taifun import / new signup)
2. Text-to-quote via Claude API
3. Voice-to-quote via browser SpeechRecognition API
4. CL overlay: FirmBenchmark + CLBenchmark, two-layer display
5. Margin forecast on quote
6. ArticlePriceHistory signal in quote view
7. Role switcher (3 users, role-differentiated views)
8. Event trail (audit) on quotes
9. Post-calculation view (past project, actuals vs. quoted)
10. Seed data with migration narrative ("aus Ihrem Taifun-Export")
11. Two firm contexts (migrated vs. fresh) switchable in demo
12. Deployable on Render with shareable URL
13. User can navigate live (no dead ends, sensible fallbacks)

## What's OUT

- User management, auth, registration (real)
- Real DATANORM/IDS integration (articles are seed data)
- Scheduling / Plantafel (A4)
- Invoicing (A7)
- Time tracking (A5)
- External MCP consumption
- Payment processing (A8)
- Real FirmBenchmark computation (pre-seeded)
- Multi-language UI (German only; i18n-ready in data model)
- MCP stub pages (mentioned verbally, not built as UI)
- Mobile-native layout (responsive Tailwind, not mobile-optimized)

---

## Time Budget

| Phase | Time | What happens |
|-------|------|-------------|
| Setup + deploy (scaffold, Neon, env, Render) | 30 min | Project structure, DB provisioning, .env, **deploy hello-world to Render immediately** |
| CLAUDE.md + seed data design | 30 min | Prototype CLAUDE.md, seed SQL/fixtures |
| Act 2: Quote + CL core | 1.5h | Text-to-quote, CL overlay, margin forecast, article catalog, **cached fallback quote** |
| Act 1 + 3: Onboarding flows | 1h | Two paths, import animation, firm switching, dashboard states |
| Voice input | 30 min | Browser SpeechRecognition -> same pipeline. **Gate to Chrome or show prominent text fallback.** |
| Polish + hardening | 1h | Tailwind, role switcher, event trail, navigation hardening |
| **Total** | **5h** | |

### Build Rules

1. **Deploy first, not last.** Get hello-world on Render in the first 30 minutes. Every subsequent epic builds on something already live. Infrastructure debugging after hour 3 is time stolen from the demo.
2. **Cached fallback quote.** Pre-generate a complete quote JSON (Heizungstausch, line items, CL overlay) that loads if Claude API response takes >5 seconds. This is non-negotiable -- live API dependency in a demo is the single biggest technical risk.
3. **MVD checkpoint at hour 3.** If text-to-quote + CL overlay works on the migrated firm, you have a demoable product. Acts 1 and 3 can be narrated from static screens. That's still a strong demo.
4. **Hard stop at hour 4.** Last hour is polish, rehearsal, and hardening -- not new features. If voice isn't working by hour 4, cut it.
5. **Voice = Chrome only.** Browser SpeechRecognition is Chrome-only and flaky in German. Gate the voice button to supported browsers. Don't let an excitement-tier feature become the thing that breaks.

**Risk:** If Act 2 (quote + CL) takes longer than 1.5h, cut voice input first (save 30 min), then simplify Act 3 to a verbal walkthrough with static mockup (save 30 min).

---

## Definition of Done

- [ ] Deployable on Render with a shareable URL
- [ ] User can navigate all 4 screens without hitting dead ends
- [ ] Voice and text input both produce structured quotes
- [ ] CL overlay shows two layers (firm + platform) for migrated firm
- [ ] CL overlay shows platform-only for new firm
- [ ] Migration narrative visible ("aus Ihrem Taifun-Export")
- [ ] Role switcher works (Meister/Geselle/Burokraft)
- [ ] Event trail visible on at least one quote
- [ ] At least one past project shows actuals vs. quoted
- [ ] All UI text in German

---

*Scope locked April 12, 2026.*

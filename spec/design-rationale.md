# Design Rationale -- AI-Native Trade Software

**Status:** Decisions locked. This document explains WHY the prototype is designed as it is.

---

## 1. Event Sourcing: Audit + Per-Firm Learning (not full event sourcing)

**Decision:** Events table tracks changes to Quote, QuoteLineItem, Project, ProjectLineItem. Application reads from projected state tables, not from event streams. Customer and Firm get `updated_by` but no event trail.

**Why not full event sourcing?** Overhead in coding, maintenance, and computation is massive for a prototype. Audit-only underdelivers on the learning value prop.

**Why this middle ground?** Events feed a FirmBenchmark layer: "Your quote revisions average 3 rounds. Your margin drift is -4% from quote to actual." Events become a learning signal, not just a log. This also enables cross-firm learning.

---

## 2. Per-Firm Learning: FirmBenchmark Entity

**Decision:** FirmBenchmark is a separate entity (mirrors CLBenchmark but scoped to one firm). Computed on a scheduled basis (weekly/monthly), with manual trigger option.

**Why not derived views?** Simpler schema but heavier queries. For dashboards and CL feed, pre-computed is better.

**Why scheduled, not real-time?** Few firms have enough activity to change their benchmark daily. Weekly is sufficient. Manual trigger covers edge cases.

---

## 3. MCP Orientation: Outside-In

**Decision:** The primary MCP consumers are external agents, not internal users. Priority order:

1. **Supply chain agents** -- wholesalers pushing availability/pricing updates (necessity, defer detailed build)
2. **Consumer AI agents** -- Google/OpenAI booking on behalf of homeowners (mass market, stub only)
3. **B2B agents** -- property management software dispatching subcontractors (stub only)
4. **Marketplace/aggregator agents** -- MyHammer, Check24
5. **Internal AI** -- users interacting with their own data via chat/voice (lowest priority -- why build a UI if this was critical?)

**Revenue distinction:** External consumers (1-4) generate new revenue. Internal AI (5) reduces cost. Different motivation.

**Prototype implication:** MCP stubs only. Verbal mention in demo. Not the demo's focus.

---

## 4. User Segments: Solo through Small

**In scope:** Solo (1 person), Micro (2-4), Small (5-12).
**Out of scope:** Medium (13-25), Large (25+).

**Why exclude medium/large?** Configuration complexity. Retaining enterprise whales means exorbitant maintenance spend that complicates the product for every other customer. Build modular for adjacent expansion instead.

**Beachhead: Micro.** Multi-user coordination creates real pain that Solo doesn't have (pen+paper works for one person). From Micro, expand down to Solo and up to Small.

---

## 5. Auth: Prepared, Not Implemented

**Decision:** Data model supports roles and trust boundaries. Prototype uses 3 hardcoded users (Meister/Geselle/Burokraft) with a role switcher in the header. No auth flows, registration, SSO.

**Why prepare?** Adding auth retroactively is painful. The role model is in the schema from day one. But demonstrating auth implementation isn't the point of the prototype.

---

## 6. Two Firms in Seed Data

**Decision:** Two demo contexts -- one migrated firm (Weber, fully populated) and one new firm (empty, CL-only).

**Why?** Enables demonstrating both the retention story (Act 1: your data migrates) and the acquisition story (Act 3: new users get platform intelligence from day one) without rebuilding context.

---

## 7. Crowd Learning: Three Layers

| Layer | Entity | Source | Update |
|-------|--------|--------|--------|
| 1. Raw events | `event` | Every user action on tracked entities | Real-time (append-only) |
| 2. Per-firm patterns | `firm_benchmark` | Computed from events + actuals per firm | Scheduled (weekly/monthly) |
| 3. Platform benchmarks | `cl_benchmark` | Aggregated across firms, anonymized | Scheduled (weekly/monthly) |

The core learning signal: QuoteLineItem (predicted) vs. ProjectLineItem (actual). The delta feeds FirmBenchmark, which feeds back into the next quote. This is the network effect -- every completed job makes the system smarter for every firm.

---

## 8. i18n: Ready From Day One

Firm carries `country` and `currency`. All monetary fields are bare decimals; currency context comes from the firm. Benchmarks are currency-scoped. Adding Swiss/Austrian support later should be config, not migration.

**Prototype:** German only. But the schema supports multi-country from day one.

---

## 9. Segment-Agnostic Core

The business cycle (quote -> project -> post-calc) is trade-agnostic. SHK-specific data (articles, job types, compliance rules) is injected as configuration. No SHK hardcoded in core logic. SHK is a plugin.

**Prototype:** SHK seed data only. But the schema supports any segment enum value.

---

*Rationale locked April 12, 2026.*

# AI-Native Trade Software -- User Story Map

**Framework:** Jeff Patton's User Story Mapping (2D: journey x priority)
**Framing:** Every activity has a money-losing failure mode. The product makes them visible and preventable.

---

## Reading This Map

**Backbone (horizontal):** Activities A0-A9 represent the craftsperson's full business cycle, from getting a customer to learning from the completed job.

**Depth (vertical):** Under each activity, stories are layered by wave:
- **W1** = What legacy trade ERPs solve today (admin after the job)
- **W2** = What modern competitors add (admin on the go, emerging AI)
- **W3** = What next-gen platforms add (growth engine, AI-native)
- **CL** = Crowd Learning -- intelligence from data, first from your own jobs, then from aggregated anonymized data across all users. The network effect layer. Nobody solves this yet.

**Index notation:** `[A2.W1.a]` = Activity 2, Wave 1, story a.

**Desired outcomes** (from JTBD analysis) are placed at the activity where they belong.

---

## The Crowd Learning Thesis

A trade software company with tens of thousands of customers generating quotes, invoices, time logs, and material orders every day sits on a massive dataset. That data is not tech debt -- it is the training set for a learning system that no startup can replicate.

**The network effect:** Every craftsperson who completes a job makes the system smarter for every other craftsperson. More users -> better benchmarks -> better quotes -> higher margins -> stronger lock-in.

**"Outcome over output" at platform level:** When output (software features) is cheap, the only defensible asset is the outcome engine -- the system that learns what works across thousands of businesses and feeds that knowledge back. That's where margin comes from.

---

## Roles & Async Handoffs

The target firm has 2-12 people. Three roles matter:

| Role | Who | Where | Primary activities |
|------|-----|-------|-------------------|
| **Meister / Inhaber** | Owner or master craftsperson. Decides, quotes, reviews. | Office + occasional site visits | A0, A1, A2, A3, A4, A8, A9 |
| **Geselle / Techniker** | Skilled worker on-site. Executes, records, documents. | On-site, mobile-only | A1 (assessment), A5, A6 |
| **Burokraft** | Office admin. Invoices, DATEV, follow-ups, scheduling. | Office | A0 (phone), A3, A4, A7, A8 |

**Async handoffs (where data flows between roles):**

| Handoff | From -> To | What flows | Failure mode |
|---------|-----------|-----------|--------------|
| Site assessment -> Quote | Geselle -> Meister | Photos, measurements, voice notes from site visit | Lost notes, Meister quotes blind |
| Dispatch -> Execution | Meister/Burokraft -> Geselle | Job assignment, schedule, materials list, customer context | Geselle arrives unprepared, wrong materials |
| Time/material logging -> Post-calc | Geselle -> Meister | Hours worked, materials used, photos | "I'll log it later" = never logged = post-calc impossible |
| Post-calc -> Next quote | System -> Meister | Margin analysis, adjustment suggestions | Without CL, this loop doesn't exist |
| Invoice -> Payment tracking | Burokraft -> Meister | Open items, overdue invoices | Cash flow invisible to owner |

**For the prototype:** Single-user flow, but UI shows role context ("Meister Weber" in header). CL benchmarks reference "Ihr Betrieb" (your firm), not "du." This signals multi-user without building auth.

---

## Segment Extensibility

The backbone (A0-A9) is trade-agnostic. A roofer quotes, plans, executes, invoices the same way an SHK firm does. What changes per segment is injected as configuration:

| Segment-specific layer | SHK example | Elektro example |
|----------------------|-------------|-----------------|
| Article catalogues | DATANORM SHK, SHK-Connect | DATANORM Elektro, E-MASTER |
| Compliance / regulations | EnEV, Heizlast (DIN 12831) | VDE, DGUV V3 Prüfung |
| Wholesaler networks | GC-Gruppe, Mainmetall | Sonepar, Rexel |
| Domain calculations | Heizlastberechnung, Rohrnetzberechnung | Leitungsquerschnitt, Kurzschlussstrom |
| Typical job types | Heizungstausch, Bad-Sanierung, Wartung | Zählerschrankumbau, Smart Home, PV |

**Architecture principle:** The core is the business cycle. The trade segment is injected -- article sources, compliance rules, calculation modules, job type taxonomies. No SHK in the core. SHK is a plugin.

---

## A0: Get a Customer (Kundenakquise)

**Money-losing failure:** Waiting for the phone to ring instead of generating leads. Customer finds a competitor on Google/MyHammer first.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Customer calls, Burokraft takes info, creates record | [A0.W1.a] |
| W2 | Lead form on website -> auto-creates customer record | [A0.W2.a] |
| W3 | AI answers initial customer inquiry, qualifies lead, books assessment | [A0.W3.a] |
| CL | "Firms in your region that respond within 2h win 3x more jobs" | [A0.CL.a] |

**Desired outcome (Taifun):** Minimize the time lost when a technician on-site needs access to customer history or open orders.

**Prototype scope:** Not in scope. Customer records are seeded.

---

## A1: Assess the Job (Aufnahme vor Ort)

**Money-losing failure:** Meister quotes from memory because Geselle's site notes were incomplete or lost. Quote is wrong before it's even written.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Geselle takes measurements on paper, drives back to office | [A1.W1.a] |
| W2 | Geselle enters measurements on tablet, syncs to office | [A1.W2.a] |
| W2 | Geselle takes photos, attaches to job | [A1.W2.b] |
| W3 | AI reads photos + measurements, pre-fills quote template | [A1.W3.a] |
| CL | "Jobs assessed with photos have 30% fewer quote errors" | [A1.CL.a] |

**Desired outcome (SmartHandwerk):** Minimize errors when exchanging data with wholesalers and accountants.

**Prototype scope:** Not directly built, but the voice-to-quote flow simulates the output of this step.

---

## A2: Create a Quote (Angebot erstellen) -- PROTOTYPE HERO

**Money-losing failure:** Meister underquotes because he doesn't know his true costs. Or overquotes and loses the job. Both are invisible without data.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Meister manually builds quote from article catalog, enters line items | [A2.W1.a] |
| W1 | Quote includes materials from DATANORM + labor hours | [A2.W1.b] |
| W2 | Quote creation on mobile, sync to office | [A2.W2.a] |
| W2 | Template library for common job types | [A2.W2.b] |
| W3 | **AI generates quote from natural language description** (text or voice) | [A2.W3.a] |
| W3 | AI selects articles from catalog, calculates quantities from job description | [A2.W3.b] |
| CL | **CL overlay: "Your firm avg for this job type: X. Platform median: Y."** | [A2.CL.a] |
| CL | **Margin forecast: "At these prices, expected margin: 19%. Your target: 25%."** | [A2.CL.b] |
| CL | **Material cost signal: "Copper pipe +8% in 30 days. Consider price trend."** | [A2.CL.c] |

**Desired outcomes:**
- Minimize the time it takes to create and send a quote including materials from wholesaler catalogues (Taifun, SmartHandwerk)
- Minimize the gap between estimated and actual costs (Sykasoft)
- Reduce the effort required to compare supplier prices at point of ordering (Taifun)

**Prototype scope:** Full implementation. This is the demo's hero screen.

---

## A3: Send Quote to Customer (Angebot versenden)

**Money-losing failure:** Quote sits in the system for 3 days because Burokraft was busy. Customer already got a quote from a competitor.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Print/email quote as PDF | [A3.W1.a] |
| W2 | Customer portal: customer views and accepts online | [A3.W2.a] |
| W3 | AI follow-up: "Customer hasn't responded in 5 days. Suggest: call or adjust price." | [A3.W3.a] |
| CL | "Firms that send quotes within 24h convert 40% more" | [A3.CL.a] |

**Prototype scope:** Not in scope.

---

## A4: Plan + Schedule (Planen / Plantafel)

**Money-losing failure:** Geselle shows up at wrong job, or two Gesellen show up at same job, or material delivery arrives after crew leaves.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Meister assigns jobs to Gesellen, manual calendar | [A4.W1.a] |
| W2 | Drag-and-drop Plantafel, team calendar view | [A4.W2.a] |
| W3 | AI scheduling: optimize routes, match skills to jobs | [A4.W3.a] |
| CL | "Your avg travel time between jobs: 45min. Top 25%: 28min." | [A4.CL.a] |

**Prototype scope:** Not in scope.

---

## A5: Execute + Log Time (Ausfuhrung + Zeiterfassung)

**Money-losing failure:** Geselle works 8 hours, logs 6. Or logs nothing. Post-calculation is impossible. Margin is invisible.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Paper time sheets, entered at end of week | [A5.W1.a] |
| W2 | Mobile time tracking per job | [A5.W2.a] |
| W3 | Auto-tracking (GPS/location-based start/stop) | [A5.W3.a] |
| CL | "Your Gesellen log 78% of hours. Top firms: 95%. The gap is €X/year in invisible cost." | [A5.CL.a] |

**Prototype scope:** Not in scope.

---

## A6: Document + Handoff (Dokumentation + Ubergabe)

**Money-losing failure:** Job is done but nothing is documented. Customer disputes scope. Warranty claim has no evidence.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Geselle writes completion note, Meister signs off | [A6.W1.a] |
| W2 | Photo documentation on-site, synced to job | [A6.W2.a] |
| W3 | AI generates completion report from photos + time logs | [A6.W3.a] |

**Prototype scope:** Not in scope.

---

## A7: Invoice (Rechnung stellen)

**Money-losing failure:** Invoice doesn't match actual work done. Or takes 2 weeks to send. Or isn't GoBD-compliant.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Burokraft creates invoice from quote, exports to DATEV | [A7.W1.a] |
| W1 | ZUGFeRD/XRechnung compliant | [A7.W1.b] |
| W2 | Auto-invoice from completed project (quote -> actuals -> invoice) | [A7.W2.a] |
| W3 | AI adjusts invoice based on actual vs. quoted, flags discrepancies | [A7.W3.a] |

**Prototype scope:** Not in scope.

---

## A8: Collect Payment (Zahlung einziehen)

**Money-losing failure:** Outstanding invoices invisible to owner. Cash flow surprises.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Track payment status manually | [A8.W1.a] |
| W2 | Automated payment reminders | [A8.W2.a] |
| W3 | AI cash flow forecast | [A8.W3.a] |
| CL | "Your avg collection period: 38 days. Industry: 28 days." | [A8.CL.a] |

**Prototype scope:** Not in scope.

---

## A9: Post-Calculate (Nachkalkulation) -- PROTOTYPE SECONDARY HERO

**Money-losing failure:** Nobody knows if a job was profitable. Meister quotes the next one the same way. Margin erosion is invisible.

| Wave | Story | Index |
|------|-------|-------|
| W1 | Burokraft compares invoice to quote (if she has time) | [A9.W1.a] |
| W2 | System shows quoted vs. actual per project | [A9.W2.a] |
| W3 | **AI identifies patterns: "Your bathroom renos consistently exceed quote by 22%"** | [A9.W3.a] |
| CL | **"Your firm: avg 14h for bathroom reno. Platform: avg 12h. You're quoting 10h."** | [A9.CL.a] |
| CL | **Feed-forward: next quote for same job type is auto-adjusted based on actuals** | [A9.CL.b] |

**Desired outcomes:**
- Minimize the gap between estimated and actual costs on complex projects (Sykasoft)
- Increase the share of invoices that are audit-ready without extra effort (Sykasoft)

**Prototype scope:** Project detail screen with actuals vs. quoted. This is the "Das haben Sie vorher nie gesehen" moment.

**The gap nobody solves:** A9 is the highest-impact activity AND the least served by existing software. Legacy ERPs stop at A7 (invoice). The quote-to-actual feedback loop doesn't exist. This is where CL creates the most value.

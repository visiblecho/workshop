# Workshop Prototype

## What this is
A working prototype demonstrating AI-native craft business software for German SHK/Elektro trades.
Built to show what "revolution not evolution" looks like -- AI that thinks alongside the Meister, not software that digitizes paperwork.

## Spec
All design decisions, data model, user stories, and visual direction are in `spec/`. Read these before building:
- `prototype-scope.md` -- 8 screens, 3-act demo script, build rules, budget
- `design-rationale.md` -- 9 locked decisions with rationale (start here for "why")
- `erd.md` -- full DBML schema, 13 tables, relationships, CL signals
- `prototype-backlog.md` -- 25 stories across 5 epics, sorted build order
- `user-story-map.md` -- activity backbone A0-A9, MoSCoW priorities
- `user-segments-personas.md` -- 6 personas, 3 segments, adoption sequence
- `visual-identity-research.md` -- competitor analysis, color direction, positioning

## Stack
- Frontend: React + Vite + TypeScript + Tailwind CSS (in `frontend/`)
- Backend: FastAPI + Python (in `backend/`)
- Database: Neon (serverless Postgres)
- AI: Anthropic Claude API via `anthropic` Python SDK

## Demo context
- **Demo firm:** Weber Haustechnik (4 people: Meister Weber, 2 Gesellen, Burokraft Yilmaz)
- **Seed data:** 3 active projects (planned/in-progress) + 5 completed projects (with actuals)
- **Second firm:** Neuer Betrieb (empty, no history -- shows CL-only value)
- **Three hardcoded users:** Meister (sees margins + CL), Geselle (sees jobs, not margins), Burokraft (sees admin)
- **Role switcher** in UI to toggle between perspectives

## Three-act demo script
1. **Retain** (migration story): Weber's 5 completed projects arrive with full history. Day-one intelligence, not cold start.
2. **Product** (AI + CL): Meister describes a job -> AI generates structured quote -> CL overlay shows "firms like yours quote X" with margin indicator.
3. **Acquire** (PLG): Geselle tracks own hours on free tier -> sees gap between quoted and actual -> evidence that convinces the Meister to upgrade.

## Crowd Learning (CL) -- the core concept
Three-layer intelligence: raw events (quotes, actuals, hours) -> FirmBenchmark (your own patterns) -> CLBenchmark (anonymized cross-firm intelligence). The CL overlay on quotes is the key differentiator. For the prototype, CL data is seeded/mocked -- the point is to show the UX, not run real ML.

## Rules
- This is a prototype, not production. Optimize for speed and demo impact.
- All UI text in German (target users are German Handwerker).
- Mobile-first design (craftsmen use phones on job sites).
- No authentication. Hardcoded user context with role switcher.
- Follow the backlog build order (E0 -> E1 -> E2 -> E3 -> E4).
- When in doubt, check the spec. When the spec is silent, ask.

## Definition of Done
- Deployable on Render with a shareable URL
- Works on mobile browser (iPhone Safari, Android Chrome)
- AI quote generation functional with real Claude API calls
- CL overlay visible on quotes with seeded benchmark data
- Role switcher shows different views per persona
- Looks clean and professional -- matches the visual identity direction

## What NOT to do
- No unit tests (prototype)
- No CI/CD beyond Render auto-deploy
- No auth, no user management (hardcoded roles)
- No elaborate error handling
- No English in the UI
- No feature creep beyond the 25 backlog stories

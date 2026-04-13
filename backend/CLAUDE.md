# Backend -- FastAPI + Python

## Commands
- `source venv/bin/activate` -- Activate virtualenv
- `uvicorn main:app --reload --port 8000` -- Start dev server
- `pip install -r requirements.txt` -- Install deps

## Data Model
The full ERD is at `spec/erd.md` (13 tables in DBML). Generate SQLAlchemy models from it. Key tables:
- `firms`, `users`, `roles` -- multi-tenant, role-based access
- `projects`, `quote_line_items` -- the core business objects
- `cl_events`, `firm_benchmarks`, `cl_benchmarks` -- the CL intelligence layer

**CL data flow:** Raw events (quotes, actuals, hours) -> `firm_benchmarks` (per-firm patterns) -> `cl_benchmarks` (anonymized cross-firm). For the prototype, seed the benchmarks directly -- no real aggregation pipeline.

## Conventions
- Async def for all endpoints.
- Pydantic models for request/response schemas.
- AI service calls go in `services/` (not in route handlers).
- Use `python-dotenv` for env vars. Never hardcode secrets.
- SQLAlchemy 2.0 style with `mapped_column`.

## How to add a feature
1. Define model in `models/` (match `spec/erd.md`)
2. Create Pydantic schema in `schemas/`
3. Implement business logic in `services/`
4. Add API route in `routers/`
5. Generate Alembic migration if DB changed

## AI Integration
- Use the `anthropic` Python SDK for Claude API calls
- AI quote generation: Meister describes job in plain German -> structured Leistungsverzeichnis with line items
- System prompts go in `services/prompts/` as plain text files
- Use prompt caching for cost control on repeated system prompts

## Structure
```
main.py          -- FastAPI app, CORS, router includes
routers/         -- API route modules (one per resource)
services/        -- Business logic + AI calls
  prompts/       -- System prompt templates
models/          -- SQLAlchemy ORM models (from spec/erd.md)
schemas/         -- Pydantic request/response schemas
seed.py          -- Seed script for demo data (Weber firm + 8 projects)
.env             -- API keys, DATABASE_URL (not committed)
```

## Environment Variables
- `DATABASE_URL` -- Neon Postgres connection string
- `ANTHROPIC_API_KEY` -- Claude API key

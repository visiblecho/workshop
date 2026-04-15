# Workshop

AI-native craft business software prototype for German SHK/Elektro trades.

AI that thinks alongside the user, not software that digitizes paperwork.

## What it does

- **Voice-to-quote:** User describes a job, AI generates a structured quote
- **Crowd Learning (CL):** Anonymized cross-firm benchmarks overlay quotes with "firms like yours quote X"
- **Role-based views:** Meister sees margins + CL, Geselle sees jobs, Burokraft sees admin
- **Migration story:** Legacy data imports with day-one intelligence, not a cold start

## Stack

| Layer | Tech |
|-------|------|
| Frontend | React + Vite + TypeScript + Tailwind CSS |
| Backend | FastAPI + Python |
| Database | Neon (serverless Postgres) |
| AI | Anthropic Claude API |
| Deploy | Render |

## Local development

### Prerequisites

- Node.js 18+
- Python 3.11+
- A Neon database (or any Postgres)
- Anthropic API key

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `localhost:5173` and proxies API requests to `localhost:8000`.

### Environment variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Neon Postgres connection string |
| `ANTHROPIC_API_KEY` | Claude API key for quote generation |


## License

Proprietary. Not for redistribution.

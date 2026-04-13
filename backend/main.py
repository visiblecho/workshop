from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine

app = FastAPI(title="Workshop")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM firm"))
            firm_count = result.scalar()
        return {"status": "ok", "db": "connected", "firm_count": firm_count}
    except Exception as e:
        return {"status": "error", "db": str(e), "firm_count": 0}

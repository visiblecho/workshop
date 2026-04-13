from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Workshop")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock down for production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}
import json
import os
import asyncio
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from models.reference import Article

load_dotenv()

PROMPT_PATH = Path(__file__).parent / "prompts" / "quote_system.txt"
FALLBACK_PATH = Path(__file__).parent.parent / "fallback_quotes" / "heizungstausch.json"
SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")
FALLBACK_QUOTE = json.loads(FALLBACK_PATH.read_text(encoding="utf-8"))


def get_article_catalog(db: Session) -> str:
    articles = db.query(Article).filter(Article.deleted_at.is_(None)).all()
    lines = []
    for a in articles:
        lines.append(f"- ID: {a.id} | {a.name} | {a.unit.value} | {float(a.default_price):.2f} EUR | {a.wholesaler or ''}")
    return "\n".join(lines)


async def generate_quote_ai(description: str, job_type_name: str, catalog: str) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return FALLBACK_QUOTE

    client = Anthropic(api_key=api_key)

    user_message = f"""Auftragstyp: {job_type_name}

Auftragsbeschreibung: {description}

Artikelkatalog:
{catalog}"""

    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(
                client.messages.create,
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": user_message}],
            ),
            timeout=15.0,
        )

        text = response.content[0].text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        return json.loads(text)

    except (asyncio.TimeoutError, Exception):
        return FALLBACK_QUOTE

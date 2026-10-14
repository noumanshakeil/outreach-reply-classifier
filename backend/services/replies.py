from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import Reply
from backend.utils.text import token_set

RULES = {
    "unsubscribe": {"unsubscribe", "remove", "stop emailing"},
    "ooo": {"out of office", "ooo", "away until"},
    "objection": {"not interested", "no budget", "maybe later", "expensive"},
    "interest": {"interested", "book", "demo", "sounds good", "send more"},
}

def rule_label(text: str) -> tuple[str, float]:
    low = text.lower()
    for label, cues in RULES.items():
        hits = sum(1 for c in cues if c in low)
        if hits:
            return label, min(0.95, 0.55 + 0.15 * hits)
    return "other", 0.35

async def classify(session: AsyncSession, body: str, subject: str = "") -> Reply:
    label, conf = rule_label(f"{subject}\n{body}")
    if label == "other":
        llm = get_llm()
        raw = await llm.complete(f"Classify reply as interest|objection|ooo|unsubscribe|other:\n{body}", system="One word label.")
        for cand in ("interest", "objection", "ooo", "unsubscribe"):
            if cand in raw.lower():
                label, conf = cand, 0.55
                break
    row = Reply(id=uuid.uuid4().hex[:10], subject=subject[:240], body=body.strip(), label=label, confidence=conf)
    session.add(row); await session.commit(); await session.refresh(row); return row

async def list_replies(session: AsyncSession) -> list[Reply]:
    return list((await session.execute(select(Reply).order_by(Reply.created_at.desc()))).scalars())

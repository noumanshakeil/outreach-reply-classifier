from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import replies as svc

class ReplyIn(BaseModel):
    body: str = Field(min_length=2)
    subject: str = ""

router = APIRouter()

@router.get("/replies")
async def replies(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_replies(db)
    return {"replies": [{"id": r.id, "label": r.label, "confidence": r.confidence, "subject": r.subject} for r in rows]}

@router.post("/replies")
async def create(payload: ReplyIn, db: AsyncSession = Depends(get_db)):
    r = await svc.classify(db, payload.body, payload.subject)
    return {"id": r.id, "label": r.label, "confidence": r.confidence}

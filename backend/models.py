from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base
def utcnow(): return datetime.utcnow()
class Reply(Base):
    __tablename__ = "replies"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    subject: Mapped[str] = mapped_column(String(240), default="")
    body: Mapped[str] = mapped_column(Text)
    label: Mapped[str] = mapped_column(String(64), index=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

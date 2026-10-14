from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import replies as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Outreach Reply Classifier", "replies": await svc.list_replies(db)})

@router.post("/ui/replies")
async def ui_r(body: str = Form(...), subject: str = Form(""), db: AsyncSession = Depends(get_db)):
    await svc.classify(db, body, subject); return RedirectResponse("/", status_code=303)

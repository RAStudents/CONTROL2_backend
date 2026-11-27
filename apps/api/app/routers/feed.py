from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventIn

router = APIRouter()

@router.get("/", summary="Лента событий")
async def get_feed(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).order_by(Event.received_at.desc()))
    events = result.scalars().all()
    
    return [
        {
            "id": str(e.id),
            "occurred_at": e.occurred_at,
            "code": e.code,
            "confidence": e.confidence,
            "payload": e.payload
        } for e in events
    ]
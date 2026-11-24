import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventIn

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/events", status_code=status.HTTP_202_ACCEPTED, summary="Приём события")
async def receive_event(
    event_in: EventIn,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    existing = await db.scalar(
        select(Event).where(Event.idempotency_key == event_in.event.idempotency_key)
    )

    if existing is not None:
        logger.warning("Дубликат события: %s", event_in.event.idempotency_key)
        return {"status": "ignored", "message": "Duplicate event"}

    confidence = None
    if event_in.inference and event_in.inference.detections:
        confidence = event_in.inference.detections[0].confidence

    new_event = Event(
        company_id=None,
        schema_version=event_in.schema_version,
        event_external_id=event_in.event.id,
        code=event_in.event.code,
        occurred_at=event_in.event.occurred_at,
        idempotency_key=event_in.event.idempotency_key,
        confidence=confidence,
        payload=event_in.payload,
        raw_json=event_in.model_dump(mode="json"),
    )

    db.add(new_event)
    await db.commit()

    logger.info("Событие %s сохранено", event_in.event.code)
    return {"status": "accepted", "idempotency_key": event_in.event.idempotency_key}
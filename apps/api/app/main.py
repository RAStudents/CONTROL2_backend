import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import engine
from app.routers import auth, telemetry, feed

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    logger.info("Database connection established")
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Веб-сервис учёта Edge-устройств",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.PROJECT_NAME}


app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/cabinet/auth",
    tags=["cabinet:auth"],
)

app.include_router(
    feed.router,
    prefix=f"{settings.API_V1_STR}/cabinet/feed",
    tags=["cabinet:feed"]
)

app.include_router(
    telemetry.router,
    prefix=f"{settings.API_V1_STR}/device",
    tags=["device:telemetry"],
)
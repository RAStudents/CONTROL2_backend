import asyncio
import json
import logging
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

API_URL = "http://127.0.0.1:8000/api/device/events"


async def send_event() -> None:
    file_path = Path(__file__).parent / "fixtures" / "telemetry.json"
    
    with open(file_path, "r", encoding="utf-8") as f:
        event_data = json.load(f)

    logger.info("Читаем файл: %s", file_path)

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=event_data)

    logger.info("Статус ответа: %s", response.status_code)
    logger.info("Ответ сервера: %s", response.json())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(send_event())
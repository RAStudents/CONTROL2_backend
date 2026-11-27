import asyncio
import json
import logging
from pathlib import Path
import httpx

logger = logging.getLogger(__name__)

API_URL = "http://127.0.0.1:8000/api/device/events"
FIXTURES_DIR = Path(__file__).parent / "fixtures"

async def send_file(client: httpx.AsyncClient, file_path: Path) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        event_data = json.load(f)
    
    try:
        response = await client.post(API_URL, json=event_data)
        status = response.status_code
        result = response.json()
        logger.info(f"Файл {file_path.name} -> Статус: {status}, Ответ: {result.get('status')}")
    except Exception as e:
        logger.error(f"Ошибка при отправке {file_path.name}: {e}")

async def send_all_events():
    json_files = list(FIXTURES_DIR.glob("*.json"))
    
    if not json_files:
        logger.warning(f"В папке {FIXTURES_DIR} нет JSON файлов!")
        return

    logger.info(f"Найдено {len(json_files)} файлов для отправки.")
    
    async with httpx.AsyncClient() as client:
        for file_path in json_files:
            await send_file(client, file_path)
            await asyncio.sleep(0.5) 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    asyncio.run(send_all_events())
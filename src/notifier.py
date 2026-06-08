import logging
import httpx
from src.config import settings

logger = logging.getLogger(__name__)

async def send_alert(message: str) -> bool:
    payload = {"content": f"🚨 **LOG ALERT** 🚨\n{message}"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(str(settings.WEBHOOK_URL), json=payload)
            return response.status_code in [200, 204]
    except Exception as e:
        logger.error(f"Network error: {e}")
        return False
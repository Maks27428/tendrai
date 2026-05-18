import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def get_embedding(text: str) -> list[float] | None:
    """Get text embedding from Alem Plus Embedder API (OpenAI-compatible)."""
    if not settings.EMBEDDER_API_KEY:
        return None

    try:
        resp = requests.post(
            settings.EMBEDDER_API_URL,
            headers={
                'Authorization': f'Bearer {settings.EMBEDDER_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': settings.EMBEDDER_MODEL,
                'input': text[:8000],
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()['data'][0]['embedding']
    except Exception as e:
        logger.warning(f'Embedder API error: {e}')
        return None

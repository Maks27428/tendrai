import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def call_llm(system_prompt: str, user_prompt: str, max_tokens: int = 4000, temperature: float = 0.3) -> str:
    """Call Alem Plus LLM via OpenAI-compatible chat completions API."""
    resp = requests.post(
        f"{settings.LLM_API_URL}/chat/completions",
        headers={
            'Authorization': f'Bearer {settings.LLM_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            'model': settings.LLM_MODEL,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
            'max_tokens': max_tokens,
            'temperature': temperature,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']

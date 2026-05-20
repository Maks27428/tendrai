import time
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BASE_DELAY = 5


class LLMError(Exception):
    pass


def _get_credentials(model: str) -> tuple:
    """Return (api_url, api_key) for the given model."""
    fallback_models = getattr(settings, 'LLM_FALLBACK_MODELS', [])
    if model in fallback_models:
        return (
            getattr(settings, 'LLM_FALLBACK_API_URL', settings.LLM_API_URL),
            getattr(settings, 'LLM_FALLBACK_API_KEY', settings.LLM_API_KEY),
        )
    return settings.LLM_API_URL, settings.LLM_API_KEY


def call_llm(system_prompt: str, user_prompt: str, max_tokens: int = 4000, temperature: float = 0.3) -> str:
    models = [settings.LLM_MODEL] + getattr(settings, 'LLM_FALLBACK_MODELS', [])
    last_error = None

    for model in models:
        api_url, api_key = _get_credentials(model)

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = requests.post(
                    f"{api_url}/chat/completions",
                    headers={
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json',
                    },
                    json={
                        'model': model,
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
            except requests.HTTPError as e:
                status_code = e.response.status_code if e.response is not None else 0
                body = ''
                try:
                    body = e.response.text[:300] if e.response is not None else ''
                except Exception:
                    pass
                logger.warning("LLM %s attempt %d/%d HTTP %d: %s | %s", model, attempt, MAX_RETRIES, status_code, e, body)
                last_error = e

                if 400 <= status_code < 500 and status_code != 429:
                    break

                delay = BASE_DELAY * (2 ** (attempt - 1))
                if attempt < MAX_RETRIES:
                    time.sleep(delay)
            except Exception as e:
                last_error = e
                delay = BASE_DELAY * (2 ** (attempt - 1))
                logger.warning("LLM %s attempt %d/%d failed: %s. Retry in %ds", model, attempt, MAX_RETRIES, e, delay)
                if attempt < MAX_RETRIES:
                    time.sleep(delay)

        logger.error("Model %s exhausted all retries", model)

    raise LLMError("Сервис AI временно недоступен. Попробуйте позже.")

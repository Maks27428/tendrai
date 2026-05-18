import os
import anthropic
from django.conf import settings
from .prompts import EXTRACTION_SYSTEM, EXTRACTION_USER
from .utils import extract_json

MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514')


def extract_requirements(tender_text: str) -> dict:
    """Send parsed text to Claude and extract structured requirements."""
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    message = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        system=[{
            "type": "text",
            "text": EXTRACTION_SYSTEM,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[
            {
                "role": "user",
                "content": EXTRACTION_USER.format(tender_text=tender_text),
            }
        ],
    )

    return extract_json(message.content[0].text)

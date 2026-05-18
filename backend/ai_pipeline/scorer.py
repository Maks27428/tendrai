import os
import anthropic
from django.conf import settings
from .prompts import SCORING_SYSTEM, SCORING_USER
from .utils import extract_json

MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514')


def calculate_risk_score(extracted_data: dict) -> dict:
    """Calculate risk score using Claude analysis + rule-based factors."""
    requirements = extracted_data.get('requirements', [])
    pitfalls = extracted_data.get('pitfalls', [])

    requirements_text = "\n".join(
        f"- [{r.get('severity', 'ok')}] [{r.get('category', '')}] {r['text']}"
        for r in requirements
    )
    pitfalls_text = "\n".join(
        f"- [{p.get('severity', 'medium')}] {p['text']}"
        for p in pitfalls
    ) or "Не обнаружены"

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=[{
            "type": "text",
            "text": SCORING_SYSTEM,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[
            {
                "role": "user",
                "content": SCORING_USER.format(
                    title=extracted_data.get('title', 'Не указано'),
                    amount=extracted_data.get('amount', 'Не указано'),
                    deadline=extracted_data.get('deadline', 'Не указано'),
                    category=extracted_data.get('category', 'Не указано'),
                    requirements_text=requirements_text,
                    pitfalls_text=pitfalls_text,
                ),
            }
        ],
    )

    return extract_json(message.content[0].text)

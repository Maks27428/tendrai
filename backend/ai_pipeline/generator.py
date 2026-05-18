import os
import anthropic
from django.conf import settings
from .prompts import PROPOSAL_SYSTEM, PROPOSAL_USER

MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514')


def generate_proposal(extracted_data: dict) -> str:
    """Generate a draft technical proposal based on extracted tender data."""
    requirements_text = "\n".join(
        f"{i+1}. [{r.get('category', '')}] {r['text']}"
        for i, r in enumerate(extracted_data.get('requirements', []))
    )

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    message = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        system=[{
            "type": "text",
            "text": PROPOSAL_SYSTEM,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[
            {
                "role": "user",
                "content": PROPOSAL_USER.format(
                    title=extracted_data.get('title', 'Не указано'),
                    customer=extracted_data.get('customer', 'Не указано'),
                    amount=extracted_data.get('amount', 'Не указано'),
                    category=extracted_data.get('category', 'Не указано'),
                    delivery_location=extracted_data.get('delivery_location', 'Не указано'),
                    requirements_text=requirements_text,
                ),
            }
        ],
    )

    return message.content[0].text

from .prompts import PROPOSAL_SYSTEM, PROPOSAL_USER
from .llm_client import call_llm


def generate_proposal(extracted_data: dict) -> str:
    """Generate a draft technical proposal based on extracted tender data."""
    requirements_text = "\n".join(
        f"{i+1}. [{r.get('category', '')}] {r['text']}"
        for i, r in enumerate(extracted_data.get('requirements', []))
    )

    return call_llm(
        PROPOSAL_SYSTEM,
        PROPOSAL_USER.format(
            title=extracted_data.get('title', 'Не указано'),
            customer=extracted_data.get('customer', 'Не указано'),
            amount=extracted_data.get('amount', 'Не указано'),
            category=extracted_data.get('category', 'Не указано'),
            delivery_location=extracted_data.get('delivery_location', 'Не указано'),
            requirements_text=requirements_text,
        ),
        max_tokens=8000,
    )

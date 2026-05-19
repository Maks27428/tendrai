from .prompts import SCORING_SYSTEM, SCORING_USER
from .utils import extract_json
from .llm_client import call_llm


def calculate_risk_score(extracted_data: dict) -> dict:
    """Calculate risk score using LLM analysis."""
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

    response = call_llm(
        SCORING_SYSTEM,
        SCORING_USER.format(
            title=extracted_data.get('title', 'Не указано'),
            amount=extracted_data.get('amount', 'Не указано'),
            deadline=extracted_data.get('deadline', 'Не указано'),
            category=extracted_data.get('category', 'Не указано'),
            requirements_text=requirements_text,
            pitfalls_text=pitfalls_text,
        ),
        max_tokens=2000,
    )
    return extract_json(response)

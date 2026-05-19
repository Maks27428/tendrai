from .prompts import EXTRACTION_SYSTEM, EXTRACTION_USER
from .utils import extract_json
from .llm_client import call_llm


def extract_requirements(tender_text: str) -> dict:
    """Send parsed text to LLM and extract structured requirements."""
    response = call_llm(
        EXTRACTION_SYSTEM,
        EXTRACTION_USER.format(tender_text=tender_text),
        max_tokens=8000,
    )
    return extract_json(response)

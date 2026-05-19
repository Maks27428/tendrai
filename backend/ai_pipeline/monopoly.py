import json
import logging

from .prompts import MONOPOLY_SYSTEM, MONOPOLY_USER
from .utils import extract_json
from .llm_client import call_llm

logger = logging.getLogger(__name__)


def check_monopoly(tenders_data: list[dict]) -> dict:
    tenders_text = json.dumps(tenders_data, ensure_ascii=False, indent=2)
    prompt = MONOPOLY_USER.format(tenders_data=tenders_text)

    try:
        response = call_llm(MONOPOLY_SYSTEM, prompt, max_tokens=4000)
        return extract_json(response)
    except Exception:
        logger.exception('Monopoly check failed')
        return {
            'monopoly_score': 0,
            'verdict': 'clean',
            'summary': 'Не удалось выполнить проверку',
            'flags': [],
            'recommendations': [],
        }


def prepare_tender_data(tender) -> dict:
    return {
        'id': tender.id,
        'title': tender.title,
        'customer': tender.summary.get('customer', '') if tender.summary else '',
        'amount': tender.summary.get('amount', '') if tender.summary else '',
        'deadline': tender.summary.get('deadline', '') if tender.summary else '',
        'category': tender.summary.get('category', '') if tender.summary else '',
        'delivery_location': tender.summary.get('delivery_location', '') if tender.summary else '',
        'contacts': tender.contacts or {},
        'requirements_summary': [
            r.text[:200] for r in tender.requirements.all()[:10]
        ],
    }

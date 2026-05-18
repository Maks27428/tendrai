import hashlib
import json
import logging

from django.core.cache import cache

from tenders.models import Tender, Requirement
from .pdf_parser import parse_pdf
from .extractor import extract_requirements
from .scorer import calculate_risk_score
from .generator import generate_proposal
from .rag import store_tender_embedding, find_similar_tenders

logger = logging.getLogger(__name__)

CACHE_TTL = 60 * 60 * 24 * 7  # 7 days


def update_status(tender: Tender, status: str, message: str = ''):
    tender.status = status
    tender.progress_message = message
    tender.save(update_fields=['status', 'progress_message', 'updated_at'])


def process_tender(tender_id: int):
    """Full AI pipeline: parse -> extract -> score -> generate."""
    tender = Tender.objects.get(id=tender_id)

    try:
        # Stage 1: Parse PDF
        update_status(tender, 'parsing', 'Извлекаем текст из PDF...')
        parsed = parse_pdf(tender.pdf_file.path)
        tender.parsed_text = parsed['full_text']
        tender.page_count = parsed['page_count']
        tender.save(update_fields=['parsed_text', 'page_count'])
        update_status(tender, 'parsing', f'Обработано {parsed["page_count"]} страниц')

        # Stage 2: Extract requirements via Claude (with cache)
        update_status(tender, 'extracting', 'AI анализирует требования...')
        text_hash = hashlib.md5(parsed['full_text'].encode()).hexdigest()
        cache_key = f'extract:{text_hash}'
        extracted = cache.get(cache_key)
        if not extracted:
            extracted = extract_requirements(parsed['full_text'])
            cache.set(cache_key, extracted, CACHE_TTL)

        tender.title = extracted.get('title', '')[:500]
        tender.summary = {
            'amount': extracted.get('amount', ''),
            'deadline': extracted.get('deadline', ''),
            'customer': extracted.get('customer', ''),
            'category': extracted.get('category', ''),
            'delivery_location': extracted.get('delivery_location', ''),
        }
        tender.pitfalls = extracted.get('pitfalls', [])
        tender.save(update_fields=['title', 'summary', 'pitfalls'])

        # Save requirements
        Requirement.objects.filter(tender=tender).delete()
        for i, req in enumerate(extracted.get('requirements', [])):
            Requirement.objects.create(
                tender=tender,
                text=req.get('text', ''),
                category=req.get('category', 'technical'),
                status=_map_severity(req.get('severity', 'ok')),
                details=req.get('details', ''),
                order=i,
            )

        req_count = len(extracted.get('requirements', []))
        update_status(tender, 'extracting', f'Найдено {req_count} требований')

        # Stage 3: Risk scoring
        update_status(tender, 'scoring', 'Оцениваем риски...')
        scoring = calculate_risk_score(extracted)
        tender.risk_score = max(0, min(100, scoring.get('risk_score', 50)))
        tender.risk_explanation = scoring.get('risk_explanation', '')
        tender.save(update_fields=['risk_score', 'risk_explanation'])

        # Stage 4: Generate proposal
        update_status(tender, 'generating', 'Генерируем техническое предложение...')
        proposal = generate_proposal(extracted)
        tender.technical_proposal = proposal
        tender.save(update_fields=['technical_proposal'])

        # Stage 5: Store embedding for RAG (non-blocking)
        try:
            store_tender_embedding(
                tender_id=tender.id,
                title=tender.title,
                category=extracted.get('category', ''),
                text=parsed['full_text'][:4000],
            )
        except Exception as e:
            logger.warning(f'RAG storage skipped: {e}')

        update_status(tender, 'completed', 'Анализ завершён')

    except Exception as e:
        logger.exception(f'Pipeline failed for tender {tender_id}')
        update_status(tender, 'failed', f'Ошибка: {str(e)[:150]}')


def _map_severity(severity: str) -> str:
    mapping = {
        'critical': 'critical',
        'warning': 'warning',
        'ok': 'ok',
        'high': 'critical',
        'medium': 'warning',
        'low': 'ok',
    }
    return mapping.get(severity, 'needs_review')

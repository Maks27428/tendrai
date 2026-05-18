import logging
from django.conf import settings
from .embedder import get_embedding

logger = logging.getLogger(__name__)

COLLECTION_NAME = 'tender_embeddings'
VECTOR_DIM = 1024

_connected = False


def _ensure_connection():
    """Lazy-connect to Milvus. No-op if not configured."""
    global _connected
    if _connected or not settings.MILVUS_HOST:
        return _connected

    try:
        from pymilvus import connections, utility, CollectionSchema, FieldSchema, DataType, Collection

        secure = settings.MILVUS_SECURE
        protocol = 'https' if secure else 'http'
        uri = f'{protocol}://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}'

        connections.connect(
            alias='default',
            uri=uri,
            user=settings.MILVUS_USER or None,
            password=settings.MILVUS_PASSWORD or None,
            secure=secure,
        )

        if not utility.has_collection(COLLECTION_NAME):
            fields = [
                FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name='tender_id', dtype=DataType.INT64),
                FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=512),
                FieldSchema(name='category', dtype=DataType.VARCHAR, max_length=64),
                FieldSchema(name='text_preview', dtype=DataType.VARCHAR, max_length=2000),
                FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=VECTOR_DIM),
            ]
            schema = CollectionSchema(fields, description='Tender text embeddings for RAG')
            col = Collection(COLLECTION_NAME, schema)
            col.create_index('embedding', {
                'index_type': 'IVF_FLAT',
                'metric_type': 'COSINE',
                'params': {'nlist': 128},
            })
            col.load()
            logger.info('Milvus collection created and loaded')
        else:
            from pymilvus import Collection
            Collection(COLLECTION_NAME).load()

        _connected = True
        logger.info('Milvus connected')
    except Exception as e:
        logger.warning(f'Milvus connection failed: {e}')
        _connected = False

    return _connected


def store_tender_embedding(tender_id: int, title: str, category: str, text: str):
    """Embed and store a tender for future similarity search."""
    if not _ensure_connection():
        return

    embedding = get_embedding(text)
    if not embedding:
        return

    try:
        from pymilvus import Collection
        col = Collection(COLLECTION_NAME)
        col.insert([
            [tender_id],
            [title[:500]],
            [category[:60]],
            [text[:1900]],
            [embedding],
        ])
        col.flush()
        logger.info(f'Stored embedding for tender {tender_id}')
    except Exception as e:
        logger.warning(f'Milvus insert error: {e}')


def find_similar_tenders(text: str, top_k: int = 3) -> list[dict]:
    """Find similar tenders by text. Returns list of {tender_id, title, category, score}."""
    if not _ensure_connection():
        return []

    embedding = get_embedding(text)
    if not embedding:
        return []

    try:
        from pymilvus import Collection
        col = Collection(COLLECTION_NAME)
        results = col.search(
            data=[embedding],
            anns_field='embedding',
            param={'metric_type': 'COSINE', 'params': {'nprobe': 16}},
            limit=top_k,
            output_fields=['tender_id', 'title', 'category', 'text_preview'],
        )

        similar = []
        for hits in results:
            for hit in hits:
                similar.append({
                    'tender_id': hit.entity.get('tender_id'),
                    'title': hit.entity.get('title'),
                    'category': hit.entity.get('category'),
                    'text_preview': hit.entity.get('text_preview'),
                    'score': round(hit.score, 4),
                })
        return similar
    except Exception as e:
        logger.warning(f'Milvus search error: {e}')
        return []

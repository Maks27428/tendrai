# TendrAI — AI-ассистент для госзакупок РК

## Стек
- **Frontend:** React + Vite + TypeScript + Tailwind CSS v4 (порт 5173/5174)
- **Backend:** Django 5 + DRF (порт 8000)
- **БД:** SQLite (хакатон) / PostgreSQL (Alem Plus)
- **LLM:** Claude API (Anthropic SDK), модель claude-sonnet-4-20250514
- **Векторная БД:** Milvus (Alem Plus)
- **Кеш:** Redis (Alem Plus)
- **Эмбеддинги:** Alem Plus Embedder API

## Alem Plus (plus.alem.ai)

Облачная платформа хакатона. Все сервисы подключаются через `.env`.

### PostgreSQL
- В `.env` поставить `DB_ENGINE=postgresql` и заполнить DB_HOST/DB_USER/DB_PASSWORD
- Django автоматически переключится с SQLite

### Redis (кеш ответов Claude)
- Host: `a1-redis1.alem.ai`, Port: `31003`
- Заполнить REDIS_PASSWORD в `.env`
- Django автоматически включает Redis-кеш если REDIS_HOST задан

### Embedder API
- Endpoint: `https://llm.alem.ai/v1/embeddings`
- Модель: `text-1024` (1024-мерные векторы)
- Заполнить EMBEDDER_API_KEY в `.env`
- Код: `ai_pipeline/embedder.py`

### Milvus (векторный поиск похожих тендеров)
- Заполнить MILVUS_HOST/MILVUS_USER/MILVUS_PASSWORD в `.env`
- Код: `ai_pipeline/rag.py`
- Коллекция `tender_embeddings` создаётся автоматически

## Важные команды
```bash
# Сид демо-данных (2 тендера с полным анализом)
python manage.py seed_demo --reset

# Запуск бэкенда
python manage.py runserver 0.0.0.0:8000

# Запуск фронтенда
cd ../frontend && npm run dev
```

## TypeScript
- `verbatimModuleSyntax: true` — все type-импорты через `import type { ... }`

## Архитектура AI Pipeline
```
PDF → PyMuPDF → Claude (extract) → Claude (score) → Claude (generate)
                     ↓                                      ↑
              Embedder API → Milvus (store)          RAG context
                                 ↓
                        find_similar_tenders()
```

Кеш Redis хранит ответы Claude по MD5 хешу текста — повторный анализ одинакового PDF мгновенный.

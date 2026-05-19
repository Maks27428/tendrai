# TendrAI — AI-ассистент для госзакупок РК

## Стек
- **Frontend:** React + Vite + TypeScript + Tailwind CSS v4 (порт 5173/5174)
- **Backend:** Django 5 + DRF (порт 8000)
- **БД:** PostgreSQL (Alem Plus), SQLite как fallback
- **LLM:** Alem Plus LLM (OpenAI-compatible API), модель `alemllm`
- **Векторная БД:** Milvus (Alem Plus)
- **Кеш:** Redis (Alem Plus)
- **Эмбеддинги:** Alem Plus Embedder API

## Alem Plus (plus.alem.ai)

Облачная платформа хакатона. Все сервисы подключаются через `.env`.

### PostgreSQL
- В `.env` поставить `DB_ENGINE=postgresql` и заполнить DB_HOST/DB_USER/DB_PASSWORD
- Django автоматически переключится с SQLite

### Redis (кеш ответов LLM)
- Host: `a1-redis1.alem.ai`, Port: `31003`
- Заполнить REDIS_PASSWORD в `.env`
- Django автоматически включает Redis-кеш если REDIS_HOST задан

### AlemLLM (основная языковая модель)
- Endpoint: `https://llm.alem.ai/v1/chat/completions`
- Модель: `alemllm` (247B параметров, MoE)
- OpenAI-compatible API (requests POST)
- Заполнить LLM_API_KEY в `.env`
- Код: `ai_pipeline/llm_client.py` — единый клиент, все модули (extractor, scorer, generator, monopoly) используют `call_llm()`
- Запасной вариант: GPT OSS (ключ тоже запрошен, модель `gpt-oss`)

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
PDF → PyMuPDF → LLM (extract) → LLM (score) → LLM (generate)
                     ↓                                      ↑
              Embedder API → Milvus (store)          RAG context
                                 ↓
                        find_similar_tenders()
```

Кеш Redis хранит ответы LLM по MD5 хешу текста — повторный анализ одинакового PDF мгновенный.

## Хакатон AlemAI

### Ключевые даты
- **18 мая** — Open Day, старт хакатона
- **20 мая, 14:00** — дедлайн сдачи проекта
- **21 мая** — экспертная оценка
- **22 мая, 15:30–17:30** — Demo Day (3 мин питч + 2 мин Q&A)

### Обязательные требования к проекту
1. Код на **GitLab AlemPlus** (`a1-gitlab3.alem.ai`)
2. Деплой с публичным URL на `*.gitlabapp.alem.ai`
3. Минимум **3 инструмента AlemPlus** (у нас 6: PostgreSQL, Redis, Embedder, Milvus, AlemLLM, GitLab)
4. Публикация на **Витрине AlemPlus**
5. **Pitch Deck PDF** (до 10 слайдов)
6. Работающее MVP с реальным AI-компонентом

### Что НЕ принимается
- Чат-боты без уникальной логики
- Проекты без AI
- Без инструментов AlemPlus
- Заранее готовые проекты
- Неработающие демо

### Критерии оценки (по 5 баллов)
- Техническая реализация
- Рыночный анализ
- UX/UI
- Питчинг

### Призы
- 1 место: $10,000
- 2 место: $5,000
- 3 место: $3,000

## Pitch Deck — структура (11 слайдов)

1. **Команда** — название + фото участников + fun fact
2. **Продукт + Рынок** — название, размер рынка, ЦА, тренды, конкуренты
3. **О продукте (1)** — что это, какую проблему решает
4. **О продукте (2)** — для кого, как работает
5. **Технологии** — стек, архитектура, процесс разработки
6. **Скриншоты MVP** — 3 пользовательских сценария со скриншотами
7. **Бизнес-модель** — ЦА, ценностное предложение, монетизация, go-to-market, CJM
8. **MVP-сценарий 1** — первое касание (скриншот)
9. **MVP-сценарий 2** — ключевая фича (скриншот)
10. **MVP-сценарий 3** — результат / обратная связь (скриншот)
11. **Инструменты AlemPlus** — какие использовали + скриншоты-доказательства

## Деплой

### Docker (production)
- `Dockerfile` — multi-stage: node:20-alpine (frontend build) → python:3.13-slim (backend + gunicorn + whitenoise)
- `docker-compose.yml` — single `web` service, env_file из `backend/.env`
- `gunicorn.conf.py` — 2 workers, bind 0.0.0.0:8000
- `vite.config.ts` — `base: '/static/frontend/'` только для build, dev остаётся `/`
- `config/urls.py` — SPA catch-all для non-API routes в production

### GitLab CI/CD
- `.gitlab-ci.yml` — stages: build → deploy (manual)
- Переменные: LLM_API_URL, LLM_API_KEY, LLM_MODEL, DB_*, REDIS_*, EMBEDDER_*, MILVUS_*

## Монополия (фича)

Кросс-тендерный анализ на коррупцию:
- Backend: `ai_pipeline/monopoly.py` — `check_monopoly()`, `prepare_tender_data()`
- Промпты: `ai_pipeline/prompts.py` — MONOPOLY_SYSTEM, MONOPOLY_USER
- API: `POST /api/tenders/monopoly-check/` — принимает `{tender_ids: [1,2,3]}`
- Frontend: `/monopoly` — выбор 2+ тендеров, ScoreGauge, флаги с severity
- Проверяет: совпадение телефонов, email, ИИН/БИН, адресов, банковских реквизитов, идентичные ТЗ, привязка к бренду, дробление закупок

## Git

Репозиторий инициализирован в `D:\Alem AI\`. Remote — GitLab AlemPlus (`a1-gitlab3.alem.ai`), репо `tendrai`.

```bash
# Push на GitLab (после добавления remote)
git remote add origin https://a1-gitlab3.alem.ai/<username>/tendrai.git
git push -u origin master
```

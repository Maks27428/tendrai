# Single-stage: Python backend + pre-built frontend
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

COPY frontend/dist /app/frontend_dist

RUN DEBUG=0 DJANGO_SECRET_KEY=build-placeholder python manage.py collectstatic --noinput 2>/dev/null || true

EXPOSE 8000

CMD python manage.py migrate --noinput && gunicorn config.wsgi:application -c gunicorn.conf.py

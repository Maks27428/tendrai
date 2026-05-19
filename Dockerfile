# ============================================
# Stage 1: Build frontend
# ============================================
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# ============================================
# Stage 2: Python backend + serve everything
# ============================================
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

# Install system deps for psycopg2, pymupdf
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend into backend static dir
COPY --from=frontend-build /app/frontend/dist /app/frontend_dist

# Collect static files (uses whitenoise)
RUN DEBUG=0 DJANGO_SECRET_KEY=build-placeholder python manage.py collectstatic --noinput 2>/dev/null || true

EXPOSE 8000

# Run migrations then start gunicorn
CMD python manage.py migrate --noinput && gunicorn config.wsgi:application -c gunicorn.conf.py

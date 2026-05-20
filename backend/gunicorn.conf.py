"""Gunicorn configuration for TendrAI."""

bind = "0.0.0.0:80"
workers = 2
worker_class = "sync"
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"

web: gunicorn EditEngine.wsgi --log-file -
# Worker concurrency matches DEFAULT_WORKER_CONCURRENCY in services/core/constants.py
# This ensures alignment with LLM API semaphore limits for optimal rate limiting
worker: celery -A EditEngine worker -l info --concurrency=100

web: gunicorn EditEngine.wsgi:application --bind 0.0.0.0:8000 --workers $DJANGO_WORKERS --max-requests $DJANGO_MAX_REQUESTS --log-file -
migrate: python manage.py migrate
collectstatic: python manage.py collectstatic --noinput
celery-worker: celery -A EditEngine worker -l info --concurrency=$CELERY_WORKER_CONCURRENCY --pool=$CELERY_WORKER_POOL --max-tasks-per-child=$CELERY_MAX_TASKS_PER_CHILD
celery-beat: celery -A EditEngine beat -l info

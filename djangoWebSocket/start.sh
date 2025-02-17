#!/bin/sh

while ! nc -z frontend 8000; do
  echo "Waiting for frontend..."
  sleep 1
done

python manage.py makemigrations
python manage.py migrate

daphne -b 0.0.0.0 -p 8065 djangoWebSocket.asgi:application & gunicorn djangoWebSocket.wsgi:application --bind 0.0.0.0:8066 --workers 1 --timeout 300

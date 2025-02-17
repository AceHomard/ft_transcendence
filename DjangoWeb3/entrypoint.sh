#!/bin/sh

while ! nc -z matchmaking 8065; do
  echo "Waiting for matchmaking..."
  sleep 1
done

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
exec "$@"

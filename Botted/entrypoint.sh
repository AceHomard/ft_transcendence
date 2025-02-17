#!/bin/sh

while ! nc -z crypto 8020; do
  echo "Waiting for crypto..."
  sleep 2
done

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
exec "$@"

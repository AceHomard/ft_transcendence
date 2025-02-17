#!/bin/sh

while ! nc -z authentification 8050; do
  echo "Waiting for authentification..."
  sleep 1
done

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
exec "$@"

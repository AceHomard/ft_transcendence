#!/bin/sh

# Attendre que PostgreSQL soit prêt
until pg_isready -h db -p 5432 -U admin; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

sleep 1

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
exec "$@"

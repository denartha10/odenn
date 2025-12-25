#!/bin/bash
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Running database migrations..."
python manage.py migrate --noinput

# Create superuser if one doesn't exist
echo "Checking for superuser..."
python create_superuser.py

echo "Starting gunicorn server..."
exec gunicorn oden_site.wsgi:application --bind 0.0.0.0:$PORT --log-level info --access-logfile - --error-logfile -


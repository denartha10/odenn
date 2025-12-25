#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Starting gunicorn server..."
exec gunicorn oden_site.wsgi:application --bind 0.0.0.0:$PORT --log-level info --access-logfile - --error-logfile -


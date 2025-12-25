#!/bin/bash
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Running database migrations..."
python manage.py migrate --noinput

# One-time data import (will only run if flag file doesn't exist)
if [ -f "local_data.json" ] && [ ! -f ".data_imported" ]; then
    echo "Importing local data..."
    python manage.py loaddata local_data.json && touch .data_imported
    echo "Data import complete!"
fi

echo "Starting gunicorn server..."
exec gunicorn oden_site.wsgi:application --bind 0.0.0.0:$PORT --log-level info --access-logfile - --error-logfile -


#!/bin/bash
# Script to build the static site

echo "Building static site..."
python manage.py collectstatic --noinput
python manage.py build

echo "Static site built in the 'build' directory!"
echo "You can now deploy the contents of the 'build' directory to any static hosting service."


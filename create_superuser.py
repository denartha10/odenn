#!/usr/bin/env python
"""
Script to create a superuser if one doesn't exist.
Run this on Railway or locally.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oden_site.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if any superuser exists
if not User.objects.filter(is_superuser=True).exists():
    print("No superuser found. Creating one...")
    
    # Get credentials from environment or use defaults
    username = os.environ.get('SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')
    
    # Create superuser
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"Superuser created!")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("\n⚠️  IMPORTANT: Change the password after first login!")
else:
    print("Superuser already exists. Skipping creation.")


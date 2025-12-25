#!/usr/bin/env python
"""
Generate a secure secret key for Django production use.
Run: python generate_secret_key.py
"""
import secrets

if __name__ == '__main__':
    secret_key = secrets.token_urlsafe(50)
    print(f"\nYour Django SECRET_KEY:")
    print(f"{secret_key}\n")
    print("Copy this value and add it to your Railway environment variables as SECRET_KEY\n")


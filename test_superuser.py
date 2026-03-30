#!/usr/bin/env python
"""
Quick test to create superuser locally before Render deploy
Run this while venv is activated: python test_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FSWD.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'admin'
email = 'admin@example.com'
password = 'Admin@123456'

if User.objects.filter(is_superuser=True).exists():
    print("✓ Superuser already exists")
else:
    User.objects.create_superuser(username, email, password)
    print(f"✓ Superuser '{username}' created!")
    print(f"  Email: {email}")
    print(f"  Password: {password}")

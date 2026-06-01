#!/usr/bin/env python
"""
Script pour créer un utilisateur de test
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User

# Delete if exists
User.objects.filter(username='testuser').delete()

# Create new user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='Test123456!'
)

print(f"✓ User created: {user.username}")
print(f"  Email: {user.email}")

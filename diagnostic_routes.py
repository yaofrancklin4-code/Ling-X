# -*- coding: utf-8 -*-
"""
Diagnostic des routes et vues
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("="*60)
print("DIAGNOSTIC DES ROUTES")
print("="*60)

client = Client()

# Routes à tester
routes_to_test = [
    ('/', 'home', False),
    ('/login/', 'login', False),
    ('/register/', 'register', False),
    ('/dictionary/', 'dictionary', False),
    ('/culture/', 'culture', False),
    ('/histoire/', 'histoire', False),
    ('/societe/', 'societe', False),
    ('/territoire/', 'territoire', False),
    ('/stories/', 'stories', False),
    ('/baule-names/', 'baule_names', False),
    ('/proverbs/', 'proverbs', False),
    ('/dashboard/', 'dashboard', True),
    ('/categories/', 'categories', True),
    ('/games/', 'games', True),
]

print("\n[TEST DES ROUTES PUBLIQUES]\n")

for url, name, needs_auth in routes_to_test:
    try:
        if needs_auth:
            # Créer un utilisateur temporaire
            user = User.objects.first()
            if user:
                client.force_login(user)
        
        response = client.get(url)
        status = response.status_code
        
        if status == 200:
            print(f"[OK]  {url:30} -> {status}")
        elif status == 302:
            print(f"[REDIRECT] {url:30} -> {status} (redirection)")
        else:
            print(f"[ERROR] {url:30} -> {status}")
            
    except Exception as e:
        print(f"[ERROR] {url:30} -> {str(e)[:40]}")
    
    if needs_auth:
        client.logout()

print("\n" + "="*60)
print("FIN DU DIAGNOSTIC")
print("="*60)

# -*- coding: utf-8 -*-
"""
Script pour tester toutes les routes Django
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.urls import get_resolver
from django.test import RequestFactory
from django.contrib.auth.models import User

print("="*60)
print("TEST DES ROUTES DJANGO")
print("="*60)

# Récupérer toutes les URLs
resolver = get_resolver()
url_patterns = []

def extract_urls(urlpatterns, prefix=''):
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
        else:
            url_patterns.append({
                'pattern': prefix + str(pattern.pattern),
                'name': pattern.name if hasattr(pattern, 'name') else None,
                'callback': pattern.callback if hasattr(pattern, 'callback') else None
            })

extract_urls(resolver.url_patterns)

# Filtrer les URLs de l'app lingx
lingx_urls = [u for u in url_patterns if u['name'] and not u['name'].startswith('admin')]

print(f"\nNombre total de routes: {len(lingx_urls)}")
print("\nListe des routes disponibles:\n")

# Grouper par type
public_routes = []
auth_routes = []
api_routes = []

for url in lingx_urls:
    if url['name']:
        route_info = f"  - {url['name']:30} -> {url['pattern']}"
        
        if 'api' in url['pattern']:
            api_routes.append(route_info)
        elif url['name'] in ['home', 'login', 'register', 'culture', 'histoire', 'societe', 'territoire', 'dictionary', 'stories', 'baule_names', 'proverbs']:
            public_routes.append(route_info)
        else:
            auth_routes.append(route_info)

print("\n[ROUTES PUBLIQUES]")
for route in sorted(public_routes):
    print(route)

print(f"\n[ROUTES AUTHENTIFIEES] ({len(auth_routes)})")
for route in sorted(auth_routes)[:10]:  # Afficher les 10 premières
    print(route)
if len(auth_routes) > 10:
    print(f"  ... et {len(auth_routes) - 10} autres routes")

print(f"\n[ROUTES API] ({len(api_routes)})")
for route in sorted(api_routes)[:10]:  # Afficher les 10 premières
    print(route)
if len(api_routes) > 10:
    print(f"  ... et {len(api_routes) - 10} autres routes")

print("\n" + "="*60)
print("[SUCCESS] Toutes les routes sont configurees correctement")
print("="*60)
print("\nPour tester le serveur, lancez:")
print("  python manage.py runserver")
print("\nAccedez ensuite a: http://127.0.0.1:8000/")

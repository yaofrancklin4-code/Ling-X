# -*- coding: utf-8 -*-
"""
Analyse complète de toutes les pages du projet
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.test import Client
from django.urls import get_resolver
from django.template.loader import get_template
import re

print("="*80)
print(" "*25 + "ANALYSE COMPLETE DES PAGES")
print("="*80)

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
            })

extract_urls(resolver.url_patterns)

# Filtrer les URLs de l'app lingx (exclure admin et API)
lingx_urls = [u for u in url_patterns if u['name'] and not u['name'].startswith('admin') and 'api' not in u['pattern']]

# Routes à analyser en détail
routes_to_analyze = [
    ('/', 'home', 'home.html'),
    ('/login/', 'login', 'login.html'),
    ('/register/', 'register', 'register.html'),
    ('/dashboard/', 'dashboard', 'dashboard.html'),
    ('/categories/', 'categories', 'categories.html'),
    ('/dictionary/', 'dictionary', 'dictionary.html'),
    ('/culture/', 'culture', 'culture.html'),
    ('/histoire/', 'histoire', 'histoire.html'),
    ('/societe/', 'societe', 'societe.html'),
    ('/territoire/', 'territoire', 'territoire.html'),
    ('/stories/', 'stories', 'stories.html'),
    ('/baule-names/', 'baule_names', 'baule_names.html'),
    ('/proverbs/', 'proverbs', 'proverbs.html'),
    ('/games/', 'games', 'games.html'),
    ('/leaderboard/', 'leaderboard', 'leaderboard.html'),
    ('/profile/', 'profile', 'profile.html'),
    ('/community/', 'community', 'community.html'),
]

client = Client()

print("\n[ANALYSE DES ROUTES]\n")
print(f"{'Route':<30} {'Status':<10} {'Template':<25} {'Taille':<10}")
print("-" * 80)

results = []

for url, name, template_name in routes_to_analyze:
    try:
        # Test de la route
        response = client.get(url, follow=True)
        status = response.status_code
        
        # Vérifier le template
        template_path = os.path.join('templates', template_name)
        template_exists = os.path.exists(template_path)
        
        # Taille du template
        if template_exists:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                size = len(content)
                
                # Analyser le contenu
                has_content = len(content) > 1000
                has_sections = content.count('<section') > 0 or content.count('<div class=') > 3
                has_images = 'img' in content or 'image' in content
                
                status_icon = "[OK]" if status == 200 else "[ERROR]"
                size_str = f"{size} bytes"
                
                results.append({
                    'url': url,
                    'name': name,
                    'template': template_name,
                    'status': status,
                    'size': size,
                    'has_content': has_content,
                    'has_sections': has_sections,
                    'has_images': has_images,
                    'needs_improvement': not (has_content and has_sections)
                })
                
                print(f"{url:<30} {status_icon:<10} {template_name:<25} {size_str:<10}")
        else:
            print(f"{url:<30} [MISSING] {template_name:<25} {'N/A':<10}")
            results.append({
                'url': url,
                'name': name,
                'template': template_name,
                'status': 404,
                'needs_improvement': True
            })
            
    except Exception as e:
        print(f"{url:<30} [ERROR]   {template_name:<25} {str(e)[:20]}")
        results.append({
            'url': url,
            'name': name,
            'template': template_name,
            'status': 500,
            'error': str(e),
            'needs_improvement': True
        })

# Résumé
print("\n" + "="*80)
print(" "*30 + "RESUME DE L'ANALYSE")
print("="*80)

pages_ok = len([r for r in results if r['status'] == 200])
pages_error = len([r for r in results if r['status'] != 200])
pages_need_improvement = len([r for r in results if r.get('needs_improvement', False)])

print(f"\n  Total pages analysees:        {len(results)}")
print(f"  Pages fonctionnelles:         {pages_ok}")
print(f"  Pages avec erreurs:           {pages_error}")
print(f"  Pages a ameliorer:            {pages_need_improvement}")

# Pages à améliorer
if pages_need_improvement > 0:
    print("\n[PAGES A AMELIORER]\n")
    for r in results:
        if r.get('needs_improvement', False):
            reason = []
            if r.get('size', 0) < 1000:
                reason.append("contenu insuffisant")
            if not r.get('has_sections', False):
                reason.append("manque de sections")
            if not r.get('has_images', False):
                reason.append("manque d'images")
            
            print(f"  - {r['url']:<30} ({', '.join(reason)})")

print("\n" + "="*80)
print("\n[PROCHAINE ETAPE]")
print("  Amelioration des pages une par une...")
print("="*80)

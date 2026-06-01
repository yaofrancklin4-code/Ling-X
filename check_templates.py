#!/usr/bin/env python
import os
import sys
import django
from django.template import TemplateSyntaxError

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.template.loader import get_template
from django.template import engines

# Templates to check
templates_to_check = [
    'category_detail.html',
    'lesson_detail.html',
    'categories.html',
    'tests_list.html',
    'quiz.html',
]

print("=== VÉRIFICATION DE LA SYNTAXE DES TEMPLATES ===\n")

for template_name in templates_to_check:
    try:
        template = get_template(template_name)
        print(f"✓ {template_name}: OK")
    except TemplateSyntaxError as e:
        print(f"✗ {template_name}: ERREUR DE SYNTAXE")
        print(f"  Line {e.lineno}: {e.msg}")
    except Exception as e:
        print(f"✗ {template_name}: ERREUR")
        print(f"  {str(e)}")

print("\n=== FIN DE LA VÉRIFICATION ===")

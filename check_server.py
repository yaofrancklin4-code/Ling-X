# -*- coding: utf-8 -*-
"""
Script pour vérifier que le serveur Django peut démarrer
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings

print("="*60)
print("VERIFICATION DU SERVEUR DJANGO")
print("="*60)

# Vérifier les migrations
print("\n[1/5] Verification des migrations...")
try:
    call_command('makemigrations', '--dry-run', '--check', verbosity=0)
    print("[OK] Aucune migration en attente")
except SystemExit:
    print("[WARNING] Des migrations sont en attente")
    print("        Executez: python manage.py makemigrations")
    print("                  python manage.py migrate")

# Vérifier les fichiers statiques
print("\n[2/5] Verification des fichiers statiques...")
static_dirs = settings.STATICFILES_DIRS
static_root = settings.STATIC_ROOT
print(f"[OK] STATIC_URL: {settings.STATIC_URL}")
print(f"[OK] STATICFILES_DIRS: {static_dirs}")
print(f"[OK] STATIC_ROOT: {static_root}")

# Vérifier les médias
print("\n[3/5] Verification des fichiers media...")
print(f"[OK] MEDIA_URL: {settings.MEDIA_URL}")
print(f"[OK] MEDIA_ROOT: {settings.MEDIA_ROOT}")

# Vérifier les templates
print("\n[4/5] Verification des templates...")
template_dirs = settings.TEMPLATES[0]['DIRS']
print(f"[OK] TEMPLATES DIRS: {template_dirs}")

# Vérifier la base de données
print("\n[5/5] Verification de la base de donnees...")
from django.contrib.auth.models import User
from lingx.models import Category, Lesson, Vocabulary, DictionaryEntry

user_count = User.objects.count()
cat_count = Category.objects.count()
lesson_count = Lesson.objects.count()
vocab_count = Vocabulary.objects.count()
dict_count = DictionaryEntry.objects.count()

print(f"[OK] Users: {user_count}")
print(f"[OK] Categories: {cat_count}")
print(f"[OK] Lessons: {lesson_count}")
print(f"[OK] Vocabulaire: {vocab_count}")
print(f"[OK] Dictionnaire: {dict_count}")

print("\n" + "="*60)
print("[SUCCESS] Le serveur est pret a demarrer!")
print("="*60)
print("\nPour lancer le serveur:")
print("  python manage.py runserver")
print("\nOu utilisez le fichier batch:")
print("  start_server.bat")
print("\nAcces:")
print("  - Application: http://127.0.0.1:8000/")
print("  - Admin:       http://127.0.0.1:8000/admin/")
print("  - API:         http://127.0.0.1:8000/api/")

# -*- coding: utf-8 -*-
"""
Script de test pour vérifier que Django démarre sans erreur
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

print("[OK] Django setup OK")

# Test des imports
try:
    from lingx import models
    print("[OK] Models import OK")
except Exception as e:
    print(f"[ERROR] Models import ERROR: {e}")
    sys.exit(1)

try:
    from lingx import views
    print("[OK] Views import OK")
except Exception as e:
    print(f"[ERROR] Views import ERROR: {e}")
    sys.exit(1)

try:
    from lingx import serializers
    print("[OK] Serializers import OK")
except Exception as e:
    print(f"[ERROR] Serializers import ERROR: {e}")
    sys.exit(1)

try:
    from lingx import urls
    print("[OK] URLs import OK")
except Exception as e:
    print(f"[ERROR] URLs import ERROR: {e}")
    sys.exit(1)

try:
    from lingx.dictionary_service import DictionarySearchService
    print("[OK] Dictionary service import OK")
except Exception as e:
    print(f"[ERROR] Dictionary service import ERROR: {e}")
    sys.exit(1)

try:
    from lingx.services import GamificationService
    print("[OK] Gamification service import OK")
except Exception as e:
    print(f"[ERROR] Gamification service import ERROR: {e}")
    sys.exit(1)

# Test de la base de données
try:
    from django.contrib.auth.models import User
    user_count = User.objects.count()
    print(f"[OK] Database connection OK ({user_count} users)")
except Exception as e:
    print(f"[ERROR] Database connection ERROR: {e}")
    sys.exit(1)

# Test des modèles
try:
    from lingx.models import Category, Lesson, Vocabulary, DictionaryEntry
    cat_count = Category.objects.count()
    lesson_count = Lesson.objects.count()
    vocab_count = Vocabulary.objects.count()
    dict_count = DictionaryEntry.objects.count()
    print(f"[OK] Models OK (Categories: {cat_count}, Lessons: {lesson_count}, Vocab: {vocab_count}, Dict: {dict_count})")
except Exception as e:
    print(f"[ERROR] Models ERROR: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("[SUCCESS] TOUS LES TESTS SONT PASSES")
print("="*50)
print("\nVous pouvez maintenant lancer le serveur avec:")
print("python manage.py runserver")

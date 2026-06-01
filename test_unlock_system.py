#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from lingx.models import Lesson, Category, UserProfile
from lingx.views import is_lesson_unlocked_for_user, is_test_unlocked_for_user

print("=== TEST DU SYSTÈME DE VERROUILLAGE ===\n")

# Créer un utilisateur de test (ou utiliser le premier)
try:
    test_user = User.objects.create_user(username='test_unlock_user', password='testpass123')
    test_user.profile.level = 3  # Niveau 3
    test_user.profile.save()
    print(f"Utilisateur créé : {test_user.username} (Niveau {test_user.profile.level})")
except:
    # L'utilisateur existe déjà, l'utiliser
    test_user = User.objects.get(username='test_unlock_user')
    print(f"Utilisateur existant : {test_user.username} (Niveau {test_user.profile.level})")

print()

# Tester le déblocage avec des leçons
print("=== TEST DE DÉBLOCAGE DES LEÇONS ===")
lessons = Lesson.objects.all().order_by('number')[:15]  # Premiers 15 leçons

for lesson in lessons:
    is_unlocked = is_lesson_unlocked_for_user(test_user, lesson)
    status = "✓ DÉBLOQUÉE" if is_unlocked else "🔒 VERROUILLÉE"
    print(f"Leçon {lesson.number}: {lesson.title[:40]:<40} {status}")

print()
print(f"=== RÉSUMÉ ===")
print(f"Niveau de l'utilisateur: {test_user.profile.level}")
print(f"Leçons accessibles: 1 à {test_user.profile.level}")
print(f"Leçons verrouillées: {test_user.profile.level + 1} à 22")

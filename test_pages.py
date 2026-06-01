#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from lingx.models import Category, Lesson

print("=" * 70)
print("TEST DES PAGES DE COURS")
print("=" * 70)

client = Client()

# Créer un utilisateur de test
User.objects.filter(username='test_course').delete()
user = User.objects.create_user(username='test_course', password='test123')
client.login(username='test_course', password='test123')

# Test 1 : Page categories
print("\n1️⃣  TEST PAGE CATEGORIES")
response = client.get('/categories/')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✓ Page categories charge correctement")
else:
    print(f"✗ Erreur: {response.status_code}")

# Test 2 : Page category_detail avec ID 17
print("\n2️⃣  TEST PAGE CATEGORY_DETAIL (ID=17)")
try:
    category = Category.objects.get(id=17)
    response = client.get(f'/category/{category.id}/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ Page category {category.name} charge correctement")
    else:
        print(f"✗ Erreur: {response.status_code}")
except Category.DoesNotExist:
    print("✗ Catégorie ID=17 n'existe pas")
    # Afficher les catégories disponibles
    categories = Category.objects.all()
    print(f"Catégories disponibles: {categories.count()}")
    for cat in categories:
        print(f"  - ID={cat.id}: {cat.name}")

# Test 3 : Page lessons
print("\n3️⃣  TEST PAGE LESSONS")
try:
    lesson = Lesson.objects.first()
    if lesson:
        response = client.get(f'/lesson/{lesson.id}/')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ Page lesson {lesson.title} charge correctement")
        else:
            print(f"✗ Erreur: {response.status_code}")
    else:
        print("✗ Aucune leçon trouvée")
except Exception as e:
    print(f"✗ Erreur: {e}")

# Test 4 : Page games
print("\n4️⃣  TEST PAGE GAMES")
response = client.get('/games/')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✓ Page games charge correctement")
else:
    print(f"✗ Erreur: {response.status_code}")

# Test 5 : Page tests
print("\n5️⃣  TEST PAGE TESTS")
response = client.get('/tests/')
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✓ Page tests charge correctement")
else:
    print(f"✗ Erreur: {response.status_code}")

# Nettoyage
user.delete()

print("\n" + "=" * 70)
print("TESTS TERMINÉS")
print("=" * 70)

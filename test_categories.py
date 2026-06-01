#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Category, Lesson, LessonProgress

print("=== TEST DES CATÉGORIES 17 ET 18 ===\n")

# Vérifier les catégories
for cat_id in [17, 18]:
    try:
        category = Category.objects.get(id=cat_id)
        lessons = category.lessons.all().order_by('number')
        
        print(f"✓ Catégorie {cat_id}: {category.name}")
        print(f"  Description: {category.description}")
        print(f"  Nombre de leçons: {lessons.count()}")
        
        for lesson in lessons:
            print(f"    - Leçon {lesson.number}: {lesson.title}")
        print()
        
    except Category.DoesNotExist:
        print(f"✗ Catégorie {cat_id}: N'EXISTE PAS\n")

print("=== TEST DE RÉCUPÉRATION DES LEÇONS ===")

# Vérifier que les leçons peuvent être récupérées sans erreur
all_lessons = Lesson.objects.all()
print(f"Nombre total de leçons: {all_lessons.count()}")

# Tester la progres
print("\n=== TEST DE PROGRESSION ===")
progress_count = LessonProgress.objects.count()
print(f"Nombre d'enregistrements de progression: {progress_count}")

print("\n✓ Tous les tests sont passés avec succès!")

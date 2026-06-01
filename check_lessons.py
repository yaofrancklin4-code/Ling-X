#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Category, Lesson

# Vérifier les catégories 17 et 18
print("=== CATÉGORIES 17 et 18 ===\n")
for cat_id in [17, 18]:
    try:
        cat = Category.objects.get(id=cat_id)
        print(f"Catégorie {cat_id}: {cat.name}")
        print(f"  Description: {cat.description[:100]}")
        print(f"  Leçons:")
        lessons = cat.lessons.all()
        print(f"  Nombre de leçons: {lessons.count()}")
        for lesson in lessons:
            print(f"    - ID {lesson.id}: {lesson.title} (number={lesson.number})")
        print()
    except Category.DoesNotExist:
        print(f"Catégorie {cat_id}: N'EXISTE PAS")
        print()

import os
import sys
import django

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Category, Lesson

print("📊 Vérification du contenu\n")
print(f"Catégories totales: {Category.objects.count()}")
print(f"Leçons totales: {Lesson.objects.count()}\n")

print("🎨 Catégorie Couleurs:")
couleurs = Category.objects.filter(name='Couleurs').first()
if couleurs:
    print(f"  ✅ Existe")
    print(f"  Leçons: {couleurs.lessons.count()}")
    for lesson in couleurs.lessons.all():
        print(f"    - {lesson.title}")
else:
    print("  ❌ N'existe pas")

print("\n🦁 Catégorie Animaux:")
animaux = Category.objects.filter(name='Animaux').first()
if animaux:
    print(f"  ✅ Existe")
    print(f"  Leçons: {animaux.lessons.count()}")
    for lesson in animaux.lessons.all():
        print(f"    - {lesson.title}")
else:
    print("  ❌ N'existe pas")

print("\n📋 Toutes les catégories:")
for cat in Category.objects.all():
    print(f"  - {cat.name} ({cat.lessons.count()} leçons)")

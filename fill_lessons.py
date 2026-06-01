#!/usr/bin/env python3
import django, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Lesson

LESSON_CONTENT = {
    "Salutations": "# Bienvenue dans votre première leçon de Baoulé !\n\nLe Baoulé est une langue Akan parlée par environ 2 millions de personnes en Côte d'Ivoire.\n\n## Les salutations fondamentales\n\n- **N'gôh** = Bonjour\n- **Akwaba** = Bienvenue\n- **Yao** = Au revoir\n- **Dômlê** = Merci",
    "Les chiffres": "# Les Chiffres en Baoulé\n\n- 1 = Kunle\n- 2 = Nyo\n- 3 = Sa\n- 4 = Nyon\n- 5 = Nnu\n- 10 = Blu",
    "La famille": "# La Famille en Baoulé\n\n- **Ni** = Mère\n- **Sy** = Père\n- **Kpata** = Grand-père\n- **Nana** = Grand-mère\n- **Wawale** = Frère/Sœur aîné",
    "Les couleurs": "# Les Couleurs en Baoulé\n\n- **Rôô** = Rouge\n- **Funfun** = Blanc\n- **Blêlê** = Noir\n- **Gyigyi** = Vert\n- **Wlawlô** = Jaune/Or",
}

print("📚 Remplissage des leçons...")
for lesson in Lesson.objects.all():
    for key, content in LESSON_CONTENT.items():
        if key.lower() in lesson.title.lower():
            if len(lesson.content.strip()) < 50:
                lesson.content = content
                lesson.save()
                print(f"  ✅ {lesson.title}")
            break

print("\n✅ Terminé!")

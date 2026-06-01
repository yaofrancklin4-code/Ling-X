#!/usr/bin/env python
"""
Script pour configurer un système strict de 22 niveaux.
- Numérote les 22 premières leçons de 1 à 22
- Crée/numérote un quiz (test) par leçon de 1 à 22
- Supprime les leçons et quizzes en excès si nécessaire
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Lesson, Quiz, Category

def setup_22_levels():
    print("="*60)
    print("Configuration du système 22 niveaux")
    print("="*60)
    
    # Obtenir toutes les leçons triées par ID
    all_lessons = Lesson.objects.all().order_by('id')
    total_lessons = all_lessons.count()
    
    print(f"\nEtat actuel:")
    print(f"  - Leçons totales: {total_lessons}")
    print(f"  - Quizzes totaux: {Quiz.objects.count()}")
    
    # Garder les 22 premières leçons
    if total_lessons > 22:
        lessons_to_delete = all_lessons[22:]
        print(f"\n⚠️  Suppression de {len(lessons_to_delete)} leçons en excès...")
        deleted_count = 0
        for lesson in lessons_to_delete:
            lesson.delete()
            deleted_count += 1
        print(f"  ✓ {deleted_count} leçons supprimées")
    
    # Numéroter les 22 premières leçons
    lessons = Lesson.objects.all().order_by('id')[:22]
    print(f"\nNumérotation des leçons (1-22):")
    for idx, lesson in enumerate(lessons, start=1):
        lesson.number = idx
        lesson.save()
        print(f"  Leçon {idx}: {lesson.title}")
    
    # Pour chaque leçon, garder UN seul quiz et le numéroter
    print(f"\nNumérotation des tests (1 par leçon):")
    for idx, lesson in enumerate(lessons, start=1):
        quizzes = lesson.quizzes.all()
        quiz_count = quizzes.count()
        
        if quiz_count == 0:
            print(f"  ⚠️  Leçon {idx} ({lesson.title}): AUCUN quiz!")
        else:
            # Garder le premier quiz, supprimer les autres
            first_quiz = quizzes.first()
            if quiz_count > 1:
                quizzes_to_delete = quizzes[1:]
                for q in quizzes_to_delete:
                    q.delete()
                print(f"  Test {idx}: Suppression de {quiz_count - 1} quizzes en excès")
            
            # Numéroter le quiz conservé
            first_quiz.number = idx
            first_quiz.save()
            print(f"  Test {idx}: {first_quiz.question[:50]}...")
    
    # Nettoyage final
    print(f"\nNettoyage final:")
    print(f"  - Leçons: {Lesson.objects.count()}")
    print(f"  - Tests: {Quiz.objects.count()}")
    
    # Vérifier les utilisateurs
    from django.contrib.auth.models import User
    users = User.objects.filter(is_superuser=False)
    print(f"\n  - Utilisateurs: {users.count()}")
    
    for user in users[:5]:
        try:
            level = user.profile.level
            print(f"    • {user.username}: niveau {level}")
        except:
            print(f"    • {user.username}: pas de profil")
    
    print("\n✅ Configuration complétée!")
    print("="*60)

if __name__ == '__main__':
    setup_22_levels()

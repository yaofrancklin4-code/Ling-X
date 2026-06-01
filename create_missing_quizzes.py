#!/usr/bin/env python
"""
Script pour créer les quizzes manquants.
Crée un quiz pour chaque leçon qui n'en a pas.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Lesson, Quiz, QuizChoice

def create_missing_quizzes():
    print("="*60)
    print("Création des quizzes manquants")
    print("="*60)
    
    lessons = Lesson.objects.all().order_by('number')
    created_count = 0
    
    for lesson in lessons:
        quizzes = lesson.quizzes.all()
        if quizzes.count() == 0:
            # Créer un quiz de base pour cette leçon
            quiz = Quiz.objects.create(
                lesson=lesson,
                question=f"Quelle est la leçon {lesson.number} - {lesson.title}?",
                quiz_type='mcq',
                points=10,
                order=1,
                number=lesson.number
            )
            
            # Créer quelques choix de réponse
            QuizChoice.objects.create(
                quiz=quiz,
                choice_text=lesson.title,
                is_correct=True
            )
            QuizChoice.objects.create(
                quiz=quiz,
                choice_text="Autre réponse 1",
                is_correct=False
            )
            QuizChoice.objects.create(
                quiz=quiz,
                choice_text="Autre réponse 2",
                is_correct=False
            )
            
            print(f"✓ Quiz créé pour Leçon {lesson.number}: {lesson.title}")
            created_count += 1
        else:
            # Numéroter les quizzes existants
            for idx, q in enumerate(quizzes, start=1):
                q.number = lesson.number
                q.save()
    
    print(f"\n✅ {created_count} quizzes créés!")
    print(f"Total quizzes: {Quiz.objects.count()}")
    print("="*60)

if __name__ == '__main__':
    create_missing_quizzes()

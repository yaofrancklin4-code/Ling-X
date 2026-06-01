#!/usr/bin/env python
"""
Script pour créer/mettre à jour les utilisateurs avancés avec points
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from lingx.models import UserProfile, Lesson, LessonProgress

def create_or_update_user(email, username, points, lessons_to_complete):
    """Créer ou mettre à jour un utilisateur avec des points et des leçons complétées"""
    
    # Créer ou récupérer l'utilisateur
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'first_name': username}
    )
    
    if created:
        user.set_password('password123')
        user.save()
        print(f"✓ Utilisateur créé: {username}")
    else:
        print(f"✓ Utilisateur trouvé: {username}")
    
    # Créer ou récupérer le profil
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    # Mettre à jour les points
    profile.total_points = points
    profile.level = (points // 100) + 1
    
    # Promouvoir en avancé si 1000+ points
    if points >= 1000 and profile.role == 'student':
        profile.role = 'avance'
        profile.is_verified = True
        print(f"  → Promu en AVANCÉ (role='avance')")
    
    profile.save()
    print(f"  → Points: {points} | Niveau: {profile.level} | Rôle: {profile.role}")
    
    # Compléter les leçons spécifiées
    completed_count = 0
    for lesson_id in lessons_to_complete:
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            progress, created = LessonProgress.objects.get_or_create(
                user=user,
                lesson=lesson
            )
            if not progress.is_completed:
                progress.is_completed = True
                progress.score = lesson.points
                progress.attempts = 1
                progress.save()
                completed_count += 1
        except Lesson.DoesNotExist:
            pass
    
    if completed_count > 0:
        print(f"  → {completed_count} leçons complétées")
    
    return user, profile

def main():
    print("=" * 60)
    print("  Création/Mise à jour des utilisateurs avancés")
    print("=" * 60)
    
    # Récupérer tous les IDs de leçons
    all_lessons = Lesson.objects.values_list('id', flat=True)
    lesson_ids = list(all_lessons)
    total_lessons = len(lesson_ids)
    
    print(f"\n📚 Total de leçons disponibles: {total_lessons}")
    
    # Utilisateur 1: Yao - 1200 points (avancé) - 80% des leçons
    lessons_to_unlock_yao = lesson_ids[:int(total_lessons * 0.8)]
    print(f"\n1. Yao (franckliny77@gmail.com) - 1200 points")
    user1, profile1 = create_or_update_user(
        email='franckliny77@gmail.com',
        username='yao',
        points=1200,
        lessons_to_complete=lessons_to_unlock_yao
    )
    
    # Utilisateur 2: Francklin - 1500 points (avancé) - 100% des leçons
    lessons_to_unlock_francklin = lesson_ids  # Toutes les leçons
    print(f"\n2. Francklin (yaofrancklin4@gmail.com) - 1500 points")
    user2, profile2 = create_or_update_user(
        email='yaofrancklin4@gmail.com',
        username='francklin',
        points=1500,
        lessons_to_complete=lessons_to_unlock_francklin
    )
    
    print("\n" + "=" * 60)
    print("  Utilisateurs avancés créés/mis à jour avec succès!")
    print("=" * 60)
    print("\nMots de passe: password123")
    print("Noms d'utilisateurs: yao, francklin")
    print(f"\nYao: {len(lessons_to_unlock_yao)} leçons débloquées")
    print(f"Francklin: {len(lessons_to_unlock_francklin)} leçons débloquées")

if __name__ == '__main__':
    main()

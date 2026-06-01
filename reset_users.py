#!/usr/bin/env python
"""
Script pour réinitialiser le système - reset tous les utilisateurs au niveau 1.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User

def reset_users():
    print("="*60)
    print("Réinitialisation des utilisateurs au niveau 1")
    print("="*60)
    
    users = User.objects.filter(is_superuser=False)
    
    print(f"\nUtilisateurs à réinitialiser: {users.count()}")
    
    for user in users:
        try:
            profile = user.profile
            old_level = profile.level
            profile.level = 1
            profile.total_points = 0
            profile.save()
            print(f"  ✓ {user.username}: niveau {old_level} → 1")
        except:
            print(f"  ⚠️  {user.username}: pas de profil")
    
    print("\n✅ Réinitialisation complétée!")
    print("="*60)

if __name__ == '__main__':
    reset_users()

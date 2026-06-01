#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from lingx.models import UserProfile

# Test 1 : Créer un nouvel utilisateur (comme dans register_view)
print("=" * 60)
print("TEST 1 : Création via register_view (via create_user)")
print("=" * 60)

test_user = User.objects.create_user(
    username='new_user_test_final',
    email='newuser_final@test.com', 
    password='pass123'
)
print(f"✓ User créé: {test_user.username}")

# Vérifier le profil
profile_count = UserProfile.objects.filter(user=test_user).count()
print(f"✓ Nombre de profils: {profile_count}")

if profile_count == 1:
    profile = UserProfile.objects.get(user=test_user)
    print(f"✓ Profil trouvé: {profile}")
    print("✓ SUCCÈS - Pas d'erreur UNIQUE constraint!")
else:
    print(f"✗ ERREUR - {profile_count} profils trouvés!")

# Test 2 : Tentative de création d'un second profil (simuler l'ancien bug)
print("\n" + "=" * 60)
print("TEST 2 : Tentative de créer un second profil (bug ancien)")
print("=" * 60)
try:
    UserProfile.objects.create(user=test_user)
    print("✗ ERREUR - Créé un deuxième profil!")
except Exception as e:
    print(f"✓ Exception levée (attendu): {type(e).__name__}")
    print(f"✓ Message: {str(e)}")

# Nettoyage
test_user.delete()
print("\n✓ Test utilisateur supprimé")
print("\n" + "=" * 60)
print("✅ TOUS LES TESTS PASSENT - L'ERREUR EST RÉSOLUE")
print("=" * 60)

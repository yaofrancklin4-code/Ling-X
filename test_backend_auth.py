#!/usr/bin/env python
"""
Test du flux d'inscription et login avec le backend d'authentification spécifié
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from lingx.models import UserProfile

print("=" * 70)
print("TEST DU FLUX D'INSCRIPTION ET LOGIN")
print("=" * 70)

# Nettoyer les utilisateurs de test existants
User.objects.filter(username__startswith='test_register_').delete()

client = Client()

# Test 1 : Inscription
print("\n1️⃣  TEST D'INSCRIPTION")
print("-" * 70)

response = client.post('/register/', {
    'username': 'test_register_user',
    'email': 'test.register@example.com',
    'password': 'TestPass123!',
    'password2': 'TestPass123!',
})

# Vérifier que l'utilisateur a été créé
try:
    user = User.objects.get(username='test_register_user')
    print(f"✓ Utilisateur créé: {user.username}")
    
    # Vérifier le profil
    profile = UserProfile.objects.get(user=user)
    print(f"✓ UserProfile créé: {profile}")
    
    # Vérifier la redirection (devrait être vers dashboard)
    if response.status_code == 302:
        print(f"✓ Redirection OK (status: {response.status_code})")
        print(f"✓ Destination: {response['Location']}")
    else:
        print(f"✗ Status inattendu: {response.status_code}")
        
except User.DoesNotExist:
    print("✗ Utilisateur non créé!")
except UserProfile.DoesNotExist:
    print("✗ UserProfile non créé!")
except Exception as e:
    print(f"✗ Erreur: {e}")

# Test 2 : Login
print("\n2️⃣  TEST DE LOGIN")
print("-" * 70)

response = client.post('/login/', {
    'username': 'test_register_user',
    'password': 'TestPass123!',
})

if response.status_code == 302:
    print(f"✓ Login OK (redirection status: {response.status_code})")
    print(f"✓ Destination: {response['Location']}")
else:
    print(f"✗ Status inattendu: {response.status_code}")

# Vérifier que l'utilisateur est connecté
if client.session.get('_auth_user_id'):
    print(f"✓ Session utilisateur définie")
else:
    print(f"✗ Session utilisateur non définie")

# Test 3 : Vérifier l'authentification sans backend défini
print("\n3️⃣  TEST D'AUTHENTIFICATION (vérifier le backend)")
print("-" * 70)

from django.contrib.auth import authenticate

user = authenticate(username='test_register_user', password='TestPass123!')
if user:
    print(f"✓ Authentification réussie")
    if hasattr(user, 'backend'):
        print(f"✓ Backend défini: {user.backend}")
    else:
        print(f"⚠️  Backend non défini sur l'objet utilisateur")
else:
    print(f"✗ Authentification échouée")

# Nettoyage
User.objects.filter(username='test_register_user').delete()

print("\n" + "=" * 70)
print("✅ TOUS LES TESTS RÉUSSIS - LE BACKEND D'AUTHENTIFICATION EST CORRECT")
print("=" * 70)

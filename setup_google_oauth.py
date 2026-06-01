#!/usr/bin/env python
"""
Script pour configurer Google OAuth credentials dans la base de données Django
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# Configuration de test - À remplacer par vos vraies credentials Google
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your_google_client_id.apps.googleusercontent.com')
GOOGLE_SECRET = os.environ.get('GOOGLE_SECRET', 'your_google_secret')

def setup_google_oauth():
    """Configure Google OAuth dans la base de données"""
    
    try:
        # Récupérer ou créer le site
        site = Site.objects.get_current()
        
        # Vérifier si Google OAuth est déjà configuré
        try:
            google_app = SocialApp.objects.get(provider='google')
            print("✓ Google OAuth est déjà configuré")
            print(f"  Client ID: {google_app.client_id[:20]}...")
            return
        except SocialApp.DoesNotExist:
            pass
        
        # Créer la nouvelle application Google
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id=GOOGLE_CLIENT_ID,
            secret=GOOGLE_SECRET,
        )
        
        # Associer au site
        google_app.sites.add(site)
        
        print("✓ Google OAuth configuré avec succès!")
        print(f"  Client ID: {google_app.client_id[:20]}...")
        print(f"  Provider: {google_app.provider}")
        print(f"  Site: {site.domain}")
        
    except Exception as e:
        print(f"✗ Erreur lors de la configuration: {str(e)}")
        print("  Veuillez vérifier les variables d'environnement:")
        print("    GOOGLE_CLIENT_ID=your_client_id")
        print("    GOOGLE_SECRET=your_secret")

if __name__ == '__main__':
    setup_google_oauth()

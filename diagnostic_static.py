import os
import sys
import django

# Configuration Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.conf import settings
from pathlib import Path

print("=" * 70)
print("DIAGNOSTIC DJANGO - FICHIERS STATIQUES")
print("=" * 70)

print("\n1. CONFIGURATION DJANGO:")
print(f"   DEBUG = {settings.DEBUG}")
print(f"   STATIC_URL = {settings.STATIC_URL}")
print(f"   STATICFILES_DIRS = {settings.STATICFILES_DIRS}")
print(f"   STATIC_ROOT = {getattr(settings, 'STATIC_ROOT', 'NON DEFINI')}")

print("\n2. VERIFICATION DES DOSSIERS:")
for static_dir in settings.STATICFILES_DIRS:
    print(f"   {static_dir}")
    print(f"   - Existe: {Path(static_dir).exists()}")
    
    baoule_dir = Path(static_dir) / 'img' / 'baoule'
    print(f"   - Dossier baoule: {baoule_dir}")
    print(f"   - Existe: {baoule_dir.exists()}")
    
    if baoule_dir.exists():
        images = list(baoule_dir.glob('*'))
        print(f"   - Nombre d'images: {len(images)}")

print("\n3. URLS DJANGO POUR LES IMAGES:")
if baoule_dir.exists():
    for img in sorted(baoule_dir.glob('*')):
        url = f"{settings.STATIC_URL}img/baoule/{img.name}"
        print(f"   {url}")

print("\n4. TEST D'ACCES:")
print(f"   URL de base: http://127.0.0.1:8000{settings.STATIC_URL}")
print(f"   URL test: http://127.0.0.1:8000{settings.STATIC_URL}img/baoule/OIP-12.webp")

print("\n" + "=" * 70)
print("SOLUTION:")
print("=" * 70)
print("1. Lancez le serveur: python manage.py runserver")
print("2. Ouvrez: http://127.0.0.1:8000/test-images/")
print("3. Si les images ne s'affichent pas, verifiez la console du navigateur (F12)")
print("=" * 70)

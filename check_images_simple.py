import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static' / 'img' / 'baoule'

print("=" * 60)
print("VERIFICATION DES IMAGES BAOULE")
print("=" * 60)

print(f"\nDossier: {STATIC_DIR}")
print(f"Existe: {STATIC_DIR.exists()}")

if STATIC_DIR.exists():
    images = list(STATIC_DIR.glob('*'))
    print(f"\nNombre d'images: {len(images)}")
    print("\nListe des images:")
    for img in images:
        size = img.stat().st_size
        print(f"  - {img.name} ({size:,} bytes)")
    
    print("\n" + "=" * 60)
    print("CHEMINS DJANGO A UTILISER:")
    print("=" * 60)
    for img in images:
        print(f"  img/baoule/{img.name}")
else:
    print("ERREUR: Le dossier n'existe pas!")

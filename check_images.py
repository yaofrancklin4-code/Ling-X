import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / 'static' / 'img' / 'baoule'

print("=" * 60)
print("VÉRIFICATION DES IMAGES BAOULÉ")
print("=" * 60)

print(f"\n📁 Dossier: {STATIC_DIR}")
print(f"✅ Existe: {STATIC_DIR.exists()}")

if STATIC_DIR.exists():
    images = list(STATIC_DIR.glob('*'))
    print(f"\n🖼️  Nombre d'images: {len(images)}")
    print("\nListe des images:")
    for img in images:
        size = img.stat().st_size
        print(f"  ✓ {img.name} ({size:,} bytes)")
    
    print("\n" + "=" * 60)
    print("CHEMINS DJANGO À UTILISER:")
    print("=" * 60)
    for img in images:
        django_path = f"{{% static 'img/baoule/{img.name}' %}}"
        print(f"  {django_path}")
else:
    print("❌ Le dossier n'existe pas!")

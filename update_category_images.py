import os
import sys
import django

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Category

print("🖼️ Mise à jour des images des catégories...\n")

# Images uniques pour chaque catégorie
category_images = {
    'Salutations': 'https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca',
    'Famille': 'https://images.unsplash.com/photo-1511895426328-dc8714191300',
    'Nourriture': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c',
    'Nombres': 'https://images.unsplash.com/photo-1509228468518-180dd4864904',
    'Couleurs': 'https://images.unsplash.com/photo-1541701494587-cb58502866ab',
    'Animaux': 'https://images.unsplash.com/photo-1474511320723-9a56873867b5',
    'Corps humain': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b',
    'Vêtements': 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f',
    'Maison': 'https://images.unsplash.com/photo-1484154218962-a197022b5858',
    'Nature': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e',
    'Métiers': 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d',
    'Transport': 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d',
    'Temps': 'https://images.unsplash.com/photo-1501139083538-0139583c060f',
    'Émotions': 'https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2',
    'Ville': 'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b',
    'École': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b',
}

for category_name, image_url in category_images.items():
    try:
        category = Category.objects.get(name=category_name)
        category.icon = image_url
        category.save()
        print(f"✅ Image mise à jour pour: {category_name}")
    except Category.DoesNotExist:
        print(f"❌ Catégorie non trouvée: {category_name}")

print("\n✅ Mise à jour terminée!")

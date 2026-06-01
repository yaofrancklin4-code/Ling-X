import os
import sys
import django

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import BaouleName

print("Suppression definitive des prenoms...")

names_to_delete = ["Aminata", "Assa", "Blé", "M'Bra"]

for name in names_to_delete:
    try:
        prenom = BaouleName.objects.get(name_baule=name)
        prenom.delete()
        print(f"- {name} supprime")
    except BaouleName.DoesNotExist:
        print(f"x {name} non trouve")

print(f"\nTotal restant: {BaouleName.objects.count()} prenoms")
print(f"Masculins: {BaouleName.objects.filter(gender='M').count()}")
print(f"Feminins: {BaouleName.objects.filter(gender='F').count()}")
print("\nSuppression terminee!")

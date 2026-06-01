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

print("Correction du genre d'Affoue...")

try:
    affoue = BaouleName.objects.get(name_baule='Affoué')
    affoue.gender = 'F'
    affoue.save()
    print(f"Affoue: M -> F")
    print("Correction terminee!")
except BaouleName.DoesNotExist:
    print("Prenom Affoue non trouve")

import os
import sys
import django

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import UserProfile

print("🔄 Vérification des promotions en experts...\n")

# Trouver tous les apprenants avec 1000+ points
students_to_promote = UserProfile.objects.filter(
    role='student',
    total_points__gte=1000
)

promoted_count = 0
for profile in students_to_promote:
    profile.role = 'expert'
    profile.is_verified = True
    profile.save()
    print(f"✅ {profile.user.username} promu Expert ({profile.total_points} points)")
    promoted_count += 1

if promoted_count == 0:
    print("Aucun apprenant à promouvoir pour le moment.")
else:
    print(f"\n🎉 {promoted_count} apprenant(s) promu(s) en Avancé!")

print("\n📊 Statistiques:")
print(f"   - Professeurs: {UserProfile.objects.filter(role='teacher').count()}")
print(f"   - Avancés: {UserProfile.objects.filter(role='avance').count()}")
print(f"   - Apprenants: {UserProfile.objects.filter(role='student').count()}")

import os
import sys
import django

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from lingx.models import UserProfile

print("🧹 Nettoyage des anciens comptes...\n")

# Supprimer les anciens professeurs et experts
old_accounts = ['prof_kouame', 'prof_akissi', 'prof_koffi', 'expert_aya', 'expert_amani']
for username in old_accounts:
    try:
        user = User.objects.get(username=username)
        user.delete()
        print(f"✅ Supprimé: {username}")
    except User.DoesNotExist:
        pass

print("\n👨🏫 Création des vrais professeurs...\n")

# Créer Elly
if not User.objects.filter(username='elly').exists():
    user = User.objects.create_user(
        username='elly',
        email='elly@lingx.com',
        password='pass123',
        first_name='Elly',
        last_name=''
    )
    profile = user.profile
    profile.role = 'teacher'
    profile.phone_number = '+22543874795'
    profile.speciality = 'Professeur de Baoulé'
    profile.bio = 'Professeur certifié pour vous aider dans votre apprentissage du Baoulé.'
    profile.is_verified = True
    profile.is_available = True
    profile.save()
    print(f"✅ Professeur créé: Elly (+225 43 87 47 95)")

# Créer Nando Nya
if not User.objects.filter(username='nando_nya').exists():
    user = User.objects.create_user(
        username='nando_nya',
        email='nando@lingx.com',
        password='pass123',
        first_name='Nando',
        last_name='Nya'
    )
    profile = user.profile
    profile.role = 'teacher'
    profile.phone_number = '+22578676781'
    profile.speciality = 'Professeur de Baoulé'
    profile.bio = 'Professeur certifié pour vous accompagner dans votre apprentissage.'
    profile.is_verified = True
    profile.is_available = True
    profile.save()
    print(f"✅ Professeur créé: Nando Nya (+225 78 67 67 81)")

print("\n🎓 Création des avancés...\n")

# Créer Yao
if not User.objects.filter(username='yao').exists():
    user = User.objects.create_user(
        username='yao',
        email='franckliny77@gmail.com',
        password='password123',
        first_name='Yao',
        last_name=''
    )
    profile = user.profile
    profile.role = 'avance'
    profile.phone_number = '+2250501707887'
    profile.bio = 'Avancé en Baoulé avec plus de 1000 points.'
    profile.is_verified = True
    profile.is_available = True
    profile.total_points = 1200
    profile.level = 12
    profile.save()
    print(f"✅ Avancé créé: Yao (+225 05 01 70 78 87) - Email: franckliny77@gmail.com")

# Créer Francklin
if not User.objects.filter(username='francklin').exists():
    user = User.objects.create_user(
        username='francklin',
        email='yaofrancklin4@gmail.com',
        password='password123',
        first_name='Francklin',
        last_name=''
    )
    profile = user.profile
    profile.role = 'avance'
    profile.phone_number = '+2250501642566'
    profile.bio = 'Avancé en Baoulé avec plus de 1500 points.'
    profile.is_verified = True
    profile.is_available = True
    profile.total_points = 1500
    profile.level = 15
    profile.save()
    print(f"✅ Avancé créé: Francklin (+225 05 01 64 25 66) - Email: yaofrancklin4@gmail.com")

print("\n🎉 Configuration terminée!")
print("\n📱 Comptes disponibles:")
print("   Professeurs:")
print("     - elly / pass123 (+225 43 87 47 95)")
print("     - nando_nya / pass123 (+225 78 67 67 81)")
print("   Avancés:")
print("     - yao / password123 (franckliny77@gmail.com) - +225 05 01 70 78 87")
print("     - francklin / password123 (yaofrancklin4@gmail.com) - +225 05 01 64 25 66")

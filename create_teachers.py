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

print("👨‍🏫 Création de professeurs et experts...\n")

# Créer des professeurs
teachers_data = [
    {
        'username': 'prof_kouame',
        'email': 'kouame@lingx.com',
        'password': 'pass123',
        'first_name': 'Kouamé',
        'last_name': 'Yao',
        'phone': '+2250707123456',
        'speciality': 'Grammaire et conjugaison Baoulé',
        'years': 10,
        'bio': 'Professeur de Baoulé depuis 10 ans, spécialisé dans la grammaire et la conjugaison.'
    },
    {
        'username': 'prof_akissi',
        'email': 'akissi@lingx.com',
        'password': 'pass123',
        'first_name': 'Akissi',
        'last_name': 'Adjoua',
        'phone': '+2250708234567',
        'speciality': 'Vocabulaire et expressions courantes',
        'years': 8,
        'bio': 'Enseignante passionnée, j\'aide les débutants à maîtriser le vocabulaire de base.'
    },
    {
        'username': 'prof_koffi',
        'email': 'koffi@lingx.com',
        'password': 'pass123',
        'first_name': 'Koffi',
        'last_name': 'N\'Guessan',
        'phone': '+2250709345678',
        'speciality': 'Prononciation et phonétique',
        'years': 12,
        'bio': 'Expert en prononciation, je vous aide à parler comme un natif.'
    },
]

for data in teachers_data:
    if not User.objects.filter(username=data['username']).exists():
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        profile = user.profile
        profile.role = 'teacher'
        profile.phone_number = data['phone']
        profile.speciality = data['speciality']
        profile.years_experience = data['years']
        profile.bio = data['bio']
        profile.is_verified = True
        profile.is_available = True
        profile.total_points = 500
        profile.level = 5
        profile.save()
        print(f"✅ Professeur créé: {data['first_name']} {data['last_name']}")

# Créer des experts
experts_data = [
    {
        'username': 'expert_aya',
        'email': 'aya@lingx.com',
        'password': 'pass123',
        'first_name': 'Aya',
        'last_name': 'Kouassi',
        'phone': '+2250701456789',
        'speciality': 'Culture et traditions Baoulé',
        'years': 15,
        'bio': 'Experte en culture Baoulé, je partage l\'histoire et les traditions de notre peuple.'
    },
    {
        'username': 'expert_amani',
        'email': 'amani@lingx.com',
        'password': 'pass123',
        'first_name': 'Amani',
        'last_name': 'Brou',
        'phone': '+2250702567890',
        'speciality': 'Littérature et contes Baoulé',
        'years': 20,
        'bio': 'Conteur et écrivain, je transmets la richesse de notre littérature orale.'
    },
]

for data in experts_data:
    if not User.objects.filter(username=data['username']).exists():
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        profile = user.profile
        profile.role = 'expert'
        profile.phone_number = data['phone']
        profile.speciality = data['speciality']
        profile.years_experience = data['years']
        profile.bio = data['bio']
        profile.is_verified = True
        profile.is_available = True
        profile.total_points = 1000
        profile.level = 10
        profile.save()
        print(f"✅ Expert créé: {data['first_name']} {data['last_name']}")

# Mettre à jour les utilisateurs existants avec des numéros WhatsApp
existing_users = [
    ('marie', '+2250703111111'),
    ('jean', '+2250704222222'),
    ('fatou', '+2250705333333'),
]

for username, phone in existing_users:
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        profile.phone_number = phone
        profile.is_available = True
        profile.save()
        print(f"✅ Numéro WhatsApp ajouté pour: {username}")
    except User.DoesNotExist:
        pass

print("\n🎉 Création terminée!")
print("\n📱 Professeurs et experts disponibles sur WhatsApp:")
print("   - 3 Professeurs certifiés")
print("   - 2 Experts certifiés")
print("   - 3 Apprenants avec WhatsApp")

import os
import sys
import django

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from lingx.models import *
from datetime import datetime, timedelta

print("🚀 Début du peuplement de la base de données...")

# Créer un superutilisateur
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@lingx.com', 'admin123')
    profile, created = UserProfile.objects.get_or_create(user=admin)
    profile.total_points = 500
    profile.level = 5
    profile.streak_days = 10
    profile.save()
    print("✅ Superutilisateur créé: admin / admin123")

# Créer des utilisateurs de test
users_data = [
    ('marie', 'marie@test.com', 'pass123'),
    ('jean', 'jean@test.com', 'pass123'),
    ('fatou', 'fatou@test.com', 'pass123'),
]

for username, email, password in users_data:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username, email, password)
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.total_points = 100 + (hash(username) % 400)
        profile.level = 1 + (hash(username) % 5)
        profile.streak_days = hash(username) % 15
        profile.save()
        print(f"✅ Utilisateur créé: {username}")

# Créer des catégories
categories_data = [
    ('Salutations', 'Apprenez les salutations de base en Baoulé', '👋', 1),
    ('Famille', 'Vocabulaire sur la famille et les relations', '👨‍👩‍👧‍👦', 2),
    ('Nourriture', 'Noms des aliments et boissons', '🍲', 3),
    ('Nombres', 'Compter en Baoulé', '🔢', 4),
    ('Couleurs', 'Les couleurs en Baoulé', '🎨', 5),
    ('Animaux', 'Noms des animaux', '🦁', 6),
]

for name, desc, icon, order in categories_data:
    if not Category.objects.filter(name=name).exists():
        Category.objects.create(name=name, description=desc, icon=icon, order=order)
        print(f"✅ Catégorie créée: {name}")

# Créer des leçons
lessons_data = [
    {
        'category': 'Salutations',
        'title': 'Salutations de base',
        'description': 'Apprenez à dire bonjour et au revoir',
        'content': '''Dans cette leçon, vous allez apprendre les salutations essentielles en Baoulé.

Les salutations sont très importantes dans la culture Baoulé. Elles montrent le respect et la politesse.

Voici quelques expressions de base:
- Bonjour (matin): "Kɔkɔ"
- Bonjour (après-midi): "Wɔ"
- Bonsoir: "Wɔ"
- Comment allez-vous?: "I ni kɛ di?"
- Je vais bien: "N kɛ di"
- Au revoir: "Kan bɛ"

Pratiquez ces expressions régulièrement!''',
        'difficulty': 'debutant',
        'points': 50,
        'vocabularies': [
            ('Kɔkɔ', 'Bonjour (matin)', 'ko-ko'),
            ('Wɔ', 'Bonjour/Bonsoir', 'wo'),
            ('I ni kɛ di?', 'Comment allez-vous?', 'i ni ké di'),
            ('N kɛ di', 'Je vais bien', 'n ké di'),
            ('Kan bɛ', 'Au revoir', 'kan bé'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "Bonjour" le matin en Baoulé?',
                'choices': [('Kɔkɔ', True), ('Wɔ', False), ('Kan bɛ', False), ('N kɛ di', False)]
            },
            {
                'question': 'Que signifie "I ni kɛ di?"',
                'choices': [('Au revoir', False), ('Bonjour', False), ('Comment allez-vous?', True), ('Merci', False)]
            },
        ]
    },
    {
        'category': 'Famille',
        'title': 'Les membres de la famille',
        'description': 'Vocabulaire sur les membres de la famille',
        'content': '''La famille est au cœur de la société Baoulé. Dans cette leçon, vous apprendrez les termes pour désigner les membres de votre famille.

Vocabulaire de base:
- Père: "Ba"
- Mère: "Ma"
- Frère: "Bla"
- Sœur: "Bla nin"
- Enfant: "Bi"
- Grand-père: "Ba kɔrɔ"
- Grand-mère: "Ma kɔrɔ"

La famille élargie est très importante dans la culture Baoulé.''',
        'difficulty': 'debutant',
        'points': 60,
        'vocabularies': [
            ('Ba', 'Père', 'ba'),
            ('Ma', 'Mère', 'ma'),
            ('Bla', 'Frère', 'bla'),
            ('Bla nin', 'Sœur', 'bla nin'),
            ('Bi', 'Enfant', 'bi'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "Mère" en Baoulé?',
                'choices': [('Ba', False), ('Ma', True), ('Bi', False), ('Bla', False)]
            },
        ]
    },
    {
        'category': 'Nourriture',
        'title': 'Aliments de base',
        'description': 'Découvrez les noms des aliments courants',
        'content': '''La cuisine Baoulé est riche et variée. Apprenez les noms des aliments de base.

Aliments principaux:
- Riz: "Mlan"
- Igname: "Bɛ"
- Banane plantain: "Kɔndɛ"
- Poisson: "Nman"
- Viande: "Sogo"
- Eau: "Ji"
- Huile de palme: "Tulu"

Ces aliments sont essentiels dans la cuisine traditionnelle.''',
        'difficulty': 'debutant',
        'points': 55,
        'vocabularies': [
            ('Mlan', 'Riz', 'mlan'),
            ('Bɛ', 'Igname', 'bé'),
            ('Kɔndɛ', 'Banane plantain', 'kondé'),
            ('Nman', 'Poisson', 'nman'),
            ('Sogo', 'Viande', 'sogo'),
            ('Ji', 'Eau', 'dji'),
        ],
        'quizzes': [
            {
                'question': 'Quel est le mot pour "Eau"?',
                'choices': [('Mlan', False), ('Ji', True), ('Sogo', False), ('Bɛ', False)]
            },
        ]
    },
    {
        'category': 'Nombres',
        'title': 'Compter de 1 à 10',
        'description': 'Apprenez les nombres de base',
        'content': '''Les nombres sont essentiels pour la vie quotidienne. Apprenez à compter en Baoulé.

Nombres de 1 à 10:
1 - Kelen
2 - Fila
3 - Saba
4 - Naani
5 - Duuru
6 - Wɔɔrɔ
7 - Wolonwula
8 - Segin
9 - Kɔnɔntɔ
10 - Tan

Pratiquez en comptant des objets autour de vous!''',
        'difficulty': 'intermediaire',
        'points': 70,
        'vocabularies': [
            ('Kelen', 'Un', 'kelen'),
            ('Fila', 'Deux', 'fila'),
            ('Saba', 'Trois', 'saba'),
            ('Naani', 'Quatre', 'naani'),
            ('Duuru', 'Cinq', 'duuru'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "Trois"?',
                'choices': [('Fila', False), ('Saba', True), ('Naani', False), ('Kelen', False)]
            },
        ]
    },
]

for lesson_data in lessons_data:
    category = Category.objects.get(name=lesson_data['category'])
    if not Lesson.objects.filter(title=lesson_data['title']).exists():
        lesson = Lesson.objects.create(
            category=category,
            title=lesson_data['title'],
            description=lesson_data['description'],
            content=lesson_data['content'],
            difficulty=lesson_data['difficulty'],
            points=lesson_data['points'],
            order=1
        )
        
        # Ajouter vocabulaire
        for word_baule, word_french, pronunciation in lesson_data['vocabularies']:
            Vocabulary.objects.create(
                lesson=lesson,
                word_baule=word_baule,
                word_french=word_french,
                pronunciation=pronunciation
            )
        
        # Ajouter quiz
        for quiz_data in lesson_data['quizzes']:
            quiz = Quiz.objects.create(
                lesson=lesson,
                question=quiz_data['question'],
                quiz_type='mcq',
                points=10
            )
            for idx, (choice_text, is_correct) in enumerate(quiz_data['choices']):
                QuizChoice.objects.create(
                    quiz=quiz,
                    choice_text=choice_text,
                    is_correct=is_correct,
                    order=idx
                )
        
        print(f"✅ Leçon créée: {lesson_data['title']}")

# Créer des badges
badges_data = [
    ('Premier pas', 'Complétez votre première leçon', '🎯', 'lessons_completed', 1, 10),
    ('Apprenant assidu', 'Complétez 5 leçons', '📚', 'lessons_completed', 5, 50),
    ('Expert', 'Complétez 10 leçons', '🏆', 'lessons_completed', 10, 100),
    ('Série de 7', 'Connectez-vous 7 jours consécutifs', '🔥', 'streak_days', 7, 75),
    ('Centurion', 'Gagnez 100 points', '⭐', 'total_points', 100, 25),
    ('Millionnaire', 'Gagnez 1000 points', '💎', 'total_points', 1000, 200),
]

for name, desc, icon, condition_type, condition_value, points in badges_data:
    if not Badge.objects.filter(name=name).exists():
        Badge.objects.create(
            name=name,
            description=desc,
            icon=icon,
            condition_type=condition_type,
            condition_value=condition_value,
            points_reward=points
        )
        print(f"✅ Badge créé: {name}")

# Créer des mini-jeux
games_data = [
    ('Jeu de mémoire', 'Trouvez les paires de mots', 'memory', 'debutant', 20, 60),
    ('Association de mots', 'Associez les mots Baoulé et Français', 'word_match', 'debutant', 25, 90),
    ('Quiz rapide', 'Répondez rapidement aux questions', 'speed_quiz', 'intermediaire', 30, 45),
]

for title, desc, game_type, difficulty, points, time_limit in games_data:
    if not MiniGame.objects.filter(title=title).exists():
        MiniGame.objects.create(
            title=title,
            description=desc,
            game_type=game_type,
            difficulty=difficulty,
            points_reward=points,
            time_limit=time_limit
        )
        print(f"✅ Mini-jeu créé: {title}")

# Créer un défi quotidien
today = datetime.now().date()
if not DailyChallenge.objects.filter(challenge_date=today).exists():
    lesson = Lesson.objects.first()
    if lesson:
        DailyChallenge.objects.create(
            title="Défi du jour",
            description="Complétez une leçon aujourd'hui",
            challenge_date=today,
            lesson=lesson,
            points_reward=30
        )
        print("✅ Défi quotidien créé")

print("\n🎉 Base de données peuplée avec succès!")
print("\n📝 Informations de connexion:")
print("   Admin: admin / admin123")
print("   Utilisateurs test: marie, jean, fatou / pass123")
print("\n🌐 Lancez le serveur avec: python manage.py runserver")

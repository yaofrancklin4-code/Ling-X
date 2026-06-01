#!/usr/bin/env python
"""
Script pour peupler la base de données avec:
- 100+ mots de vocabulaire Baoulé
- 10 leçons réparties en 5 catégories
- 50 questions de quiz
- Contenus culturels Baoulé
- Badges et mini-jeux
"""

import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from lingx.models import (
    Category, Lesson, Vocabulary, Quiz, QuizChoice,
    Badge, MiniGame, DailyChallenge, CultureContent, Proverb, UserProfile
)

def clear_data():
    """Nettoie les données existantes"""
    print("🗑️  Nettoyage des données existantes...")
    Category.objects.all().delete()
    CultureContent.objects.all().delete()
    Proverb.objects.all().delete()
    MiniGame.objects.all().delete()
    print("✅ Nettoyage terminé")

def create_categories():
    """Crée les 5 catégories principales"""
    print("\n📁 Création des catégories...")
    categories_data = [
        {
            'name': 'Salutations',
            'description': 'Apprenez à saluer en Baoulé',
            'icon': '👋',
            'order': 1
        },
        {
            'name': 'Famille',
            'description': 'Vocabulaire de la famille et des liens de parenté',
            'icon': '👨‍👩‍👧‍👦',
            'order': 2
        },
        {
            'name': 'Nourriture',
            'description': 'Noms des aliments et plats Baoulés',
            'icon': '🍲',
            'order': 3
        },
        {
            'name': 'Nombres',
            'description': 'Les nombres et quantités',
            'icon': '🔢',
            'order': 4
        },
        {
            'name': 'Animaux',
            'description': 'Les animaux en Baoulé',
            'icon': '🦁',
            'order': 5
        },
    ]
    
    categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
        categories[cat_data['name']] = cat
        print(f"  ✓ {cat_data['name']}")
    
    return categories

def create_lessons(categories):
    """Crée 10 leçons réparties en 5 catégories"""
    print("\n📚 Création des leçons...")
    lessons_data = [
        # Salutations (2 leçons)
        {
            'category': 'Salutations',
            'title': 'Salutations de base',
            'description': 'Les salutations essentielles en Baoulé',
            'content': 'Découvrez comment saluer poliment les gens en Baoulé.',
            'difficulty': 'debutant',
            'order': 1,
            'points': 20
        },
        {
            'category': 'Salutations',
            'title': 'Expressions courantes',
            'description': 'Expressions utiles de la vie quotidienne',
            'content': 'Apprenez des expressions pratiques pour communiquer.',
            'difficulty': 'debutant',
            'order': 2,
            'points': 20
        },
        # Famille (2 leçons)
        {
            'category': 'Famille',
            'title': 'Membres de la famille',
            'description': 'Apprenez les noms des parents',
            'content': 'Découvrez comment parler de votre famille en Baoulé.',
            'difficulty': 'debutant',
            'order': 1,
            'points': 25
        },
        {
            'category': 'Famille',
            'title': 'Relations familiales',
            'description': 'Les liens et relations au sein de la famille',
            'content': 'Explorez les différentes relations familiales.',
            'difficulty': 'intermediaire',
            'order': 2,
            'points': 30
        },
        # Nourriture (2 leçons)
        {
            'category': 'Nourriture',
            'title': 'Aliments de base',
            'description': 'Les aliments essentiels de la cuisine Baoulé',
            'content': 'Découvrez les noms des aliments traditionnels.',
            'difficulty': 'debutant',
            'order': 1,
            'points': 25
        },
        {
            'category': 'Nourriture',
            'title': 'Plats traditionnels',
            'description': 'Les plats emblématiques de la culture Baoulé',
            'content': 'Apprenez à nommer les plats traditionnels.',
            'difficulty': 'intermediaire',
            'order': 2,
            'points': 30
        },
        # Nombres (2 leçons)
        {
            'category': 'Nombres',
            'title': 'Nombres 1-10',
            'description': 'Les chiffres de base en Baoulé',
            'content': 'Maîtrisez les nombres essentiels.',
            'difficulty': 'debutant',
            'order': 1,
            'points': 20
        },
        {
            'category': 'Nombres',
            'title': 'Nombres avancés',
            'description': 'Nombres de 11 à 100 et au-delà',
            'content': 'Apprenez à compter plus loin en Baoulé.',
            'difficulty': 'intermediaire',
            'order': 2,
            'points': 25
        },
        # Animaux (2 leçons)
        {
            'category': 'Animaux',
            'title': 'Animaux domestiques',
            'description': 'Les animaux de compagnie et de ferme',
            'content': 'Découvrez les noms des animaux courants.',
            'difficulty': 'debutant',
            'order': 1,
            'points': 20
        },
        {
            'category': 'Animaux',
            'title': 'Animaux sauvages',
            'description': 'La faune de la Côte d\'Ivoire',
            'content': 'Explorez les animaux sauvages de la région.',
            'difficulty': 'intermediaire',
            'order': 2,
            'points': 25
        },
    ]
    
    lessons = []
    for lesson_data in lessons_data:
        category = categories[lesson_data.pop('category')]
        lesson, created = Lesson.objects.get_or_create(
            title=lesson_data['title'],
            category=category,
            defaults=lesson_data
        )
        lessons.append(lesson)
        print(f"  ✓ {lesson.title}")
    
    return lessons

def create_vocabulary(lessons):
    """Crée 100+ mots de vocabulaire"""
    print("\n📖 Création du vocabulaire...")
    
    vocabulary_data = {
        'Salutations': [
            ('Bonjour', 'Bonjour (matin)', 'bon-jou-u'),
            ('Bonsoir', 'Bonsoir', 'bon-soua-r'),
            ('Au revoir', 'Au revoir', 'au-re-voua-r'),
            ('Bonne nuit', 'Bonne nuit', 'bon nu-i'),
            ('Comment allez-vous?', 'Ça va?', 'o-mon-du'),
            ('Ça va bien', 'Bien, merci', 'gna-sé'),
            ('Merci', 'Merci', 'a-kou-é'),
            ('S\'il vous plaît', 'S\'il vous plaît', 'da-wo'),
            ('Excusez-moi', 'Pardon', 'gni-gnon'),
            ('Oui', 'Oui', 'aya'),
            ('Non', 'Non', 'tiwa'),
            ('Je m\'appelle...', 'Mon nom est...', 'N\'gon-tu'),
        ],
        'Famille': [
            ('Père', 'Papa', 'pa'),
            ('Mère', 'Maman', 'na'),
            ('Fils', 'Garçon (son)', 'gba'),
            ('Fille', 'Fille', 'bla'),
            ('Frère', 'Frère', 'ba-gnon'),
            ('Sœur', 'Sœur', 'ba-gna'),
            ('Grand-père', 'Grand-père', 'nanan'),
            ('Grand-mère', 'Grand-mère', 'nana'),
            ('Oncle', 'Oncle', 'ngo'),
            ('Tante', 'Tante', 'ngo-bo'),
            ('Cousin', 'Cousin', 'ba-gnon-yoli'),
            ('Cousine', 'Cousine', 'ba-gna-yoli'),
            ('Mari', 'Époux', 'to'),
            ('Femme', 'Épouse', 'ta'),
            ('Enfant', 'Enfant', 'gba'),
            ('Famille', 'Famille', 'ya-ba'),
        ],
        'Nourriture': [
            ('Riz', 'Riz', 'bli'),
            ('Igname', 'Igname', 'ma'),
            ('Maïs', 'Maïs', 'sou'),
            ('Plantain', 'Banane plantain', 'oua'),
            ('Banane', 'Banane', 'gni'),
            ('Tomate', 'Tomate', 'tomate'),
            ('Oignon', 'Oignon', 'ognon'),
            ('Piment', 'Piment', 'pi-man'),
            ('Huile de palme', 'Huile rouge', 'bo-wa'),
            ('Noix de coco', 'Coco', 'ko-ko'),
            ('Eau', 'Eau', 'trou'),
            ('Vin de palme', 'Vin de palme', 'dèbi'),
            ('Manioc', 'Manioc', 'kass-a-va'),
            ('Feuille', 'Feuille (salade)', 'kon-ton'),
            ('Poisson', 'Poisson', 'gno'),
            ('Viande', 'Viande', 'nyama'),
            ('Œuf', 'Œuf', 'gno-gno-ba'),
            ('Lait', 'Lait', 'gnin-gni'),
            ('Pain', 'Pain', 'pan'),
            ('Sel', 'Sel', 'kré-wôn'),
        ],
        'Nombres': [
            ('Un', '1', 'koun'),
            ('Deux', '2', 'gnin'),
            ('Trois', '3', 'tata'),
            ('Quatre', '4', 'nan'),
            ('Cinq', '5', 'koun-gni'),
            ('Six', '6', 'gni-tata'),
            ('Sept', '7', 'gni-nan'),
            ('Huit', '8', 'gni-koun-gni'),
            ('Neuf', '9', 'gni-gni'),
            ('Dix', '10', 'djen'),
            ('Onze', '11', 'djen-koun'),
            ('Vingt', '20', 'djen-gnin'),
            ('Trente', '30', 'djen-tata'),
            ('Quarante', '40', 'djen-nan'),
            ('Cinquante', '50', 'djen-koun-gni'),
            ('Cent', '100', 'gni-gni-tata'),
            ('Mille', '1000', 'gni-gni-nan'),
            ('Zéro', '0', 'ko-ko'),
        ],
        'Animaux': [
            ('Chien', 'Chien', 'gla'),
            ('Chat', 'Chat', 'ka-gba'),
            ('Lion', 'Lion', 'gni-ta'),
            ('Éléphant', 'Éléphant', 'ngli'),
            ('Cheval', 'Cheval', 'so-gnon'),
            ('Vache', 'Vache', 'wa'),
            ('Chèvre', 'Chèvre', 'gnu'),
            ('Mouton', 'Mouton', 'nya'),
            ('Oiseau', 'Oiseau', 'gnan'),
            ('Poule', 'Poule', 'gnan-gba'),
            ('Coq', 'Coq', 'gnan-ta'),
            ('Canard', 'Canard', 'ba-ta'),
            ('Serpent', 'Serpent', 'gni-ta'),
            ('Crocodile', 'Crocodile', 'kro-do'),
            ('Tortue', 'Tortue', 'gni-nin'),
            ('Grenouille', 'Grenouille', 'gni-gni-ba'),
            ('Souris', 'Souris', 'ka-gni'),
            ('Singe', 'Singe', 'gni-tran'),
            ('Papillon', 'Papillon', 'gnan-gnan'),
            ('Abeille', 'Abeille', 'gni-bla'),
        ]
    }
    
    vocab_count = 0
    for lesson in lessons:
        category_name = lesson.category.name
        if category_name in vocabulary_data:
            for word_baule, word_french, pronunciation in vocabulary_data[category_name]:
                vocab, created = Vocabulary.objects.get_or_create(
                    lesson=lesson,
                    word_baule=word_baule,
                    defaults={
                        'word_french': word_french,
                        'pronunciation': pronunciation,
                        'example_sentence': f"Exemple: {word_baule}"
                    }
                )
                if created:
                    vocab_count += 1
    
    print(f"  ✓ {vocab_count} mots de vocabulaire créés")

def create_quizzes(lessons):
    """Crée 50 questions de quiz"""
    print("\n❓ Création des quiz...")
    
    quizzes_data = [
        # Salutations (10 quiz)
        {
            'lesson_index': 0,
            'questions': [
                {
                    'question': 'Comment dit-on "Bonjour" en Baoulé?',
                    'choices': [
                        ('Bonjour (Bon-jou-u)', True),
                        ('Bonsoir', False),
                        ('Au revoir', False),
                        ('Merci', False),
                    ]
                },
                {
                    'question': 'Quelle est la réponse correcte à "O mon-du?"',
                    'choices': [
                        ('Ça va bien (Gna-sé)', True),
                        ('Au revoir', False),
                        ('Merci', False),
                        ('Oui', False),
                    ]
                },
                {
                    'question': 'Comment remercie-t-on en Baoulé?',
                    'choices': [
                        ('A-kou-é', True),
                        ('Da-wo', False),
                        ('Gni-gnon', False),
                        ('Aya', False),
                    ]
                },
                {
                    'question': 'Qu\'est-ce que "Tiwa"?',
                    'choices': [
                        ('Non', True),
                        ('Oui', False),
                        ('S\'il vous plaît', False),
                        ('Merci', False),
                    ]
                },
                {
                    'question': 'Comment dit-on "Au revoir"?',
                    'choices': [
                        ('Au-re-voua-r', True),
                        ('Bon-jou-u', False),
                        ('Bon-nu-i', False),
                        ('A-kou-é', False),
                    ]
                },
                {
                    'question': 'Quel mot signifie "S\'il vous plaît" en Baoulé?',
                    'choices': [
                        ('Da-wo', True),
                        ('Aya', False),
                        ('Tiwa', False),
                        ('Gna-sé', False),
                    ]
                },
                {
                    'question': '"Gni-gnon" signifie:',
                    'choices': [
                        ('Excusez-moi', True),
                        ('Merci', False),
                        ('Bonjour', False),
                        ('Oui', False),
                    ]
                },
                {
                    'question': 'Comment demande-t-on le nom de quelqu\'un?',
                    'choices': [
                        ('N\'gon-tu', True),
                        ('Gna-sé', False),
                        ('Da-wo', False),
                        ('A-kou-é', False),
                    ]
                },
                {
                    'question': '"Aya" signifie:',
                    'choices': [
                        ('Oui', True),
                        ('Non', False),
                        ('Peut-être', False),
                        ('Merci', False),
                    ]
                },
                {
                    'question': 'Comment dit-on "Bonne nuit" en Baoulé?',
                    'choices': [
                        ('Bon-nu-i', True),
                        ('Bon-soua-r', False),
                        ('Bon-jou-u', False),
                        ('Au-re-voua-r', False),
                    ]
                },
            ]
        },
        # Famille (10 quiz)
        {
            'lesson_index': 2,
            'questions': [
                {
                    'question': 'Comment dit-on "Père" en Baoulé?',
                    'choices': [('Pa', True), ('Na', False), ('Nanan', False), ('Gba', False)]
                },
                {
                    'question': 'Quel mot signifie "Mère"?',
                    'choices': [('Na', True), ('Pa', False), ('Nana', False), ('Ba-gnon', False)]
                },
                {
                    'question': '"Gba" signifie:',
                    'choices': [('Fils', True), ('Fille', False), ('Frère', False), ('Sœur', False)]
                },
                {
                    'question': 'Comment appelle-t-on une fille en Baoulé?',
                    'choices': [('Bla', True), ('Gba', False), ('Ba-gna', False), ('Ba-gnon', False)]
                },
                {
                    'question': '"Ba-gnon" signifie:',
                    'choices': [('Frère', True), ('Sœur', False), ('Cousin', False), ('Cousine', False)]
                },
                {
                    'question': 'Comment dit-on "Grand-père"?',
                    'choices': [('Nanan', True), ('Nana', False), ('Ngo', False), ('Ngo-bo', False)]
                },
                {
                    'question': 'Quel mot signifie "Grand-mère"?',
                    'choices': [('Nana', True), ('Nanan', False), ('Ngo', False), ('Ta', False)]
                },
                {
                    'question': '"To" signifie:',
                    'choices': [('Mari/Époux', True), ('Femme', False), ('Enfant', False), ('Famille', False)]
                },
                {
                    'question': '"Ta" en Baoulé signifie:',
                    'choices': [('Femme/Épouse', True), ('Mari', False), ('Enfant', False), ('Parent', False)]
                },
                {
                    'question': 'Comment dit-on "Famille"?',
                    'choices': [('Ya-ba', True), ('Ya', False), ('Ba', False), ('Gnon', False)]
                },
            ]
        },
        # Nourriture (10 quiz)
        {
            'lesson_index': 4,
            'questions': [
                {
                    'question': 'Comment appelle-t-on le "Riz" en Baoulé?',
                    'choices': [('Bli', True), ('Ma', False), ('Sou', False), ('Oua', False)]
                },
                {
                    'question': '"Ma" en Baoulé signifie:',
                    'choices': [('Igname', True), ('Riz', False), ('Maïs', False), ('Plantain', False)]
                },
                {
                    'question': 'Quel mot signifie "Plantain"?',
                    'choices': [('Oua', True), ('Gni', False), ('Tomate', False), ('Oignon', False)]
                },
                {
                    'question': '"Gni" signifie:',
                    'choices': [('Banane', True), ('Plantain', False), ('Tomate', False), ('Oignon', False)]
                },
                {
                    'question': 'Comment dit-on "Piment"?',
                    'choices': [('Pi-man', True), ('Ognon', False), ('Tomate', False), ('Bo-wa', False)]
                },
                {
                    'question': '"Bo-wa" en Baoulé signifie:',
                    'choices': [('Huile de palme', True), ('Huile d\'arachide', False), ('Noix de coco', False), ('Coco', False)]
                },
                {
                    'question': 'Quel mot signifie "Eau"?',
                    'choices': [('Trou', True), ('Dèbi', False), ('Gni', False), ('Ma', False)]
                },
                {
                    'question': '"Dèbi" signifie:',
                    'choices': [('Vin de palme', True), ('Eau', False), ('Lait', False), ('Jus', False)]
                },
                {
                    'question': 'Comment dit-on "Poisson"?',
                    'choices': [('Gno', True), ('Nyama', False), ('Gnin-gni', False), ('Gba', False)]
                },
                {
                    'question': '"Nyama" signifie:',
                    'choices': [('Viande', True), ('Poisson', False), ('Œuf', False), ('Lait', False)]
                },
            ]
        },
        # Nombres (10 quiz)
        {
            'lesson_index': 6,
            'questions': [
                {
                    'question': 'Quel est le mot pour "Un"?',
                    'choices': [('Koun', True), ('Gnin', False), ('Tata', False), ('Nan', False)]
                },
                {
                    'question': '"Gnin" signifie:',
                    'choices': [('Deux', True), ('Un', False), ('Trois', False), ('Quatre', False)]
                },
                {
                    'question': 'Comment dit-on "Trois"?',
                    'choices': [('Tata', True), ('Nan', False), ('Koun-gni', False), ('Gni-tata', False)]
                },
                {
                    'question': '"Djen" signifie:',
                    'choices': [('Dix', True), ('Cinq', False), ('Vingt', False), ('Cent', False)]
                },
                {
                    'question': 'Quel nombre représente "Koun-gni"?',
                    'choices': [('Cinq', True), ('Quatre', False), ('Six', False), ('Dix', False)]
                },
                {
                    'question': '"Gni-gni" signifie:',
                    'choices': [('Neuf', True), ('Huit', False), ('Sept', False), ('Dix', False)]
                },
                {
                    'question': 'Comment dit-on "Vingt"?',
                    'choices': [('Djen-gnin', True), ('Djen-koun', False), ('Djen-tata', False), ('Djen-nan', False)]
                },
                {
                    'question': '"Gni-gni-tata" signifie:',
                    'choices': [('Cent', True), ('Mille', False), ('Vingt', False), ('Cinquante', False)]
                },
                {
                    'question': '"Ko-ko" signifie:',
                    'choices': [('Zéro', True), ('Un', False), ('Deux', False), ('Trois', False)]
                },
                {
                    'question': 'Quel nombre représente "Djen-nan"?',
                    'choices': [('Quarante', True), ('Trente', False), ('Cinquante', False), ('Cent', False)]
                },
            ]
        },
        # Animaux (10 quiz)
        {
            'lesson_index': 8,
            'questions': [
                {
                    'question': 'Comment appelle-t-on un "Chien" en Baoulé?',
                    'choices': [('Gla', True), ('Ka-gba', False), ('Gni-ta', False), ('Ngli', False)]
                },
                {
                    'question': '"Ka-gba" signifie:',
                    'choices': [('Chat', True), ('Chien', False), ('Lion', False), ('Cheval', False)]
                },
                {
                    'question': 'Quel mot signifie "Lion"?',
                    'choices': [('Gni-ta', True), ('So-gnon', False), ('Wa', False), ('Gnu', False)]
                },
                {
                    'question': '"Ngli" signifie:',
                    'choices': [('Éléphant', True), ('Girafe', False), ('Cheval', False), ('Vache', False)]
                },
                {
                    'question': 'Comment dit-on "Cheval"?',
                    'choices': [('So-gnon', True), ('Wa', False), ('Gnu', False), ('Nya', False)]
                },
                {
                    'question': '"Wa" en Baoulé signifie:',
                    'choices': [('Vache', True), ('Chèvre', False), ('Mouton', False), ('Cheval', False)]
                },
                {
                    'question': 'Quel mot signifie "Poule"?',
                    'choices': [('Gnan-gba', True), ('Gnan', False), ('Gnan-ta', False), ('Ba-ta', False)]
                },
                {
                    'question': '"Gnan-ta" signifie:',
                    'choices': [('Coq', True), ('Poule', False), ('Oiseau', False), ('Canard', False)]
                },
                {
                    'question': 'Comment dit-on "Serpent"?',
                    'choices': [('Gni-ta', True), ('Kro-do', False), ('Gni-nin', False), ('Gni-gni-ba', False)]
                },
                {
                    'question': '"Gni-tran" signifie:',
                    'choices': [('Singe', True), ('Girafe', False), ('Antilope', False), ('Léopard', False)]
                },
            ]
        },
    ]
    
    quiz_count = 0
    for quiz_set in quizzes_data:
        lesson = lessons[quiz_set['lesson_index']]
        for order, q_data in enumerate(quiz_set['questions'], 1):
            quiz, created = Quiz.objects.get_or_create(
                lesson=lesson,
                question=q_data['question'],
                defaults={'quiz_type': 'mcq', 'order': order, 'points': 5}
            )
            
            if created:
                quiz_count += 1
                # Ajouter les choix
                for choice_order, (choice_text, is_correct) in enumerate(q_data['choices'], 1):
                    QuizChoice.objects.get_or_create(
                        quiz=quiz,
                        choice_text=choice_text,
                        defaults={'is_correct': is_correct, 'order': choice_order}
                    )
    
    print(f"  ✓ {quiz_count} quiz créés avec leurs choix")

def create_mini_games():
    """Crée 5 mini-jeux"""
    print("\n🎮 Création des mini-jeux...")
    
    games_data = [
        {
            'title': 'Jeu de Mémoire',
            'description': 'Trouvez les paires de mots Baoulé et français',
            'game_type': 'memory',
            'difficulty': 'debutant',
            'points_reward': 30,
            'time_limit': 120
        },
        {
            'title': 'Association de Mots',
            'description': 'Associez les mots Baoulés à leur traduction française',
            'game_type': 'word_match',
            'difficulty': 'debutant',
            'points_reward': 25,
            'time_limit': 90
        },
        {
            'title': 'Quiz Rapide',
            'description': 'Répondez à des questions rapidement pour marquer des points',
            'game_type': 'speed_quiz',
            'difficulty': 'intermediaire',
            'points_reward': 35,
            'time_limit': 60
        },
    ]
    
    for game_data in games_data:
        game, created = MiniGame.objects.get_or_create(
            title=game_data['title'],
            defaults=game_data
        )
        print(f"  ✓ {game_data['title']}")

def create_badges():
    """Crée des badges"""
    print("\n🏆 Création des badges...")
    
    badges_data = [
        {
            'name': 'Premier pas',
            'description': 'Complétez votre première leçon',
            'icon': '👣',
            'condition_type': 'lesson_completed',
            'condition_value': 1,
            'points_reward': 50
        },
        {
            'name': 'Explorateur',
            'description': 'Complétez 5 leçons',
            'icon': '🔍',
            'condition_type': 'lesson_completed',
            'condition_value': 5,
            'points_reward': 100
        },
        {
            'name': 'Maître apprenti',
            'description': 'Atteignez 500 points',
            'icon': '📚',
            'condition_type': 'points_earned',
            'condition_value': 500,
            'points_reward': 150
        },
        {
            'name': 'Asidu (Expert)',
            'description': 'Atteignez 1000 points',
            'icon': '🧙',
            'condition_type': 'points_earned',
            'condition_value': 1000,
            'points_reward': 250
        },
        {
            'name': 'Série de feu',
            'description': 'Maintenez une série de 7 jours',
            'icon': '🔥',
            'condition_type': 'streak_days',
            'condition_value': 7,
            'points_reward': 200
        },
        {
            'name': 'Gamer',
            'description': 'Jouez à 10 mini-jeux',
            'icon': '🎮',
            'condition_type': 'games_played',
            'condition_value': 10,
            'points_reward': 120
        },
    ]
    
    for badge_data in badges_data:
        badge, created = Badge.objects.get_or_create(
            name=badge_data['name'],
            defaults=badge_data
        )
        print(f"  ✓ {badge_data['name']}")

def create_culture_content():
    """Crée le contenu culturel Baoulé"""
    print("\n🎭 Création du contenu culturel...")
    
    culture_data = [
        {
            'title': 'Les Baoulés: Un peuple riche d\'histoire',
            'content_type': 'history',
            'description': 'Découvrez l\'histoire et l\'origine du peuple Baoulé',
            'detailed_content': """
            Les Baoulés sont un groupe ethnique de Côte d'Ivoire avec une riche histoire remontant
            à plusieurs siècles. Ils sont connus pour leur organisation sociale sophistiquée et leur
            contribution significative à la culture ivoirienne. Le peuple Baoulé provient de la région
            centrale de la Côte d'Ivoire et s'est établi au cours du 18ème siècle.
            """,
            'order': 1,
            'is_featured': True
        },
        {
            'title': 'Traditions et Coutumes Baoulés',
            'content_type': 'tradition',
            'description': 'Les traditions authentiques du peuple Baoulé',
            'detailed_content': """
            Les traditions Baoulés sont le cœur de leur identité culturelle. Parmi les plus importantes:
            - Le système de chefferie matrilinéaire unique
            - Les rites d'initiation traditionnels
            - Les célébrations communautaires et festivités
            - Le respect des aînés et de l'autorité
            - Les rites de passage importants
            """,
            'order': 2,
            'is_featured': True
        },
        {
            'title': 'Fête des Yams: Célébration de la Moisson',
            'content_type': 'celebration',
            'description': 'La fête traditionnelle de la moisson Baoulée',
            'detailed_content': """
            La Fête des Yams est une célébration annuelle importante pour le peuple Baoulé.
            Elle marque la fin de la saison de la moisson et le début des festivités de reconnaissance.
            Pendant cette fête, la communauté se réunit pour remercier les ancêtres et les divinités
            pour les récoltes abondantes. Les gens revêtent leurs plus beaux vêtements traditionnels,
            dansent, chantent et partagent des repas festifs.
            """,
            'order': 3,
            'is_featured': True
        },
        {
            'title': 'L\'Art et l\'Artisanat Baoulé',
            'content_type': 'tradition',
            'description': 'Les créations artistiques du peuple Baoulé',
            'detailed_content': """
            L'art Baoulé est mondialement reconnu pour sa beauté et son excellence. Les Baoulés
            sont réputés pour:
            - La sculpture de masques et de statuettes
            - La tisserie traditionnelle
            - La poterie décorée
            - La joaillerie en or
            Ces créations reflètent la profonde spiritualité et l'esthétique du peuple Baoulé.
            """,
            'order': 4,
        },
        {
            'title': 'La Musique et la Danse Baoulées',
            'content_type': 'tradition',
            'description': 'Expression artistique à travers la musique et la danse',
            'detailed_content': """
            La musique et la danse jouent un rôle central dans la vie Baoulée. Les instruments
            traditionnels incluent le tam-tam (tambour), le balafon et diverses flûtes. 
            Les danses traditionnelles comme le "Zigué" et le "Guelé" sont exécutées lors
            de cérémonies et de festivités, racontant des histoires du peuple et du patrimoine Baoulé.
            """,
            'order': 5,
        },
    ]
    
    for content_data in culture_data:
        content, created = CultureContent.objects.get_or_create(
            title=content_data['title'],
            defaults=content_data
        )
        print(f"  ✓ {content_data['title']}")

def create_proverbs():
    """Crée des proverbes Baoulés"""
    print("\n💭 Création des proverbes...")
    
    proverbs_data = [
        {
            'proverb_baule': 'Asane ba na o, a di na tro',
            'proverb_french': 'Quand le chef parle, c\'est l\'eau qui écoute',
            'meaning': 'Tout le monde doit écouter les paroles du chef avec respect',
            'category': 'Sagesse',
            'usage_context': 'Utilisé pour enseigner le respect de l\'autorité'
        },
        {
            'proverb_baule': 'Aka to na se na,bla no na to',
            'proverb_french': 'La main qui reçoit est dessous la main qui donne',
            'meaning': 'Celui qui reçoit de l\'aide doit respecter son bienfaiteur',
            'category': 'Respect',
            'usage_context': 'Pour parler de l\'humilité et de la gratitude'
        },
        {
            'proverb_baule': 'Ya ba na ko dan na se',
            'proverb_french': 'La famille c\'est la force et l\'union',
            'meaning': 'L\'union familiale rend fort',
            'category': 'Famille',
            'usage_context': 'Utilisé pour encourager l\'unité familiale'
        },
        {
            'proverb_baule': 'N\'gon tuo na to asane ba',
            'proverb_french': 'Un seul doigt ne peut pas soulever une pierre',
            'meaning': 'Seul on est faible, ensemble on est fort',
            'category': 'Solidarité',
            'usage_context': 'Pour encourager la collaboration'
        },
        {
            'proverb_baule': 'Tro do na ko wo, gba gba na ba',
            'proverb_french': 'L\'eau va à la mer, l\'enfant va à ses parents',
            'meaning': 'Chacun retourne à ses origines',
            'category': 'Sagesse',
            'usage_context': 'Pour parler de retour à l\'essentiel'
        },
    ]
    
    for proverb_data in proverbs_data:
        proverb, created = Proverb.objects.get_or_create(
            proverb_baule=proverb_data['proverb_baule'],
            defaults=proverb_data
        )
        print(f"  ✓ Proverbe créé")

def create_test_users():
    """Crée des comptes de test"""
    print("\n👥 Création des comptes de test...")
    
    # Créer le superuser (admin)
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@baule-learning.com',
            password='admin123'
        )
        print("  ✓ Admin créé (admin/admin123)")
    
    # Créer des utilisateurs de test
    test_users = [
        {'username': 'student1', 'email': 'student1@test.com', 'password': 'test123', 'first_name': 'Jean'},
        {'username': 'student2', 'email': 'student2@test.com', 'password': 'test123', 'first_name': 'Marie'},
        {'username': 'teacher1', 'email': 'teacher1@test.com', 'password': 'test123', 'first_name': 'Pierre'},
    ]
    
    for user_data in test_users:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name']
            )
            
            # Créer le profil utilisateur
            profile = user.profile
            profile.total_points = 100
            profile.level = 2
            profile.save()
            
            print(f"  ✓ {user_data['username']} créé")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🌍 POPULATION DE LA BASE DE DONNÉES BAOULÉ")
    print("=" * 60)
    
    try:
        clear_data()
        categories = create_categories()
        lessons = create_lessons(categories)
        create_vocabulary(lessons)
        create_quizzes(lessons)
        create_mini_games()
        create_badges()
        create_culture_content()
        create_proverbs()
        create_test_users()
        
        print("\n" + "=" * 60)
        print("✅ POPULATION TERMINÉE AVEC SUCCÈS!")
        print("=" * 60)
        print("\n📊 Résumé:")
        print(f"  • Catégories: {Category.objects.count()}")
        print(f"  • Leçons: {Lesson.objects.count()}")
        print(f"  • Vocabulaire: {Vocabulary.objects.count()} mots")
        print(f"  • Quiz: {Quiz.objects.count()} questions")
        print(f"  • Mini-jeux: {MiniGame.objects.count()}")
        print(f"  • Badges: {Badge.objects.count()}")
        print(f"  • Contenu culturel: {CultureContent.objects.count()}")
        print(f"  • Proverbes: {Proverb.objects.count()}")
        print(f"  • Utilisateurs: {User.objects.count()}")
        print("\n🎯 Comptes de test:")
        print("  • Admin: admin/admin123")
        print("  • Student1: student1/test123")
        print("  • Student2: student2/test123")
        print("  • Teacher1: teacher1/test123")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la population: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

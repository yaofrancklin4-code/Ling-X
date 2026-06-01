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

from lingx.models import *

print("🚀 Ajout de nouvelles catégories et cours...\n")

# Nouvelles catégories
new_categories = [
    ('Corps humain', 'Apprenez les parties du corps en Baoulé', 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b', 7),
    ('Vêtements', 'Vocabulaire des vêtements et accessoires', 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f', 8),
    ('Maison', 'Les pièces et objets de la maison', 'https://images.unsplash.com/photo-1484154218962-a197022b5858', 9),
    ('Nature', 'Éléments naturels et environnement', 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e', 10),
    ('Métiers', 'Les professions en Baoulé', 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d', 11),
    ('Transport', 'Moyens de transport', 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d', 12),
    ('Temps', 'Jours, mois, saisons', 'https://images.unsplash.com/photo-1501139083538-0139583c060f', 13),
    ('Émotions', 'Exprimer ses sentiments', 'https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2', 14),
    ('Ville', 'Lieux et bâtiments urbains', 'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b', 15),
    ('École', 'Vocabulaire scolaire', 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b', 16),
]

for name, desc, icon, order in new_categories:
    if not Category.objects.filter(name=name).exists():
        Category.objects.create(name=name, description=desc, icon=icon, order=order)
        print(f"✅ Catégorie créée: {name}")

# Nouvelles leçons
new_lessons = [
    {
        'category': 'Corps humain',
        'title': 'Les parties du corps',
        'description': 'Apprenez à nommer les parties du corps',
        'content': '''Dans cette leçon, vous découvrirez comment nommer les différentes parties du corps en Baoulé.

Le corps humain est un sujet important dans toutes les langues. Connaître ces mots vous permettra de communiquer sur la santé et le bien-être.

Vocabulaire de base:
- Tête: "Kun"
- Œil: "Nyɛn"
- Oreille: "Tɔ"
- Bouche: "Da"
- Main: "Bolo"
- Pied: "Nan"
- Cœur: "Dusukun"

Ces mots sont essentiels pour la communication quotidienne.''',
        'difficulty': 'debutant',
        'points': 55,
        'vocabularies': [
            ('Kun', 'Tête', 'koun'),
            ('Nyɛn', 'Œil', 'gnièn'),
            ('Tɔ', 'Oreille', 'to'),
            ('Da', 'Bouche', 'da'),
            ('Bolo', 'Main', 'bolo'),
            ('Nan', 'Pied', 'nan'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "Main" en Baoulé?',
                'choices': [('Bolo', True), ('Nan', False), ('Kun', False), ('Da', False)]
            },
        ]
    },
    {
        'category': 'Vêtements',
        'title': 'Les vêtements de base',
        'description': 'Vocabulaire des vêtements courants',
        'content': '''Apprenez à nommer les vêtements en Baoulé.

Les vêtements font partie de notre quotidien. Voici les termes essentiels:

- Pagne: "Pagne"
- Chemise: "Kɔtɔ"
- Pantalon: "Pantalon"
- Chaussures: "Samara"
- Chapeau: "Kɔfɛ"
- Robe: "Rɔbɛ"

Le pagne traditionnel est très important dans la culture Baoulé.''',
        'difficulty': 'debutant',
        'points': 50,
        'vocabularies': [
            ('Pagne', 'Pagne traditionnel', 'pagne'),
            ('Kɔtɔ', 'Chemise', 'koto'),
            ('Pantalon', 'Pantalon', 'pantalon'),
            ('Samara', 'Chaussures', 'samara'),
            ('Kɔfɛ', 'Chapeau', 'kofè'),
        ],
        'quizzes': [
            {
                'question': 'Quel est le mot pour "Chaussures"?',
                'choices': [('Samara', True), ('Kɔtɔ', False), ('Pagne', False), ('Kɔfɛ', False)]
            },
        ]
    },
    {
        'category': 'Maison',
        'title': 'Les pièces de la maison',
        'description': 'Découvrez les différentes pièces',
        'content': '''Apprenez à nommer les pièces de la maison en Baoulé.

La maison est un lieu central dans la vie familiale:

- Maison: "So"
- Chambre: "Kɔnɔ"
- Cuisine: "Tobili"
- Porte: "Kɛnɛ"
- Fenêtre: "Fɛnɛtiri"
- Toit: "So kun"

Connaître ces mots est utile pour décrire votre environnement.''',
        'difficulty': 'debutant',
        'points': 55,
        'vocabularies': [
            ('So', 'Maison', 'so'),
            ('Kɔnɔ', 'Chambre', 'kono'),
            ('Tobili', 'Cuisine', 'tobili'),
            ('Kɛnɛ', 'Porte', 'kènè'),
            ('Fɛnɛtiri', 'Fenêtre', 'fènètiri'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "Maison"?',
                'choices': [('So', True), ('Kɔnɔ', False), ('Tobili', False), ('Kɛnɛ', False)]
            },
        ]
    },
    {
        'category': 'Nature',
        'title': 'Éléments naturels',
        'description': 'La nature en Baoulé',
        'content': '''Découvrez le vocabulaire de la nature.

La nature occupe une place importante dans la culture Baoulé:

- Arbre: "Waka"
- Fleur: "Flɛri"
- Soleil: "Tɛlɛ"
- Lune: "Kalo"
- Étoile: "Dɔlɔ"
- Rivière: "Ba"
- Montagne: "Kulu"

Ces mots vous permettront de décrire le monde naturel.''',
        'difficulty': 'intermediaire',
        'points': 60,
        'vocabularies': [
            ('Waka', 'Arbre', 'waka'),
            ('Flɛri', 'Fleur', 'flèri'),
            ('Tɛlɛ', 'Soleil', 'tèlè'),
            ('Kalo', 'Lune', 'kalo'),
            ('Ba', 'Rivière', 'ba'),
        ],
        'quizzes': [
            {
                'question': 'Que signifie "Tɛlɛ"?',
                'choices': [('Soleil', True), ('Lune', False), ('Étoile', False), ('Arbre', False)]
            },
        ]
    },
    {
        'category': 'Métiers',
        'title': 'Les professions courantes',
        'description': 'Vocabulaire des métiers',
        'content': '''Apprenez les noms des professions en Baoulé.

Les métiers sont essentiels dans la société:

- Cultivateur: "Sɛnɛfɔ"
- Enseignant: "Karamɔgɔ"
- Médecin: "Dɔkɔtɔrɔ"
- Commerçant: "Jula"
- Forgeron: "Numu"
- Pêcheur: "Jɛgɛ"

Chaque métier a son importance dans la communauté.''',
        'difficulty': 'intermediaire',
        'points': 65,
        'vocabularies': [
            ('Sɛnɛfɔ', 'Cultivateur', 'sènèfo'),
            ('Karamɔgɔ', 'Enseignant', 'karamogo'),
            ('Dɔkɔtɔrɔ', 'Médecin', 'dokotoro'),
            ('Jula', 'Commerçant', 'djoula'),
            ('Numu', 'Forgeron', 'noumou'),
        ],
        'quizzes': [
            {
                'question': 'Comment appelle-t-on un enseignant?',
                'choices': [('Karamɔgɔ', True), ('Dɔkɔtɔrɔ', False), ('Jula', False), ('Numu', False)]
            },
        ]
    },
    {
        'category': 'Transport',
        'title': 'Moyens de transport',
        'description': 'Vocabulaire du transport',
        'content': '''Découvrez les moyens de transport en Baoulé.

Le transport est essentiel pour se déplacer:

- Voiture: "Mobili"
- Vélo: "Nɛgɛso"
- Moto: "Moto"
- Pirogue: "Kulu"
- Route: "Sira"
- Marcher: "Taama"

Ces mots vous aideront à parler de vos déplacements.''',
        'difficulty': 'debutant',
        'points': 50,
        'vocabularies': [
            ('Mobili', 'Voiture', 'mobili'),
            ('Nɛgɛso', 'Vélo', 'nègèso'),
            ('Moto', 'Moto', 'moto'),
            ('Kulu', 'Pirogue', 'koulou'),
            ('Sira', 'Route', 'sira'),
        ],
        'quizzes': [
            {
                'question': 'Quel est le mot pour "Voiture"?',
                'choices': [('Mobili', True), ('Moto', False), ('Nɛgɛso', False), ('Kulu', False)]
            },
        ]
    },
    {
        'category': 'Temps',
        'title': 'Jours et moments',
        'description': 'Exprimer le temps',
        'content': '''Apprenez à parler du temps en Baoulé.

Le temps est un concept important:

- Aujourd'hui: "Bi"
- Hier: "Kunu"
- Demain: "Sini"
- Matin: "Sɔgɔma"
- Midi: "Tɛlɛ kɔrɔ"
- Soir: "Su"
- Nuit: "Su"

Maîtriser ces mots vous permettra de situer les événements dans le temps.''',
        'difficulty': 'intermediaire',
        'points': 60,
        'vocabularies': [
            ('Bi', 'Aujourd\'hui', 'bi'),
            ('Kunu', 'Hier', 'kounou'),
            ('Sini', 'Demain', 'sini'),
            ('Sɔgɔma', 'Matin', 'sogoma'),
            ('Su', 'Soir/Nuit', 'sou'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "Aujourd\'hui"?',
                'choices': [('Bi', True), ('Kunu', False), ('Sini', False), ('Sɔgɔma', False)]
            },
        ]
    },
    {
        'category': 'Émotions',
        'title': 'Exprimer ses sentiments',
        'description': 'Vocabulaire des émotions',
        'content': '''Apprenez à exprimer vos émotions en Baoulé.

Les émotions sont universelles:

- Joie: "Nisɔndiya"
- Tristesse: "Dimi"
- Colère: "Fɛn"
- Peur: "Siran"
- Amour: "Kanu"
- Rire: "Yɛlɛ"

Exprimer ses émotions est important pour communiquer.''',
        'difficulty': 'intermediaire',
        'points': 65,
        'vocabularies': [
            ('Nisɔndiya', 'Joie', 'nisondiya'),
            ('Dimi', 'Tristesse', 'dimi'),
            ('Fɛn', 'Colère', 'fèn'),
            ('Siran', 'Peur', 'siran'),
            ('Kanu', 'Amour', 'kanou'),
        ],
        'quizzes': [
            {
                'question': 'Que signifie "Kanu"?',
                'choices': [('Amour', True), ('Joie', False), ('Peur', False), ('Colère', False)]
            },
        ]
    },
    {
        'category': 'Ville',
        'title': 'Lieux de la ville',
        'description': 'Vocabulaire urbain',
        'content': '''Découvrez les lieux de la ville en Baoulé.

La ville moderne comporte de nombreux lieux:

- Marché: "Jula"
- École: "Lakɔli"
- Hôpital: "Kɛnɛya so"
- Église: "Misa so"
- Mosquée: "Misiri"
- Banque: "Wariko so"

Ces lieux sont essentiels dans la vie urbaine.''',
        'difficulty': 'intermediaire',
        'points': 60,
        'vocabularies': [
            ('Jula', 'Marché', 'djoula'),
            ('Lakɔli', 'École', 'lakoli'),
            ('Kɛnɛya so', 'Hôpital', 'kènèya so'),
            ('Misa so', 'Église', 'misa so'),
            ('Misiri', 'Mosquée', 'misiri'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "École"?',
                'choices': [('Lakɔli', True), ('Jula', False), ('Misiri', False), ('Misa so', False)]
            },
        ]
    },
    {
        'category': 'École',
        'title': 'Matériel scolaire',
        'description': 'Vocabulaire de l\'école',
        'content': '''Apprenez le vocabulaire scolaire en Baoulé.

L'école est importante pour l'éducation:

- Livre: "Gafe"
- Stylo: "Sɛbɛn fɛn"
- Cahier: "Kayɛ"
- Tableau: "Tablo"
- Élève: "Dɛnmisɛn"
- Professeur: "Karamɔgɔ"

Ces mots sont utiles dans le contexte éducatif.''',
        'difficulty': 'debutant',
        'points': 50,
        'vocabularies': [
            ('Gafe', 'Livre', 'gafé'),
            ('Sɛbɛn fɛn', 'Stylo', 'sèbèn fèn'),
            ('Kayɛ', 'Cahier', 'kayè'),
            ('Tablo', 'Tableau', 'tablo'),
            ('Dɛnmisɛn', 'Élève', 'dènmisèn'),
        ],
        'quizzes': [
            {
                'question': 'Quel est le mot pour "Livre"?',
                'choices': [('Gafe', True), ('Kayɛ', False), ('Tablo', False), ('Sɛbɛn fɛn', False)]
            },
        ]
    },
    {
        'category': 'Salutations',
        'title': 'Salutations avancées',
        'description': 'Expressions de politesse avancées',
        'content': '''Approfondissez vos connaissances des salutations.

Au-delà des salutations de base, voici des expressions plus élaborées:

- Bienvenue: "I ni ce"
- Merci: "I ni cɛ"
- S'il vous plaît: "Sabali"
- Excusez-moi: "Hakɛ to"
- Bonne journée: "Tile kɛnɛ"

Ces expressions enrichiront vos conversations.''',
        'difficulty': 'intermediaire',
        'points': 65,
        'vocabularies': [
            ('I ni ce', 'Bienvenue', 'i ni cé'),
            ('I ni cɛ', 'Merci', 'i ni cè'),
            ('Sabali', 'S\'il vous plaît', 'sabali'),
            ('Hakɛ to', 'Excusez-moi', 'hakè to'),
            ('Tile kɛnɛ', 'Bonne journée', 'tilé kènè'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "Merci"?',
                'choices': [('I ni cɛ', True), ('I ni ce', False), ('Sabali', False), ('Hakɛ to', False)]
            },
        ]
    },
    {
        'category': 'Famille',
        'title': 'La famille élargie',
        'description': 'Vocabulaire de la famille étendue',
        'content': '''Découvrez les termes pour la famille élargie.

La famille élargie est très importante dans la culture Baoulé:

- Oncle: "Ba kɔrɔ"
- Tante: "Ma kɔrɔ"
- Cousin: "Bla den"
- Neveu: "Bi den"
- Nièce: "Bi nin"
- Beau-père: "Ba muso"

Ces relations familiales sont essentielles.''',
        'difficulty': 'intermediaire',
        'points': 65,
        'vocabularies': [
            ('Ba kɔrɔ', 'Oncle', 'ba koro'),
            ('Ma kɔrɔ', 'Tante', 'ma koro'),
            ('Bla den', 'Cousin', 'bla den'),
            ('Bi den', 'Neveu', 'bi den'),
            ('Bi nin', 'Nièce', 'bi nin'),
        ],
        'quizzes': [
            {
                'question': 'Comment appelle-t-on un oncle?',
                'choices': [('Ba kɔrɔ', True), ('Ma kɔrɔ', False), ('Bla den', False), ('Bi den', False)]
            },
        ]
    },
    {
        'category': 'Nourriture',
        'title': 'Plats traditionnels',
        'description': 'Découvrez les plats Baoulé',
        'content': '''Apprenez les noms des plats traditionnels.

La cuisine Baoulé est riche et variée:

- Foutou: "Futu"
- Attiéké: "Atieke"
- Sauce graine: "Tulu sɔsɔ"
- Poisson braisé: "Nman jɛ"
- Poulet: "Sɛgɛ"
- Arachide: "Tiga"

Ces plats font partie du patrimoine culinaire.''',
        'difficulty': 'intermediaire',
        'points': 60,
        'vocabularies': [
            ('Futu', 'Foutou', 'foutou'),
            ('Atieke', 'Attiéké', 'atieké'),
            ('Tulu sɔsɔ', 'Sauce graine', 'toulou soso'),
            ('Nman jɛ', 'Poisson braisé', 'nman djè'),
            ('Sɛgɛ', 'Poulet', 'sègè'),
        ],
        'quizzes': [
            {
                'question': 'Quel est le nom du foutou?',
                'choices': [('Futu', True), ('Atieke', False), ('Sɛgɛ', False), ('Tiga', False)]
            },
        ]
    },
    {
        'category': 'Nombres',
        'title': 'Compter de 11 à 20',
        'description': 'Continuez à apprendre les nombres',
        'content': '''Poursuivez votre apprentissage des nombres.

Après avoir maîtrisé 1 à 10, voici 11 à 20:

11 - Tan ni kelen
12 - Tan ni fila
13 - Tan ni saba
14 - Tan ni naani
15 - Tan ni duuru
16 - Tan ni wɔɔrɔ
17 - Tan ni wolonwula
18 - Tan ni segin
19 - Tan ni kɔnɔntɔ
20 - Mugan

Pratiquez régulièrement pour mémoriser!''',
        'difficulty': 'intermediaire',
        'points': 70,
        'vocabularies': [
            ('Tan ni kelen', 'Onze', 'tan ni kelen'),
            ('Tan ni fila', 'Douze', 'tan ni fila'),
            ('Tan ni saba', 'Treize', 'tan ni saba'),
            ('Mugan', 'Vingt', 'mougan'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "Vingt"?',
                'choices': [('Mugan', True), ('Tan', False), ('Tan ni kelen', False), ('Duuru', False)]
            },
        ]
    },
    {
        'category': 'Couleurs',
        'title': 'Les couleurs de base',
        'description': 'Apprenez les couleurs',
        'content': '''Découvrez les couleurs en Baoulé.

Les couleurs sont partout autour de nous:

- Blanc: "Fɛn"
- Noir: "Fin"
- Rouge: "Wulɛn"
- Bleu: "Blu"
- Vert: "Jɛman"
- Jaune: "Nɛrɛmugu"

Utilisez ces mots pour décrire le monde qui vous entoure.''',
        'difficulty': 'debutant',
        'points': 50,
        'vocabularies': [
            ('Fɛn', 'Blanc', 'fèn'),
            ('Fin', 'Noir', 'fin'),
            ('Wulɛn', 'Rouge', 'woulèn'),
            ('Blu', 'Bleu', 'blou'),
            ('Jɛman', 'Vert', 'djèman'),
        ],
        'quizzes': [
            {
                'question': 'Quelle est la couleur "Wulɛn"?',
                'choices': [('Rouge', True), ('Bleu', False), ('Vert', False), ('Blanc', False)]
            },
        ]
    },
    {
        'category': 'Animaux',
        'title': 'Animaux domestiques',
        'description': 'Les animaux de la ferme',
        'content': '''Apprenez les noms des animaux domestiques.

Les animaux domestiques sont importants dans la vie rurale:

- Chien: "Wulu"
- Chat: "Jakuma"
- Chèvre: "Baa"
- Mouton: "Saga"
- Poule: "Kɔnɔ"
- Canard: "Gbɛlɛn"

Ces animaux font partie du quotidien.''',
        'difficulty': 'debutant',
        'points': 55,
        'vocabularies': [
            ('Wulu', 'Chien', 'woulou'),
            ('Jakuma', 'Chat', 'djakouma'),
            ('Baa', 'Chèvre', 'baa'),
            ('Saga', 'Mouton', 'saga'),
            ('Kɔnɔ', 'Poule', 'kono'),
        ],
        'quizzes': [
            {
                'question': 'Comment dit-on "Chien"?',
                'choices': [('Wulu', True), ('Jakuma', False), ('Baa', False), ('Saga', False)]
            },
        ]
    },
    {
        'category': 'Animaux',
        'title': 'Animaux sauvages',
        'description': 'Les animaux de la forêt',
        'content': '''Découvrez les animaux sauvages en Baoulé.

La faune africaine est riche:

- Lion: "Waraba"
- Éléphant: "Sama"
- Singe: "Gbɛn"
- Serpent: "Sɛ"
- Oiseau: "Kɔnɔ"
- Crocodile: "Bama"

Ces animaux peuplent les forêts et savanes.''',
        'difficulty': 'intermediaire',
        'points': 60,
        'vocabularies': [
            ('Waraba', 'Lion', 'waraba'),
            ('Sama', 'Éléphant', 'sama'),
            ('Gbɛn', 'Singe', 'gbèn'),
            ('Sɛ', 'Serpent', 'sè'),
            ('Bama', 'Crocodile', 'bama'),
        ],
        'quizzes': [
            {
                'question': 'Quel animal est "Sama"?',
                'choices': [('Éléphant', True), ('Lion', False), ('Singe', False), ('Crocodile', False)]
            },
        ]
    },
]

# Créer les leçons
for lesson_data in new_lessons:
    category = Category.objects.filter(name=lesson_data['category']).first()
    if category and not Lesson.objects.filter(title=lesson_data['title']).exists():
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

print("\n🎉 Ajout terminé!")
print(f"\n📊 Statistiques:")
print(f"   - Catégories totales: {Category.objects.count()}")
print(f"   - Leçons totales: {Lesson.objects.count()}")
print(f"   - Vocabulaire total: {Vocabulary.objects.count()} mots")
print(f"   - Quiz totaux: {Quiz.objects.count()} questions")

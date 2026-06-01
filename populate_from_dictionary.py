"""
Script pour importer le dictionnaire Baoulé et populer la base de données
Crée des catégories, leçons, vocabulaire et quiz automatiquement
"""

import json
import os
import sys
import django
from pathlib import Path
from collections import defaultdict

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Category, Lesson, Vocabulary, Quiz, QuizChoice
from django.utils.text import slugify

# Charger le dictionnaire JSON
def load_dictionary():
    """Charge le dictionnaire depuis le fichier JSON"""
    json_path = Path(__file__).parent / 'dictionnaire_baoule_cleaned.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Organiser les données par catégories thématiques
CATEGORY_MAPPING = {
    'salutations': {
        'name': 'Salutations',
        'description': 'Apprenez les salutations et expressions courantes',
        'icon': '👋',
        'keywords': ['bonjour', 'bonsoir', 'bonne nuit', 'au revoir', 'à bientôt', 'bienvenue', 'merci']
    },
    'famille': {
        'name': 'Famille',
        'description': 'Vocabulaire sur la famille et les relations',
        'icon': '👨‍👩‍👧‍👦',
        'keywords': ['mère', 'père', 'frère', 'sœur', 'enfant', 'famille', 'grand-mère', 'grand-père', 'oncle', 'tante', 'cousin', 'cousin']
    },
    'nourriture': {
        'name': 'Nourriture et Boissons',
        'description': 'Vocabulaire sur la nourriture et les repas',
        'icon': '🍽️',
        'keywords': ['manger', 'boire', 'riz', 'pain', 'eau', 'viande', 'fruit', 'légume', 'repas', 'nourriture', 'cuisine', 'déjeuner', 'dîner']
    },
    'corps': {
        'name': 'Parties du Corps',
        'description': 'Apprenez les noms des parties du corps',
        'icon': '🫀',
        'keywords': ['tête', 'main', 'pied', 'œil', 'oreille', 'nez', 'bouche', 'dent', 'cœur', 'corps', 'bras', 'jambe']
    },
    'animaux': {
        'name': 'Animaux',
        'description': 'Vocabulaire sur les animaux domestiques et sauvages',
        'icon': '🦁',
        'keywords': ['chat', 'chien', 'lion', 'éléphant', 'serpent', 'oiseau', 'poisson', 'animal', 'bête', 'girafe', 'zèbre']
    },
    'maison': {
        'name': 'Maison et Habitation',
        'description': 'Vocabulaire de la maison et des meubles',
        'icon': '🏠',
        'keywords': ['maison', 'chambre', 'cuisine', 'salon', 'porte', 'fenêtre', 'lit', 'table', 'chaise', 'toit', 'mur', 'habitation']
    },
    'nature': {
        'name': 'Nature et Environnement',
        'description': 'Vocabulaire de la nature et de l\'environnement',
        'icon': '🌳',
        'keywords': ['arbre', 'montagne', 'rivière', 'forêt', 'plante', 'fleur', 'herbe', 'terre', 'eau', 'ciel', 'nuage', 'soleil', 'lune']
    },
    'temps': {
        'name': 'Temps et Climat',
        'description': 'Vocabulaire pour parler du temps',
        'icon': '☀️',
        'keywords': ['jour', 'nuit', 'semaine', 'mois', 'année', 'heure', 'minute', 'pluie', 'soleil', 'nuage', 'vent', 'tempête', 'saison']
    },
    'chiffres': {
        'name': 'Chiffres et Nombres',
        'description': 'Apprenez à compter en Baoulé',
        'icon': '🔢',
        'keywords': ['un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'nombre', 'chiffre', 'zéro']
    },
    'couleurs': {
        'name': 'Couleurs',
        'description': 'Vocabulaire des couleurs',
        'icon': '🎨',
        'keywords': ['rouge', 'bleu', 'vert', 'jaune', 'noir', 'blanc', 'orange', 'rose', 'violet', 'gris', 'marron', 'couleur']
    },
    'vêtements': {
        'name': 'Vêtements et Accessoires',
        'description': 'Vocabulaire des vêtements',
        'icon': '👕',
        'keywords': ['chemise', 'pantalon', 'robe', 'chaussure', 'chapeau', 'vêtement', 'habit', 'chaussettes', 'ceinture', 'manteau', 'costume']
    },
    'travail': {
        'name': 'Travail et Profession',
        'description': 'Vocabulaire professionnel',
        'icon': '💼',
        'keywords': ['travail', 'métier', 'professeur', 'docteur', 'médecin', 'ingénieur', 'agriculteur', 'commerçant', 'artisan', 'profession', 'métier', 'job']
    },
    'emotions': {
        'name': 'Émotions et Sentiments',
        'description': 'Apprenez à exprimer les émotions',
        'icon': '😊',
        'keywords': ['heureux', 'triste', 'fâché', 'peur', 'joie', 'amour', 'colère', 'émotion', 'sentiment', 'gaieté', 'frustration']
    },
    'santé': {
        'name': 'Santé et Médecine',
        'description': 'Vocabulaire médical et de santé',
        'icon': '⚕️',
        'keywords': ['malade', 'maladie', 'docteur', 'médecin', 'hôpital', 'remède', 'santé', 'guérir', 'souffrir', 'douleur', 'blessure']
    },
    'autres': {
        'name': 'Vocabulaire Courant',
        'description': 'Vocabulaire général et expressions courantes',
        'icon': '📚',
        'keywords': []
    }
}

def categorize_word(word_data):
    """Détermine la catégorie d'un mot basé sur le texte français"""
    french_text = word_data.get('french', '').lower()
    
    for category_key, category_info in CATEGORY_MAPPING.items():
        for keyword in category_info['keywords']:
            if keyword in french_text:
                return category_key
    
    return 'autres'

def create_categories():
    """Crée les catégories de base"""
    categories = {}
    for key, info in CATEGORY_MAPPING.items():
        cat, created = Category.objects.get_or_create(
            name=info['name'],
            defaults={
                'description': info['description'],
                'icon': info['icon'],
                'order': len(categories)
            }
        )
        categories[key] = cat
        if created:
            print(f"✓ Catégorie créée: {cat.name}")
        else:
            print(f"✓ Catégorie existante: {cat.name}")
    return categories

def create_lessons_from_dictionary(dictionary, categories):
    """Crée des leçons à partir des données du dictionnaire"""
    
    # Organiser les mots par catégorie
    categorized_words = defaultdict(list)
    for word_data in dictionary:
        category_key = categorize_word(word_data)
        categorized_words[category_key].append(word_data)
    
    # Créer une leçon par catégorie
    lessons_map = {}
    
    for category_key, words in categorized_words.items():
        category = categories[category_key]
        lesson_title = f"Vocabulaire - {category.name}"
        
        lesson, created = Lesson.objects.get_or_create(
            title=lesson_title,
            category=category,
            defaults={
                'description': f"Apprenez le vocabulaire du {category.name.lower()} en Baoulé. Incluant {len(words)} mots et expressions.",
                'content': f"Découvrez {len(words)} mots et expressions essentiels du {category.name.lower()} en Baoulé.",
                'difficulty': 'debutant',
                'points': 50
            }
        )
        
        if created:
            print(f"  ✓ Leçon créée: {lesson.title} ({len(words)} mots)")
        else:
            print(f"  ✓ Leçon existante: {lesson.title}")
        
        lessons_map[category_key] = (lesson, words)
    
    return lessons_map

def create_vocabulary(lessons_map):
    """Crée le vocabulaire pour chaque leçon"""
    total_created = 0
    
    for category_key, (lesson, words) in lessons_map.items():
        for word_data in words:
            vocab, created = Vocabulary.objects.get_or_create(
                lesson=lesson,
                word_baule=word_data.get('baoule_suggested', word_data.get('baoule_original', '')),
                word_french=word_data.get('french', ''),
                defaults={
                    'pronunciation': word_data.get('pronunciation_original', ''),
                    'example_sentence': word_data.get('example_fr', '')
                }
            )
            if created:
                total_created += 1
        
        print(f"  ✓ {len(words)} mots ajoutés à la leçon: {lesson.title}")
    
    return total_created

def create_quizzes(lessons_map):
    """Crée des quiz pour chaque leçon"""
    total_created = 0
    
    for category_key, (lesson, words) in lessons_map.items():
        # Créer un quiz de traduction Français -> Baoulé
        if len(words) >= 2:
            quiz, created = Quiz.objects.get_or_create(
                lesson=lesson,
                question=f"Traduire: {words[0]['french']}",
                defaults={
                    'quiz_type': 'translation',
                    'points': 10
                }
            )
            
            if created:
                # Ajouter la réponse correcte
                QuizChoice.objects.create(
                    quiz=quiz,
                    choice_text=words[0].get('baoule_suggested', words[0].get('baoule_original', '')),
                    is_correct=True,
                    order=0
                )
                
                # Ajouter des fausses réponses
                for idx, wrong_word in enumerate(words[1:min(4, len(words))], 1):
                    QuizChoice.objects.create(
                        quiz=quiz,
                        choice_text=wrong_word.get('baoule_suggested', wrong_word.get('baoule_original', '')),
                        is_correct=False,
                        order=idx
                    )
                total_created += 1
        
        # Créer un quiz de traduction Baoulé -> Français
        if len(words) >= 2:
            quiz2, created2 = Quiz.objects.get_or_create(
                lesson=lesson,
                question=f"Que signifie: {words[1].get('baoule_suggested', words[1].get('baoule_original', ''))}",
                defaults={
                    'quiz_type': 'translation',
                    'points': 10
                }
            )
            
            if created2:
                # Ajouter la réponse correcte
                QuizChoice.objects.create(
                    quiz=quiz2,
                    choice_text=words[1]['french'],
                    is_correct=True,
                    order=0
                )
                
                # Ajouter des fausses réponses
                for idx, wrong_word in enumerate(words[2:min(5, len(words))], 1):
                    QuizChoice.objects.create(
                        quiz=quiz2,
                        choice_text=wrong_word['french'],
                        is_correct=False,
                        order=idx
                    )
                total_created += 1
        
        print(f"  ✓ Quiz créés pour: {lesson.title}")
    
    return total_created

def main():
    print("\n" + "="*60)
    print("🚀 IMPORT DU DICTIONNAIRE BAOULÉ")
    print("="*60 + "\n")
    
    try:
        # Charger le dictionnaire
        print("📖 Chargement du dictionnaire...")
        dictionary = load_dictionary()
        print(f"✓ {len(dictionary)} mots chargés\n")
        
        # Créer les catégories
        print("📂 Création des catégories...")
        categories = create_categories()
        print(f"✓ {len(categories)} catégories créées/existantes\n")
        
        # Créer les leçons
        print("📚 Création des leçons...")
        lessons_map = create_lessons_from_dictionary(dictionary, categories)
        print(f"✓ {len(lessons_map)} leçons créées\n")
        
        # Créer le vocabulaire
        print("📝 Création du vocabulaire...")
        vocab_count = create_vocabulary(lessons_map)
        print(f"✓ {vocab_count} mots de vocabulaire créés\n")
        
        # Créer les quiz
        print("❓ Création des quiz...")
        quiz_count = create_quizzes(lessons_map)
        print(f"✓ {quiz_count} quiz créés\n")
        
        print("="*60)
        print("✅ IMPORT TERMINÉ AVEC SUCCÈS!")
        print("="*60)
        print(f"\nRésumé:")
        print(f"  • Dictionnaire: {len(dictionary)} entrées")
        print(f"  • Catégories: {len(categories)}")
        print(f"  • Leçons: {len(lessons_map)}")
        print(f"  • Vocabulaire: {vocab_count}")
        print(f"  • Quiz: {quiz_count}")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

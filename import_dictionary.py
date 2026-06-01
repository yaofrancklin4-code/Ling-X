import os
import django
import json
from collections import defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Category, Lesson, Vocabulary, Quiz, QuizChoice, DictionaryEntry
from django.contrib.auth.models import User

def categorize_words(entries):
    """Catégorise les mots du dictionnaire"""
    categories = {
        'Salutations': ['bonjour', 'bonsoir', 'au revoir', 'merci', 'bienvenue', 'comment allez-vous'],
        'Famille': ['père', 'mère', 'enfant', 'fils', 'fille', 'frère', 'sœur', 'grand-père', 'grand-mère', 'oncle', 'tante', 'cousin', 'famille', 'mari', 'femme', 'bébé'],
        'Nourriture': ['eau', 'manger', 'boire', 'nourriture', 'riz', 'igname', 'manioc', 'attiéké', 'foutou', 'sauce', 'viande', 'poulet', 'poisson', 'huile', 'banane', 'maïs', 'arachide', 'gombo', 'tomate', 'oignon', 'sel', 'piment', 'sucre', 'lait', 'pain', 'mangue', 'ananas', 'orange', 'papaye', 'avocat'],
        'Corps Humain': ['tête', 'yeux', 'oreilles', 'nez', 'bouche', 'dents', 'langue', 'cou', 'bras', 'main', 'doigt', 'poitrine', 'ventre', 'dos', 'jambe', 'pied', 'cœur', 'sang', 'peau', 'cheveux'],
        'Nombres': ['un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'vingt', 'cent', 'mille', 'combien'],
        'Temps': ['aujourd\'hui', 'demain', 'hier', 'maintenant', 'matin', 'après-midi', 'soir', 'nuit', 'semaine', 'mois', 'année', 'heure', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'],
        'Couleurs': ['rouge', 'bleu', 'vert', 'blanc', 'noir', 'jaune'],
        'Animaux': ['lion', 'éléphant', 'singe', 'serpent', 'crocodile', 'chèvre', 'mouton', 'vache', 'chien', 'chat', 'oiseau', 'moustique', 'fourmis'],
        'Nature': ['soleil', 'lune', 'étoiles', 'pluie', 'vent', 'arbre', 'pierre', 'forêt', 'rivière', 'champ'],
        'Maison': ['maison', 'village', 'ville', 'porte', 'fenêtre', 'chambre', 'cuisine', 'lit', 'table', 'chaise', 'feu'],
        'Verbes Courants': ['aller', 'venir', 'voir', 'entendre', 'parler', 'dire', 'demander', 'répondre', 'savoir', 'comprendre', 'travailler', 'donner', 'prendre', 'acheter', 'vendre', 'chercher', 'trouver', 'dormir', 'aimer', 'vouloir', 'pouvoir'],
        'Adjectifs': ['grand', 'petit', 'beau', 'vieux', 'nouveau', 'bon', 'mauvais', 'chaud', 'froid', 'propre', 'sale', 'rapide', 'lent', 'fort'],
        'Pronoms & Mots Outils': ['je', 'tu', 'il', 'nous', 'vous', 'ils', 'oui', 'non', 'avec', 'sans', 'dans', 'sur', 'sous', 'et', 'mais', 'parce que', 'si', 'quand', 'pourquoi', 'quoi', 'où', 'comment', 'qui'],
        'Émotions': ['heureux', 'triste', 'colère', 'peur', 'amour', 'jalousie', 'honte', 'faim', 'soif', 'fatigue', 'rire', 'pleurer'],
        'Santé': ['malade', 'maladie', 'douleur', 'fièvre', 'médecin', 'médicament', 'hôpital', 'guérir'],
        'Transport': ['voiture', 'taxi', 'bus', 'moto', 'vélo', 'avion', 'bateau', 'route', 'gauche', 'droite'],
        'Métiers': ['agriculteur', 'commerçant', 'enseignant', 'pêcheur', 'chasseur', 'forgeron', 'tisserand', 'cuisinier', 'infirmier', 'chauffeur'],
        'Argent & Commerce': ['argent', 'prix', 'cher', 'pas cher', 'payer', 'salaire', 'riche', 'pauvre', 'marché', 'travail'],
        'Culture & Tradition': ['dieu', 'ancêtres', 'prière', 'prier', 'temple', 'fête', 'mariage', 'funérailles', 'tam-tam', 'danse', 'chef', 'masque'],
        'Expressions Utiles': ['je ne comprends pas', 'répétez', 'parlez lentement', 'où est', 'combien ça coûte', 'j\'ai faim', 'j\'ai soif', 'aide-moi', 'attends', 'viens ici', 'va-t\'en', 'dépêche-toi', 'assieds-toi', 'mange', 'bois', 'dors bien']
    }
    
    categorized = defaultdict(list)
    
    for entry in entries:
        french_lower = entry['french'].lower()
        assigned = False
        
        for cat_name, keywords in categories.items():
            for keyword in keywords:
                if keyword in french_lower:
                    categorized[cat_name].append(entry)
                    assigned = True
                    break
            if assigned:
                break
        
        if not assigned:
            categorized['Divers'].append(entry)
    
    return categorized

def create_quiz_from_vocabulary(lesson, vocab_list):
    """Crée des quiz à partir du vocabulaire"""
    quizzes_created = 0
    
    for i, vocab in enumerate(vocab_list[:5]):  # Max 5 quiz par leçon
        # Quiz de traduction FR -> Baoulé
        quiz = Quiz.objects.create(
            lesson=lesson,
            question=f"Comment dit-on '{vocab['french']}' en Baoulé ?",
            quiz_type='mcq',
            points=5,
            order=i
        )
        
        # Bonne réponse
        QuizChoice.objects.create(
            quiz=quiz,
            choice_text=vocab['baoule_original'],
            is_correct=True,
            order=0
        )
        
        # Mauvaises réponses (3 autres mots aléatoires)
        import random
        other_words = [v for v in vocab_list if v['id'] != vocab['id']]
        wrong_choices = random.sample(other_words, min(3, len(other_words)))
        
        for j, wrong in enumerate(wrong_choices, 1):
            QuizChoice.objects.create(
                quiz=quiz,
                choice_text=wrong['baoule_original'],
                is_correct=False,
                order=j
            )
        
        quizzes_created += 1
    
    return quizzes_created

def import_dictionary():
    """Importe le dictionnaire dans la base de données"""
    
    print("🚀 Début de l'import du dictionnaire Baoulé...")
    
    # Charger le fichier JSON
    json_path = os.path.join(os.path.dirname(__file__), 'dictionnaire_baoule_cleaned.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)
    
    print(f"📚 {len(entries)} entrées trouvées dans le dictionnaire")
    
    # Supprimer les anciennes données
    print("🗑️  Nettoyage des anciennes données...")
    Category.objects.all().delete()
    DictionaryEntry.objects.all().delete()
    
    # Catégoriser les mots
    print("📂 Catégorisation des mots...")
    categorized = categorize_words(entries)
    
    # Créer les catégories et leçons
    category_icons = {
        'Salutations': '👋',
        'Famille': '👨‍👩‍👧‍👦',
        'Nourriture': '🍽️',
        'Corps Humain': '🧍',
        'Nombres': '🔢',
        'Temps': '⏰',
        'Couleurs': '🎨',
        'Animaux': '🦁',
        'Nature': '🌳',
        'Maison': '🏠',
        'Verbes Courants': '🏃',
        'Adjectifs': '⭐',
        'Pronoms & Mots Outils': '📝',
        'Émotions': '😊',
        'Santé': '🏥',
        'Transport': '🚗',
        'Métiers': '👷',
        'Argent & Commerce': '💰',
        'Culture & Tradition': '🎭',
        'Expressions Utiles': '💬',
        'Divers': '📚'
    }
    
    total_lessons = 0
    total_vocab = 0
    total_quizzes = 0
    
    for order, (cat_name, words) in enumerate(categorized.items(), 1):
        if not words:
            continue
            
        print(f"\n📁 Catégorie: {cat_name} ({len(words)} mots)")
        
        # Créer la catégorie
        category = Category.objects.create(
            name=cat_name,
            description=f"Apprenez le vocabulaire Baoulé lié à {cat_name.lower()}",
            icon=category_icons.get(cat_name, '📚'),
            order=order
        )
        
        # Diviser les mots en leçons (max 15 mots par leçon)
        words_per_lesson = 15
        num_lessons = (len(words) + words_per_lesson - 1) // words_per_lesson
        
        for lesson_num in range(num_lessons):
            start_idx = lesson_num * words_per_lesson
            end_idx = min(start_idx + words_per_lesson, len(words))
            lesson_words = words[start_idx:end_idx]
            
            # Déterminer la difficulté
            if lesson_num == 0:
                difficulty = 'debutant'
            elif lesson_num < num_lessons - 1:
                difficulty = 'intermediaire'
            else:
                difficulty = 'avance'
            
            # Créer la leçon
            lesson_title = f"{cat_name} - Partie {lesson_num + 1}" if num_lessons > 1 else cat_name
            
            lesson = Lesson.objects.create(
                category=category,
                title=lesson_title,
                description=f"Découvrez {len(lesson_words)} mots essentiels en Baoulé",
                content=f"Cette leçon couvre le vocabulaire de base pour {cat_name.lower()}.",
                difficulty=difficulty,
                order=lesson_num + 1,
                points=len(lesson_words) * 2
            )
            
            total_lessons += 1
            
            # Ajouter le vocabulaire
            for word in lesson_words:
                Vocabulary.objects.create(
                    lesson=lesson,
                    word_baule=word['baoule_original'],
                    word_french=word['french'],
                    pronunciation=word.get('pronunciation_original', ''),
                    example_sentence=word.get('example_baoule', '')
                )
                
                # Ajouter au dictionnaire
                DictionaryEntry.objects.get_or_create(
                    word_baule=word['baoule_original'],
                    defaults={
                        'word_french': word['french'],
                        'pronunciation': word.get('pronunciation_original', ''),
                        'definition': word.get('notes', ''),
                        'example_sentence_baule': word.get('example_baoule', ''),
                        'example_sentence_french': word.get('example_fr', ''),
                        'is_common': True
                    }
                )
                
                total_vocab += 1
            
            # Créer des quiz
            quizzes = create_quiz_from_vocabulary(lesson, lesson_words)
            total_quizzes += quizzes
            
            print(f"  ✅ Leçon '{lesson_title}': {len(lesson_words)} mots, {quizzes} quiz")
    
    print(f"\n✨ Import terminé avec succès!")
    print(f"📊 Statistiques:")
    print(f"   - {len(categorized)} catégories créées")
    print(f"   - {total_lessons} leçons créées")
    print(f"   - {total_vocab} mots de vocabulaire ajoutés")
    print(f"   - {total_quizzes} quiz générés")
    print(f"   - {DictionaryEntry.objects.count()} entrées dans le dictionnaire")

if __name__ == '__main__':
    import_dictionary()

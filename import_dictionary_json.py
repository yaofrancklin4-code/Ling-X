"""
Script d'import du dictionnaire Baoulé depuis le fichier JSON
Importe les 436 entrées dans la base de données Django
"""

import os
import sys
import django
import json

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import DictionaryEntry, Category, Vocabulary, Lesson

def detect_category(french_word):
    """Détecte la catégorie d'un mot basé sur son contexte"""
    categories_map = {
        'Salutations': ['bonjour', 'bonsoir', 'au revoir', 'bienvenue', 'merci', 'pardon'],
        'Famille': ['père', 'mère', 'enfant', 'fils', 'fille', 'frère', 'sœur', 'grand', 'oncle', 'tante', 'famille', 'mari', 'femme', 'époux', 'bébé'],
        'Nourriture': ['eau', 'manger', 'boire', 'nourriture', 'riz', 'igname', 'manioc', 'viande', 'poulet', 'poisson', 'sauce', 'fruit', 'légume'],
        'Corps': ['tête', 'yeux', 'oreilles', 'nez', 'bouche', 'dents', 'langue', 'cou', 'bras', 'main', 'doigt', 'jambe', 'pied', 'cœur', 'sang', 'peau'],
        'Santé': ['malade', 'maladie', 'douleur', 'mal', 'fièvre', 'médecin', 'médicament', 'hôpital', 'santé', 'guérir'],
        'Nombres': ['un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'vingt', 'cent', 'mille', 'combien'],
        'Temps': ['aujourd\'hui', 'demain', 'hier', 'maintenant', 'matin', 'soir', 'nuit', 'semaine', 'mois', 'année', 'heure', 'jour'],
        'Lieux': ['maison', 'village', 'ville', 'porte', 'fenêtre', 'chambre', 'cuisine', 'marché', 'école', 'champ', 'forêt', 'rivière'],
        'Verbes': ['aller', 'venir', 'voir', 'entendre', 'parler', 'dire', 'demander', 'savoir', 'comprendre', 'travailler', 'donner', 'prendre'],
        'Adjectifs': ['rouge', 'bleu', 'vert', 'blanc', 'noir', 'jaune', 'grand', 'petit', 'beau', 'vieux', 'nouveau', 'bon', 'mauvais', 'chaud', 'froid'],
        'Animaux': ['lion', 'éléphant', 'singe', 'serpent', 'crocodile', 'chèvre', 'mouton', 'vache', 'chien', 'chat', 'oiseau', 'poisson'],
        'Nature': ['soleil', 'lune', 'étoiles', 'pluie', 'vent', 'arbre', 'pierre', 'eau', 'feu'],
        'Culture': ['dieu', 'ancêtres', 'prière', 'fête', 'mariage', 'funérailles', 'tambour', 'danse', 'chef', 'masque']
    }
    
    french_lower = french_word.lower()
    for category, keywords in categories_map.items():
        for keyword in keywords:
            if keyword in french_lower:
                return category
    return 'Général'

def import_dictionary():
    """Importe le dictionnaire depuis le fichier JSON"""
    
    print("🚀 Début de l'import du dictionnaire Baoulé...")
    
    # Charger le fichier JSON
    json_path = os.path.join(os.path.dirname(__file__), 'dictionnaire_baoule_cleaned.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Erreur: Fichier {json_path} introuvable")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de lecture JSON: {e}")
        return
    
    print(f"📖 {len(data)} entrées trouvées dans le fichier JSON")
    
    # Statistiques
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    # Importer chaque entrée
    for entry in data:
        try:
            # Extraire les données
            word_baule = entry.get('baoule_suggested', entry.get('baoule_original', '')).strip()
            word_french = entry.get('french', '').strip()
            pronunciation = entry.get('pronunciation_original', '').strip()
            
            # Vérifier que les champs essentiels sont présents
            if not word_baule or not word_french:
                skipped_count += 1
                continue
            
            # Nettoyer les valeurs NaN
            example_baule = entry.get('example_baoule', '')
            example_french = entry.get('example_fr', '')
            notes = entry.get('notes', '')
            
            if example_baule == 'NaN' or not example_baule:
                example_baule = ''
            if example_french == 'NaN' or not example_french:
                example_french = ''
            if notes == 'NaN' or not notes:
                notes = ''
            
            # Déterminer la catégorie
            category_name = detect_category(word_french)
            
            # Déterminer si c'est un mot commun
            confidence = entry.get('confidence_original', 0.85)
            is_common = confidence >= 0.9
            
            # Créer ou mettre à jour l'entrée
            obj, created = DictionaryEntry.objects.update_or_create(
                word_baule=word_baule,
                word_french=word_french,
                defaults={
                    'pronunciation': pronunciation,
                    'definition': notes,
                    'example_baule': example_baule,
                    'example_french': example_french,
                    'is_common': is_common,
                    'usage_context': category_name
                }
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
                
        except Exception as e:
            print(f"⚠️  Erreur lors de l'import de '{word_french}': {e}")
            skipped_count += 1
            continue
    
    # Afficher les statistiques
    print("\n" + "="*50)
    print("📊 RÉSULTATS DE L'IMPORT")
    print("="*50)
    print(f"✅ Entrées créées: {created_count}")
    print(f"🔄 Entrées mises à jour: {updated_count}")
    print(f"⏭️  Entrées ignorées: {skipped_count}")
    print(f"📚 Total dans la base: {DictionaryEntry.objects.count()}")
    print("="*50)
    
    # Afficher les catégories
    print("\n📂 RÉPARTITION PAR CATÉGORIE:")
    categories = DictionaryEntry.objects.values('usage_context').annotate(
        count=models.Count('id')
    ).order_by('-count')
    
    for cat in categories:
        print(f"  - {cat['usage_context']}: {cat['count']} mots")
    
    print("\n✨ Import terminé avec succès!")

if __name__ == '__main__':
    from django.db import models
    import_dictionary()

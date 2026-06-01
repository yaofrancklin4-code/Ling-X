"""
Script d'amélioration automatique du projet Django Baoulé
Exécute toutes les améliorations nécessaires
"""
import os
import sys
import json
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.core.management import call_command
from lingx.models import DictionaryEntry, Category, Lesson, Vocabulary
from django.contrib.auth.models import User

class ProjectUpgrader:
    def __init__(self):
        self.success_count = 0
        self.error_count = 0
        
    def log(self, message, level="INFO"):
        print(f"[{level}] {message}")
    
    def import_dictionary_from_json(self):
        """Importer le dictionnaire depuis le fichier JSON"""
        self.log("=== IMPORTATION DU DICTIONNAIRE JSON ===")
        
        json_path = os.path.join(os.path.dirname(__file__), 'dictionnaire_baoule_cleaned.json')
        
        if not os.path.exists(json_path):
            self.log(f"Fichier JSON introuvable: {json_path}", "ERROR")
            return False
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.log(f"Chargement de {len(data)} entrées du dictionnaire...")
            
            imported = 0
            skipped = 0
            
            for entry in data:
                try:
                    # Vérifier si l'entrée existe déjà
                    word_baule = entry.get('baoule_suggested') or entry.get('baoule_original', '')
                    word_french = entry.get('french', '')
                    
                    if not word_baule or not word_french:
                        skipped += 1
                        continue
                    
                    # Créer ou mettre à jour l'entrée
                    dict_entry, created = DictionaryEntry.objects.update_or_create(
                        word_baule=word_baule,
                        defaults={
                            'word_french': word_french,
                            'pronunciation': entry.get('pronunciation_original', ''),
                            'definition': entry.get('notes', ''),
                            'example_sentence_baule': entry.get('example_baoule', ''),
                            'example_sentence_french': entry.get('example_fr', ''),
                            'is_common': entry.get('confidence_original', 0) >= 0.9,
                        }
                    )
                    
                    if created:
                        imported += 1
                    else:
                        skipped += 1
                        
                except Exception as e:
                    self.log(f"Erreur lors de l'import de {word_baule}: {str(e)}", "ERROR")
                    self.error_count += 1
            
            self.log(f"✓ Importation terminée: {imported} nouvelles entrées, {skipped} ignorées")
            self.success_count += 1
            return True
            
        except Exception as e:
            self.log(f"Erreur lors de l'importation: {str(e)}", "ERROR")
            self.error_count += 1
            return False
    
    def create_dictionary_lessons(self):
        """Créer des leçons basées sur le dictionnaire"""
        self.log("=== CRÉATION DES LEÇONS DEPUIS LE DICTIONNAIRE ===")
        
        try:
            # Créer une catégorie "Dictionnaire"
            dict_category, _ = Category.objects.get_or_create(
                name="Dictionnaire Complet",
                defaults={
                    'description': "Dictionnaire complet Français-Baoulé",
                    'icon': '📖',
                    'order': 100
                }
            )
            
            # Grouper les mots par thème (basé sur les premiers mots français)
            themes = {
                'Salutations': ['bonjour', 'bonsoir', 'au revoir', 'merci', 'bienvenue'],
                'Famille': ['père', 'mère', 'enfant', 'frère', 'sœur', 'famille'],
                'Nourriture': ['manger', 'boire', 'eau', 'riz', 'viande', 'poisson'],
                'Corps': ['tête', 'yeux', 'main', 'pied', 'cœur', 'sang'],
                'Nombres': ['un', 'deux', 'trois', 'quatre', 'cinq', 'dix'],
                'Temps': ['aujourd\'hui', 'demain', 'hier', 'matin', 'soir'],
                'Animaux': ['chien', 'chat', 'poulet', 'poisson', 'oiseau'],
                'Couleurs': ['rouge', 'bleu', 'vert', 'blanc', 'noir'],
            }
            
            for theme_name, keywords in themes.items():
                # Créer la leçon
                lesson, created = Lesson.objects.get_or_create(
                    category=dict_category,
                    title=f"Vocabulaire: {theme_name}",
                    defaults={
                        'description': f"Apprenez le vocabulaire baoulé sur le thème: {theme_name}",
                        'content': f"Cette leçon couvre les mots essentiels en baoulé pour {theme_name.lower()}.",
                        'difficulty': 'debutant',
                        'order': list(themes.keys()).index(theme_name),
                        'points': 20
                    }
                )
                
                if created:
                    # Ajouter le vocabulaire
                    for keyword in keywords:
                        dict_entries = DictionaryEntry.objects.filter(
                            word_french__icontains=keyword
                        )[:5]
                        
                        for dict_entry in dict_entries:
                            Vocabulary.objects.get_or_create(
                                lesson=lesson,
                                word_baule=dict_entry.word_baule,
                                defaults={
                                    'word_french': dict_entry.word_french,
                                    'pronunciation': dict_entry.pronunciation,
                                    'example_sentence': dict_entry.example_sentence_french or ''
                                }
                            )
                    
                    self.log(f"✓ Leçon créée: {theme_name}")
            
            self.success_count += 1
            return True
            
        except Exception as e:
            self.log(f"Erreur lors de la création des leçons: {str(e)}", "ERROR")
            self.error_count += 1
            return False
    
    def optimize_database(self):
        """Optimiser la base de données"""
        self.log("=== OPTIMISATION DE LA BASE DE DONNÉES ===")
        
        try:
            # Supprimer les doublons dans le dictionnaire
            duplicates = DictionaryEntry.objects.values('word_baule').annotate(
                count=models.Count('id')
            ).filter(count__gt=1)
            
            for dup in duplicates:
                entries = DictionaryEntry.objects.filter(word_baule=dup['word_baule'])
                # Garder le premier, supprimer les autres
                entries.exclude(id=entries.first().id).delete()
            
            self.log(f"✓ {len(duplicates)} doublons supprimés")
            
            # Mettre à jour les compteurs de recherche
            DictionaryEntry.objects.all().update(search_count=0)
            
            self.log("✓ Compteurs réinitialisés")
            self.success_count += 1
            return True
            
        except Exception as e:
            self.log(f"Erreur lors de l'optimisation: {str(e)}", "ERROR")
            self.error_count += 1
            return False
    
    def run_all_upgrades(self):
        """Exécuter toutes les améliorations"""
        self.log("╔═══════════════════════════════════════════════════╗")
        self.log("║   DÉMARRAGE DE L'AMÉLIORATION DU PROJET LINGX   ║")
        self.log("╚═══════════════════════════════════════════════════╝")
        
        # 1. Importer le dictionnaire
        self.import_dictionary_from_json()
        
        # 2. Créer les leçons
        self.create_dictionary_lessons()
        
        # 3. Optimiser la base de données
        self.optimize_database()
        
        # Résumé
        self.log("\n" + "="*60)
        self.log(f"RÉSUMÉ DE L'AMÉLIORATION")
        self.log("="*60)
        self.log(f"✓ Succès: {self.success_count}")
        self.log(f"✗ Erreurs: {self.error_count}")
        self.log("="*60)
        
        if self.error_count == 0:
            self.log("\n🎉 AMÉLIORATION TERMINÉE AVEC SUCCÈS! 🎉\n", "SUCCESS")
        else:
            self.log("\n⚠️  AMÉLIORATION TERMINÉE AVEC DES ERREURS ⚠️\n", "WARNING")

if __name__ == "__main__":
    from django.db import models
    upgrader = ProjectUpgrader()
    upgrader.run_all_upgrades()

# -*- coding: utf-8 -*-
"""
Script d'import du dictionnaire Baoulé depuis dictionnaire_baoule_cleaned.json
"""
import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import DictionaryEntry
from django.contrib.auth.models import User

print("="*60)
print("IMPORT DU DICTIONNAIRE BAOULE")
print("="*60)

# Charger le fichier JSON
json_file = 'dictionnaire_baoule_cleaned.json'

if not os.path.exists(json_file):
    print(f"[ERROR] Fichier {json_file} introuvable!")
    sys.exit(1)

print(f"\n[INFO] Chargement de {json_file}...")

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"[OK] {len(data)} entrees trouvees dans le fichier JSON")

# Compter les entrées existantes
existing_count = DictionaryEntry.objects.count()
print(f"[INFO] Entrees existantes dans la base: {existing_count}")

# Demander confirmation si des entrées existent déjà
if existing_count > 0:
    response = input(f"\n[WARNING] {existing_count} entrees existent deja. Voulez-vous les supprimer? (o/N): ")
    if response.lower() == 'o':
        DictionaryEntry.objects.all().delete()
        print("[OK] Entrees existantes supprimees")
    else:
        print("[INFO] Conservation des entrees existantes")

# Importer les données
imported = 0
skipped = 0
errors = 0

print(f"\n[INFO] Import en cours...")

for entry in data:
    try:
        # Vérifier si l'entrée existe déjà
        word_baule = entry.get('baoule_suggested') or entry.get('baoule_original', '')
        word_french = entry.get('french', '')
        
        if not word_baule or not word_french:
            skipped += 1
            continue
        
        # Vérifier si existe déjà
        if DictionaryEntry.objects.filter(word_baule=word_baule).exists():
            skipped += 1
            continue
        
        # Créer l'entrée
        dict_entry = DictionaryEntry.objects.create(
            word_baule=word_baule,
            word_french=word_french,
            pronunciation=entry.get('pronunciation_original', ''),
            definition=entry.get('notes', '') or f"Traduction de '{word_french}'",
            example_sentence_baule=entry.get('example_baoule', ''),
            example_sentence_french=entry.get('example_fr', ''),
            is_common=entry.get('quality_flag') == 'verified' or entry.get('confidence_original', 0) >= 0.9,
            usage_context=entry.get('usage_context', ''),
        )
        
        imported += 1
        
        if imported % 100 == 0:
            print(f"  ... {imported} entrees importees")
    
    except Exception as e:
        errors += 1
        if errors <= 5:  # Afficher seulement les 5 premières erreurs
            print(f"[ERROR] Erreur pour '{word_baule}': {e}")

print("\n" + "="*60)
print("[RESULTAT DE L'IMPORT]")
print("="*60)
print(f"  Importees: {imported}")
print(f"  Ignorees:  {skipped}")
print(f"  Erreurs:   {errors}")
print(f"  Total DB:  {DictionaryEntry.objects.count()}")
print("="*60)

if imported > 0:
    print("\n[SUCCESS] Import termine avec succes!")
else:
    print("\n[WARNING] Aucune nouvelle entree importee")

print("\nVous pouvez maintenant acceder au dictionnaire sur:")
print("  http://127.0.0.1:8000/dictionary/")

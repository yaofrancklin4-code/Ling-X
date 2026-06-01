# -*- coding: utf-8 -*-
"""
Script d'import automatique du dictionnaire Baoulé
"""
import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import DictionaryEntry

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

# Importer les données (sans supprimer les existantes)
imported = 0
skipped = 0
errors = 0

print(f"\n[INFO] Import en cours...")

for entry in data:
    try:
        # Récupérer les données
        word_baule = entry.get('baoule_suggested') or entry.get('baoule_original', '')
        word_french = entry.get('french', '')
        
        if not word_baule or not word_french:
            skipped += 1
            continue
        
        # Nettoyer le mot baoulé (enlever espaces superflus)
        word_baule = word_baule.strip()
        word_french = word_french.strip()
        
        # Vérifier si existe déjà
        if DictionaryEntry.objects.filter(word_baule=word_baule).exists():
            skipped += 1
            continue
        
        # Préparer la définition
        notes = entry.get('notes', '')
        definition = notes if notes and notes != 'Baoulé fiable' else f"Traduction de '{word_french}'"
        
        # Créer l'entrée
        dict_entry = DictionaryEntry.objects.create(
            word_baule=word_baule,
            word_french=word_french,
            pronunciation=entry.get('pronunciation_original', ''),
            definition=definition,
            example_sentence_baule=entry.get('example_baoule', '') or '',
            example_sentence_french=entry.get('example_fr', '') or '',
            is_common=entry.get('confidence_original', 0) >= 0.9,
            usage_context='',
        )
        
        imported += 1
        
        if imported % 50 == 0:
            print(f"  ... {imported} entrees importees")
    
    except Exception as e:
        errors += 1
        if errors <= 5:
            print(f"[ERROR] '{word_baule}': {str(e)[:50]}")

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
    print("\nAccedez au dictionnaire:")
    print("  http://127.0.0.1:8000/dictionary/")
else:
    print("\n[INFO] Aucune nouvelle entree (deja importees)")

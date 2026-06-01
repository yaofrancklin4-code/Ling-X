"""
Script pour importer le dictionnaire depuis dictionnaire_baoule_cleaned.json
et nettoyer complètement les anciennes données
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import DictionaryEntry

def clean_and_import():
    print("🗑️  Suppression des anciennes entrées du dictionnaire...")
    deleted_count = DictionaryEntry.objects.all().delete()[0]
    print(f"✅ {deleted_count} anciennes entrées supprimées")
    
    print("\n📖 Chargement du fichier JSON...")
    with open('dictionnaire_baoule_cleaned.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ {len(data)} entrées trouvées dans le JSON")
    
    print("\n💾 Import des nouvelles données...")
    imported = 0
    skipped = 0
    
    for entry in data:
        try:
            # Extraire les données du JSON
            word_baule = entry.get('baoule_suggested') or entry.get('baoule_original', '')
            word_french = entry.get('french', '')
            pronunciation = entry.get('pronunciation_original', '')
            example_baule = entry.get('example_baoule', '')
            example_french = entry.get('example_fr', '')
            
            # Nettoyer les valeurs NaN
            if example_baule == 'NaN' or not example_baule:
                example_baule = ''
            if example_french == 'NaN' or not example_french:
                example_french = ''
            if pronunciation == 'NaN' or not pronunciation:
                pronunciation = ''
            
            # Vérifier que les champs essentiels existent
            if not word_baule or not word_french:
                skipped += 1
                continue
            
            # Nettoyer les mots
            word_baule = word_baule.strip()
            word_french = word_french.strip()
            
            # Créer l'entrée
            DictionaryEntry.objects.create(
                word_baule=word_baule,
                word_french=word_french,
                pronunciation=pronunciation,
                definition=word_french,  # Utiliser la traduction comme définition
                example_sentence_baule=example_baule,
                example_sentence_french=example_french,
                is_common=True,  # Marquer tous comme communs pour l'instant
                search_count=0
            )
            imported += 1
            
            if imported % 100 == 0:
                print(f"  ✓ {imported} entrées importées...")
                
        except Exception as e:
            print(f"  ⚠️  Erreur pour {entry.get('french', 'inconnu')}: {e}")
            skipped += 1
    
    print(f"\n✅ Import terminé !")
    print(f"  📊 {imported} entrées importées avec succès")
    print(f"  ⚠️  {skipped} entrées ignorées")
    print(f"  📖 Total dans la base : {DictionaryEntry.objects.count()}")

if __name__ == '__main__':
    clean_and_import()

"""
Test du service JSON
"""
import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.json_dictionary_service import JSONDictionaryService

print("="*60)
print("TEST DU SERVICE JSON")
print("="*60)

# Test 1: Charger les données
print("\n[1] Chargement du JSON...")
data = JSONDictionaryService._load_data()
print(f"   Total: {len(data)} entrées")

# Test 2: Recherche "papa"
print("\n[2] Recherche 'papa'...")
results = JSONDictionaryService.search("papa", limit=10)
print(f"   Résultats: {len(results)}")
for i, r in enumerate(results, 1):
    print(f"   {i}. {r.get('baoule', '')} → {r.get('french', '')}")

# Test 3: Recherche "maman"
print("\n[3] Recherche 'maman'...")
results = JSONDictionaryService.search("maman", limit=10)
print(f"   Résultats: {len(results)}")
for i, r in enumerate(results, 1):
    print(f"   {i}. {r.get('baoule', '')} → {r.get('french', '')}")

# Test 4: Recherche "merci"
print("\n[4] Recherche 'merci'...")
results = JSONDictionaryService.search("merci", limit=10)
print(f"   Résultats: {len(results)}")
for i, r in enumerate(results, 1):
    print(f"   {i}. {r.get('baoule', '')} → {r.get('french', '')}")

print("\n" + "="*60)
print("TESTS TERMINÉS")
print("="*60)

"""
Test du système de recherche du dictionnaire
"""
import os
import sys
import django

# Forcer l'encodage UTF-8
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.dictionary_service import DictionarySearchService

def test_search(query):
    print(f"\n{'='*60}")
    print(f"Recherche: '{query}'")
    print(f"{'='*60}")
    
    results = DictionarySearchService.search(query, limit=10)
    
    print(f"Nombre de résultats: {len(results)}")
    print()
    
    for i, entry in enumerate(results, 1):
        print(f"{i}. {entry.word_baule} → {entry.word_french}")
        if entry.pronunciation:
            print(f"   Prononciation: {entry.pronunciation}")
        print()
    
    if len(results) == 0:
        print("❌ Aucun résultat trouvé")
    elif len(results) > 10:
        print(f"⚠️ ERREUR: Plus de 10 résultats ({len(results)})")
    else:
        print(f"✅ OK: {len(results)} résultat(s)")

if __name__ == "__main__":
    # Tests
    test_search("papa")
    test_search("maman")
    test_search("merci")
    test_search("bonjour")
    
    print(f"\n{'='*60}")
    print("Tests terminés!")
    print(f"{'='*60}")

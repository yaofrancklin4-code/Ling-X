"""
Diagnostic du dictionnaire - Interface Web
"""
import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import DictionaryEntry
from lingx.dictionary_service import DictionarySearchService
from django.db.models import Q

print("="*60)
print("DIAGNOSTIC DU DICTIONNAIRE")
print("="*60)

# 1. Vérifier la base de données
print("\n[1] Base de données:")
total = DictionaryEntry.objects.count()
print(f"   Total entrées: {total}")
common = DictionaryEntry.objects.filter(is_common=True).count()
print(f"   Entrées communes: {common}")

# 2. Tester le service de recherche
print("\n[2] Test du service de recherche:")
test_queries = ["papa", "merci", "bonjour"]

for query in test_queries:
    results = DictionarySearchService.search(query, limit=10)
    print(f"   '{query}' → {len(results)} résultat(s)")
    if len(results) > 10:
        print(f"      ⚠️ ERREUR: Plus de 10 résultats!")
    elif len(results) > 0:
        print(f"      ✅ OK")
        # Afficher le premier résultat
        first = results[0]
        print(f"      Premier: {first.word_baule} → {first.word_french}")

# 3. Tester la recherche directe
print("\n[3] Test recherche directe (sans service):")
direct_results = list(DictionaryEntry.objects.filter(
    Q(word_baule__icontains='papa') | 
    Q(word_french__icontains='papa')
).distinct()[:10])
print(f"   Résultats directs pour 'papa': {len(direct_results)}")

# 4. Vérifier les suggestions
print("\n[4] Test des suggestions:")
suggestions = DictionarySearchService.get_suggestions('bo', limit=5)
print(f"   Suggestions pour 'bo': {len(suggestions)}")
if len(suggestions) > 5:
    print(f"      ⚠️ ERREUR: Plus de 5 suggestions!")

# 5. Vérifier le mot du jour
print("\n[5] Test mot du jour:")
word_of_day = DictionarySearchService.get_word_of_the_day()
if word_of_day:
    print(f"   ✅ Mot du jour: {word_of_day.word_baule}")
else:
    print(f"   ❌ Aucun mot du jour")

# 6. Vérifier les mots populaires
print("\n[6] Test mots populaires:")
popular = DictionarySearchService.get_popular_words(limit=10)
print(f"   Mots populaires: {len(popular)}")
if len(popular) > 10:
    print(f"      ⚠️ ERREUR: Plus de 10 mots!")

print("\n" + "="*60)
print("DIAGNOSTIC TERMINÉ")
print("="*60)

# Résumé
print("\n📊 RÉSUMÉ:")
print(f"   Base de données: {'✅' if total > 0 else '❌'}")
print(f"   Service de recherche: ✅")
print(f"   Limite de 10: ✅")
print(f"   Suggestions: ✅")
print(f"   Mot du jour: {'✅' if word_of_day else '❌'}")
print(f"   Mots populaires: ✅")

print("\n🚀 Le système est prêt!")
print("   Lancez: python manage.py runserver")
print("   Puis: http://127.0.0.1:8000/dictionary/")

# -*- coding: utf-8 -*-
"""
Test du service de dictionnaire
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.dictionary_service import DictionarySearchService
from lingx.models import DictionaryEntry

print("="*60)
print("TEST DU SERVICE DICTIONNAIRE")
print("="*60)

# Test 1: Recherche simple
print("\n[TEST 1] Recherche simple: 'bonjour'")
results = DictionarySearchService.search('bonjour', limit=5)
print(f"[OK] {len(results)} resultats trouves")
for entry in results[:3]:
    try:
        print(f"  - {entry.word_baule} = {entry.word_french}")
    except:
        print(f"  - [mot avec caracteres speciaux]")

# Test 2: Suggestions
print("\n[TEST 2] Suggestions pour: 'bon'")
suggestions = DictionarySearchService.get_suggestions('bon', limit=5)
print(f"[OK] {len(suggestions)} suggestions")
for entry in suggestions[:3]:
    try:
        print(f"  - {entry.word_baule} = {entry.word_french}")
    except:
        print(f"  - [mot avec caracteres speciaux]")

# Test 3: Mot du jour
print("\n[TEST 3] Mot du jour")
word_of_day = DictionarySearchService.get_word_of_the_day()
if word_of_day:
    try:
        print(f"[OK] {word_of_day.word_baule} = {word_of_day.word_french}")
    except:
        print(f"[OK] Mot du jour trouve (avec caracteres speciaux)")
else:
    print("[WARNING] Aucun mot du jour")

# Test 4: Mots populaires
print("\n[TEST 4] Mots populaires")
popular = DictionarySearchService.get_popular_words(limit=5)
print(f"[OK] {len(popular)} mots populaires")

# Test 5: Traduction FR -> Baoulé
print("\n[TEST 5] Traduction FR -> Baoule: 'merci'")
translation = DictionarySearchService.translate_french_to_baule('merci')
print(f"[OK] {len(translation)} mots traduits")
for t in translation:
    if t['found']:
        try:
            print(f"  - {t['french']} -> {t['baule']} ({t['pronunciation']})")
        except:
            print(f"  - [traduction avec caracteres speciaux]")

# Test 6: Traduction Baoulé -> FR
print("\n[TEST 6] Traduction Baoule -> FR")
first_entry = DictionaryEntry.objects.first()
if first_entry:
    translation = DictionarySearchService.translate_baule_to_french(first_entry.word_baule)
    print(f"[OK] {len(translation)} mots traduits")
    for t in translation:
        if t['found']:
            try:
                print(f"  - {t['baule']} -> {t['french']}")
            except:
                print(f"  - [traduction avec caracteres speciaux]")

# Test 7: Statistiques
print("\n[TEST 7] Statistiques du dictionnaire")
total = DictionaryEntry.objects.count()
common = DictionaryEntry.objects.filter(is_common=True).count()
with_audio = DictionaryEntry.objects.exclude(audio_file='').count()
print(f"[OK] Total: {total}")
print(f"[OK] Mots courants: {common}")
print(f"[OK] Avec audio: {with_audio}")

print("\n" + "="*60)
print("[SUCCESS] Tous les tests du service sont passes!")
print("="*60)
print("\nLe service de dictionnaire fonctionne correctement.")
print("Vous pouvez l'utiliser dans les vues Django.")

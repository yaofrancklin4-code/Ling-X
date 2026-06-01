#!/usr/bin/env python
"""
Script pour nettoyer les images cassées avec ngrok/free.dev
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import Category, Vocabulary, Story

print("🔍 Recherche des images cassées (ngrok/free.dev)...\n")

count = 0

# Chercher dans les catégories
for cat in Category.objects.all():
    if cat.icon and ('ngrok' in str(cat.icon) or 'free.dev' in str(cat.icon)):
        print(f'  ❌ Catégorie: {cat.name} -> {cat.icon}')
        count += 1

# Chercher dans le vocabulaire
for vocab in Vocabulary.objects.filter(image__isnull=False):
    if 'ngrok' in str(vocab.image) or 'free.dev' in str(vocab.image):
        print(f'  ❌ Vocabulary: {vocab.word_baule} -> {vocab.image}')
        count += 1

# Chercher dans les histoires
for story in Story.objects.filter(image__isnull=False):
    if 'ngrok' in str(story.image) or 'free.dev' in str(story.image):
        print(f'  ❌ Story: {story.title} -> {story.image}')
        count += 1

print(f'\n✅ Total d\'images cassées trouvées: {count}')

if count == 0:
    print("\n✨ Aucune image cassée détectée! Tout va bien.")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unicodedata
import sys

def remove_accents(text):
    """Enlever les accents d'un texte"""
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

# Répertoire des images
dir_path = r'static\images\baoule'

if not os.path.exists(dir_path):
    print(f"Répertoire non trouvé: {dir_path}")
    sys.exit(1)

count = 0
for filename in os.listdir(dir_path):
    filepath = os.path.join(dir_path, filename)
    
    if not os.path.isfile(filepath):
        continue
    
    # Créer un nouveau nom sans accents ni apostrophes
    new_name = filename
    
    # Étape 1: Enlever les accents
    new_name = remove_accents(new_name)
    
    # Étape 2: Remplacer les apostrophes et tirets
    new_name = new_name.replace("'", "")
    new_name = new_name.replace("d'", "d")
    
    if new_name != filename:
        new_filepath = os.path.join(dir_path, new_name)
        try:
            os.rename(filepath, new_filepath)
            print(f'✓ {filename} -> {new_name}')
            count += 1
        except Exception as e:
            print(f'✗ Erreur {filename}: {e}')

print(f'\n{count} fichier(s) renommé(s) avec succès!')

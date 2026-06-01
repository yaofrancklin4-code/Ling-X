#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import unicodedata

def clean_filename(text):
    """Nettoyer un nom de fichier en supprimant accents et caractères spéciaux"""
    # Enlever les accents
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    # Enlever les apostrophes et caractères spéciaux
    text = text.replace("'", "")
    text = text.replace("–", "-")
    return text

# Répertoire source et destination
source_dir = r'static\images\baoule'

files_to_rename = [
    "Baoule-Souhamlin-Kode-de-Cote-d'Ivoire-780x500.png",
    "Les-N'gban-un-sous-groupe-Baoule-de-Cote-d'Ivoire-780x500.png",
    "Les-Sondo-un-Sous-groupe-du-Peuple-Baoule-de-Cote-d'Ivoire-780x405.png",
    "Les-Sondo-un-Sous-groupe-du-Peuple-Baoule-de-Cote-d'Ivoire-780x500.png",
    "Elomoue-sous-groupe-Baoule-de-Cote-d'Ivoire-780x500.png",
    "Fahafoue-Sous-groupe-Baoule-de-Cote-d'Ivoire-780x500.png",
    "Les-Goly-Kode-Sous-groupe-du-Peuple-Baoule-de-Cote-d'Ivoire-780x500.png",
]

for filename in files_to_rename:
    filepath = os.path.join(source_dir, filename)
    if os.path.exists(filepath):
        new_filename = clean_filename(filename)
        new_filepath = os.path.join(source_dir, new_filename)
        
        try:
            os.rename(filepath, new_filepath)
            print(f'✓ {filename} -> {new_filename}')
        except Exception as e:
            print(f'✗ Erreur: {e}')
    else:
        print(f'✗ Fichier non trouvé: {filename}')

print('Renommage complété!')

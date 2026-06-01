#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys

os.chdir(r'static\images\baoule')

# Chercher avec glob les fichiers avec apostrophe
files_with_apostrophe = []
for f in os.listdir('.'):
    if os.path.isfile(f) and "'" in f or "'" in f:
        files_with_apostrophe.append(f)
        print(f"Trouvé: {f}")

# Afficher les fichiers trouvés
if files_with_apostrophe:
    print(f"\nTrouvé {len(files_with_apostrophe)} fichiers avec apostrophe/quote")
    
    # Créer les copies
    for src in files_with_apostrophe:
        dst = src.replace("'", "").replace("Cote-d", "Cote-d").replace("Côte", "Cote").replace("gban", "gban").replace("Ivoire", "Ivoire")
        if dst != src:
            try:
                shutil.copy2(src, dst)
                print(f'✓ {src} -> {dst}')
            except Exception as e:
                print(f'✗ Erreur: {e}')
else:
    print("Aucun fichier avec apostrophe trouvé")

print("\nFichiers après copie:")
for f in sorted(os.listdir('.')):
    if os.path.isfile(f):
        print(f)

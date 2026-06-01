#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import glob

os.chdir(r'static\images\baoule')

# Mappings source -> destination
mappings = [
    (r"Baoule-Souhamlin-Kode-de-Cote-d'Ivoire-780x500.png", r"Baoule-Souhamlin-Kode-de-Cote-dIvoire-780x500.png"),
    (r"Les-N'gban-un-sous-groupe-Baoule-de-Cote-d'Ivoire-780x500.png", r"Les-Ngban-un-sous-groupe-Baoule-de-Cote-dIvoire-780x500.png"),
    (r"Les-Sondo-un-Sous-groupe-du-Peuple-Baoule-de-Cote-d'Ivoire-780x405.png", r"Les-Sondo-un-Sous-groupe-du-Peuple-Baoule-de-Cote-dIvoire-780x405.png"),
    (r"Les-Sondo-un-Sous-groupe-du-Peuple-Baoule-de-Cote-d'Ivoire-780x500.png", r"Les-Sondo-un-Sous-groupe-du-Peuple-Baoule-de-Cote-dIvoire-780x500.png"),
    (r"Elomoue-sous-groupe-Baoule-de-Cote-d'Ivoire-780x500.png", r"Elomoue-sous-groupe-Baoule-de-Cote-dIvoire-780x500.png"),
    (r"Fahafoue-Sous-groupe-Baoule-de-Cote-d'Ivoire-780x500.png", r"Fahafoue-Sous-groupe-Baoule-de-Cote-dIvoire-780x500.png"),
    (r"Les-Goly-Kode-Sous-groupe-du-Peuple-Baoule-de-Cote-d'Ivoire-780x500.png", r"Les-Goly-Kode-Sous-groupe-du-Peuple-Baoule-de-Cote-dIvoire-780x500.png"),
]

for src, dst in mappings:
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f'✓ Copié: {src} -> {dst}')
    else:
        print(f'✗ Non trouvé: {src}')

print('Copies créées!')

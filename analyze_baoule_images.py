#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse prudente de baoule.ci pour trouver les images réelles
Étape 0 : Extraire les URLs des images du HTML
"""

import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

print("""
════════════════════════════════════════════════════════════
  🔍 ANALYSE DE BAOULE.CI
════════════════════════════════════════════════════════════
""")

try:
    # Télécharger le HTML de la page d'accueil
    print("\n[1/3] Téléchargement du HTML...")
    response = requests.get(
        'https://baoule.ci/',
        timeout=15,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    )
    response.raise_for_status()
    print(f"    ✅ OK ({len(response.content)} bytes)")
    
    # Parser le HTML
    print("\n[2/3] Analyse du HTML...")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trouver toutes les images
    print("\n[3/3] Extraction des images...")
    images = []
    
    # Chercher les images dans les attributs src et data-src
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src and src.startswith('http'):
            alt = img.get('alt', 'Sans titre')
            images.append({
                "url": src,
                "alt": alt,
                "filename": src.split('/')[-1][:30]
            })
    
    # Afficher les résultats
    print(f"\n    📊 Total images trouvées: {len(images)}\n")
    
    if images:
        print("    URLs des images (premières 10) :")
        for i, img in enumerate(images[:10], 1):
            print(f"    {i}. {img['filename']}")
            print(f"       URL: {img['url'][:70]}...")
            print(f"       ALT: {img['alt'][:50]}")
            print()
    
    # Sauvegarder pour analyse
    output_file = Path(__file__).parent / "images_found_baoule.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(images, f, indent=2, ensure_ascii=False)
    
    print(f"    📄 Sauvegardé dans: {output_file.name}")
    print(f"    ✅ Analyse complète - {len(images)} images trouvées")
    
except requests.Timeout:
    print("    ❌ TIMEOUT - Le site met trop de temps à répondre")
except requests.RequestException as e:
    print(f"    ❌ ERREUR RÉSEAU: {str(e)[:80]}")
except Exception as e:
    print(f"    ❌ ERREUR: {str(e)[:80]}")

print("""
════════════════════════════════════════════════════════════
""")

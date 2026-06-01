#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extraction SIMPLE des URLs d'images de baoule.ci
Sans dépendances externes (pas de beautifulsoup)
"""

import requests
import re
from pathlib import Path
import json

print("""
════════════════════════════════════════════════════════════
  🔍 EXTRACTION - baoule.ci
════════════════════════════════════════════════════════════
""")

try:
    print("\n[1/2] Téléchargement du HTML...")
    response = requests.get(
        'https://baoule.ci/',
        timeout=15,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    )
    response.raise_for_status()
    html = response.text
    print(f"    ✅ {len(html)} caractères reçus")
    
    print("\n[2/2] Recherche des URLs d'images...")
    
    # Chercher tous les URLs d'images (src, data-src, srcset)
    patterns = [
        r'src=["\']([^"\']*\.(?:jpg|jpeg|png|gif|webp))',  # src
        r'data-src=["\']([^"\']*\.(?:jpg|jpeg|png|gif|webp))',  # data-src (lazy loading)
        r'(?:http|https)://[^"\'\s<>]+\.(?:jpg|jpeg|png|gif|webp)'  # URLs directes
    ]
    
    images_urls = set()
    for pattern in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        for match in matches:
            if match.startswith('http'):
                images_urls.add(match)
            else:
                # URL relative - construire l'URL complète
                if match.startswith('/'):
                    images_urls.add(f"https://baoule.ci{match}")
                else:
                    images_urls.add(f"https://baoule.ci/{match}")
    
    # Filtrer les URLs
    images_list = []
    for url in sorted(images_urls):
        # Ignorer les petites images (logos, icons)
        if any(skip in url.lower() for skip in ['/icons/', '/logo', '/favicon']):
            continue
        # Garder seulement les images intéressantes
        if 'baoule' in url.lower() or 'wp-content' in url.lower() or 'unsplash' in url.lower():
            images_list.append(url)
    
    print(f"\n    📊 {len(images_list)} images trouvées (filtrées)\n")
    
    if images_list:
        print("    Premières images identifiées :\n")
        for i, url in enumerate(images_list[:10], 1):
            filename = url.split('/')[-1]
            print(f"    {i}. {filename[:40]}")
            print(f"       {url[:80]}...")
            print()
    
    # Sauvegarder la liste
    output_file = Path(__file__).parent / "baoule_images_urls.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(images_list),
            "images": images_list
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n    📄 Sauvegardé: {output_file.name}")
    print(f"\n    ✅ ÉTAPE 1 COMPLÈTE")
    print(f"    📊 {len(images_list)} images à analyser")
    
except Exception as e:
    print(f"\n    ❌ ERREUR: {str(e)}")

print("""
════════════════════════════════════════════════════════════
""")

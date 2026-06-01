#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Téléchargement PRUDENT des images de baoule.ci
Étape 1 : Télécharger SEULEMENT les images principales de la page d'accueil
Maximum : 5 images
"""

import os
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
import json
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).resolve().parent
STATIC_BASE = BASE_DIR / "static" / "images"
CULTURE_DIR = STATIC_BASE / "culture"
BANNER_DIR = STATIC_BASE / "banner"
LEARNING_DIR = STATIC_BASE / "learning"

# Créer les dossiers
for directory in [CULTURE_DIR, BANNER_DIR, LEARNING_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# URLs des images PRINCIPALES de baoule.ci (page d'accueil seulement)
images_to_download = [
    {
        "nom": "baoule_culture",
        "url": "https://baoule.ci/wp-content/uploads/2018/05/baoule_culture.jpg",
        "dest": CULTURE_DIR,
        "max_size_mb": 2,
        "description": "La culture Baoulé"
    },
    {
        "nom": "villages_emblematiques",
        "url": "https://baoule.ci/wp-content/uploads/2024/01/villages_baoule.jpg",
        "dest": CULTURE_DIR,
        "max_size_mb": 2,
        "description": "Villes et villages emblématiques"
    },
    {
        "nom": "fetes_rituels",
        "url": "https://baoule.ci/wp-content/uploads/2024/01/fetes_baoule.jpg",
        "dest": BANNER_DIR,
        "max_size_mb": 2,
        "description": "Fêtes et rituels"
    }
]

print("""
════════════════════════════════════════════════════════════
  🔍 TÉLÉCHARGEMENT PRUDENT - baoule.ci (Étape 1)
════════════════════════════════════════════════════════════
  
  ⚠️  Mode: SÉCURISÉ
  🎯 Cible: Page d'accueil uniquement
  📊 Max images: 3
  
════════════════════════════════════════════════════════════
""")

# Session avec timeout
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

# Rapport de téléchargement
rapport = {
    "date": datetime.now().isoformat(),
    "total": len(images_to_download),
    "succes": 0,
    "erreurs": 0,
    "images": []
}

for i, img_info in enumerate(images_to_download, 1):
    print(f"\n[{i}/{len(images_to_download)}] {img_info['nom']}")
    print(f"    URL: {img_info['url']}")
    
    try:
        # Télécharger avec timeout strict
        response = session.get(
            img_info['url'],
            timeout=10,
            stream=True,
            verify=True
        )
        response.raise_for_status()
        
        # Vérifier la taille avant traitement
        content_length = int(response.headers.get('content-length', 0))
        max_bytes = img_info['max_size_mb'] * 1024 * 1024
        
        if content_length > max_bytes:
            print(f"    ❌ TROP VOLUMINEUX ({content_length / 1024 / 1024:.1f} MB > {img_info['max_size_mb']} MB)")
            rapport["erreurs"] += 1
            rapport["images"].append({
                "nom": img_info['nom'],
                "status": "SKIP",
                "raison": "Fichier trop volumineux"
            })
            continue
        
        # Charger l'image
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        
        # Redimensionner si trop grande
        max_width = 1200
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"    📐 Redimensionnée: {max_width}x{new_height}px")
        
        # Sauvegarder
        filename = f"{img_info['nom']}.jpg"
        filepath = img_info['dest'] / filename
        
        img.save(filepath, quality=85, optimize=True)
        file_size = filepath.stat().st_size / 1024
        
        print(f"    ✅ Téléchargée: {file_size:.1f} KB")
        print(f"    📁 {filepath.relative_to(BASE_DIR)}")
        
        rapport["succes"] += 1
        rapport["images"].append({
            "nom": img_info['nom'],
            "status": "OK",
            "size_kb": file_size,
            "path": str(filepath.relative_to(BASE_DIR))
        })
        
    except requests.Timeout:
        print(f"    ❌ TIMEOUT (>10s)")
        rapport["erreurs"] += 1
        rapport["images"].append({
            "nom": img_info['nom'],
            "status": "ERROR",
            "raison": "Timeout"
        })
    except Exception as e:
        print(f"    ❌ ERREUR: {str(e)[:60]}")
        rapport["erreurs"] += 1
        rapport["images"].append({
            "nom": img_info['nom'],
            "status": "ERROR",
            "raison": str(e)[:100]
        })

# Sauvegarder le rapport
rapport_file = BASE_DIR / "rapport_baoule_etape1.json"
with open(rapport_file, 'w', encoding='utf-8') as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)

print(f"""
════════════════════════════════════════════════════════════
  📊 RÉSUMÉ
════════════════════════════════════════════════════════════
  
  ✅ Succès:  {rapport['succes']}
  ❌ Erreurs: {rapport['erreurs']}
  
  📄 Rapport: {rapport_file.name}
  
════════════════════════════════════════════════════════════
""")

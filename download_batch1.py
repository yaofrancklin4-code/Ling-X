#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Téléchargement SÉLECTIF des meilleures images de baoule.ci
Stratégie: Garder les 780x500, 780x478, 780x405 (résolutions principales)
Ignorer: 220x150, 270x270, 32x32, 192x192 (trop petites)
Limiter: 5 images max pour cette première vague
"""

import requests
import json
from pathlib import Path
from PIL import Image
from io import BytesIO
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).resolve().parent
STATIC_IMAGES = BASE_DIR / "static" / "images" / "baoule"
STATIC_IMAGES.mkdir(parents=True, exist_ok=True)

print("""
════════════════════════════════════════════════════════════
  ⬇️  TÉLÉCHARGEMENT SÉLECTIF (Batch 1/5)
════════════════════════════════════════════════════════════

  🎯 Stratégie: Meilleure qualité seulement
  🔍 Filtres: -780x500, -780x478, -780x405
  📊 Max: 5 images / vague
  
════════════════════════════════════════════════════════════
""")

# Charger les URLs trouvées
with open(BASE_DIR / "baoule_images_urls.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filtrer les images de bonne résolution (780+ pixels de large)
good_quality = [
    url for url in data["images"]
    if any(size in url for size in ['780x', '500x'])
    and all(small not in url for small in ['220x', '270x', '32x', '192x', 'cropped-Logo'])
]

# Limiter à 5 et exclure les doublons/variantes
selected = []
seen_keywords = set()

for url in good_quality[:10]:  # Checker les 10 premières
    # Extraire le nom descriptif
    filename = url.split('/')[-1]
    base_name = filename.split('-')[0]
    
    if base_name not in seen_keywords and len(selected) < 5:
        selected.append(url)
        seen_keywords.add(base_name)

print(f"\n📋 {len(selected)} images sélectionnées :\n")

# Session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
})

rapport = {
    "date": datetime.now().isoformat(),
    "batch": 1,
    "total_selected": len(selected),
    "success": 0,
    "failed": 0,
    "images": []
}

for i, url in enumerate(selected, 1):
    filename = url.split('/')[-1]
    print(f"[{i}/{len(selected)}] {filename}")
    
    try:
        # Télécharger
        response = session.get(url, timeout=10, stream=True)
        response.raise_for_status()
        
        # Charger l'image
        img = Image.open(BytesIO(response.content))
        
        # Redimensionner si trop grande (max 1200px de large)
        if img.width > 1200:
            ratio = 1200 / img.width
            new_height = int(img.height * ratio)
            img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
        
        # Sauvegarder
        filepath = STATIC_IMAGES / filename
        img.save(filepath, quality=85, optimize=True)
        size_kb = filepath.stat().st_size / 1024
        
        print(f"    ✅ {size_kb:.1f} KB - {img.width}x{img.height}px")
        
        rapport["success"] += 1
        rapport["images"].append({
            "filename": filename,
            "status": "OK",
            "size_kb": round(size_kb, 1),
            "dimensions": f"{img.width}x{img.height}"
        })
        
    except Exception as e:
        print(f"    ❌ {str(e)[:50]}")
        rapport["failed"] += 1
        rapport["images"].append({
            "filename": filename,
            "status": "FAILED",
            "error": str(e)[:50]
        })

# Sauvegarder le rapport
rapport_file = BASE_DIR / "rapport_batch1.json"
with open(rapport_file, 'w', encoding='utf-8') as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)

print(f"""
════════════════════════════════════════════════════════════
  ✅ BATCH 1 COMPLÉTÉ
════════════════════════════════════════════════════════════
  
  ✓ Succès:  {rapport['success']}/{len(selected)}
  ✗ Erreurs: {rapport['failed']}/{len(selected)}
  
  📁 Dossier: static/images/baoule/
  📄 Rapport: {rapport_file.name}
  
════════════════════════════════════════════════════════════
""")

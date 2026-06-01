#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Téléchargement stratégique BATCHES 2-5 (20 images)
Avec validation et redémarrage possible après erreurs
"""

import requests
import json
from pathlib import Path
from PIL import Image
from io import BytesIO
from datetime import datetime
import time

BASE_DIR = Path(__file__).resolve().parent
STATIC_IMAGES = BASE_DIR / "static" / "images" / "baoule"
STATIC_IMAGES.mkdir(parents=True, exist_ok=True)

print("""
╔══════════════════════════════════════════════════════════════╗
║         📥 TÉLÉCHARGEMENT BATCHES 2-5 (20 IMAGES)           ║
╚══════════════════════════════════════════════════════════════╝

🎯 Stratégie: 4 batches × 5 images = 20 au total
✅ Objectif: 100% de succès

""")

# Charger les URLs trouvées
with open(BASE_DIR / "baoule_images_urls.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# URLs déjà téléchargées (Batch 1)
already_downloaded = {
    "Pagne_Baoule2-780x405.png",
    "ashanti-empire-people-780x478.jpg",
    "femmes_baoules-780x500.png",
    "funerailles_baoule-780x405.jpg",
    "Conversation-en-Baoule-780x500.png"
}

# Filtrer: bonne qualité + pas déjà téléchargé + pas trop petit
quality_images = []
for url in data["images"]:
    filename = url.split('/')[-1]
    
    # Critères:
    # 1. Pas déjà téléchargé
    if filename in already_downloaded:
        continue
    
    # 2. Résolution décente (780+ ou 500+ pixels)
    if not any(size in url for size in ['780x', '500x', '600x']):
        continue
    
    # 3. Pas de miniature (exclure 220x, 270x, 32x, 192x)
    if any(small in url for small in ['220x', '270x', '32x', '192x', 'cropped-Logo']):
        continue
    
    quality_images.append((filename, url))

# Sélectionner 20 images
selected_20 = quality_images[:20]

print(f"📊 Images disponibles: {len(quality_images)}")
print(f"📌 Images sélectionnées: {len(selected_20)}\n")

# Diviser en 4 batches de 5
batches = {
    2: selected_20[0:5],
    3: selected_20[5:10],
    4: selected_20[10:15],
    5: selected_20[15:20]
}

# Session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
})

# Rapport global
rapport_global = {
    "date": datetime.now().isoformat(),
    "batches_total": 4,
    "images_total": 20,
    "batches": {}
}

# Télécharger chaque batch
for batch_num in sorted(batches.keys()):
    print(f"\n{'='*60}")
    print(f"  ⬇️  BATCH {batch_num} ({len(batches[batch_num])} images)")
    print(f"{'='*60}\n")
    
    batch_data = {
        "total": len(batches[batch_num]),
        "success": 0,
        "failed": 0,
        "images": []
    }
    
    for i, (filename, url) in enumerate(batches[batch_num], 1):
        print(f"[{i}/5] {filename[:45]:<45} ", end="", flush=True)
        
        try:
            # Télécharger avec timeout
            response = session.get(url, timeout=15, stream=True)
            response.raise_for_status()
            
            # Charger l'image
            img = Image.open(BytesIO(response.content))
            
            # Redimensionner si nécessaire
            if img.width > 1200:
                ratio = 1200 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((1200, new_height), Image.Resampling.LANCZOS)
            
            # Sauvegarder
            filepath = STATIC_IMAGES / filename
            img.save(filepath, quality=85, optimize=True)
            size_kb = filepath.stat().st_size / 1024
            
            print(f"✅ {size_kb:>7.1f} KB")
            
            batch_data["success"] += 1
            batch_data["images"].append({
                "filename": filename,
                "status": "OK",
                "size_kb": round(size_kb, 1),
                "dimensions": f"{img.width}x{img.height}"
            })
            
        except Exception as e:
            print(f"❌ {str(e)[:30]}")
            batch_data["failed"] += 1
            batch_data["images"].append({
                "filename": filename,
                "status": "FAILED",
                "error": str(e)[:50]
            })
        
        time.sleep(0.5)  # Délai entre téléchargements
    
    rapport_global["batches"][f"batch_{batch_num}"] = batch_data
    
    print(f"\n  ✅ {batch_data['success']}/5 succès | ❌ {batch_data['failed']}/5 erreurs")
    
    # Pause entre batches
    if batch_num < 5:
        print(f"  ⏳ Pause 2s avant Batch {batch_num + 1}...")
        time.sleep(2)

# Résumé final
total_success = sum(b["success"] for b in rapport_global["batches"].values())
total_failed = sum(b["failed"] for b in rapport_global["batches"].values())

print(f"""
╔══════════════════════════════════════════════════════════════╗
║                   🎉 RÉSUMÉ GLOBAL                          ║
╚══════════════════════════════════════════════════════════════╝

  📊 TOTAUX:
     ✅ Succès:  {total_success}/20
     ❌ Erreurs: {total_failed}/20
     📈 Taux:    {(total_success/20)*100:.0f}%

  📁 Dossier: static/images/baoule/
  
  ⏭️  PROCHAINE ÉTAPE: Intégration dans les templates
  
╚══════════════════════════════════════════════════════════════╝
""")

# Sauvegarder rapport
rapport_file = BASE_DIR / "rapport_batches_2to5.json"
with open(rapport_file, 'w', encoding='utf-8') as f:
    json.dump(rapport_global, f, indent=2, ensure_ascii=False)

print(f"📄 Rapport sauvegardé: {rapport_file.name}")

# Sauvegarder aussi la liste des images pour l'intégration
images_list = []
for batch_num in sorted(batches.keys()):
    for filename, url in batches[batch_num]:
        images_list.append({
            "batch": batch_num,
            "filename": filename,
            "url": url
        })

images_file = BASE_DIR / "images_to_integrate.json"
with open(images_file, 'w', encoding='utf-8') as f:
    json.dump(images_list, f, indent=2, ensure_ascii=False)

print(f"📋 Liste intégration: {images_file.name}")

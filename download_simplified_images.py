#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Télécharger les 7 images problématiques depuis baoule.ci avec noms simplifiés
"""
import requests
import time
import json

# URLs directs des images depuis baoule.ci
image_urls = {
    "Baoule-Souhamlin-Kode-de-Cote-dIvoire-780x500.png": "https://baoule.ci/wp-content/uploads/2024/01/Baoulé-Souhamlin-Kôdè-de-Côte-d'Ivoire-780x500.png",
    "Les-Ngban-un-sous-groupe-Baoule-de-Cote-dIvoire-780x500.png": "https://baoule.ci/wp-content/uploads/2024/01/Les-N'gban-un-sous-groupe-Baoulé-de-Côte-d'Ivoire-780x500.png",
    "Les-Sondo-un-Sous-groupe-du-Peuple-Baoule-de-Cote-dIvoire-780x405.png": "https://baoule.ci/wp-content/uploads/2024/01/Les-Sondo-un-Sous-groupe-du-Peuple-Baoulé-de-Côte-d'Ivoire-780x405.png",
    "Les-Sondo-un-Sous-groupe-du-Peuple-Baoule-de-Cote-dIvoire-780x500.png": "https://baoule.ci/wp-content/uploads/2024/01/Les-Sondo-un-Sous-groupe-du-Peuple-Baoulé-de-Côte-d'Ivoire-780x500.png",
    "Elomoue-sous-groupe-Baoule-de-Cote-dIvoire-780x500.png": "https://baoule.ci/wp-content/uploads/2024/01/Elomoué-sous-groupe-Baoulé-de-Côte-d'Ivoire-780x500.png",
    "Fahafoue-Sous-groupe-Baoule-de-Cote-dIvoire-780x500.png": "https://baoule.ci/wp-content/uploads/2024/01/Fahafouè-Sous-groupe-Baoulé-de-Côte-d'Ivoire-780x500.png",
    "Les-Goly-Kode-Sous-groupe-du-Peuple-Baoule-de-Cote-dIvoire-780x500.png": "https://baoule.ci/wp-content/uploads/2024/01/Les-Gôly-Kôdê-Sous-groupe-du-Peuple-Baoulé-de-Côte-d'Ivoire-780x500.png",
}

results = {
    "total": len(image_urls),
    "downloaded": 0,
    "failed": 0,
    "files": []
}

for filename, url in image_urls.items():
    filepath = f"static/images/baoule/{filename}"
    try:
        print(f"Téléchargement: {filename}...")
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✓ {filename} ({len(response.content)/1024:.1f} KB)")
            results["downloaded"] += 1
            results["files"].append({"name": filename, "size": len(response.content), "status": "success"})
        else:
            print(f"✗ Erreur HTTP {response.status_code}: {filename}")
            results["failed"] += 1
            results["files"].append({"name": filename, "status": "http_error", "code": response.status_code})
    except Exception as e:
        print(f"✗ Erreur: {filename} - {e}")
        results["failed"] += 1
        results["files"].append({"name": filename, "status": "error", "error": str(e)})
    
    time.sleep(2)  # Pause 2 sec entre les téléchargements

print(f"\n=== Résumé ===")
print(f"Total: {results['total']}")
print(f"Téléchargés: {results['downloaded']}")
print(f"Échoués: {results['failed']}")

# Sauvegarder le rapport
with open('rapport_images_simplifiees.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nRapport sauvegardé: rapport_images_simplifiees.json")

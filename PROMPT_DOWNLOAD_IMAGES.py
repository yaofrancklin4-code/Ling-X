"""
PROMPT SIMPLE POUR TÉLÉCHARGER DES IMAGES BAOULÉ
==================================================

OBJECTIF:
Créer un script Python pour télécharger automatiquement des images culturelles Baoulé 
depuis des sites web spécialisés et les organiser dans le projet Django LingX.

SOURCES D'IMAGES PRIORITAIRES:
1. https://baoule.ci/ (site officiel de la culture Baoulé)
2. https://www.google.com/search?q=culture+baoule&tbm=isch
3. https://www.bing.com/images/search?q=baoule+cote+ivoire
4. Sites culturels ivoiriens et africains

CATÉGORIES D'IMAGES À TÉLÉCHARGER:
===================================

1. SALUTATIONS (5 images)
   - Personnes qui se saluent
   - Scènes sociales africaines
   - Rencontres traditionnelles
   → Dossier: static/images/categories/greetings/

2. FAMILLE (5 images)
   - Familles africaines
   - Parents et enfants
   - Réunions familiales
   → Dossier: static/images/categories/family/

3. NOURRITURE (5 images)
   - Plats ivoiriens (attiéké, foutou, alloco)
   - Cuisine traditionnelle
   - Marchés alimentaires
   → Dossier: static/images/categories/food/

4. PARTIES DU CORPS (3 images)
   - Illustrations éducatives
   - Enfants africains
   → Dossier: static/images/categories/body/

5. NOMBRES (3 images)
   - Écoles africaines
   - Tableaux scolaires
   - Apprentissage
   → Dossier: static/images/categories/numbers/

6. CULTURE BAOULÉ (10 images)
   - Tissus traditionnels
   - Artisanat (poterie, sculpture)
   - Masques Baoulé
   - Femmes en tenue traditionnelle
   - Cérémonies
   → Dossier: static/images/culture/

7. SYMBOLES ADINKRA (5 images)
   - Vrais symboles Akan
   - Motifs traditionnels
   - Tissus avec symboles
   → Dossier: static/images/adinkra/

8. VILLAGES (5 images)
   - Villages Baoulé
   - Architecture traditionnelle
   - Vie quotidienne
   → Dossier: static/images/backgrounds/

9. HISTOIRES ET CONTES (3 images)
   - Conteurs traditionnels
   - Anciens du village
   - Rassemblements
   → Dossier: static/images/culture/stories/

10. APPRENTISSAGE (5 images)
    - Étudiants africains
    - Salles de classe
    - Livres et cahiers
    → Dossier: static/images/learning/

CRITÈRES DE QUALITÉ:
====================
✓ Résolution minimum: 800x600 pixels
✓ Taille fichier: 50KB - 500KB
✓ Format: JPG ou PNG
✓ Images authentiques (pas d'IA)
✓ Pas de watermarks visibles
✓ Bonne luminosité
✓ Pertinence culturelle

STRUCTURE DU SCRIPT PYTHON:
============================

import requests
import os
from PIL import Image
from io import BytesIO
import time

# Configuration
DOWNLOAD_DELAY = 2  # secondes entre téléchargements
MAX_IMAGES_PER_CATEGORY = 5
MIN_SIZE_KB = 50
MAX_SIZE_KB = 500

# Dossiers de destination
FOLDERS = {
    'greetings': 'static/images/categories/greetings',
    'family': 'static/images/categories/family',
    'food': 'static/images/categories/food',
    'body': 'static/images/categories/body',
    'numbers': 'static/images/categories/numbers',
    'culture': 'static/images/culture',
    'adinkra': 'static/images/adinkra',
    'villages': 'static/images/backgrounds',
    'stories': 'static/images/culture/stories',
    'learning': 'static/images/learning'
}

# URLs d'images (à compléter avec vraies URLs)
IMAGE_SOURCES = {
    'greetings': [
        'URL_IMAGE_1',
        'URL_IMAGE_2',
        # ...
    ],
    'family': [
        'URL_IMAGE_1',
        'URL_IMAGE_2',
        # ...
    ],
    # ... autres catégories
}

def create_folders():
    '''Créer tous les dossiers nécessaires'''
    for folder in FOLDERS.values():
        os.makedirs(folder, exist_ok=True)
        print(f'✓ Dossier créé: {folder}')

def download_image(url, filepath):
    '''Télécharger une image depuis une URL'''
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Vérifier la taille
            size_kb = len(response.content) / 1024
            
            if MIN_SIZE_KB <= size_kb <= MAX_SIZE_KB:
                # Sauvegarder l'image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f'✓ Téléchargé: {filepath} ({size_kb:.1f}KB)')
                return True
            else:
                print(f'✗ Taille incorrecte: {size_kb:.1f}KB')
        else:
            print(f'✗ Erreur HTTP: {response.status_code}')
            
    except Exception as e:
        print(f'✗ Erreur: {str(e)[:50]}')
    
    return False

def download_category(category, urls):
    '''Télécharger toutes les images d'une catégorie'''
    print(f'\n=== CATÉGORIE: {category.upper()} ===')
    
    folder = FOLDERS[category]
    downloaded = 0
    
    for i, url in enumerate(urls[:MAX_IMAGES_PER_CATEGORY], 1):
        filename = f'{category}_{i}.jpg'
        filepath = os.path.join(folder, filename)
        
        if download_image(url, filepath):
            downloaded += 1
        
        time.sleep(DOWNLOAD_DELAY)
    
    print(f'✓ {downloaded}/{len(urls[:MAX_IMAGES_PER_CATEGORY])} images téléchargées')
    return downloaded

def main():
    print('=' * 60)
    print('TÉLÉCHARGEMENT D\'IMAGES BAOULÉ POUR LINGX')
    print('=' * 60)
    
    # Créer les dossiers
    create_folders()
    
    # Télécharger par catégorie
    total_downloaded = 0
    
    for category, urls in IMAGE_SOURCES.items():
        downloaded = download_category(category, urls)
        total_downloaded += downloaded
    
    print(f'\n' + '=' * 60)
    print(f'TERMINÉ: {total_downloaded} images téléchargées')
    print('=' * 60)

if __name__ == '__main__':
    main()

INSTRUCTIONS D'UTILISATION:
===========================

1. Compléter IMAGE_SOURCES avec vraies URLs d'images Baoulé
2. Installer les dépendances:
   pip install requests pillow

3. Exécuter le script:
   python download_baoule_images.py

4. Vérifier les images téléchargées dans les dossiers

5. Intégrer dans Django:
   - Les images sont déjà dans les bons dossiers
   - Utiliser {% static 'images/...' %} dans les templates

SITES RECOMMANDÉS POUR TROUVER DES URLS:
=========================================

1. Site officiel Baoulé:
   https://baoule.ci/
   
2. Google Images (clic droit > Copier l'adresse de l'image):
   https://www.google.com/search?q=culture+baoule&tbm=isch
   
3. Unsplash (images libres):
   https://unsplash.com/s/photos/ivory-coast
   
4. Pexels (images libres):
   https://www.pexels.com/search/african%20culture/

5. Wikimedia Commons:
   https://commons.wikimedia.org/wiki/Category:Baoulé_people

EXEMPLE D'URLS À UTILISER:
===========================

IMAGE_SOURCES = {
    'greetings': [
        'https://images.unsplash.com/photo-1531384441138-2736e62e0919?w=800',
        'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=800',
        # ... ajouter plus d'URLs
    ],
    'family': [
        'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=800',
        # ... ajouter plus d'URLs
    ],
    # ... autres catégories
}

NOTES IMPORTANTES:
==================

✓ Télécharger progressivement (2-3 secondes entre images)
✓ Vérifier les droits d'utilisation des images
✓ Privilégier les images libres de droits
✓ Tester avec 2-3 images avant téléchargement massif
✓ Sauvegarder les URLs sources pour référence
✓ Renommer les images de façon cohérente
✓ Vérifier la qualité visuelle après téléchargement

RÉSULTAT ATTENDU:
=================

Après exécution du script, vous aurez:
- 50+ images culturelles Baoulé authentiques
- Organisées dans les bons dossiers
- Prêtes à être utilisées dans Django
- Nommées de façon cohérente
- Tailles optimisées pour le web

"""

print(__doc__)

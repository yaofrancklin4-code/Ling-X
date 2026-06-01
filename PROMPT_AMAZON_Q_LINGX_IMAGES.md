#  PROMPT AMAZON Q — TÉLÉCHARGEMENT D'IMAGES CULTURELLES BAOULÉ
## Projet: LingX — Application Django d'apprentissage de la langue Baoulé

---

##  CONTEXTE DU PROJET

Je travaille sur **LingX**, une application web Django éducative pour apprendre la langue **Baoulé** 
(Côte d'Ivoire) via la gamification.

**Stack technique :**
- Django 6.0.3 + SQLite
- Bootstrap 5 + Vanilla JS
- Django REST Framework

**Structure des dossiers d'images dans le projet :**
```
monprojet/
└── static/images/
    ├── categories/
    │   ├── greetings/       ← Salutations
    │   ├── family/          ← Famille
    │   ├── food/            ← Nourriture
    │   ├── body/            ← Parties du corps
    │   └── numbers/         ← Nombres
    ├── culture/
    │   ├── stories/         ← Contes et histoires
    │   ├── masks/           ← Masques traditionnels  ← NOUVEAU
    │   ├── traditions/      ← Traditions et cérémonies ← NOUVEAU
    │   └── fields/          ← Champs et agriculture  ← NOUVEAU
    ├── adinkra/             ← Symboles Adinkra/Akan
    ├── backgrounds/         ← Villages et paysages
    ├── learning/            ← Apprentissage
    └── baoule/              ← Images générales Baoulé
```

---

##  MISSION

Crée un script Python complet et fonctionnel `download_baoule_images.py` qui télécharge 
automatiquement des images culturelles Baoulé authentiques depuis le web et les organise 
dans la structure Django ci-dessus.

---

## ⚠️ RÈGLES ABSOLUES — À RESPECTER IMPÉRATIVEMENT

```
❌ INTERDIT - Images générées par IA
❌ INTERDIT - Images de personnes blanches ou non-africaines
❌ INTERDIT - Images floues, de mauvaise qualité ou avec watermarks
❌ INTERDIT - Images sans rapport avec la culture Baoulé / Ivoirienne / Africaine

✅ OBLIGATOIRE - Personnes noires (femmes noires, hommes noirs, enfants noirs)
✅ OBLIGATOIRE - Contexte culturel africain / ivoirien / Baoulé authentique
✅ OBLIGATOIRE - Images du web réelles (photos authentiques)
✅ OBLIGATOIRE - Masques Baoulé traditionnels authentiques
✅ OBLIGATOIRE - Tissus, artisanat, cérémonies, champs, villages Baoulé
```

---

##  CATÉGORIES ET CONTENU EXACT DES IMAGES

### 1. SALUTATIONS — `static/images/categories/greetings/` (5 images)
- Hommes et femmes noirs qui se saluent (poignée de mains, salut traditionnel)
- Groupes de personnes africaines qui se rencontrent
- Scènes de marché ivoirien avec interactions sociales
- Personnes en tenue traditionnelle Baoulé se saluant

### 2. FAMILLE — `static/images/categories/family/` (5 images)
- Familles africaines noires (parents + enfants)
- Femmes noires avec leurs enfants en Côte d'Ivoire
- Réunions familiales africaines traditionnelles
- Grands-parents africains avec petits-enfants
- Familles Baoulé en tenue traditionnelle

### 3. NOURRITURE — `static/images/categories/food/` (5 images)
- Attiéké (plat ivoirien typique) servi dans une assiette
- Foutou banane avec sauce ivoirienne
- Alloco (bananes plantain frites)
- Femmes noires préparant des repas traditionnels ivoiriens
- Marché alimentaire ivoirien avec fruits et légumes tropicaux

### 4. PARTIES DU CORPS — `static/images/categories/body/` (3 images)
- Enfants africains noirs souriants (visage, bras, mains visibles)
- Femme noire africaine (portrait éducatif propre)
- Illustration éducative avec enfant noir africain

### 5. NOMBRES — `static/images/categories/numbers/` (3 images)
- Enfants africains noirs dans une salle de classe
- Tableau scolaire avec chiffres dans une école africaine
- Enfants ivoiriens qui apprennent à compter

### 6. MASQUES BAOULÉ — `static/images/culture/masks/` (6 images) ← IMPORTANT
- Masques Baoulé traditionnels authentiques (bois sculpté)
- Masque Goli Baoulé (masque de cérémonie rond)
- Masque portrait Baoulé (visage humain stylisé)
- Masque animal Baoulé (buffle, bélier)
- Danseur portant un masque Baoulé lors d'une cérémonie
- Collection de masques Baoulé dans un musée ou village

### 7. TRADITIONS ET CÉRÉMONIES — `static/images/culture/traditions/` (5 images)
- Cérémonie traditionnelle Baoulé avec costumes
- Femmes Baoulé en tenue traditionnelle colorée (pagne, bijoux)
- Hommes Baoulé en tenue de cérémonie
- Danse traditionnelle Baoulé
- Rituel ou fête culturelle Baoulé

### 8. CHAMPS ET AGRICULTURE — `static/images/culture/fields/` (4 images) ← NOUVEAU
- Champs de culture en Côte d'Ivoire (igname, manioc, maïs)
- Femmes noires travaillant aux champs en Côte d'Ivoire
- Plantation de cacao ivoirienne (culture importante des Baoulé)
- Agriculteur africain dans ses champs avec outils traditionnels

### 9. ARTISANAT BAOULÉ — `static/images/culture/` (5 images)
- Sculpture sur bois Baoulé (statuettes, objets rituels)
- Tisserands Baoulé travaillant sur des métiers à tisser
- Potières africaines façonnant de l'argile
- Bijoux traditionnels Baoulé (or, bronze)
- Tissus Kente ou Baoulé avec motifs géométriques colorés

### 10. SYMBOLES ADINKRA — `static/images/adinkra/` (5 images)
- Symboles Adinkra/Akan gravés sur tissu ou bois
- Tissu avec motifs Adinkra imprimés (authentique)
- Symbole Sankofa (oiseau symbolique Akan)
- Motifs Adinkra peints sur mur ou poterie
- Bijou ou objet avec symboles Akan gravés

### 11. VILLAGES BAOULÉ — `static/images/backgrounds/` (5 images)
- Village Baoulé traditionnel avec cases en terre
- Cases africaines rondes avec toits de chaume en Côte d'Ivoire
- Rue d'un village ivoirien animée
- Puits ou point d'eau dans un village africain
- Vue panoramique d'un village Baoulé dans la forêt

### 12. CONTEURS ET HISTOIRES — `static/images/culture/stories/` (3 images)
- Vieux conteur africain entouré d'enfants la nuit (au feu)
- Ancêtre ou sage Baoulé qui parle à la communauté
- Rassemblement villageois autour d'un feu de camp africain

### 13. APPRENTISSAGE — `static/images/learning/` (5 images)
- Enfants africains noirs avec des livres et cahiers
- Salle de classe africaine avec élèves noirs attentifs
- Étudiant africain qui écrit sur un tableau
- Groupe d'enfants ivoiriens qui étudient ensemble
- Femme africaine qui enseigne à des enfants

---

##  SOURCES D'IMAGES À UTILISER (par ordre de priorité)

### SOURCE 1 — Wikimedia Commons (LIBRE DE DROITS, priorité absolue)
```
https://commons.wikimedia.org/wiki/Category:Baoulé_people
https://commons.wikimedia.org/wiki/Category:Masks_from_Ivory_Coast
https://commons.wikimedia.org/wiki/Category:Culture_of_Ivory_Coast
https://commons.wikimedia.org/wiki/Category:Adinkra_symbols
https://commons.wikimedia.org/wiki/Category:Kente_cloth
https://commons.wikimedia.org/wiki/Category:Ivory_Coast
```
→ Utiliser l'API Wikimedia pour récupérer les URLs directes des images

### SOURCE 2 — Site Officiel Baoulé
```
https://baoule.ci/
```
→ Scraper les images de ce site avec BeautifulSoup

### SOURCE 3 — Cultures.fr
```
https://cultures.fr/file/img/culture-des-baoule-1024x585.webp
https://cultures.fr/ (rechercher "Baoulé")
```

### SOURCE 4 — Pexels API (LIBRE DE DROITS)
```
https://www.pexels.com/api/
Mots-clés: "ivory coast", "west africa traditional", "african mask", "african woman traditional"
"ivorian food", "african village", "african children school", "adinkra"
```

### SOURCE 5 — Unsplash API (LIBRE DE DROITS)
```
https://unsplash.com/developers
Mots-clés: "ivory coast", "african culture", "african mask", "african woman"
"west africa", "african village", "african children"
```

### SOURCE 6 — Pinterest (scraping)
```
https://www.pinterest.com/search/pins/?q=culture+baoule+cote+ivoire
https://www.pinterest.com/search/pins/?q=masque+baoule
https://www.pinterest.com/search/pins/?q=femme+baoule+traditionnelle
https://www.pinterest.com/search/pins/?q=village+baoule
```

### SOURCE 7 — URLs Directes Connues (à utiliser en premier)
```python
DIRECT_URLS = {
    'masks': [
        'https://th.bing.com/th/id/R.4bd76ddde738733d78d92eb148d50193?rik=iWQecDy0y%2b4ogw&pid=ImgRaw&r=0',
        'https://th.bing.com/th/id/R.6708ccc7c099d33e48290a8592dace43?rik=IQPbF9JD4qYHOA&pid=ImgRaw&r=0',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Baule_mask_Louvre.jpg/800px-Baule_mask_Louvre.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Baule_mask_MET.jpg/800px-Baule_mask_MET.jpg',
    ],
    'culture': [
        'https://cultures.fr/file/img/culture-des-baoule-1024x585.webp',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Ivory_Coast_woman.jpg/800px-Ivory_Coast_woman.jpg',
    ]
}
```

---

##  SCRIPT PYTHON COMPLET À GÉNÉRER

```python
"""
download_baoule_images.py
Script de téléchargement d'images culturelles Baoulé pour LingX
"""

import requests
import os
import time
import json
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse
from PIL import Image
from io import BytesIO

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path('monprojet/static/images')  # Adapter selon ton projet
DOWNLOAD_DELAY = 2        # secondes entre téléchargements
MIN_SIZE_KB = 30
MAX_SIZE_KB = 2000        # 2MB max
MIN_WIDTH = 400
MIN_HEIGHT = 300
MAX_IMAGES_PER_CATEGORY = 6

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
}

# ============================================================
# DOSSIERS DE DESTINATION
# ============================================================

FOLDERS = {
    'greetings':   BASE_DIR / 'categories/greetings',
    'family':      BASE_DIR / 'categories/family',
    'food':        BASE_DIR / 'categories/food',
    'body':        BASE_DIR / 'categories/body',
    'numbers':     BASE_DIR / 'categories/numbers',
    'masks':       BASE_DIR / 'culture/masks',
    'traditions':  BASE_DIR / 'culture/traditions',
    'fields':      BASE_DIR / 'culture/fields',
    'culture':     BASE_DIR / 'culture',
    'adinkra':     BASE_DIR / 'adinkra',
    'villages':    BASE_DIR / 'backgrounds',
    'stories':     BASE_DIR / 'culture/stories',
    'learning':    BASE_DIR / 'learning',
    'baoule':      BASE_DIR / 'baoule',
}

# ============================================================
# URLS DIRECTES PAR CATÉGORIE
# (URLs vérifiées et authentiques — personnes noires, culture Baoulé)
# ============================================================

IMAGE_SOURCES = {

    'masks': [
        # Masques Baoulé — Wikimedia Commons (libre de droits)
        'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Baule_mask_Louvre.jpg/800px-Baule_mask_Louvre.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Baule-mask-1.jpg/600px-Baule-mask-1.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Masque_Goli.jpg/600px-Masque_Goli.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Baule_helmet_mask.jpg/600px-Baule_helmet_mask.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/IvoryCoastMask.jpg/600px-IvoryCoastMask.jpg',
        # URL directe depuis Bing/cultures.fr (fournie dans le prompt)
        'https://th.bing.com/th/id/R.4bd76ddde738733d78d92eb148d50193?rik=iWQecDy0y%2b4ogw&pid=ImgRaw&r=0',
    ],

    'culture': [
        # Femmes Baoulé en tenue traditionnelle
        'https://cultures.fr/file/img/culture-des-baoule-1024x585.webp',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Ivorian_woman_traditional.jpg/800px-Ivorian_woman_traditional.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Baule_weaver.jpg/800px-Baule_weaver.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Ivory_Coast_culture.jpg/800px-Ivory_Coast_culture.jpg',
        'https://th.bing.com/th/id/R.6708ccc7c099d33e48290a8592dace43?rik=IQPbF9JD4qYHOA&pid=ImgRaw&r=0',
    ],

    'traditions': [
        # Cérémonies et tenues traditionnelles Baoulé
        'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Ivory_Coast_ceremony.jpg/800px-Ivory_Coast_ceremony.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Baule_dance.jpg/800px-Baule_dance.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/African_traditional_dress_CI.jpg/800px-African_traditional_dress_CI.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Kente_ceremony.jpg/800px-Kente_ceremony.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Baule_costume.jpg/800px-Baule_costume.jpg',
    ],

    'fields': [
        # Champs et agriculture Côte d'Ivoire
        'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Cocoa_farmers_ivory_coast.jpg/800px-Cocoa_farmers_ivory_coast.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Ivory_Coast_farm.jpg/800px-Ivory_Coast_farm.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/African_woman_field.jpg/800px-African_woman_field.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Cassava_field_africa.jpg/800px-Cassava_field_africa.jpg',
    ],

    'greetings': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Ivorian_greeting.jpg/800px-Ivorian_greeting.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/African_market_greetings.jpg/800px-African_market_greetings.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/West_africa_greeting.jpg/800px-West_africa_greeting.jpg',
        'https://images.pexels.com/photos/8940936/pexels-photo-8940936.jpeg?w=800',
        'https://images.pexels.com/photos/5029859/pexels-photo-5029859.jpeg?w=800',
    ],

    'family': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Ivory_Coast_family.jpg/800px-Ivory_Coast_family.jpg',
        'https://images.pexels.com/photos/7649157/pexels-photo-7649157.jpeg?w=800',
        'https://images.pexels.com/photos/8363104/pexels-photo-8363104.jpeg?w=800',
        'https://images.pexels.com/photos/5622395/pexels-photo-5622395.jpeg?w=800',
        'https://images.pexels.com/photos/9037566/pexels-photo-9037566.jpeg?w=800',
    ],

    'food': [
        # Plats ivoiriens
        'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Attieke.jpg/800px-Attieke.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Foutou_banane.jpg/800px-Foutou_banane.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Alloco.jpg/800px-Alloco.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Ivorian_market_food.jpg/800px-Ivorian_market_food.jpg',
        'https://images.pexels.com/photos/5560763/pexels-photo-5560763.jpeg?w=800',
    ],

    'body': [
        'https://images.pexels.com/photos/8363172/pexels-photo-8363172.jpeg?w=800',
        'https://images.pexels.com/photos/8363049/pexels-photo-8363049.jpeg?w=800',
        'https://images.pexels.com/photos/7529390/pexels-photo-7529390.jpeg?w=800',
    ],

    'numbers': [
        'https://images.pexels.com/photos/8613089/pexels-photo-8613089.jpeg?w=800',
        'https://images.pexels.com/photos/8612927/pexels-photo-8612927.jpeg?w=800',
        'https://images.pexels.com/photos/5428836/pexels-photo-5428836.jpeg?w=800',
    ],

    'adinkra': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Adinkra_symbols.svg/800px-Adinkra_symbols.svg.png',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Adinkra_cloth.jpg/800px-Adinkra_cloth.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Sankofa_symbol.svg/600px-Sankofa_symbol.svg.png',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Kente_adinkra.jpg/800px-Kente_adinkra.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Adinkra_fabric.jpg/800px-Adinkra_fabric.jpg',
    ],

    'villages': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Village_cote_ivoire.jpg/800px-Village_cote_ivoire.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Baule_village.jpg/800px-Baule_village.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Traditional_african_huts.jpg/800px-Traditional_african_huts.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Ivory_Coast_village.jpg/800px-Ivory_Coast_village.jpg',
        'https://images.pexels.com/photos/3894378/pexels-photo-3894378.jpeg?w=800',
    ],

    'stories': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/African_storyteller.jpg/800px-African_storyteller.jpg',
        'https://images.pexels.com/photos/8613060/pexels-photo-8613060.jpeg?w=800',
        'https://images.pexels.com/photos/7529333/pexels-photo-7529333.jpeg?w=800',
    ],

    'learning': [
        'https://images.pexels.com/photos/8613089/pexels-photo-8613089.jpeg?w=800',
        'https://images.pexels.com/photos/5428836/pexels-photo-5428836.jpeg?w=800',
        'https://images.pexels.com/photos/8612991/pexels-photo-8612991.jpeg?w=800',
        'https://images.pexels.com/photos/8612927/pexels-photo-8612927.jpeg?w=800',
        'https://images.pexels.com/photos/7659564/pexels-photo-7659564.jpeg?w=800',
    ],
}
```

---

##  FONCTIONS SUPPLÉMENTAIRES À IMPLÉMENTER

Le script doit contenir les fonctions suivantes :

### `create_folders()` 
Créer tous les dossiers FOLDERS s'ils n'existent pas (os.makedirs avec exist_ok=True)

### `validate_image(content) -> bool`
Valider qu'une image respecte :
- Taille entre MIN_SIZE_KB et MAX_SIZE_KB
- Dimensions minimales MIN_WIDTH x MIN_HEIGHT
- Format valide (JPG, PNG, WEBP)
- Image non corrompue (ouvrir avec PIL sans erreur)

### `download_image(url, filepath) -> bool`
- Utiliser requests avec HEADERS et timeout=20
- Gérer les redirections (allow_redirects=True)
- Appeler validate_image avant de sauvegarder
- Convertir WEBP en JPG automatiquement avec PIL
- Gestion complète des erreurs (timeout, connexion, HTTP)

### `download_with_wikimedia_api(category_query, folder, count=5)`
- Utiliser l'API Wikimedia : `https://commons.wikimedia.org/w/api.php`
- Paramètres : action=query, list=search, gsrsearch="{query}", generator=images
- Récupérer les URLs directes des images de haute qualité
- Filtrer uniquement JPG et PNG

### `scrape_baoule_ci(folder)`
- Scraper https://baoule.ci/ avec BeautifulSoup
- Extraire toutes les balises `<img>` avec src
- Filtrer les images pertinentes (taille > 50KB)
- Télécharger dans le dossier `baoule/`

### `download_category(category, urls)`
- Itérer sur les URLs de la catégorie
- Nommer les fichiers : `{category}_01.jpg`, `{category}_02.jpg`, etc.
- Logger le résultat (✓ succès / ✗ échec)
- Respecter DOWNLOAD_DELAY entre chaque téléchargement

### `generate_report(results)`
- Créer un fichier `download_report.json` avec :
  - Nombre d'images téléchargées par catégorie
  - Liste des URLs sources
  - Erreurs rencontrées
  - Timestamp

### `main()`
- Afficher un header avec le nom du projet
- Appeler create_folders()
- D'abord essayer scrape_baoule_ci()
- Puis download_with_wikimedia_api() pour les masques et la culture
- Puis download_category() pour chaque catégorie avec IMAGE_SOURCES
- Appeler generate_report() à la fin
- Afficher statistiques finales

---

##  DÉPENDANCES REQUISES

```
requests>=2.28.0
Pillow>=9.0.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
```

Fichier `requirements_download.txt` à créer avec ces dépendances.

---

## ▶️ INSTRUCTIONS D'EXÉCUTION

```bash
# 1. Installer les dépendances
pip install requests Pillow beautifulsoup4 lxml

# 2. Placer le script à la racine du projet Django (où se trouve manage.py)
# monprojet/download_baoule_images.py

# 3. Exécuter
python download_baoule_images.py

# 4. Vérifier le rapport
cat download_report.json

# 5. Utiliser les images dans Django
# {% load static %}
# <img src="{% static 'images/culture/masks/masks_01.jpg' %}" alt="Masque Baoulé">
```

---

## ✅ RÉSULTAT ATTENDU

Après exécution :
- **60+ images** culturelles Baoulé authentiques téléchargées
- Toutes les images montrent des **personnes noires** et/ou du **patrimoine Baoulé**
- **Masques Baoulé** traditionnels (6 images minimum)
- **Champs et agriculture** ivoirienne (4 images)
- **Traditions et cérémonies** Baoulé (5 images)
- Organisées dans les **bons dossiers** Django
- Nommées **cohéremment** (`category_01.jpg`, `category_02.jpg`...)
- Fichier `download_report.json` généré avec le bilan complet
- Aucune image d'IA, aucune image de personne non-africaine

---

*Prompt optimisé pour Amazon Q — Projet LingX — Apprentissage Baoulé *

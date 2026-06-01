"""
download_baoule_images.py
Script de téléchargement d'images culturelles Baoulé pour LingX
"""

import requests
import os
import time
import json
from pathlib import Path
from PIL import Image
from io import BytesIO
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path('static/images')
DOWNLOAD_DELAY = 2
MIN_SIZE_KB = 30
MAX_SIZE_KB = 2000
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
}

# ============================================================
# URLS DIRECTES PAR CATÉGORIE
# ============================================================

IMAGE_SOURCES = {
    'masks': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Baule_mask_Louvre.jpg/800px-Baule_mask_Louvre.jpg',
        'https://images.unsplash.com/photo-1590012314607-cda9d9b699ae?w=800',
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
        'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800',
        'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800',
        'https://images.unsplash.com/photo-1610296669228-602fa827fc1f?w=800',
    ],

    'culture': [
        'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800',
        'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800',
        'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800',
        'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800',
        'https://images.unsplash.com/photo-1610296669228-602fa827fc1f?w=800',
    ],

    'traditions': [
        'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=800',
        'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800',
        'https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=800',
        'https://images.unsplash.com/photo-1531384370597-8590413be50a?w=800',
        'https://images.unsplash.com/photo-1531384441138-2736e62e0919?w=800',
    ],

    'fields': [
        'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800',
        'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
        'https://images.unsplash.com/photo-1588075592446-265fd1e6e76f?w=800',
        'https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=800',
    ],

    'greetings': [
        'https://images.unsplash.com/photo-1531384441138-2736e62e0919?w=800',
        'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=800',
        'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800',
        'https://images.unsplash.com/photo-1527525443983-6e60c75fff46?w=800',
        'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800',
    ],

    'family': [
        'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=800',
        'https://images.unsplash.com/photo-1489749798305-4fea3ae63d43?w=800',
        'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800',
        'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800',
        'https://images.unsplash.com/photo-1531384370597-8590413be50a?w=800',
    ],

    'food': [
        'https://images.unsplash.com/photo-1578632292335-df3abbb0d586?w=800',
        'https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=800',
        'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800',
        'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800',
        'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800',
    ],

    'body': [
        'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800',
        'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800',
        'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=800',
    ],

    'numbers': [
        'https://images.unsplash.com/photo-1484318571209-661cf29a69c3?w=800',
        'https://images.unsplash.com/photo-1497486751825-1233686d5d80?w=800',
        'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800',
    ],

    'adinkra': [
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
        'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800',
        'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800',
        'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800',
        'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800',
    ],

    'villages': [
        'https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=800',
        'https://images.unsplash.com/photo-1588075592446-265fd1e6e76f?w=800',
        'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800',
        'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
        'https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=700',
    ],

    'stories': [
        'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800',
        'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800',
        'https://images.unsplash.com/photo-1527525443983-6e60c75fff46?w=800',
    ],

    'learning': [
        'https://images.unsplash.com/photo-1484318571209-661cf29a69c3?w=800',
        'https://images.unsplash.com/photo-1497486751825-1233686d5d80?w=800',
        'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800',
        'https://images.unsplash.com/photo-1541692641319-981cc79ee10a?w=800',
        'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=800',
    ],
}

# ============================================================
# FONCTIONS
# ============================================================

def create_folders():
    """Créer tous les dossiers nécessaires"""
    print('\n=== CREATION DES DOSSIERS ===')
    for name, folder in FOLDERS.items():
        folder.mkdir(parents=True, exist_ok=True)
        print(f'OK Dossier: {folder}')

def validate_image(content):
    """Valider qu'une image respecte les critères"""
    try:
        size_kb = len(content) / 1024
        
        if size_kb < MIN_SIZE_KB or size_kb > MAX_SIZE_KB:
            return False, f'Taille incorrecte: {size_kb:.1f}KB'
        
        img = Image.open(BytesIO(content))
        width, height = img.size
        
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            return False, f'Dimensions trop petites: {width}x{height}'
        
        return True, 'OK'
        
    except Exception as e:
        return False, f'Erreur validation: {str(e)[:30]}'

def download_image(url, filepath):
    """Télécharger une image depuis une URL"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        
        if response.status_code == 200:
            valid, msg = validate_image(response.content)
            
            if valid:
                # Convertir WEBP en JPG si nécessaire
                img = Image.open(BytesIO(response.content))
                
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                img.save(filepath, 'JPEG', quality=85)
                
                size_kb = filepath.stat().st_size / 1024
                return True, f'OK ({size_kb:.1f}KB)'
            else:
                return False, msg
        else:
            return False, f'HTTP {response.status_code}'
            
    except Exception as e:
        return False, f'Erreur: {str(e)[:30]}'

def download_category(category, urls):
    """Télécharger toutes les images d'une catégorie"""
    print(f'\n=== CATEGORIE: {category.upper()} ===')
    
    folder = FOLDERS[category]
    downloaded = 0
    results = []
    
    for i, url in enumerate(urls[:MAX_IMAGES_PER_CATEGORY], 1):
        filename = f'{category}_{i:02d}.jpg'
        filepath = folder / filename
        
        print(f'[{i}/{len(urls[:MAX_IMAGES_PER_CATEGORY])}] {filename}...', end=' ')
        
        success, msg = download_image(url, filepath)
        
        if success:
            downloaded += 1
            print(msg)
            results.append({'file': filename, 'url': url, 'status': 'success'})
        else:
            print(f'ECHEC ({msg})')
            results.append({'file': filename, 'url': url, 'status': 'failed', 'error': msg})
        
        time.sleep(DOWNLOAD_DELAY)
    
    print(f'OK {downloaded}/{len(urls[:MAX_IMAGES_PER_CATEGORY])} images telechargees')
    return downloaded, results

def generate_report(all_results):
    """Générer un rapport JSON"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_downloaded': sum(r['downloaded'] for r in all_results.values()),
        'categories': all_results
    }
    
    with open('download_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print('\nRapport sauvegarde: download_report.json')

def main():
    print('=' * 60)
    print('TELECHARGEMENT D\'IMAGES BAOULE POUR LINGX')
    print('=' * 60)
    
    create_folders()
    
    all_results = {}
    total_downloaded = 0
    
    for category, urls in IMAGE_SOURCES.items():
        downloaded, results = download_category(category, urls)
        all_results[category] = {
            'downloaded': downloaded,
            'total': len(urls[:MAX_IMAGES_PER_CATEGORY]),
            'images': results
        }
        total_downloaded += downloaded
    
    print('\n' + '=' * 60)
    print(f'TERMINE: {total_downloaded} images telechargees')
    print('=' * 60)
    
    generate_report(all_results)

if __name__ == '__main__':
    main()

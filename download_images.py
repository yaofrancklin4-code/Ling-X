import requests
import os
import time
from urllib.parse import quote

# Configuration
DOWNLOAD_DIR = 'static/images/downloads'
MAX_SIZE_MB = 5
DELAY_SECONDS = 2
MAX_PER_BATCH = 5

# Termes de recherche
search_terms = [
    'baoule culture cote ivoire',
    'baoule village tradition',
    'baoule famille africaine',
    'baoule vetements traditionnels',
    'baoule artisanat art',
    'baoule nourriture cuisine',
    'baoule symboles adinkra',
    'baoule apprentissage ecole',
    'baoule paysage nature',
    'baoule ceremonie tradition'
]

def get_bing_images(query, count=5):
    """Recuperer les URLs d'images depuis Bing"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    search_url = f'https://www.bing.com/images/search?q={quote(query)}&form=HDRSC3&first=1'
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Extraire les URLs d'images de maniere simple
            content = response.text
            urls = []
            
            # Chercher les patterns d'URL d'images
            import re
            pattern = r'murl&quot;:&quot;(https?://[^&quot;]+\.(?:jpg|jpeg|png))'
            matches = re.findall(pattern, content)
            
            for url in matches[:count]:
                if url not in urls:
                    urls.append(url)
            
            return urls
    except Exception as e:
        print(f'Erreur recherche: {e}')
    
    return []

def download_image(url, filename):
    """Telecharger une image"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        
        if response.status_code == 200:
            # Verifier la taille
            size_mb = int(response.headers.get('content-length', 0)) / (1024 * 1024)
            
            if size_mb > MAX_SIZE_MB:
                print(f'  Trop lourd: {size_mb:.1f}MB')
                return False
            
            # Sauvegarder
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Verifier que c'est une vraie image
            file_size = os.path.getsize(filepath)
            if file_size < 5000:  # Moins de 5KB = probablement pas une vraie image
                os.remove(filepath)
                print(f'  Fichier trop petit: {file_size} bytes')
                return False
            
            print(f'  OK: {filename} ({file_size/1024:.1f}KB)')
            return True
            
    except Exception as e:
        print(f'  Erreur: {e}')
    
    return False

def main():
    print('=== TELECHARGEMENT PROGRESSIF D\'IMAGES BAOULE ===\n')
    
    # Creer le dossier s'il n'existe pas
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # Compter les images existantes
    existing = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith('baoule_')]
    counter = len(existing) + 1
    
    print(f'Images existantes: {len(existing)}')
    print(f'Prochain numero: baoule_{counter}.jpg\n')
    
    downloaded = 0
    total_attempts = 0
    
    for term in search_terms:
        if downloaded >= 25:  # Limite totale
            break
        
        print(f'\n--- Recherche: {term} ---')
        
        urls = get_bing_images(term, MAX_PER_BATCH)
        print(f'URLs trouvees: {len(urls)}')
        
        for url in urls:
            if downloaded >= 25:
                break
            
            total_attempts += 1
            filename = f'baoule_{counter}.jpg'
            
            print(f'\n[{total_attempts}] Telechargement: {filename}')
            
            if download_image(url, filename):
                downloaded += 1
                counter += 1
                time.sleep(DELAY_SECONDS)  # Pause entre telechargements
            else:
                time.sleep(1)
        
        # Pause entre recherches
        time.sleep(3)
    
    print(f'\n\n=== TERMINE ===')
    print(f'Images telechargees: {downloaded}')
    print(f'Tentatives totales: {total_attempts}')
    
    # Lister les images
    print(f'\n=== IMAGES DISPONIBLES ===')
    files = sorted([f for f in os.listdir(DOWNLOAD_DIR) if f.startswith('baoule_')])
    for i, f in enumerate(files, 1):
        size = os.path.getsize(os.path.join(DOWNLOAD_DIR, f)) / 1024
        print(f'{i}. {f} ({size:.1f}KB)')

if __name__ == '__main__':
    main()

import requests
import os
import time

DOWNLOAD_DIR = 'static/images/downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# URLs d'images libres de droits sur la culture africaine/ivoirienne
image_urls = [
    # Unsplash - Culture africaine
    'https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=800',  # Afrique village
    'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800',  # Tissus africains
    'https://images.unsplash.com/photo-1489749798305-4fea3ae63d43?w=800',  # Famille africaine
    'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?w=800',  # Enfants africains
    'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800',  # Artisanat
    'https://images.unsplash.com/photo-1590012314607-cda9d9b699ae?w=800',  # Masques africains
    'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800',  # Paysage africain
    'https://images.unsplash.com/photo-1484318571209-661cf29a69c3?w=800',  # Ecole enfants
    'https://images.unsplash.com/photo-1578632292335-df3abbb0d586?w=800',  # Nourriture africaine
    'https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=800',  # Vetements traditionnels
    'https://images.unsplash.com/photo-1588075592446-265fd1e6e76f?w=800',  # Village africain
    'https://images.unsplash.com/photo-1566140967404-b8b3932483f5?w=800',  # Nature Afrique
    'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800',  # Tissage
    'https://images.unsplash.com/photo-1610296669228-602fa827fc1f?w=800',  # Poterie
    'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800',  # Marche africain
    'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=800',  # Danse africaine
    'https://images.unsplash.com/photo-1568602471122-7832951cc4c5?w=800',  # Instruments musique
    'https://images.unsplash.com/photo-1541692641319-981cc79ee10a?w=800',  # Apprentissage
    'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800',  # Communaute
    'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800',  # Celebration
    'https://images.unsplash.com/photo-1609137144813-7d9921338f24?w=800',  # Tradition
    'https://images.unsplash.com/photo-1578632292335-df3abbb0d586?w=800',  # Cuisine
    'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800',  # Symboles
    'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800',  # Textile
    'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',  # Paysage
]

def download_image(url, filename):
    """Telecharger une image"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f'Telechargement: {filename}...', end=' ')
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            size = os.path.getsize(filepath) / 1024
            
            # Verifier taille minimale
            if size < 5:
                os.remove(filepath)
                print(f'SKIP (trop petit)')
                return False
            
            print(f'OK ({size:.1f}KB)')
            return True
        else:
            print(f'ERREUR ({response.status_code})')
            
    except Exception as e:
        print(f'ERREUR ({e})')
    
    return False

def main():
    print('=== TELECHARGEMENT IMAGES BAOULE ===\n')
    
    downloaded = 0
    counter = 1
    
    for i, url in enumerate(image_urls, 1):
        filename = f'baoule_{counter}.jpg'
        
        if download_image(url, filename):
            downloaded += 1
            counter += 1
        
        time.sleep(1)  # Pause entre telechargements
        
        # Pause plus longue tous les 5 telechargements
        if i % 5 == 0:
            print(f'\n--- Pause (5 images) ---\n')
            time.sleep(3)
    
    print(f'\n=== TERMINE ===')
    print(f'Images telechargees: {downloaded}/{len(image_urls)}')
    
    # Lister les images
    print(f'\n=== IMAGES DISPONIBLES ===')
    files = sorted([f for f in os.listdir(DOWNLOAD_DIR) if f.startswith('baoule_')])
    for i, f in enumerate(files, 1):
        size = os.path.getsize(os.path.join(DOWNLOAD_DIR, f)) / 1024
        print(f'{i}. {f} ({size:.1f}KB)')

if __name__ == '__main__':
    main()

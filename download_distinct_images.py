import requests
import os
import time

DOWNLOAD_DIR = 'static/images/baoule_real'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Images du site baoule.ci et sources culturelles ivoiriennes
images_sources = [
    # Salutations - personnes qui se saluent
    {'url': 'https://images.unsplash.com/photo-1531384441138-2736e62e0919?w=600', 'name': 'salutations_real.jpg', 'theme': 'salutations'},
    
    # Famille - vraie famille africaine
    {'url': 'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=600', 'name': 'famille_real.jpg', 'theme': 'famille'},
    
    # Nourriture - plats ivoiriens
    {'url': 'https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=600', 'name': 'nourriture_real.jpg', 'theme': 'nourriture'},
    
    # Corps - enfants africains
    {'url': 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=600', 'name': 'corps_real.jpg', 'theme': 'corps'},
    
    # Nombres - école africaine
    {'url': 'https://images.unsplash.com/photo-1497486751825-1233686d5d80?w=600', 'name': 'nombres_real.jpg', 'theme': 'nombres'},
    
    # Tissus - textiles africains
    {'url': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=600', 'name': 'tissus_real.jpg', 'theme': 'tissus'},
    
    # Artisanat - poterie/sculpture
    {'url': 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=600', 'name': 'artisanat_real.jpg', 'theme': 'artisanat'},
    
    # Femmes - femmes africaines
    {'url': 'https://images.unsplash.com/photo-1531384370597-8590413be50a?w=600', 'name': 'femmes_real.jpg', 'theme': 'femmes'},
    
    # Symboles Adinkra
    {'url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=600', 'name': 'adinkra_real.jpg', 'theme': 'adinkra'},
    
    # Histoires - conteur/ancien
    {'url': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=600', 'name': 'histoires_real.jpg', 'theme': 'histoires'},
    
    # Prénoms - portraits
    {'url': 'https://images.unsplash.com/photo-1531384441138-2736e62e0919?w=600', 'name': 'prenoms_real.jpg', 'theme': 'prenoms'},
    
    # Proverbes - sage/ancien
    {'url': 'https://images.unsplash.com/photo-1594744803329-e58b31de8bf5?w=600', 'name': 'proverbes_real.jpg', 'theme': 'proverbes'},
    
    # Audio - instruments
    {'url': 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600', 'name': 'audio_real.jpg', 'theme': 'audio'},
    
    # Jeux - enfants qui jouent
    {'url': 'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=600', 'name': 'jeux_real.jpg', 'theme': 'jeux'},
    
    # Badges - célébration
    {'url': 'https://images.unsplash.com/photo-1527525443983-6e60c75fff46?w=600', 'name': 'badges_real.jpg', 'theme': 'badges'},
    
    # Progression - étudiant
    {'url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=600', 'name': 'progression_real.jpg', 'theme': 'progression'},
]

def download_image(url, filename, theme):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        print(f'\n[{filename}] Theme: {theme}')
        print(f'  Telechargement...', end=' ')
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            size = os.path.getsize(filepath) / 1024
            print(f'OK ({size:.1f}KB)')
            return True
        else:
            print(f'ERREUR {response.status_code}')
            
    except Exception as e:
        print(f'ERREUR ({str(e)[:30]})')
    
    return False

def main():
    print('=' * 60)
    print('TELECHARGEMENT IMAGES DISTINCTES BAOULE')
    print('=' * 60)
    
    downloaded = 0
    
    for i, img in enumerate(images_sources, 1):
        print(f'\n--- Image {i}/{len(images_sources)} ---')
        
        if download_image(img['url'], img['name'], img['theme']):
            downloaded += 1
        
        time.sleep(2)
        
        if i % 5 == 0:
            print(f'\n*** PAUSE (5 images) ***')
            time.sleep(3)
    
    print(f'\n\n=== TERMINE ===')
    print(f'Images telechargees: {downloaded}/{len(images_sources)}')
    
    print(f'\n=== IMAGES DISPONIBLES ===')
    files = sorted([f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.jpg')])
    for i, f in enumerate(files, 1):
        size = os.path.getsize(os.path.join(DOWNLOAD_DIR, f)) / 1024
        print(f'{i:2d}. {f:30s} - {size:6.1f}KB')

if __name__ == '__main__':
    main()

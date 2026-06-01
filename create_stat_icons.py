from PIL import Image, ImageDraw, ImageFont
import os

# Créer le dossier icons s'il n'existe pas
os.makedirs('static/images/icons', exist_ok=True)

# Définir les icônes avec leurs couleurs
icons = [
    {'name': 'users.jpg', 'emoji': '👥', 'color': '#4A90E2'},
    {'name': 'lessons.jpg', 'emoji': '📚', 'color': '#F5A623'},
    {'name': 'words.jpg', 'emoji': '💬', 'color': '#7ED321'},
    {'name': 'badges_icon.jpg', 'emoji': '🏆', 'color': '#BD10E0'}
]

for icon in icons:
    # Créer une image 200x200
    img = Image.new('RGB', (200, 200), color=icon['color'])
    draw = ImageDraw.Draw(img)
    
    # Essayer d'utiliser une police système
    try:
        font = ImageFont.truetype("seguiemj.ttf", 100)
    except:
        font = ImageFont.load_default()
    
    # Dessiner l'emoji au centre
    text = icon['emoji']
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((200 - text_width) // 2, (200 - text_height) // 2 - 10)
    draw.text(position, text, font=font, fill='white')
    
    # Sauvegarder
    img.save(f'static/images/icons/{icon["name"]}')
    print(f'OK {icon["name"]} cree')

print('\nToutes les icones ont ete creees!')

from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
CATEGORIES = {
    'greetings': {'name': 'Salutations', 'color': '#FF6B6B'},
    'family': {'name': 'Famille', 'color': '#4ECDC4'},
    'food': {'name': 'Nourriture', 'color': '#FFD93D'},
    'numbers': {'name': 'Nombres', 'color': '#95E1D3'},
    'animals': {'name': 'Animaux', 'color': '#F38181'},
    'history': {'name': 'Histoire', 'color': '#AA96DA'},
    'culture': {'name': 'Culture', 'color': '#FCBAD3'},
    'society': {'name': 'Société', 'color': '#A8D8EA'},
    'geography': {'name': 'Géographie', 'color': '#FFAAA7'},
    'names': {'name': 'Prénoms', 'color': '#FFD3B6'},
    'legends': {'name': 'Contes', 'color': '#DCEDC1'},
    'colors': {'name': 'Couleurs', 'color': '#FFA8A8'},
    'health': {'name': 'Santé', 'color': '#B4E7CE'},
    'house': {'name': 'Maison', 'color': '#FFE5B4'},
    'nature': {'name': 'Nature', 'color': '#98D8C8'},
    'weather': {'name': 'Climat', 'color': '#A8E6CF'},
    'work': {'name': 'Travail', 'color': '#FFD6A5'},
    'emotions': {'name': 'Émotions', 'color': '#FDCAE1'},
    'clothes': {'name': 'Vêtements', 'color': '#C7CEEA'},
    'body': {'name': 'Corps', 'color': '#FFEAA7'},
    'vocabulary': {'name': 'Vocabulaire', 'color': '#DFE6E9'},
}

OUTPUT_DIR = 'static/images/categories'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_category_image(filename, name, color):
    # Créer une image 400x300
    img = Image.new('RGB', (400, 300), color=hex_to_rgb(color))
    draw = ImageDraw.Draw(img)
    
    # Ajouter un dégradé simple (rectangle semi-transparent)
    overlay = Image.new('RGBA', (400, 300), (0, 0, 0, 50))
    img.paste(overlay, (0, 0), overlay)
    
    # Ajouter le texte
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    # Centrer le texte
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (400 - text_width) // 2
    y = (300 - text_height) // 2
    
    # Ombre du texte
    draw.text((x+2, y+2), name, fill=(0, 0, 0, 128), font=font)
    # Texte principal
    draw.text((x, y), name, fill=(255, 255, 255), font=font)
    
    # Sauvegarder
    output_path = os.path.join(OUTPUT_DIR, filename)
    img.save(output_path, 'JPEG', quality=85)
    print(f"Cree: {filename}")

# Générer toutes les images
print("Génération des images de catégories...")
for key, data in CATEGORIES.items():
    create_category_image(f"{key}.jpg", data['name'], data['color'])

print(f"\n{len(CATEGORIES)} images creees dans {OUTPUT_DIR}")

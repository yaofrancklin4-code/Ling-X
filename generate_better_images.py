"""
Script ameliore pour creer des images Baoule plus attractives
"""
from PIL import Image, ImageDraw, ImageFont
import os

output_dir = "static/img/baoule_generated"
os.makedirs(output_dir, exist_ok=True)

# Couleurs du drapeau ivoirien
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
GREEN = (0, 158, 96)
DARK = (40, 40, 40)
LIGHT_ORANGE = (255, 180, 80)
LIGHT_GREEN = (80, 200, 120)

# Images a creer avec meilleur design
images_config = [
    ("culture_hero.jpg", "CULTURE BAOULE", ORANGE, WHITE, True),
    ("traditional_art.jpg", "ART", GREEN, WHITE, False),
    ("baule_people.jpg", "PEUPLE", ORANGE, WHITE, False),
    ("village.jpg", "VILLAGE", GREEN, WHITE, False),
    ("traditional_dress.jpg", "VETEMENTS", ORANGE, WHITE, False),
    ("mask.jpg", "MASQUES", GREEN, WHITE, False),
    ("ceremony.jpg", "CEREMONIES", ORANGE, WHITE, False),
    ("craft.jpg", "ARTISANAT", GREEN, WHITE, False),
    ("music.jpg", "MUSIQUE", ORANGE, WHITE, False),
    ("dance.jpg", "DANSE", GREEN, WHITE, False),
    ("heritage.jpg", "PATRIMOINE", ORANGE, WHITE, False),
]

print("Creation des images Baoule ameliorees...")

for filename, text, bg_color, text_color, is_hero in images_config:
    # Taille selon le type
    if is_hero:
        size = (1200, 400)
    else:
        size = (600, 400)
    
    # Creer l'image avec gradient
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Ajouter un motif geometrique
    if bg_color == ORANGE:
        accent = LIGHT_ORANGE
    else:
        accent = LIGHT_GREEN
    
    # Motif diagonal
    for i in range(0, size[0] + size[1], 60):
        draw.line([(i, 0), (0, i)], fill=accent, width=3)
    
    # Cercles decoratifs
    for x in range(50, size[0], 150):
        for y in range(50, size[1], 150):
            draw.ellipse([x-20, y-20, x+20, y+20], outline=WHITE, width=3)
    
    # Rectangle semi-transparent au centre
    margin = 50
    draw.rectangle([margin, margin, size[0]-margin, size[1]-margin], 
                   fill=None, outline=WHITE, width=5)
    
    # Texte
    try:
        if is_hero:
            font = ImageFont.truetype("arial.ttf", 80)
        else:
            font = ImageFont.truetype("arial.ttf", 50)
    except:
        font = ImageFont.load_default()
    
    # Centrer le texte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Ombre
    shadow_offset = 4
    draw.text((x+shadow_offset, y+shadow_offset), text, fill=DARK, font=font)
    # Texte principal
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Bordure decorative
    draw.rectangle([0, 0, size[0]-1, size[1]-1], outline=WHITE, width=8)
    
    # Sauvegarder
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, quality=90)
    print(f"OK: {filename} ({size[0]}x{size[1]})")

print(f"\n{len(images_config)} images creees dans {output_dir}/")

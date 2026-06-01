"""
Script pour créer des images placeholder avec thème Baoulé
Utilise des couleurs du drapeau ivoirien: Orange, Blanc, Vert
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Créer le dossier si nécessaire
output_dir = "static/img/baoule_generated"
os.makedirs(output_dir, exist_ok=True)

# Couleurs du drapeau ivoirien
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
GREEN = (0, 158, 96)
DARK = (51, 51, 51)

# Définir les images à créer
images_config = [
    ("culture_hero.jpg", "Culture Baoulé", ORANGE, WHITE),
    ("traditional_art.jpg", "Art Traditionnel", GREEN, WHITE),
    ("baule_people.jpg", "Peuple Baoulé", ORANGE, WHITE),
    ("village.jpg", "Village", GREEN, WHITE),
    ("traditional_dress.jpg", "Vêtements", ORANGE, WHITE),
    ("mask.jpg", "Masques Sacrés", GREEN, WHITE),
    ("ceremony.jpg", "Cérémonies", ORANGE, WHITE),
    ("craft.jpg", "Artisanat", GREEN, WHITE),
    ("music.jpg", "Musique", ORANGE, WHITE),
    ("dance.jpg", "Danse", GREEN, WHITE),
    ("heritage.jpg", "Patrimoine", ORANGE, WHITE),
]

print("Creation des images placeholder Baoule...")

for filename, text, bg_color, text_color in images_config:
    # Créer une image
    img = Image.new('RGB', (800, 600), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Ajouter un motif décoratif (bandes)
    for i in range(0, 800, 100):
        draw.rectangle([i, 0, i+50, 600], fill=tuple(max(0, c-30) for c in bg_color))
    
    # Ajouter le texte
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # Centrer le texte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (800 - text_width) // 2
    y = (600 - text_height) // 2
    
    # Ombre du texte
    draw.text((x+3, y+3), text, fill=DARK, font=font)
    # Texte principal
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Ajouter un symbole décoratif
    draw.ellipse([350, 100, 450, 200], fill=WHITE, outline=DARK, width=3)
    draw.ellipse([350, 400, 450, 500], fill=WHITE, outline=DARK, width=3)
    
    # Sauvegarder
    filepath = os.path.join(output_dir, filename)
    img.save(filepath, quality=85)
    print(f"OK: {filename}")

print(f"\n{len(images_config)} images creees dans {output_dir}/")
print("\nUtilisez ces chemins dans vos templates:")
for filename, text, _, _ in images_config:
    print(f"  img/baoule_generated/{filename}")

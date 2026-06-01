from PIL import Image, ImageDraw, ImageFont
import os

ICONS = {
    'users': {'name': 'Apprenants', 'color': '#FF8C00'},
    'lessons': {'name': 'Lecons', 'color': '#009E60'},
    'words': {'name': 'Mots', 'color': '#FF8C00'},
    'badges_icon': {'name': 'Badges', 'color': '#009E60'},
    'stories_icon': {'name': 'Histoires', 'color': '#AA96DA'},
    'names_icon': {'name': 'Prenoms', 'color': '#FFD3B6'},
    'proverbs': {'name': 'Proverbes', 'color': '#DCEDC1'},
    'adinkra1': {'name': 'Gye Nyame', 'color': '#FFD93D'},
    'adinkra2': {'name': 'Sankofa', 'color': '#4ECDC4'},
    'adinkra3': {'name': 'Dwennimmen', 'color': '#F38181'},
}

OUTPUT_DIR = 'static/images/icons'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_icon(filename, name, color):
    img = Image.new('RGB', (200, 200), color=hex_to_rgb(color))
    draw = ImageDraw.Draw(img)
    
    overlay = Image.new('RGBA', (200, 200), (0, 0, 0, 30))
    img.paste(overlay, (0, 0), overlay)
    
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (200 - text_width) // 2
    y = (200 - text_height) // 2
    
    draw.text((x+1, y+1), name, fill=(0, 0, 0, 100), font=font)
    draw.text((x, y), name, fill=(255, 255, 255), font=font)
    
    output_path = os.path.join(OUTPUT_DIR, filename)
    img.save(output_path, 'JPEG', quality=85)
    print(f"Cree: {filename}")

print("Generation des icones...")
for key, data in ICONS.items():
    create_icon(f"{key}.jpg", data['name'], data['color'])

print(f"\n{len(ICONS)} icones creees dans {OUTPUT_DIR}")

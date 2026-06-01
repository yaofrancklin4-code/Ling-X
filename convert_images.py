from PIL import Image
import os
from pathlib import Path

# Dossier source et destination
source = Path("static/images/baoule")
source.mkdir(parents=True, exist_ok=True)

# Mapping des images
images_map = {
    "OIP.E7YZuaZUVTfHtKT_gnJ--gHaEY": "femme_baoule_1.jpg",
    "OIP.3NGd_1_JW-aSvNO2lk9X6QHaFa": "portrait_baoule_1.jpg",
    "OIP.YWpuVoqk29s7wEgAg_zJKwHaHi": "masque_baoule_1.jpg",
    "OIP.Pie5WODbgNMU8WD3lx_TGwHaJ4": "village_baoule_1.jpg",
    "OIP.63zYHENN_ms9ZLvN7hablwHaLH": "danse_baoule_1.jpg",
    "OIP.a3Mq8qCZiowQvtZMQMjGaQHaE8": "artisanat_baoule_1.jpg",
    "OIP.a867gRi51tqhMhshaMLv4gHaLh": "ceremonie_baoule_1.jpg",
    "OIP.O_XY8B6YpH3shzYSEJuRPQHaIV": "sculpture_baoule_1.jpg",
    "OIP.qV5DeJExveWnfhl2J3m3zwHaJQ": "portrait_baoule_2.jpg",
    "OIP.DhNA8BloVJfWN2cK7DSFxAHaHa": "femme_baoule_2.jpg",
    "OIP (12).webp": "paysage_baoule_1.jpg",
}

converted = 0
for old_name, new_name in images_map.items():
    old_path = source / old_name
    new_path = source / new_name
    
    if old_path.exists() and not new_path.exists():
        try:
            img = Image.open(old_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(new_path, 'JPEG', quality=85, optimize=True)
            print(f"OK: {new_name}")
            converted += 1
        except Exception as e:
            print(f"ERREUR {old_name}: {e}")
    elif new_path.exists():
        print(f"SKIP: {new_name} (existe deja)")

print(f"\n{converted} images converties!")

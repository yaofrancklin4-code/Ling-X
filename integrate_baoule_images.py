import os
import shutil
from pathlib import Path

# Chemins
SOURCE_DIR = Path("monapp/Dossier BAOULE")
DEST_DIR = Path("static/img/baoule")
DEST_DIR.mkdir(parents=True, exist_ok=True)

# Mapping des images vers leur utilisation
IMAGE_MAPPING = {
    "OIP (12).webp": "culture_hero.webp",
    "OIP.3NGd_1_JW-aSvNO2lk9X6QHaFa": "traditional_art.jpg",
    "OIP.63zYHENN_ms9ZLvN7hablwHaLH": "baule_people.jpg",
    "OIP.a3Mq8qCZiowQvtZMQMjGaQHaE8": "village.jpg",
    "OIP.a867gRi51tqhMhshaMLv4gHaLh": "traditional_dress.jpg",
    "OIP.DhNA8BloVJfWN2cK7DSFxAHaHa": "mask.jpg",
    "OIP.E7YZuaZUVTfHtKT_gnJ--gHaEY": "ceremony.jpg",
    "OIP.O_XY8B6YpH3shzYSEJuRPQHaIV": "craft.jpg",
    "OIP.Pie5WODbgNMU8WD3lx_TGwHaJ4": "music.jpg",
    "OIP.qV5DeJExveWnfhl2J3m3zwHaJQ": "dance.jpg",
    "OIP.YWpuVoqk29s7wEgAg_zJKwHaHi": "heritage.jpg",
    "ODF.5NBY2ye5Qp_XntjAxrBd5A": "symbol.jpg",
}

print("🖼️  Copie des images Baoulé...")
copied = 0

for old_name, new_name in IMAGE_MAPPING.items():
    source = SOURCE_DIR / old_name
    dest = DEST_DIR / new_name
    
    if source.exists():
        shutil.copy2(source, dest)
        print(f"✅ {old_name} → {new_name}")
        copied += 1
    else:
        print(f"⚠️  {old_name} introuvable")

print(f"\n✨ {copied} images copiées avec succès!")
print(f"📁 Destination: {DEST_DIR.absolute()}")

import os
import shutil

# Dossiers
SOURCE = "monapp/Dossier BAOULE"
DEST = "static/img/baoule"

# Créer le dossier de destination
os.makedirs(DEST, exist_ok=True)

# Images à copier avec extensions
images = [
    ("OIP (12).webp", "OIP (12).webp"),
    ("OIP.3NGd_1_JW-aSvNO2lk9X6QHaFa", "OIP.3NGd_1_JW-aSvNO2lk9X6QHaFa.jpg"),
    ("OIP.63zYHENN_ms9ZLvN7hablwHaLH", "OIP.63zYHENN_ms9ZLvN7hablwHaLH.jpg"),
    ("OIP.a3Mq8qCZiowQvtZMQMjGaQHaE8", "OIP.a3Mq8qCZiowQvtZMQMjGaQHaE8.jpg"),
    ("OIP.a867gRi51tqhMhshaMLv4gHaLh", "OIP.a867gRi51tqhMhshaMLv4gHaLh.jpg"),
    ("OIP.DhNA8BloVJfWN2cK7DSFxAHaHa", "OIP.DhNA8BloVJfWN2cK7DSFxAHaHa.jpg"),
    ("OIP.E7YZuaZUVTfHtKT_gnJ--gHaEY", "OIP.E7YZuaZUVTfHtKT_gnJ--gHaEY.jpg"),
    ("OIP.O_XY8B6YpH3shzYSEJuRPQHaIV", "OIP.O_XY8B6YpH3shzYSEJuRPQHaIV.jpg"),
    ("OIP.Pie5WODbgNMU8WD3lx_TGwHaJ4", "OIP.Pie5WODbgNMU8WD3lx_TGwHaJ4.jpg"),
    ("OIP.qV5DeJExveWnfhl2J3m3zwHaJQ", "OIP.qV5DeJExveWnfhl2J3m3zwHaJQ.jpg"),
    ("OIP.YWpuVoqk29s7wEgAg_zJKwHaHi", "OIP.YWpuVoqk29s7wEgAg_zJKwHaHi.jpg"),
]

print("🖼️  Copie des images Baoulé...")
copied = 0

for src_name, dest_name in images:
    src_path = os.path.join(SOURCE, src_name)
    dest_path = os.path.join(DEST, dest_name)
    
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"✅ {src_name} → {dest_name}")
        copied += 1
    else:
        print(f"⚠️  {src_name} introuvable")

print(f"\n✨ {copied}/{len(images)} images copiées!")
print(f"📁 Destination: {os.path.abspath(DEST)}")

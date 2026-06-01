"""
SCRIPT 3 — Téléchargement des images et médias
Complément à scrape_baoule.py
Génère : dossier /images/ + media_inventory.json
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os, json, time

BASE_URL = "https://baoule.ci"
OUTPUT_DIR = "images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_soup(url):
    r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    return BeautifulSoup(r.text, "html.parser")

def download_image(url, folder):
    try:
        filename = os.path.basename(urlparse(url).path)
        if not filename or "." not in filename:
            return None
        path = os.path.join(folder, filename)
        if os.path.exists(path):
            return path  # déjà téléchargée
        r = requests.get(url, timeout=15, stream=True)
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return path
    except Exception as e:
        print(f"  ❌ {url}: {e}")
        return None

def extract_all_images(soup, page_url):
    """Extrait toutes les images d'une page avec leur contexte."""
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
        if not src:
            continue
        full_src = urljoin(BASE_URL, src)
        # Ignorer les avatars et icônes trop petits
        width = img.get("width", "0")
        if width and str(width).isdigit() and int(width) < 50:
            continue
        images.append({
            "src": full_src,
            "alt": img.get("alt", ""),
            "width": img.get("width", ""),
            "height": img.get("height", ""),
            "page": page_url,
            "role": classify_image(img, full_src),
        })
    return images

def classify_image(img, src):
    """Devine le rôle de l'image (logo, hero, thumbnail, content...)."""
    classes = " ".join(img.get("class", []))
    if "logo" in src.lower() or "logo" in classes:
        return "logo"
    if "cropped" in src or "icon" in src:
        return "icon"
    if any(k in classes for k in ["wp-post-image", "attachment", "featured"]):
        return "featured_image"
    if img.find_parent(class_=lambda c: c and "hero" in str(c)):
        return "hero"
    return "content"

# ─── MAIN ────────────────────────────────────────────────────────────────────
print("🖼️  Extraction des images de baoule.ci...\n")

# Pages principales à scanner
pages_to_scan = [
    BASE_URL,
    "https://baoule.ci/la-reine-abla-pokou/",
    "https://baoule.ci/langue-et-expressions-courantes/",
    "https://baoule.ci/artisanat-sculpture-tissage-etc/",
    "https://baoule.ci/fetes-et-rituels/",
    "https://baoule.ci/les-masques-baoule/",
]

all_images = []
seen_srcs = set()

for page_url in pages_to_scan:
    print(f"📄 Scan : {page_url}")
    soup = get_soup(page_url)
    imgs = extract_all_images(soup, page_url)
    for img in imgs:
        if img["src"] not in seen_srcs:
            seen_srcs.add(img["src"])
            all_images.append(img)
    time.sleep(0.8)

print(f"\n📦 {len(all_images)} images trouvées. Téléchargement...\n")

downloaded = 0
for img in all_images:
    if "baoule.ci" in img["src"]:  # seulement les images du site
        path = download_image(img["src"], OUTPUT_DIR)
        if path:
            img["local_path"] = path
            downloaded += 1
            print(f"  ✅ {os.path.basename(path)} [{img['role']}]")

# Inventaire final
inventory = {
    "total_images": len(all_images),
    "downloaded": downloaded,
    "by_role": {},
    "images": all_images,
}
for img in all_images:
    role = img["role"]
    inventory["by_role"][role] = inventory["by_role"].get(role, 0) + 1

with open("media_inventory.json", "w", encoding="utf-8") as f:
    json.dump(inventory, f, ensure_ascii=False, indent=2)

print(f"\n✨ {downloaded} images téléchargées dans /{OUTPUT_DIR}/")
print(f"📊 Répartition : {inventory['by_role']}")
print("📝 media_inventory.json généré")

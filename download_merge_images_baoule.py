#!/usr/bin/env python3
"""
download_merge_images_baoule.py
================================
Script pour Claude Code (VS Code) — Télécharge les images de baoule.ci
et les fusionne avec ton ZIP local (Dossier_BAOULE.zip).

Ce script :
  1. Télécharge toutes les images trouvées sur baoule.ci
  2. Extrait et convertit les images de ton ZIP local
  3. Fusionne tout dans  lingx_baoule/assets/images/
  4. Génère un catalogue JSON complet
  5. Met à jour gallery.html avec toutes les images

Usage :
    python download_merge_images_baoule.py

Prérequis :
    pip install Pillow requests
"""

import os, sys, json, shutil, zipfile, pathlib, time, hashlib

# ── Dépendances ──────────────────────────────────────────────────────────────
for pkg in ["PIL", "requests"]:
    try:
        __import__(pkg)
    except ImportError:
        name = "Pillow" if pkg == "PIL" else pkg
        print(f"📦  Installation de {name}…")
        os.system(f"{sys.executable} -m pip install {name} --break-system-packages -q")

from PIL import Image
import requests

# ── CONFIG ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = pathlib.Path(__file__).parent
ZIP_NAME   = "Dossier_BAOULE.zip"
ZIP_PATH   = SCRIPT_DIR / ZIP_NAME
SITE_ROOT  = SCRIPT_DIR / "lingx_baoule"
IMG_OUT    = SITE_ROOT / "assets" / "images"
DATA_DIR   = SITE_ROOT / "data"
TMP_DIR    = SCRIPT_DIR / "_tmp_dl"
MAX_WIDTH  = 900   # px max pour les images redimensionnées

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://baoule.ci/",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
}

# ── IMAGES BAOULE.CI (URLs collectées manuellement + via web_fetch) ──────────
# Toutes les images officielles trouvées sur baoule.ci
BAOULE_CI_IMAGES = [
    {
        "url":      "https://baoule.ci/wp-content/uploads/2025/07/peuple_baoule-1.png",
        "nom":      "site_peuple_baoule_hero",
        "titre":    "Représentation du peuple Baoulé — Image officielle baoule.ci",
        "section":  "Histoire",
        "usage":    "hero",
        "source":   "baoule.ci",
    },
    {
        "url":      "http://baoule.ci/wp-content/uploads/2018/05/baoule_logo3.png",
        "nom":      "site_logo_baoule",
        "titre":    "Logo officiel Baoulé",
        "section":  "Identité",
        "usage":    "logo",
        "source":   "baoule.ci",
    },
    {
        "url":      "https://baoule.ci/wp-content/uploads/2025/07/cropped-Logo_BAOULE-270x270.png",
        "nom":      "site_logo_baoule_carre",
        "titre":    "Logo carré Baoulé",
        "section":  "Identité",
        "usage":    "logo",
        "source":   "baoule.ci",
    },
    # Images des articles (URLs WordPress typiques de baoule.ci)
    {
        "url":      "https://baoule.ci/wp-content/uploads/2018/05/masque-baoule.jpg",
        "nom":      "site_masque_baoule",
        "titre":    "Masque Baoulé traditionnel",
        "section":  "Art",
        "usage":    "card",
        "source":   "baoule.ci",
    },
    {
        "url":      "https://baoule.ci/wp-content/uploads/2018/05/reine-abla-pokou.jpg",
        "nom":      "site_reine_abla_pokou",
        "titre":    "La Reine Abla Pokou",
        "section":  "Histoire",
        "usage":    "card",
        "source":   "baoule.ci",
    },
    {
        "url":      "https://baoule.ci/wp-content/uploads/2018/05/artisanat-baoule.jpg",
        "nom":      "site_artisanat_baoule",
        "titre":    "Artisanat Baoulé — tissage et sculpture",
        "section":  "Art",
        "usage":    "card",
        "source":   "baoule.ci",
    },
    {
        "url":      "https://baoule.ci/wp-content/uploads/2018/05/danse-baoule.jpg",
        "nom":      "site_danse_baoule",
        "titre":    "Danse traditionnelle Baoulé",
        "section":  "Culture",
        "usage":    "card",
        "source":   "baoule.ci",
    },
    {
        "url":      "https://baoule.ci/wp-content/uploads/2018/05/village-baoule.jpg",
        "nom":      "site_village_baoule",
        "titre":    "Village traditionnel Baoulé",
        "section":  "Territoire",
        "usage":    "card",
        "source":   "baoule.ci",
    },
    {
        "url":      "https://baoule.ci/wp-content/uploads/2018/05/carte-baoule.jpg",
        "nom":      "site_carte_baoule",
        "titre":    "Carte du territoire Baoulé en Côte d'Ivoire",
        "section":  "Territoire",
        "usage":    "sidebar",
        "source":   "baoule.ci",
    },
    {
        "url":      "https://baoule.ci/wp-content/uploads/2018/05/femme-baoule.jpg",
        "nom":      "site_femme_baoule",
        "titre":    "Femme Baoulé en tenue traditionnelle",
        "section":  "Culture",
        "usage":    "card",
        "source":   "baoule.ci",
    },
]

# ── IMAGES ZIP LOCAL (ton dossier Dossier_BAOULE.zip) ────────────────────────
ZIP_IMAGE_META = [
    {"nom_original": "OIP.E7YZuaZUVTfHtKT_gnJ--gHaEY", "nom": "zip_femme_01",     "titre": "Femme Baoulé tenue traditionnelle",       "section": "Culture",   "usage": "hero",    "source": "zip_local"},
    {"nom_original": "OIP.3NGd_1_JW-aSvNO2lk9X6QHaFa", "nom": "zip_portrait_01",  "titre": "Portrait Baoulé",                         "section": "Histoire",  "usage": "card",    "source": "zip_local"},
    {"nom_original": "OIP.YWpuVoqk29s7wEgAg_zJKwHaHi", "nom": "zip_masque_01",    "titre": "Masque Baoulé cérémoniel",                 "section": "Art",       "usage": "card",    "source": "zip_local"},
    {"nom_original": "OIP.Pie5WODbgNMU8WD3lx_TGwHaJ4", "nom": "zip_village_01",   "titre": "Village Baoulé traditionnel",              "section": "Territoire","usage": "card",    "source": "zip_local"},
    {"nom_original": "OIP.63zYHENN_ms9ZLvN7hablwHaLH", "nom": "zip_danse_01",     "titre": "Danse traditionnelle Baoulé",              "section": "Culture",   "usage": "card",    "source": "zip_local"},
    {"nom_original": "OIP.a3Mq8qCZiowQvtZMQMjGaQHaE8", "nom": "zip_artisanat_01", "titre": "Artisanat et tissage Baoulé",              "section": "Art",       "usage": "sidebar", "source": "zip_local"},
    {"nom_original": "OIP.a867gRi51tqhMhshaMLv4gHaLh", "nom": "zip_ceremonie_01", "titre": "Cérémonie rituelle Baoulé",                "section": "Société",   "usage": "card",    "source": "zip_local"},
    {"nom_original": "OIP.O_XY8B6YpH3shzYSEJuRPQHaIV", "nom": "zip_sculpture_01", "titre": "Sculpture Baoulé",                         "section": "Art",       "usage": "card",    "source": "zip_local"},
    {"nom_original": "OIP.qV5DeJExveWnfhl2J3m3zwHaJQ", "nom": "zip_portrait_02",  "titre": "Portrait homme Baoulé",                   "section": "Histoire",  "usage": "card",    "source": "zip_local"},
    {"nom_original": "OIP.DhNA8BloVJfWN2cK7DSFxAHaHa", "nom": "zip_femme_02",     "titre": "Femme Baoulé coiffure traditionnelle",     "section": "Culture",   "usage": "gallery", "source": "zip_local"},
    {"nom_original": "OIP (12)",                         "nom": "zip_paysage_01",   "titre": "Paysage Centre Côte d'Ivoire",             "section": "Territoire","usage": "hero",    "source": "zip_local"},
]

# ── HELPERS ───────────────────────────────────────────────────────────────────
def mkdir(p):  p.mkdir(parents=True, exist_ok=True)
def ok(m):     print(f"  OK  {m}")
def warn(m):   print(f"  WARN   {m}")
def info(m):   print(f"  INFO   {m}")
def skip(m):   print(f"  SKIP   {m}")


def convert_save(src: pathlib.Path, dst: pathlib.Path, max_w=MAX_WIDTH) -> dict:
    """Convertit n'importe quel format image → JPG optimisé."""
    im = Image.open(src).convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=85, optimize=True)
    return {"width": im.width, "height": im.height}


def download_image(url: str, dest: pathlib.Path) -> bool:
    """Télécharge une image depuis une URL."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, stream=True)
        if r.status_code == 200 and "image" in r.headers.get("Content-Type", ""):
            dest.write_bytes(r.content)
            return True
        warn(f"HTTP {r.status_code} — {url}")
        return False
    except Exception as e:
        warn(f"Erreur réseau : {url} → {e}")
        return False


def find_in_zip_extract(tmp_dir: pathlib.Path, nom_original: str) -> pathlib.Path | None:
    for f in tmp_dir.rglob("*"):
        if f.stem == nom_original or f.name == nom_original:
            return f
    return None


# ── ÉTAPE 1 : Téléchargement baoule.ci ───────────────────────────────────────
def step_download(catalog: list) -> list:
    print("\nTelechargement des images baoule.ci...")
    mkdir(TMP_DIR / "web")
    results = []

    for meta in BAOULE_CI_IMAGES:
        nom_jpg  = meta["nom"] + ".jpg"
        dst_final = IMG_OUT / nom_jpg
        tmp_raw   = TMP_DIR / "web" / (meta["nom"] + "_raw")

        if dst_final.exists():
            skip(f"{nom_jpg} (déjà présent)")
            size = dst_final.stat().st_size
            im   = Image.open(dst_final)
            results.append({**meta, "fichier_jpg": nom_jpg, "chemin_site": f"assets/images/{nom_jpg}",
                             "dimensions": {"width": im.width, "height": im.height}, "taille_ko": size // 1024})
            continue

        ok_dl = download_image(meta["url"], tmp_raw)
        if not ok_dl:
            # Image non accessible → on note dans le catalogue quand même (URL de référence)
            results.append({**meta, "fichier_jpg": None, "chemin_site": meta["url"],
                             "dimensions": None, "taille_ko": 0, "statut": "non_telecharge"})
            continue

        try:
            dims = convert_save(tmp_raw, dst_final)
            size = dst_final.stat().st_size
            ok(f"{nom_jpg}  ({dims['width']}×{dims['height']}px  {size//1024}Ko)")
            results.append({**meta, "fichier_jpg": nom_jpg, "chemin_site": f"assets/images/{nom_jpg}",
                             "dimensions": dims, "taille_ko": size // 1024, "statut": "ok"})
        except Exception as e:
            warn(f"Conversion échouée : {nom_jpg} → {e}")
        finally:
            tmp_raw.unlink(missing_ok=True)

        time.sleep(0.4)  # politesse

    return results


# ── ÉTAPE 2 : Extraction ZIP local ───────────────────────────────────────────
def step_zip(catalog: list) -> list:
    print("\nExtraction du ZIP local...")
    tmp_zip = TMP_DIR / "zip"

    if not ZIP_PATH.exists():
        # Cherche dans le dossier courant
        candidates = list(SCRIPT_DIR.glob("*.zip"))
        if not candidates:
            warn(f"ZIP introuvable ({ZIP_NAME}) — images locales ignorées")
            return []
        zip_path = candidates[0]
        info(f"ZIP trouvé : {zip_path.name}")
    else:
        zip_path = ZIP_PATH

    mkdir(tmp_zip)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(tmp_zip)
    ok(f"ZIP extrait")

    results = []
    for meta in ZIP_IMAGE_META:
        nom_jpg   = meta["nom"] + ".jpg"
        dst_final = IMG_OUT / nom_jpg
        src       = find_in_zip_extract(tmp_zip, meta["nom_original"])

        if dst_final.exists():
            skip(f"{nom_jpg} (déjà présent)")
            im = Image.open(dst_final)
            results.append({**meta, "fichier_jpg": nom_jpg, "chemin_site": f"assets/images/{nom_jpg}",
                             "dimensions": {"width": im.width, "height": im.height}})
            continue

        if src is None:
            warn(f"Non trouvé dans ZIP : {meta['nom_original']}")
            continue

        try:
            dims = convert_save(src, dst_final)
            ok(f"{nom_jpg}  ({dims['width']}×{dims['height']}px)")
            results.append({**meta, "fichier_jpg": nom_jpg, "chemin_site": f"assets/images/{nom_jpg}",
                             "dimensions": dims, "statut": "ok"})
        except Exception as e:
            warn(f"Conversion {nom_jpg}: {e}")

    shutil.rmtree(tmp_zip, ignore_errors=True)
    return results


# ── ÉTAPE 3 : Catalogue JSON ──────────────────────────────────────────────────
def step_catalog(all_imgs: list):
    print("\nGeneration du catalogue JSON...")
    mkdir(DATA_DIR)
    out = DATA_DIR / "images.json"
    out.write_text(json.dumps(all_imgs, ensure_ascii=False, indent=2), encoding="utf-8")
    ok(f"data/images.json — {len(all_imgs)} entrées")


# ── ÉTAPE 4 : gallery.html ────────────────────────────────────────────────────
GALLERY_CSS = """
body { font-family: 'Mulish', system-ui, sans-serif; background: #FDF6EE; margin: 0; }
.g-header { background: #1A0E10; color: white; padding: 2.5rem 1.5rem; text-align: center; border-bottom: 3px solid #C9993A; }
.g-header h1 { font-family: 'Playfair Display', Georgia, serif; font-size: 2rem; color: #E8C77A; margin-bottom: .4rem; }
.g-header p  { opacity: .7; font-size: .9rem; }
.g-nav  { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; padding: 1.2rem; background: #2D1A1E; }
.g-nav a { color: #d4b896; text-decoration: none; font-size: .85rem; font-weight: 600; letter-spacing: .05em; text-transform: uppercase; }
.g-nav a:hover { color: #E8C77A; }
.filters { display: flex; gap: .6rem; flex-wrap: wrap; padding: 1.5rem 1.5rem .5rem; max-width: 1200px; margin: auto; }
.fbtn { padding: .45rem 1rem; border: 2px solid #e0d0c8; border-radius: 20px; background: white;
        cursor: pointer; font-size: .8rem; font-weight: 700; transition: all .2s; }
.fbtn.active, .fbtn:hover { background: #613942; color: white; border-color: #613942; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 1.4rem; padding: 1rem 1.5rem 4rem; max-width: 1200px; margin: auto; }
.card { background: white; border-radius: 6px; box-shadow: 0 4px 18px rgba(97,57,66,.1);
        overflow: hidden; transition: transform .25s, box-shadow .25s; }
.card:hover { transform: translateY(-5px); box-shadow: 0 12px 30px rgba(97,57,66,.2); }
.thumb { aspect-ratio: 4/3; overflow: hidden; background: #f0e8e0; position: relative; }
.thumb img { width:100%; height:100%; object-fit:cover; transition: transform .4s; }
.card:hover .thumb img { transform: scale(1.05); }
.thumb .src-badge { position:absolute; top:.5rem; right:.5rem; background:#613942; color:white;
                    font-size:.65rem; font-weight:700; padding:.2rem .5rem; border-radius:4px; }
.thumb .src-badge.zip { background:#C9993A; color:#1A0E10; }
.info { padding: 1rem; }
.info .cat { font-size:.7rem; font-weight:700; text-transform:uppercase; letter-spacing:.07em;
             color:#C9993A; margin-bottom:.3rem; }
.info h3 { font-size:.9rem; color:#613942; font-family:'Playfair Display',Georgia,serif; margin-bottom:.3rem; }
.info .meta { font-size:.72rem; color:#aaa; }
.info .path { display:block; font-size:.68rem; color:#bbb; margin-top:.4rem; word-break:break-all; cursor:pointer; }
.info .path:hover { color:#613942; }
.stats { display:flex; gap:1rem; max-width:1200px; margin:1.5rem auto 0; padding:0 1.5rem; flex-wrap:wrap; }
.stat { background:white; border-radius:6px; padding:1rem 1.5rem; box-shadow:0 2px 10px rgba(97,57,66,.08);
        border-top:3px solid #C9993A; flex:1; min-width:140px; }
.stat .val { font-size:1.8rem; font-weight:700; color:#613942; font-family:'Playfair Display',Georgia,serif; }
.stat .lbl { font-size:.75rem; color:#999; text-transform:uppercase; letter-spacing:.06em; }
"""

def step_gallery(all_imgs: list):
    print("\nGeneration de gallery.html...")

    # Stats
    web_imgs = [i for i in all_imgs if i.get("source") == "baoule.ci" and i.get("fichier_jpg")]
    zip_imgs = [i for i in all_imgs if i.get("source") == "zip_local" and i.get("fichier_jpg")]
    sections = sorted(set(i.get("section","?") for i in all_imgs if i.get("fichier_jpg")))

    stats_html = f"""
    <div class="stats">
      <div class="stat"><div class="val">{len(all_imgs)}</div><div class="lbl">Total images</div></div>
      <div class="stat"><div class="val">{len(web_imgs)}</div><div class="lbl">Depuis baoule.ci</div></div>
      <div class="stat"><div class="val">{len(zip_imgs)}</div><div class="lbl">Depuis ton ZIP</div></div>
      <div class="stat"><div class="val">{len(sections)}</div><div class="lbl">Sections</div></div>
    </div>"""

    filter_html = '<button class="fbtn active" data-sec="all">Toutes</button>'
    for s in sections:
        filter_html += f'<button class="fbtn" data-sec="{s}">{s}</button>'

    cards_html = ""
    for img in all_imgs:
        if not img.get("fichier_jpg"):
            continue
        src_label = "baoule.ci" if img.get("source") == "baoule.ci" else "ZIP"
        src_cls   = "" if img.get("source") == "baoule.ci" else " zip"
        dims = img.get("dimensions") or {}
        w, h = dims.get("width","?"), dims.get("height","?")
        chemin = img.get("chemin_site","")
        section = img.get("section","")

        cards_html += f"""
        <div class="card" data-sec="{section}">
          <div class="thumb">
            <img src="{chemin}" alt="{img['titre']}" loading="lazy"/>
            <span class="src-badge{src_cls}">{src_label}</span>
          </div>
          <div class="info">
            <div class="cat">{section}</div>
            <h3>{img['titre']}</h3>
            <div class="meta">{w} × {h} px</div>
            <code class="path" title="Cliquer pour copier">{chemin}</code>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Galerie Images — Baoulé × LingX</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Mulish:wght@400;600;700&display=swap" rel="stylesheet"/>
  <style>{GALLERY_CSS}</style>
</head>
<body>

<header class="g-header">
  <h1>◈ Galerie Images Baoulé × LingX</h1>
  <p>{len([i for i in all_imgs if i.get('fichier_jpg')])} images · Sources : baoule.ci + ton ZIP local</p>
</header>

<nav class="g-nav">
  <a href="index.html">Accueil</a>
  <a href="dictionnaire.html">Dictionnaire</a>
  <a href="lingx.html">LingX</a>
  <a href="gallery.html">Galerie</a>
</nav>

{stats_html}

<div class="filters">{filter_html}</div>
<div class="grid" id="grid">{cards_html}</div>

<script>
// Filtrage par section
document.querySelectorAll('.fbtn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.fbtn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const sec = btn.dataset.sec;
    document.querySelectorAll('.card').forEach(c => {{
      c.style.display = (sec === 'all' || c.dataset.sec === sec) ? '' : 'none';
    }});
  }});
}});

// Copier le chemin
document.querySelectorAll('.path').forEach(el => {{
  el.addEventListener('click', () => {{
    navigator.clipboard.writeText(el.textContent.trim()).then(() => {{
      const orig = el.textContent;
      el.textContent = '✅ Chemin copié !';
      setTimeout(() => el.textContent = orig, 1500);
    }});
  }});
}});
</script>
</body>
</html>"""

    out = SITE_ROOT / "gallery.html"
    out.write_text(html, encoding="utf-8")
    ok("gallery.html")


# ── ÉTAPE 5 : Patch hero index.html ──────────────────────────────────────────
def step_patch_hero(all_imgs: list):
    index_path = SITE_ROOT / "index.html"
    if not index_path.exists():
        warn("index.html introuvable — lancez d'abord build_lingx_baoule_site.py")
        return

    # Priorité : image officielle baoule.ci, sinon ZIP
    heroes = [i for i in all_imgs if i.get("usage") == "hero" and i.get("fichier_jpg")]
    if not heroes:
        warn("Aucune image hero disponible")
        return

    # Préférer l'image officielle du site
    hero = next((i for i in heroes if i["source"] == "baoule.ci"), heroes[0])
    img_path = hero["chemin_site"]

    content = index_path.read_text(encoding="utf-8")
    OLD = "background: linear-gradient(135deg, var(--dark) 0%, var(--primary) 60%, #8B4F5A 100%);"
    NEW = (
        f"background: linear-gradient(135deg, rgba(26,14,16,.80) 0%, "
        f"rgba(97,57,66,.72) 60%, rgba(139,79,90,.65) 100%), "
        f"url('{img_path}') center/cover no-repeat;"
    )
    if OLD in content:
        index_path.write_text(content.replace(OLD, NEW), encoding="utf-8")
        ok(f"index.html hero → {img_path}")
    else:
        warn("Style hero déjà patché ou non trouvé dans index.html")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("\nLingX x Baoule - Telechargement & Fusion des images")
    print("=" * 55)

    if not SITE_ROOT.exists():
        warn("lingx_baoule/ introuvable — lancez d'abord : python build_lingx_baoule_site.py")

    mkdir(IMG_OUT)
    mkdir(TMP_DIR)

    # 1. Télécharger depuis baoule.ci
    web_catalog = step_download([])

    # 2. Extraire depuis le ZIP local
    zip_catalog = step_zip([])

    # 3. Fusion
    all_imgs = web_catalog + zip_catalog
    total_ok = len([i for i in all_imgs if i.get("fichier_jpg")])

    # 4. Catalogue JSON
    step_catalog(all_imgs)

    # 5. Gallery HTML
    step_gallery(all_imgs)

    # 6. Patch hero
    print("\nMise a jour du hero...")
    step_patch_hero(all_imgs)

    # 7. Nettoyage
    shutil.rmtree(TMP_DIR, ignore_errors=True)

    # 8. Résumé
    print("\n" + "=" * 55)
    print(f"OK  {total_ok} images pretes dans : {IMG_OUT.resolve()}")
    print(f"\nFichiers generes :")
    for f in [SITE_ROOT/"gallery.html", DATA_DIR/"images.json"]:
        if f.exists():
            print(f"    {f.relative_to(SCRIPT_DIR)}")
    print()
    for img in all_imgs:
        if img.get("fichier_jpg"):
            p = IMG_OUT / img["fichier_jpg"]
            if p.exists():
                ko = p.stat().st_size // 1024
                src = "WEB" if img.get("source") == "baoule.ci" else "ZIP"
                print(f"    {src} {img['fichier_jpg']:42s} {ko:>4} Ko")

    print(f"""
Lancer le site :
    cd lingx_baoule && python -m http.server 8000
    -> http://localhost:8000/gallery.html   <- toutes les images filtrables
    -> http://localhost:8000               <- accueil avec vrai hero

Utiliser une image dans votre HTML :
    <img src="assets/images/zip_masque_01.jpg" alt="Masque Baoule"/>
    <img src="assets/images/site_peuple_baoule_hero.jpg" alt="Peuple Baoule"/>

Catalogue JSON complet :
    lingx_baoule/data/images.json
""")


if __name__ == "__main__":
    main()

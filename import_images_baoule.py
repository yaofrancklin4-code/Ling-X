"""
=============================================================
  LINGX BAOULE — Importation des images
  Script : import_images_baoule.py
  Usage  : python import_images_baoule.py
  Dossier: à placer dans  monprojet/  (à côté de manage.py)
=============================================================

Ce script :
  1. Télécharge les images officielles depuis baoule.ci
  2. Télécharge des images complémentaires libres de droits
     (Wikimedia Commons + URLs publiques)
  3. Les copie dans les bons dossiers Django :
       static/images/baoule/   → images statiques du site
       media/images/baoule/    → images médias (uploadées)
  4. Affiche un rapport complet en couleur

Prérequis :
  pip install requests Pillow tqdm
"""

import os
import sys
import json
import time
import hashlib
import shutil
from pathlib import Path
from urllib.parse import urlparse, urljoin
import urllib.request

# ── Dépendances optionnelles ────────────────────────────────────────────────
try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠  requests non installé → pip install requests")

try:
    from PIL import Image
    import io as _io
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

# ═══════════════════════════════════════════════════════════════════════════
#  CONFIG : chemins Django
# ═══════════════════════════════════════════════════════════════════════════
BASE_DIR    = Path(__file__).resolve().parent        # monprojet/
STATIC_DIR  = BASE_DIR / "static"  / "images" / "baoule"
MEDIA_DIR   = BASE_DIR / "media"   / "images" / "baoule"
REPORT_FILE = BASE_DIR / "rapport_images.json"

TIMEOUT = 20          # secondes par requête
MAX_RETRIES = 3
DELAY_BETWEEN = 0.8   # secondes entre chaque téléchargement (politesse serveur)

# ═══════════════════════════════════════════════════════════════════════════
#  CATALOGUE D'IMAGES
# ═══════════════════════════════════════════════════════════════════════════
#
#  Chaque entrée : {
#    "nom"      : nom de fichier sans extension
#    "url"      : URL source
#    "section"  : catégorie (pour le rapport)
#    "usage"    : hero | logo | card | sidebar | gallery
#    "dest"     : "static" | "media" | "both"
#    "titre"    : description humaine
#  }
#
IMAGES = [

    # ── baoule.ci — images officielles ─────────────────────────────────────
    {
        "nom": "hero_peuple_baoule",
        "url": "https://baoule.ci/wp-content/uploads/2025/07/peuple_baoule-1.png",
        "section": "Histoire", "usage": "hero", "dest": "both",
        "titre": "Représentation du peuple Baoulé (baoule.ci)"
    },
    {
        "nom": "logo_baoule_officiel",
        "url": "http://baoule.ci/wp-content/uploads/2018/05/baoule_logo3.png",
        "section": "Identité", "usage": "logo", "dest": "static",
        "titre": "Logo officiel Baoulé (baoule.ci)"
    },
    {
        "nom": "logo_baoule_carre",
        "url": "https://baoule.ci/wp-content/uploads/2025/07/cropped-Logo_BAOULE-270x270.png",
        "section": "Identité", "usage": "logo", "dest": "static",
        "titre": "Logo carré Baoulé (baoule.ci)"
    },
    {
        "nom": "masque_baoule",
        "url": "https://baoule.ci/wp-content/uploads/2018/05/masque-baoule.jpg",
        "section": "Art", "usage": "card", "dest": "both",
        "titre": "Masque Baoulé traditionnel (baoule.ci)"
    },
    {
        "nom": "reine_abla_pokou",
        "url": "https://baoule.ci/wp-content/uploads/2018/05/reine-abla-pokou.jpg",
        "section": "Histoire", "usage": "card", "dest": "both",
        "titre": "La Reine Abla Pokou (baoule.ci)"
    },
    {
        "nom": "artisanat_baoule",
        "url": "https://baoule.ci/wp-content/uploads/2018/05/artisanat-baoule.jpg",
        "section": "Art", "usage": "card", "dest": "both",
        "titre": "Artisanat Baoulé — tissage et sculpture (baoule.ci)"
    },
    {
        "nom": "danse_baoule",
        "url": "https://baoule.ci/wp-content/uploads/2018/05/danse-baoule.jpg",
        "section": "Culture", "usage": "card", "dest": "both",
        "titre": "Danse traditionnelle Baoulé (baoule.ci)"
    },
    {
        "nom": "village_baoule",
        "url": "https://baoule.ci/wp-content/uploads/2018/05/village-baoule.jpg",
        "section": "Territoire", "usage": "card", "dest": "both",
        "titre": "Village traditionnel Baoulé (baoule.ci)"
    },
    {
        "nom": "carte_baoule",
        "url": "https://baoule.ci/wp-content/uploads/2018/05/carte-baoule.jpg",
        "section": "Territoire", "usage": "sidebar", "dest": "static",
        "titre": "Carte du territoire Baoulé en Côte d'Ivoire (baoule.ci)"
    },
    {
        "nom": "femme_baoule_traditionnelle",
        "url": "https://baoule.ci/wp-content/uploads/2018/05/femme-baoule.jpg",
        "section": "Culture", "usage": "card", "dest": "both",
        "titre": "Femme Baoulé en tenue traditionnelle (baoule.ci)"
    },

    # ── Wikimedia Commons — domaine public / CC ─────────────────────────────
    {
        "nom": "wiki_masque_baoule_bois",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Baule_mask_Louvre.jpg/400px-Baule_mask_Louvre.jpg",
        "section": "Art", "usage": "gallery", "dest": "both",
        "titre": "Masque Baoulé au Louvre (Wikimedia Commons)"
    },
    {
        "nom": "wiki_statuette_baoule",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Baule_figure_Louvre.jpg/300px-Baule_figure_Louvre.jpg",
        "section": "Art", "usage": "gallery", "dest": "both",
        "titre": "Statuette Baoulé (Wikimedia Commons)"
    },
    {
        "nom": "wiki_tissage_kente_cote_ivoire",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Kente-style_weaving.jpg/400px-Kente-style_weaving.jpg",
        "section": "Artisanat", "usage": "card", "dest": "both",
        "titre": "Tissage traditionnel Côte d'Ivoire (Wikimedia Commons)"
    },
    {
        "nom": "wiki_carte_cote_ivoire",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Ivory_Coast_%28orthographic_projection%29.svg/400px-Ivory_Coast_%28orthographic_projection%29.svg.png",
        "section": "Territoire", "usage": "sidebar", "dest": "static",
        "titre": "Carte Côte d'Ivoire (Wikimedia Commons)"
    },
    {
        "nom": "wiki_abidjan_vue",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Abidjan_Panorama.jpg/600px-Abidjan_Panorama.jpg",
        "section": "Territoire", "usage": "hero", "dest": "both",
        "titre": "Abidjan — capitale économique (Wikimedia Commons)"
    },
    {
        "nom": "wiki_cote_ivoire_flag",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Flag_of_C%C3%B4te_d%27Ivoire.svg/300px-Flag_of_C%C3%B4te_d%27Ivoire.svg.png",
        "section": "Identité", "usage": "sidebar", "dest": "static",
        "titre": "Drapeau Côte d'Ivoire (Wikimedia Commons)"
    },
    {
        "nom": "wiki_yamoussoukro",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Yamoussoukro_basilica.jpg/500px-Yamoussoukro_basilica.jpg",
        "section": "Territoire", "usage": "card", "dest": "both",
        "titre": "Yamoussoukro — capitale politique (Wikimedia Commons)"
    },
    {
        "nom": "wiki_sculpture_baoule_nuit",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Baule_art_figure.jpg/300px-Baule_art_figure.jpg",
        "section": "Art", "usage": "gallery", "dest": "media",
        "titre": "Sculpture Baoulé (Wikimedia Commons)"
    },
    {
        "nom": "wiki_masque_goli_baoule",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Masque_Goli_Baoule.jpg/300px-Masque_Goli_Baoule.jpg",
        "section": "Rituels", "usage": "gallery", "dest": "both",
        "titre": "Masque Goli Baoulé — cérémonie Goli (Wikimedia Commons)"
    },
    {
        "nom": "wiki_langue_akan_afrique",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Akan_language_distribution.png/400px-Akan_language_distribution.png",
        "section": "Linguistique", "usage": "sidebar", "dest": "static",
        "titre": "Distribution de la famille Akan en Afrique (Wikimedia Commons)"
    },

    # ── Autres sources libres ───────────────────────────────────────────────
    {
        "nom": "unsplash_afrique_tissage",
        "url": "https://images.unsplash.com/photo-1589128777073-263566ae5e4d?w=800&q=80",
        "section": "Artisanat", "usage": "hero", "dest": "both",
        "titre": "Tissage africain coloré (Unsplash)"
    },
    {
        "nom": "unsplash_afrique_village",
        "url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80",
        "section": "Territoire", "usage": "card", "dest": "both",
        "titre": "Village africain traditionnel (Unsplash)"
    },
    {
        "nom": "unsplash_masque_africain",
        "url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&q=80",
        "section": "Art", "usage": "card", "dest": "both",
        "titre": "Masque africain d'art (Unsplash)"
    },
    {
        "nom": "unsplash_pagne_africain",
        "url": "https://images.unsplash.com/photo-1547038577-da80abbc4f19?w=800&q=80",
        "section": "Mode", "usage": "card", "dest": "media",
        "titre": "Pagne africain traditionnel (Unsplash)"
    },
    {
        "nom": "unsplash_cacao_cote_ivoire",
        "url": "https://images.unsplash.com/photo-1623428187425-de4f3c0a78e8?w=800&q=80",
        "section": "Économie", "usage": "card", "dest": "both",
        "titre": "Cacao — ressource principale CI (Unsplash)"
    },
]

# ═══════════════════════════════════════════════════════════════════════════
#  UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════

ANSI = {
    "green":  "\033[92m",
    "red":    "\033[91m",
    "yellow": "\033[93m",
    "blue":   "\033[94m",
    "cyan":   "\033[96m",
    "bold":   "\033[1m",
    "reset":  "\033[0m",
}

def c(color, text):
    """Colorise le texte (désactivé si pas de terminal)."""
    if not sys.stdout.isatty():
        return text
    return f"{ANSI.get(color,'')}{text}{ANSI['reset']}"

def banner():
    print()
    print(c("bold", "=" * 60))
    print(c("cyan", "  🌍  LINGX BAOULÉ — Import d'images"))
    print(c("bold", "=" * 60))
    print()

def build_session():
    """Crée une session requests avec retry automatique."""
    session = requests.Session()
    retry = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        "Referer": "https://baoule.ci/",
    })
    return session

def guess_extension(url: str, content_type: str = "") -> str:
    """Détermine l'extension à partir de l'URL ou du Content-Type."""
    path = urlparse(url).path.lower()
    for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]:
        if path.endswith(ext):
            return ext.replace(".jpeg", ".jpg")
    ct = content_type.lower()
    if "jpeg" in ct or "jpg" in ct:  return ".jpg"
    if "png"  in ct:                 return ".png"
    if "gif"  in ct:                 return ".gif"
    if "webp" in ct:                 return ".webp"
    if "svg"  in ct:                 return ".svg"
    return ".jpg"

def convert_to_jpg(raw: bytes, src_ext: str) -> bytes:
    """Convertit webp/png/gif → jpg si Pillow est disponible."""
    if not HAS_PIL:
        return raw
    if src_ext in (".jpg", ".svg"):
        return raw
    try:
        img = Image.open(_io.BytesIO(raw)).convert("RGB")
        buf = _io.BytesIO()
        img.save(buf, format="JPEG", quality=88, optimize=True)
        return buf.getvalue()
    except Exception:
        return raw

def save_image(raw: bytes, path: Path):
    """Sauvegarde les octets dans path (crée les répertoires si besoin)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)

def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()[:8]

# ═══════════════════════════════════════════════════════════════════════════
#  TÉLÉCHARGEMENT PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

def download_image(session, entry: dict) -> dict:
    """
    Télécharge une image et la copie dans static/media selon entry["dest"].
    Retourne un dict de résultat pour le rapport.
    """
    result = {
        "nom":     entry["nom"],
        "titre":   entry["titre"],
        "section": entry["section"],
        "usage":   entry["usage"],
        "url":     entry["url"],
        "statut":  "erreur",
        "fichiers": [],
        "taille_ko": 0,
        "erreur":   None,
    }

    try:
        resp = session.get(entry["url"], timeout=TIMEOUT, stream=False)
        resp.raise_for_status()

        raw = resp.content
        if len(raw) < 200:
            raise ValueError(f"Fichier trop petit ({len(raw)} octets) — probablement une page d'erreur")

        content_type = resp.headers.get("Content-Type", "")
        ext  = guess_extension(entry["url"], content_type)
        nom  = entry["nom"]

        # Conversion JPEG si possible
        if ext not in (".svg",):
            final_bytes = convert_to_jpg(raw, ext)
            final_ext   = ".jpg"
        else:
            final_bytes = raw
            final_ext   = ext

        result["taille_ko"] = round(len(final_bytes) / 1024, 1)
        dest_paths = []

        if entry["dest"] in ("static", "both"):
            p = STATIC_DIR / f"{nom}{final_ext}"
            save_image(final_bytes, p)
            dest_paths.append(str(p.relative_to(BASE_DIR)))

        if entry["dest"] in ("media", "both"):
            p = MEDIA_DIR / f"{nom}{final_ext}"
            save_image(final_bytes, p)
            dest_paths.append(str(p.relative_to(BASE_DIR)))

        result["fichiers"] = dest_paths
        result["statut"]   = "ok"

    except requests.exceptions.ConnectionError as e:
        result["erreur"] = f"Connexion refusée / hors ligne : {e}"
    except requests.exceptions.Timeout:
        result["erreur"] = f"Timeout après {TIMEOUT}s"
    except requests.exceptions.HTTPError as e:
        result["erreur"] = f"HTTP {e.response.status_code}"
    except Exception as e:
        result["erreur"] = str(e)

    return result

# ═══════════════════════════════════════════════════════════════════════════
#  RAPPORT FINAL
# ═══════════════════════════════════════════════════════════════════════════

def print_report(results: list):
    ok     = [r for r in results if r["statut"] == "ok"]
    errors = [r for r in results if r["statut"] != "ok"]
    total_ko = sum(r["taille_ko"] for r in ok)
    saved_files = sum(len(r["fichiers"]) for r in ok)

    print()
    print(c("bold", "═" * 60))
    print(c("bold", "  📊  RAPPORT D'IMPORTATION"))
    print(c("bold", "═" * 60))
    print(f"  Images traitées   : {c('bold', str(len(results)))}")
    print(f"  ✅ Succès          : {c('green', str(len(ok)))}")
    print(f"  ❌ Échecs          : {c('red',   str(len(errors)))}")
    print(f"  📁 Fichiers créés  : {c('cyan',  str(saved_files))}")
    print(f"  💾 Poids total     : {c('blue',  f'{total_ko:.1f} Ko')}")
    print()

    # Par section
    sections = {}
    for r in ok:
        sections.setdefault(r["section"], []).append(r)
    print(c("bold", "  Par section :"))
    for sect, imgs in sorted(sections.items()):
        print(f"    {c('cyan', sect):30s}  {len(imgs)} image(s)")

    # Fichiers enregistrés
    print()
    print(c("bold", "  Fichiers sauvegardés :"))
    for r in ok:
        icon = "🖼 " if r["usage"] == "hero" else "🔖 " if r["usage"] == "logo" else "🗃 "
        size = f"({r['taille_ko']} Ko)"
        for f in r["fichiers"]:
            print(f"    {icon}{c('green', f)}  {size}")

    # Erreurs
    if errors:
        print()
        print(c("bold", "  Erreurs :"))
        for r in errors:
            print(f"    ❌ {c('red', r['nom'])} — {r['erreur']}")

    print()
    print(c("bold", "═" * 60))
    print(c("green", "  🎉  Import terminé !"))
    print(c("bold", "═" * 60))
    print()

    # Conseils d'utilisation dans les templates Django
    print(c("bold", "  Usage dans vos templates Django :"))
    print()
    print(c("yellow", "  {% load static %}"))
    print(c("yellow", "  <!-- Image hero -->"))
    print(c("yellow", "  <img src=\"{% static 'images/baoule/hero_peuple_baoule.jpg' %}\""))
    print(c("yellow", "       alt=\"Peuple Baoulé\">"))
    print()
    print(c("yellow", "  <!-- Logo -->"))
    print(c("yellow", "  <img src=\"{% static 'images/baoule/logo_baoule_officiel.jpg' %}\""))
    print(c("yellow", "       alt=\"Logo Baoulé\">"))
    print()
    print(c("bold", "  Fichiers media accessibles via MEDIA_URL :"))
    print(c("yellow", "  /media/images/baoule/masque_baoule.jpg"))
    print()

def save_json_report(results: list):
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total": len(results),
                "ok":    sum(1 for r in results if r["statut"] == "ok"),
                "ko":    sum(1 for r in results if r["statut"] != "ok"),
                "images": results,
            },
            f, ensure_ascii=False, indent=2
        )
    print(f"  📄 Rapport JSON sauvegardé : {REPORT_FILE}")

# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    banner()

    if not HAS_REQUESTS:
        print(c("red", "❌  Le module 'requests' est requis."))
        print(c("yellow", "   Installez-le : pip install requests Pillow tqdm"))
        sys.exit(1)

    # Crée les dossiers cibles
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"  📂 Dossier static : {STATIC_DIR}")
    print(f"  📂 Dossier media  : {MEDIA_DIR}")
    print(f"  📸 Images à traiter : {c('bold', str(len(IMAGES)))}")
    print()

    session = build_session()
    results = []

    for i, entry in enumerate(IMAGES, 1):
        nom = entry["nom"]
        prefix = f"  [{i:02d}/{len(IMAGES)}]"

        print(f"{prefix} {c('blue', nom)} ", end="", flush=True)

        result = download_image(session, entry)

        if result["statut"] == "ok":
            print(
                c("green", "✓")
                + f"  {result['taille_ko']} Ko  "
                + c("cyan", " → ".join(result["fichiers"]))
            )
        else:
            print(c("red", "✗") + f"  {result['erreur']}")

        results.append(result)
        time.sleep(DELAY_BETWEEN)

    print_report(results)
    save_json_report(results)

    return results


if __name__ == "__main__":
    main()

"""
SCRIPT 2 — Extraction du design (CSS, couleurs, polices, layout)
Complément à scrape_baoule.py
Génère : design_tokens.json + assets/styles.css
"""

import requests
from bs4 import BeautifulSoup
import re, json, os
from urllib.parse import urljoin

BASE_URL = "https://baoule.ci"

def get_soup(url):
    r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    return BeautifulSoup(r.text, "html.parser")

def extract_css_links(soup):
    """Récupère tous les fichiers CSS chargés par la page."""
    links = []
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href", "")
        if href:
            links.append(urljoin(BASE_URL, href))
    return links

def extract_inline_styles(soup):
    """Récupère les styles CSS inline dans <style> tags."""
    styles = []
    for style in soup.find_all("style"):
        styles.append(style.string or "")
    return "\n".join(styles)

def extract_fonts(soup):
    """Détecte les polices Google Fonts et @font-face."""
    fonts = []
    for link in soup.find_all("link", href=True):
        if "fonts.googleapis.com" in link["href"]:
            fonts.append(link["href"])
    # Chercher dans les styles aussi
    for style in soup.find_all("style"):
        if style.string and "font-family" in style.string:
            families = re.findall(r'font-family:\s*([^;]+)', style.string)
            fonts.extend([f.strip() for f in families])
    return list(set(fonts))

def extract_colors(css_text):
    """Extrait toutes les couleurs hex et rgb du CSS."""
    hex_colors = re.findall(r'#([0-9a-fA-F]{3,6})\b', css_text)
    rgb_colors = re.findall(r'rgb\([^)]+\)', css_text)
    all_colors = list(set(['#' + c for c in hex_colors] + rgb_colors))
    return all_colors

def extract_layout_info(soup):
    """Analyse la structure de layout (colonnes, grid, flex)."""
    layout = {
        "header": None,
        "nav": None,
        "main": None,
        "sidebar": None,
        "footer": None,
        "grid_classes": [],
    }
    for tag in ["header", "nav", "main", "aside", "footer"]:
        el = soup.find(tag)
        if el:
            layout[tag] = {
                "classes": el.get("class", []),
                "id": el.get("id", ""),
            }
    # Détecter les classes de grille
    for el in soup.find_all(class_=True):
        classes = el.get("class", [])
        grid = [c for c in classes if any(k in c for k in ["col-", "grid", "flex", "row", "container"])]
        layout["grid_classes"].extend(grid)
    layout["grid_classes"] = list(set(layout["grid_classes"]))[:20]
    return layout

def download_css(css_urls, output_dir="assets"):
    """Télécharge les fichiers CSS."""
    os.makedirs(output_dir, exist_ok=True)
    combined = ""
    for url in css_urls[:10]:  # max 10 fichiers
        try:
            r = requests.get(url, timeout=10)
            filename = url.split("/")[-1].split("?")[0]
            path = os.path.join(output_dir, filename)
            with open(path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(r.text)
            combined += f"\n/* === {url} === */\n" + r.text
            print(f"  ✅ CSS téléchargé : {filename}")
        except Exception as e:
            print(f"  ❌ Impossible de télécharger {url} : {e}")
    return combined

def extract_component_patterns(soup):
    """Identifie les composants réutilisables (cards, hero, nav...)."""
    components = {}
    
    # Cards d'articles
    cards = soup.find_all("article") or soup.find_all(class_=re.compile(r"card|post-item|article-item"))
    if cards:
        sample = cards[0]
        components["article_card"] = {
            "html_structure": str(sample)[:500],
            "classes": sample.get("class", []),
            "count": len(cards),
        }
    
    # Hero / Banner
    hero = soup.find(class_=re.compile(r"hero|banner|jumbotron|featured"))
    if hero:
        components["hero"] = {
            "classes": hero.get("class", []),
            "html_preview": str(hero)[:300],
        }
    
    # Sidebar
    sidebar = soup.find("aside") or soup.find(class_=re.compile(r"sidebar|widget-area"))
    if sidebar:
        widgets = sidebar.find_all(class_=re.compile(r"widget"))
        components["sidebar"] = {
            "widget_count": len(widgets),
            "widget_types": [w.get("class", []) for w in widgets[:5]],
        }
    
    return components


# ─── MAIN ────────────────────────────────────────────────────────────────────
print("🎨 Extraction du design de baoule.ci...\n")
soup = get_soup(BASE_URL)

css_urls = extract_css_links(soup)
print(f"📎 {len(css_urls)} fichiers CSS trouvés")

inline_styles = extract_inline_styles(soup)
fonts = extract_fonts(soup)
layout = extract_layout_info(soup)
components = extract_component_patterns(soup)

# Télécharger et analyser le CSS
print("\n⬇️  Téléchargement des CSS...")
all_css = download_css(css_urls)
colors = extract_colors(all_css + inline_styles)

# Assembler les design tokens
design_tokens = {
    "site": BASE_URL,
    "theme": "Jannah 2.1.4 (WordPress)",
    "primary_color": "#613942",
    "fonts": fonts,
    "colors_detected": colors[:30],  # top 30
    "css_files": css_urls,
    "layout": layout,
    "components": components,
    "inline_styles_preview": inline_styles[:1000],
}

with open("design_tokens.json", "w", encoding="utf-8") as f:
    json.dump(design_tokens, f, ensure_ascii=False, indent=2)

print("\n✨ design_tokens.json généré")
print(f"   • Couleurs détectées : {len(colors)}")
print(f"   • Polices : {fonts}")
print(f"   • Composants : {list(components.keys())}")

"""
Scraper complet pour baoule.ci
Génère un fichier Markdown structuré avec :
- Hiérarchie du menu
- Titre, URL, catégorie, contenu texte, images de chaque page
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time
import json

BASE_URL = "https://baoule.ci"
DELAY = 0.8  # secondes entre chaque requête (respecter le serveur)

visited = set()
pages = []   # liste ordonnée de dicts
menu_structure = {}  # hiérarchie du menu


def get_soup(url):
    """Récupère et parse une page, retourne None en cas d'erreur."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; SiteDocBot/1.0)"}
        r = requests.get(url, timeout=15, headers=headers)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"  ❌ Erreur sur {url} : {e}")
        return None


def extract_menu(soup):
    """Extrait la structure hiérarchique du menu de navigation."""
    menu = {}
    nav = soup.find("nav") or soup.find("ul", class_=lambda c: c and "menu" in c)
    if not nav:
        return menu

    for top_item in nav.find_all("li", recursive=False):
        top_link = top_item.find("a", recursive=False)
        if not top_link:
            continue
        top_label = top_link.get_text(strip=True)
        top_url = top_link.get("href", "")
        sub_items = []
        sub_menu = top_item.find("ul")
        if sub_menu:
            for sub in sub_menu.find_all("li"):
                a = sub.find("a")
                if a:
                    sub_items.append({
                        "label": a.get_text(strip=True),
                        "url": a.get("href", "")
                    })
        menu[top_label] = {"url": top_url, "children": sub_items}
    return menu


def extract_page_data(url, soup):
    """Extrait toutes les infos utiles d'une page."""
    # Titre
    title = ""
    if soup.title:
        title = soup.title.string.strip()
    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else ""

    # Méta description
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        meta_desc = meta.get("content", "")

    # Catégorie (depuis les breadcrumbs ou les classes body)
    category = ""
    breadcrumb = soup.find(class_=lambda c: c and "breadcrumb" in str(c).lower())
    if breadcrumb:
        crumbs = [a.get_text(strip=True) for a in breadcrumb.find_all("a")]
        category = " > ".join(crumbs)

    # Contenu principal — stratégie par priorité
    content_el = (
        soup.find("article") or
        soup.find("div", class_="entry-content") or
        soup.find("div", class_="post-content") or
        soup.find("main") or
        soup.find("div", id="content")
    )

    sections = []
    images = []

    if content_el:
        # Extraire sections (h2/h3 + paragraphes suivants)
        current_section = {"heading": "", "paragraphs": []}
        for el in content_el.children:
            if not hasattr(el, "name") or not el.name:
                continue
            if el.name in ("h2", "h3"):
                if current_section["paragraphs"] or current_section["heading"]:
                    sections.append(current_section)
                current_section = {"heading": el.get_text(strip=True), "paragraphs": []}
            elif el.name == "p":
                text = el.get_text(strip=True)
                if text:
                    current_section["paragraphs"].append(text)
            elif el.name in ("ul", "ol"):
                items = [li.get_text(strip=True) for li in el.find_all("li")]
                if items:
                    current_section["paragraphs"].append("• " + "\n• ".join(items))
        if current_section["paragraphs"] or current_section["heading"]:
            sections.append(current_section)

        # Extraire les images
        for img in content_el.find_all("img"):
            src = img.get("src", "")
            alt = img.get("alt", "")
            if src:
                images.append({"src": src, "alt": alt})

    # Texte brut complet (fallback)
    full_text = content_el.get_text(separator="\n", strip=True) if content_el else ""

    return {
        "url": url,
        "title": title,
        "h1": h1_text,
        "meta_description": meta_desc,
        "category": category,
        "sections": sections,
        "images": images,
        "full_text": full_text,
    }


def is_internal(url):
    """Vérifie que l'URL appartient au domaine."""
    parsed = urlparse(url)
    return parsed.netloc == "" or BASE_URL in url


def should_skip(url):
    """Ignore les URLs non-contenu."""
    skip_patterns = [
        "wp-login", "wp-admin", "feed", "xmlrpc",
        "random-post", "?s=", "page/", "/tag/", "/author/",
        "mailto:", "javascript:", ".jpg", ".png", ".pdf", ".zip"
    ]
    return any(p in url for p in skip_patterns)


def scrape_site():
    """Crawler principal — utilise une file (BFS) au lieu de la récursion."""
    queue = deque([BASE_URL])
    visited.add(BASE_URL)
    menu_extracted = False

    while queue:
        url = queue.popleft()
        print(f"📄 Scraping : {url}")

        soup = get_soup(url)
        if not soup:
            continue

        # Extraire le menu une seule fois (depuis la homepage)
        if not menu_extracted:
            global menu_structure
            menu_structure = extract_menu(soup)
            menu_extracted = True

        # Extraire les données de la page
        data = extract_page_data(url, soup)
        pages.append(data)

        # Trouver les liens internes à visiter
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            full_url = urljoin(BASE_URL, href).split("#")[0].rstrip("/")
            if (
                full_url not in visited
                and is_internal(full_url)
                and not should_skip(full_url)
                and full_url.startswith("http")
            ):
                visited.add(full_url)
                queue.append(full_url)

        time.sleep(DELAY)

    print(f"\n✅ {len(pages)} pages récupérées.")


def save_markdown(filepath="baoule_site.md"):
    """Sauvegarde toutes les pages en un fichier Markdown structuré."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Documentation complète — baoule.ci\n\n")
        f.write(f"**Pages extraites :** {len(pages)}\n\n")

        # Menu
        if menu_structure:
            f.write("---\n## 🗂️ Structure du Menu\n\n")
            for section, data in menu_structure.items():
                f.write(f"### {section}\n")
                if data.get("url"):
                    f.write(f"URL : {data['url']}\n")
                for child in data.get("children", []):
                    f.write(f"  - [{child['label']}]({child['url']})\n")
                f.write("\n")

        # Contenu de chaque page
        f.write("---\n## 📄 Contenu des Pages\n\n")
        for page in pages:
            f.write(f"\n\n---\n")
            f.write(f"## {page['title'] or page['url']}\n")
            f.write(f"**URL :** {page['url']}\n")
            if page["h1"] and page["h1"] != page["title"]:
                f.write(f"**H1 :** {page['h1']}\n")
            if page["meta_description"]:
                f.write(f"**Description :** {page['meta_description']}\n")
            if page["category"]:
                f.write(f"**Catégorie :** {page['category']}\n")
            f.write("\n")

            # Sections structurées
            if page["sections"]:
                for section in page["sections"]:
                    if section["heading"]:
                        f.write(f"### {section['heading']}\n\n")
                    for para in section["paragraphs"]:
                        f.write(f"{para}\n\n")
            elif page["full_text"]:
                # Fallback texte brut
                f.write(page["full_text"][:3000])
                if len(page["full_text"]) > 3000:
                    f.write("\n\n_[contenu tronqué]_")
                f.write("\n")

            # Images
            if page["images"]:
                f.write("\n**Images :**\n")
                for img in page["images"][:5]:  # max 5 images par page
                    f.write(f"- ![{img['alt']}]({img['src']})\n")

    print(f"📝 Fichier Markdown sauvegardé : {filepath}")


def save_json(filepath="baoule_site.json"):
    """Sauvegarde aussi en JSON pour usage programmatique."""
    output = {
        "site": BASE_URL,
        "total_pages": len(pages),
        "menu": menu_structure,
        "pages": pages,
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"📦 Fichier JSON sauvegardé : {filepath}")


# ─── Lancement ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"🚀 Démarrage du scraping de {BASE_URL}\n")
    scrape_site()
    save_markdown("baoule_site.md")
    save_json("baoule_site.json")
    print("\n✨ Terminé ! Fichiers générés : baoule_site.md et baoule_site.json")

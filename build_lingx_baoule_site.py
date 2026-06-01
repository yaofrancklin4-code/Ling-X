#!/usr/bin/env python3
"""
build_lingx_baoule_site.py
==========================
Script principal pour Claude Code (VS Code).
Génère un site web complet inspiré de baoule.ci + intégration LingX.

Usage (dans Claude Code / terminal VS Code) :
    python build_lingx_baoule_site.py

Structure générée :
    lingx_baoule/
    ├── index.html          → Page d'accueil (hero + articles + sidebar)
    ├── dictionnaire.html   → Dictionnaire interactif Baoulé–Français
    ├── lingx.html          → Tableau de bord LingX (analyse NLP)
    ├── assets/
    │   ├── style.css       → Design global (palette #613942 + or)
    │   ├── main.js         → Interactions, recherche, navigation
    │   └── lingx.js        → Moteur LingX (tokenisation, stats, tfidf)
    └── data/
        ├── dictionnaire.json
        └── corpus.json
"""

import os
import json
import pathlib

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
ROOT = pathlib.Path("lingx_baoule")

PALETTE = {
    "primary":   "#613942",   # rouge baoulé (logo baoule.ci)
    "secondary": "#C9993A",   # or
    "dark":      "#1A0E10",
    "light":     "#FDF6EE",
    "text":      "#2D1A1E",
    "accent":    "#E8C77A",
}

NAV_ITEMS = [
    ("Accueil", "index.html", []),
    ("Histoire", "histoire.html", [
        ("Origines", "histoire.html#origines"),
        ("Reine Abla Pokou", "histoire.html#reine"),
        ("Migration", "histoire.html#migration"),
        ("Chronologie", "histoire.html#chronologie"),
    ]),
    ("Culture", "culture.html", [
        ("Langue Baoulé", "culture.html#langue"),
        ("Art & Masques", "culture.html#art"),
        ("Musique & Danse", "culture.html#musique"),
        ("Fêtes & Rituels", "culture.html#fetes"),
    ]),
    ("Société", "societe.html", [
        ("Organisation", "societe.html#organisation"),
        ("Clans", "societe.html#clans"),
        ("Vie Quotidienne", "societe.html#vie"),
        ("Éducation", "societe.html#education"),
    ]),
    ("Territoire", "territoire.html", [
        ("Géographie", "territoire.html#geo"),
        ("Villages", "territoire.html#villages"),
        ("Ressources", "territoire.html#ressources"),
    ]),
    ("Dictionnaire", "dictionnaire.html", []),
    ("LingX", "lingx.html", []),
]

ARTICLES = [
    {
        "titre":   "Les Origines du Peuple Baoulé",
        "extrait": "Le peuple Baoulé est l'un des groupes ethniques les plus importants de la Côte d'Ivoire. Sa migration depuis le royaume Ashanti au XVIIIe siècle, menée par la Reine Abla Pokou, forge son identité profonde.",
        "categorie": "Histoire",
        "emoji":   "📜",
    },
    {
        "titre":   "La Reine Abla Pokou",
        "extrait": "Figure emblématique du XVIIIe siècle, la Reine Abla Pokou se dresse à la croisée de l'histoire, de la légende et de l'identité nationale ivoirienne. Son sacrifice légendaire au fleuve Comoé reste gravé dans la mémoire collective.",
        "categorie": "Histoire",
        "emoji":   "👑",
    },
    {
        "titre":   "Langue et Expressions Courantes",
        "extrait": "Le baoulé est une langue africaine appartenant à la famille des langues Akan (Tano central), parlée majoritairement en Côte d'Ivoire. Sa phonologie riche et ses tons en font un terrain fascinant pour l'analyse LingX.",
        "categorie": "Culture",
        "emoji":   "🗣️",
    },
    {
        "titre":   "Les Masques Baoulé",
        "extrait": "Les masques Baoulé sont des œuvres d'art sculptées d'une précision remarquable. Utilisés lors de cérémonies rituelles, ils incarnent les esprits de la nature et des ancêtres.",
        "categorie": "Art",
        "emoji":   "🎭",
    },
    {
        "titre":   "Fêtes et Rituels",
        "extrait": "Les Baoulé rythment leur existence par un riche ensemble de fêtes et rituels. Du Dipri aux cérémonies de passage, chaque rite renforce le lien entre le vivant, les ancêtres et la nature.",
        "categorie": "Culture",
        "emoji":   "🥁",
    },
    {
        "titre":   "Organisation Sociale Baoulé",
        "extrait": "La société baoulé repose sur un système de clans matrilinéaires appelés 'lo'. Le village, autour de la case du chef, reste l'unité centrale de la vie collective et des décisions communautaires.",
        "categorie": "Société",
        "emoji":   "🏘️",
    },
]

DICTIONNAIRE = [
    {"baoule": "Ago",        "francais": "Pardon / Excusez-moi",   "categorie": "Politesse"},
    {"baoule": "Mô",         "francais": "Oui",                    "categorie": "Base"},
    {"baoule": "Aïe",        "francais": "Non",                    "categorie": "Base"},
    {"baoule": "Akwaba",     "francais": "Bienvenue",              "categorie": "Politesse"},
    {"baoule": "N'dja",      "francais": "Eau",                    "categorie": "Nature"},
    {"baoule": "Tano",       "francais": "Fleuve / Esprit de l'eau","categorie": "Spirituel"},
    {"baoule": "Blô",        "francais": "Village",                "categorie": "Lieu"},
    {"baoule": "Sran",       "francais": "Être humain / Personne", "categorie": "Société"},
    {"baoule": "Lo",         "francais": "Clan matrilinéaire",     "categorie": "Société"},
    {"baoule": "Kplê",       "francais": "Assemblée / Réunion",    "categorie": "Société"},
    {"baoule": "Awlô",       "francais": "Parole / Discours",      "categorie": "Langue"},
    {"baoule": "Gnalè",      "francais": "La vérité",              "categorie": "Valeur"},
    {"baoule": "Mbra",       "francais": "Force / Puissance",      "categorie": "Valeur"},
    {"baoule": "Ôkô",        "francais": "Homme / Mari",           "categorie": "Famille"},
    {"baoule": "Bla",        "francais": "Femme / Épouse",         "categorie": "Famille"},
    {"baoule": "Ba",         "francais": "Enfant",                 "categorie": "Famille"},
    {"baoule": "Nana",       "francais": "Grand-mère / Ancêtre",   "categorie": "Famille"},
    {"baoule": "Dôlî",       "francais": "Forêt",                  "categorie": "Nature"},
    {"baoule": "Owê",        "francais": "Soleil",                 "categorie": "Nature"},
    {"baoule": "Nyamien",    "francais": "Dieu suprême / Ciel",    "categorie": "Spirituel"},
]

CORPUS_LINGX = [
    {"id": 1, "titre": "Origines Baoulé",    "texte": "Le peuple Baoulé est un peuple Akan de Côte d'Ivoire. La reine Abla Pokou a conduit la migration depuis le royaume Ashanti. Le sacrifice au fleuve Comoé reste fondateur de l'identité baoulé."},
    {"id": 2, "titre": "Langue Baoulé",      "texte": "Le baoulé est une langue tonale de la famille Akan. Les tons haut et bas modifient le sens des mots. La langue baoulé possède une riche tradition orale avec des proverbes et des contes."},
    {"id": 3, "titre": "Art et Masques",     "texte": "Les masques baoulé sont sculptés dans le bois. Ils servent lors des cérémonies rituelles et funèbres. Les figures Waka Sona représentent les époux de l'au-delà dans la cosmogonie baoulé."},
    {"id": 4, "titre": "Société et Clans",   "texte": "La société baoulé est organisée en clans matrilinéaires appelés lo. Le chef de village dirige les assemblées. Les anciens jouent un rôle central dans la transmission des traditions."},
    {"id": 5, "titre": "Spiritualité",       "texte": "Nyamien est le dieu suprême dans la cosmogonie baoulé. Les génies de la nature Asie Usu habitent les forêts et les cours d'eau. Les devins Komien assurent la médiation avec le monde spirituel."},
]


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def mkdir(path): path.mkdir(parents=True, exist_ok=True)

def write(path: pathlib.Path, content: str):
    path.write_text(content, encoding="utf-8")
    print(f"  OK  {path}")


def nav_html(active="index.html"):
    items = ""
    for label, href, submenu in NAV_ITEMS:
        cls = ' class="active"' if href == active else ""
        if submenu:
            submenu_html = "".join(f'<li><a href="{sh}">{sl}</a></li>' for sl, sh in submenu)
            items += f'<li class="has-dropdown"><a href="{href}"{cls}>{label} ▾</a><ul class="dropdown">{submenu_html}</ul></li>\n'
        else:
            items += f'<li><a href="{href}"{cls}>{label}</a></li>\n'
    return f"""
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="index.html">
      <span class="logo-icon">◈</span>
      <span class="logo-text">Baoulé<span class="logo-sub"> × LingX</span></span>
    </a>
    <nav>
      <ul>{items}</ul>
    </nav>
    <button class="menu-toggle" aria-label="Menu">☰</button>
  </div>
</header>"""


def footer_html():
    return """
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <span class="logo-icon">◈</span> Baoulé × LingX
    </div>
    <p class="footer-tagline">
      Préservation du patrimoine linguistique et culturel baoulé — propulsé par LingX
    </p>
    <nav class="footer-nav">
      <a href="index.html">Accueil</a>
      <a href="dictionnaire.html">Dictionnaire</a>
      <a href="lingx.html">LingX</a>
    </nav>
    <p class="footer-copy">© 2026 LingX × Baoulé.ci — Inspiré du peuple Baoulé de Côte d'Ivoire</p>
  </div>
</footer>"""


# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
CSS = f"""
/* ── Reset & Variables ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --primary:   {PALETTE['primary']};
  --secondary: {PALETTE['secondary']};
  --dark:      {PALETTE['dark']};
  --light:     {PALETTE['light']};
  --text:      {PALETTE['text']};
  --accent:    {PALETTE['accent']};
  --radius:    6px;
  --shadow:    0 4px 20px rgba(97,57,66,.15);
  --font-serif: 'Playfair Display', Georgia, serif;
  --font-sans:  'Mulish', system-ui, sans-serif;
}}

html {{ scroll-behavior: smooth; }}
body {{
  font-family: var(--font-sans);
  background: var(--light);
  color: var(--text);
  line-height: 1.7;
}}

/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Mulish:wght@300;400;600;700&display=swap');

/* ── Header ── */
.site-header {{
  position: sticky; top: 0; z-index: 100;
  background: var(--dark);
  border-bottom: 3px solid var(--secondary);
}}
.header-inner {{
  max-width: 1200px; margin: auto;
  display: flex; align-items: center; gap: 2rem;
  padding: .8rem 1.5rem;
}}
.logo {{
  display: flex; align-items: center; gap: .5rem;
  text-decoration: none;
  font-family: var(--font-serif);
  font-size: 1.3rem;
  color: var(--accent);
}}
.logo-icon {{ font-size: 1.6rem; color: var(--secondary); }}
.logo-sub  {{ color: var(--secondary); font-size: .9rem; }}

nav {{ margin-left: auto; }}
nav ul {{ list-style: none; display: flex; gap: 1.5rem; flex-wrap: wrap; }}
nav li {{ position: relative; }}
nav a {{
  color: #d4b896;
  text-decoration: none;
  font-size: .88rem;
  font-weight: 600;
  letter-spacing: .04em;
  text-transform: uppercase;
  padding: .25rem 0;
  border-bottom: 2px solid transparent;
  transition: color .2s, border-color .2s;
  display: block;
}}
nav a:hover, nav a.active {{ color: var(--accent); border-color: var(--secondary); }}

/* Dropdown menu */
.has-dropdown {{ position: relative; }}
.dropdown {{
  position: absolute;
  top: 100%;
  left: 0;
  background: var(--dark);
  min-width: 200px;
  border: 2px solid var(--secondary);
  border-radius: 4px;
  padding: .5rem 0;
  display: none;
  z-index: 1000;
  box-shadow: 0 8px 25px rgba(0,0,0,.4);
}}
.has-dropdown:hover .dropdown {{ display: block; }}
.dropdown li {{ padding: 0; }}
.dropdown a {{
  padding: .6rem 1.2rem;
  font-size: .8rem;
  text-transform: none;
  border: none;
}}
.dropdown a:hover {{ background: var(--primary); color: var(--accent); }}

.menu-toggle {{ display: none; background: none; border: none; color: var(--accent); font-size: 1.5rem; cursor: pointer; }}

/* ── Hero ── */
.hero {{
  background: linear-gradient(135deg, var(--dark) 0%, var(--primary) 60%, #8B4F5A 100%);
  color: white;
  padding: 5rem 1.5rem 4rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}}
.hero::before {{
  content: '';
  position: absolute; inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23C9993A' fill-opacity='0.07'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: .4;
}}
.hero-content {{ position: relative; max-width: 780px; margin: auto; }}
.hero-eyebrow {{
  display: inline-block;
  background: var(--secondary);
  color: var(--dark);
  font-size: .75rem; font-weight: 700;
  letter-spacing: .1em; text-transform: uppercase;
  padding: .3rem 1rem; border-radius: 20px;
  margin-bottom: 1.5rem;
}}
.hero h1 {{
  font-family: var(--font-serif);
  font-size: clamp(2rem, 5vw, 3.5rem);
  line-height: 1.15;
  margin-bottom: 1.2rem;
}}
.hero h1 span {{ color: var(--accent); }}
.hero p {{
  font-size: 1.1rem; opacity: .9;
  max-width: 580px; margin: 0 auto 2rem;
}}
.hero-cta {{
  display: inline-flex; gap: 1rem; flex-wrap: wrap; justify-content: center;
}}
.btn {{
  display: inline-block;
  padding: .75rem 1.8rem;
  border-radius: 3px;
  font-weight: 700; font-size: .9rem;
  text-decoration: none;
  letter-spacing: .05em; text-transform: uppercase;
  transition: transform .2s, box-shadow .2s;
  cursor: pointer; border: none;
}}
.btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.25); }}
.btn-primary  {{ background: var(--secondary); color: var(--dark); }}
.btn-outline  {{ background: transparent; color: white; border: 2px solid rgba(255,255,255,.5); }}
.btn-outline:hover {{ border-color: var(--accent); color: var(--accent); }}

/* ── Layout ── */
.container {{ max-width: 1200px; margin: auto; padding: 0 1.5rem; }}
.page-grid {{
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2.5rem;
  padding: 3rem 1.5rem;
  max-width: 1200px; margin: auto;
}}

/* ── Section titles ── */
.section-title {{
  font-family: var(--font-serif);
  font-size: 1.6rem;
  color: var(--primary);
  border-left: 4px solid var(--secondary);
  padding-left: .8rem;
  margin: 2.5rem 0 1.5rem;
}}

/* ── Article cards ── */
.articles-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}}
.card {{
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  transition: transform .25s, box-shadow .25s;
  display: flex; flex-direction: column;
}}
.card:hover {{
  transform: translateY(-5px);
  box-shadow: 0 12px 35px rgba(97,57,66,.2);
}}
.card-thumb {{
  background: linear-gradient(135deg, var(--primary), #8B4F5A);
  height: 130px;
  display: flex; align-items: center; justify-content: center;
  font-size: 3rem;
}}
.card-body {{ padding: 1.2rem; flex: 1; display: flex; flex-direction: column; }}
.card-cat {{
  font-size: .72rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--secondary); margin-bottom: .4rem;
}}
.card h3 {{
  font-family: var(--font-serif);
  font-size: 1.05rem;
  color: var(--primary);
  margin-bottom: .5rem;
}}
.card p {{ font-size: .88rem; color: #555; flex: 1; }}
.card-link {{
  display: inline-block;
  margin-top: 1rem;
  font-size: .8rem; font-weight: 700;
  color: var(--primary);
  text-decoration: none;
  letter-spacing: .05em; text-transform: uppercase;
}}
.card-link:hover {{ color: var(--secondary); }}

/* ── Sidebar ── */
.sidebar {{ }}
.sidebar-box {{
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.4rem;
  margin-bottom: 1.8rem;
}}
.sidebar-box h4 {{
  font-family: var(--font-serif);
  font-size: 1rem;
  color: var(--primary);
  border-bottom: 2px solid var(--accent);
  padding-bottom: .5rem; margin-bottom: 1rem;
}}
.sidebar-box ul {{ list-style: none; }}
.sidebar-box ul li {{
  padding: .45rem 0;
  border-bottom: 1px solid #f0e8e0;
  font-size: .88rem;
}}
.sidebar-box ul li:last-child {{ border: none; }}
.sidebar-box ul li a {{ color: var(--primary); text-decoration: none; }}
.sidebar-box ul li a:hover {{ color: var(--secondary); }}

/* ── Dictionnaire ── */
.search-bar {{
  display: flex; gap: .8rem; margin-bottom: 1.5rem; flex-wrap: wrap;
}}
.search-bar input {{
  flex: 1; min-width: 200px;
  padding: .7rem 1rem;
  border: 2px solid #e0d0c8;
  border-radius: var(--radius);
  font-family: var(--font-sans); font-size: .95rem;
  outline: none; transition: border-color .2s;
}}
.search-bar input:focus {{ border-color: var(--primary); }}
.filter-btn {{
  padding: .6rem 1.1rem;
  background: var(--light); border: 2px solid #e0d0c8;
  border-radius: var(--radius);
  cursor: pointer; font-size: .82rem; font-weight: 600;
  transition: all .2s;
}}
.filter-btn.active, .filter-btn:hover {{
  background: var(--primary); color: white; border-color: var(--primary);
}}
.dict-table {{ width: 100%; border-collapse: collapse; }}
.dict-table th {{
  background: var(--primary); color: white;
  padding: .7rem 1rem; text-align: left;
  font-size: .85rem; text-transform: uppercase; letter-spacing: .06em;
}}
.dict-table td {{
  padding: .65rem 1rem;
  border-bottom: 1px solid #f0e8e0;
  font-size: .9rem;
}}
.dict-table tr:hover td {{ background: #fdf0e8; }}
.dict-table .baoule-word {{
  font-weight: 700; color: var(--primary);
  font-family: var(--font-serif);
  font-size: 1rem;
}}
.badge {{
  display: inline-block;
  padding: .2rem .6rem;
  border-radius: 20px;
  font-size: .72rem; font-weight: 700;
  background: var(--accent); color: var(--dark);
}}

/* ── LingX Dashboard ── */
.lingx-hero {{
  background: var(--dark);
  color: white;
  padding: 3rem 1.5rem 2rem;
  text-align: center;
}}
.lingx-hero h1 {{
  font-family: var(--font-serif);
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  margin-bottom: .6rem;
}}
.lingx-hero h1 span {{ color: var(--secondary); }}
.lingx-hero p {{ opacity: .8; max-width: 580px; margin: 0 auto; }}

.lingx-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 2rem 1.5rem;
  max-width: 1200px; margin: auto;
}}
.stat-card {{
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  border-top: 4px solid var(--secondary);
}}
.stat-card h3 {{ font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; color: #888; margin-bottom: .4rem; }}
.stat-card .stat-val {{ font-family: var(--font-serif); font-size: 2.2rem; color: var(--primary); }}
.stat-card p {{ font-size: .82rem; color: #666; margin-top: .3rem; }}

.lingx-analyser {{
  max-width: 900px; margin: 0 auto 3rem;
  padding: 0 1.5rem;
}}
.lingx-analyser h2 {{ font-family: var(--font-serif); font-size: 1.5rem; color: var(--primary); margin-bottom: 1rem; }}
.analyser-box {{
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.8rem;
}}
.analyser-box textarea {{
  width: 100%; min-height: 130px;
  padding: .8rem 1rem;
  border: 2px solid #e0d0c8;
  border-radius: var(--radius);
  font-family: var(--font-sans); font-size: .95rem;
  resize: vertical; outline: none;
  transition: border-color .2s;
}}
.analyser-box textarea:focus {{ border-color: var(--primary); }}
.analyser-actions {{ display: flex; gap: .8rem; flex-wrap: wrap; margin-top: 1rem; }}

#lingx-results {{
  margin-top: 1.5rem;
  display: none;
}}
.result-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1.2rem;
}}
.result-pill {{
  background: #fdf0e8;
  border-left: 4px solid var(--secondary);
  border-radius: 4px;
  padding: .8rem 1rem;
}}
.result-pill .rp-label {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; color: #888; }}
.result-pill .rp-val {{ font-size: 1.3rem; font-weight: 700; color: var(--primary); }}

.tokens-box {{
  display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .8rem;
}}
.token-chip {{
  background: var(--primary); color: white;
  padding: .2rem .6rem;
  border-radius: 20px; font-size: .8rem;
}}
.token-chip.stopword {{ background: #bbb; }}
.corpus-item {{
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.2rem 1.4rem;
  margin-bottom: 1rem;
  cursor: pointer;
  border-left: 4px solid transparent;
  transition: border-color .2s;
}}
.corpus-item:hover, .corpus-item.selected {{ border-color: var(--secondary); }}
.corpus-item h4 {{ font-family: var(--font-serif); color: var(--primary); margin-bottom: .3rem; }}
.corpus-item p {{ font-size: .87rem; color: #666; }}

/* ── Footer ── */
.site-footer {{
  background: var(--dark);
  color: #b09a90;
  padding: 3rem 1.5rem 2rem;
  margin-top: 4rem;
  text-align: center;
}}
.footer-inner {{ max-width: 700px; margin: auto; }}
.footer-brand {{
  font-family: var(--font-serif);
  font-size: 1.4rem;
  color: var(--accent);
  margin-bottom: .6rem;
}}
.footer-tagline {{ font-size: .88rem; margin-bottom: 1.2rem; opacity: .8; }}
.footer-nav {{ display: flex; gap: 1.5rem; justify-content: center; margin-bottom: 1.2rem; }}
.footer-nav a {{ color: var(--accent); text-decoration: none; font-size: .85rem; }}
.footer-copy {{ font-size: .78rem; opacity: .6; }}

/* ── Responsive ── */
@media (max-width: 768px) {{
  .page-grid {{ grid-template-columns: 1fr; }}
  nav ul {{ display: none; }}
  .menu-toggle {{ display: block; }}
  nav.open ul {{ display: flex; flex-direction: column; gap: .5rem; padding: 1rem 0; }}
}}
"""


# ─────────────────────────────────────────────
# JS PRINCIPAL
# ─────────────────────────────────────────────
JS_MAIN = """
// Navigation mobile
const toggle = document.querySelector('.menu-toggle');
const nav    = document.querySelector('nav');
if (toggle) toggle.addEventListener('click', () => nav.classList.toggle('open'));

// Recherche dictionnaire
const searchInput = document.getElementById('dict-search');
const filterBtns  = document.querySelectorAll('.filter-btn');
const tableRows   = document.querySelectorAll('.dict-row');

function filterTable() {
  const q   = searchInput ? searchInput.value.toLowerCase() : '';
  const cat = document.querySelector('.filter-btn.active')?.dataset.cat || 'all';
  tableRows.forEach(row => {
    const text = row.textContent.toLowerCase();
    const rowCat = row.dataset.cat || '';
    const matchQ   = text.includes(q);
    const matchCat = cat === 'all' || rowCat === cat;
    row.style.display = (matchQ && matchCat) ? '' : 'none';
  });
}

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    filterTable();
  });
});
if (searchInput) searchInput.addEventListener('input', filterTable);
"""

# ─────────────────────────────────────────────
# JS LINGX — moteur NLP léger
# ─────────────────────────────────────────────
JS_LINGX = """
// ── LingX Engine (client-side NLP pour le baoulé/français) ──

const STOPWORDS_FR = new Set([
  'le','la','les','un','une','des','de','du','et','en','au','aux',
  'est','sont','a','il','elle','ils','elles','je','tu','nous','vous',
  'ce','se','sa','son','ses','si','ou','mais','donc','or','ni','car',
  'que','qui','dont','où','par','pour','sur','sous','avec','dans','sans',
  'plus','très','bien','tout','cette','ces','mon','ton','leur','leurs',
  'être','avoir','faire','dire','aller','voir','pouvoir','vouloir',
  'l\'','d\'','n\'','s\'','j\'','c\'',
]);

function tokenize(text) {
  return text.toLowerCase()
    .replace(/[.,!?;:«»"'(){}\\[\\]]/g, ' ')
    .split(/\\s+/)
    .filter(t => t.length > 1);
}

function countSyllables(word) {
  const vowels = word.match(/[aeiouyéèêëàâîïôùûü]/gi);
  return vowels ? vowels.length : 1;
}

function readabilityScore(text) {
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const tokens    = tokenize(text).filter(t => !STOPWORDS_FR.has(t));
  if (!sentences.length || !tokens.length) return 0;
  const avgWords     = tokens.length / sentences.length;
  const avgSyllables = tokens.reduce((s, t) => s + countSyllables(t), 0) / tokens.length;
  // Flesch-Kincaid adapté (approximation)
  const score = 206.835 - 1.015 * avgWords - 84.6 * avgSyllables;
  return Math.max(0, Math.min(100, Math.round(score)));
}

function tfidf(term, doc, allDocs) {
  const tokens = tokenize(doc);
  const tf = tokens.filter(t => t === term).length / tokens.length;
  const docsWithTerm = allDocs.filter(d => tokenize(d).includes(term)).length;
  const idf = Math.log((allDocs.length + 1) / (docsWithTerm + 1)) + 1;
  return +(tf * idf).toFixed(4);
}

function topKeywords(text, n = 8) {
  const tokens  = tokenize(text);
  const content = tokens.filter(t => !STOPWORDS_FR.has(t) && t.length > 3);
  const freq    = {};
  content.forEach(t => freq[t] = (freq[t] || 0) + 1);
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, n)
    .map(([w, c]) => ({ word: w, count: c }));
}

function analyseText(text) {
  const tokens    = tokenize(text);
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const words     = tokens.filter(t => !STOPWORDS_FR.has(t) && t.length > 1);
  const types     = new Set(words);
  const ttr       = words.length ? +(types.size / words.length).toFixed(3) : 0;
  const readab    = readabilityScore(text);
  const keywords  = topKeywords(text);
  return {
    tokens, sentences, words,
    nTokens:    tokens.length,
    nSentences: sentences.length,
    nTypes:     types.size,
    ttr,
    readab,
    keywords,
    avgWordLen: +(tokens.reduce((s, t) => s + t.length, 0) / (tokens.length || 1)).toFixed(1),
  };
}

// ── UI ──
const corpusData = window.CORPUS || [];

function renderResults(stats) {
  const box = document.getElementById('lingx-results');
  if (!box) return;
  box.style.display = 'block';

  const kwHtml = stats.keywords.map(k =>
    `<span class="token-chip">${k.word} <b>(${k.count})</b></span>`
  ).join('');

  const tokHtml = stats.tokens.slice(0, 60).map(t =>
    `<span class="token-chip ${STOPWORDS_FR.has(t) ? 'stopword' : ''}">${t}</span>`
  ).join('');

  box.innerHTML = `
    <div class="result-grid">
      <div class="result-pill"><div class="rp-label">Tokens</div><div class="rp-val">${stats.nTokens}</div></div>
      <div class="result-pill"><div class="rp-label">Phrases</div><div class="rp-val">${stats.nSentences}</div></div>
      <div class="result-pill"><div class="rp-label">Types uniques</div><div class="rp-val">${stats.nTypes}</div></div>
      <div class="result-pill"><div class="rp-label">TTR (richesse)</div><div class="rp-val">${stats.ttr}</div></div>
      <div class="result-pill"><div class="rp-label">Lisibilité</div><div class="rp-val">${stats.readab}/100</div></div>
      <div class="result-pill"><div class="rp-label">Long. moy. mot</div><div class="rp-val">${stats.avgWordLen}</div></div>
    </div>
    <h4 style="color:var(--primary);margin:.8rem 0 .4rem;font-family:var(--font-serif)">Mots-clés détectés</h4>
    <div class="tokens-box">${kwHtml}</div>
    <h4 style="color:var(--primary);margin:.8rem 0 .4rem;font-family:var(--font-serif)">Tokens (60 premiers — gris = mot vide)</h4>
    <div class="tokens-box">${tokHtml}</div>
  `;
}

document.addEventListener('DOMContentLoaded', () => {
  const analyseBtn = document.getElementById('btn-analyse');
  const clearBtn   = document.getElementById('btn-clear');
  const textarea   = document.getElementById('lingx-input');
  const results    = document.getElementById('lingx-results');

  // Corpus items
  const corpusItems = document.querySelectorAll('.corpus-item');
  corpusItems.forEach(item => {
    item.addEventListener('click', () => {
      corpusItems.forEach(i => i.classList.remove('selected'));
      item.classList.add('selected');
      if (textarea) textarea.value = item.dataset.texte || '';
    });
  });

  if (analyseBtn) {
    analyseBtn.addEventListener('click', () => {
      const text = textarea?.value.trim();
      if (!text) { alert('Veuillez entrer ou sélectionner un texte.'); return; }
      const stats = analyseText(text);
      renderResults(stats);
    });
  }
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (textarea) textarea.value = '';
      if (results)  { results.style.display = 'none'; results.innerHTML = ''; }
      corpusItems.forEach(i => i.classList.remove('selected'));
    });
  }
});
"""


# ─────────────────────────────────────────────
# PAGE : index.html
# ─────────────────────────────────────────────
def build_index():
    cards_html = ""
    for a in ARTICLES:
        cards_html += f"""
        <article class="card">
          <div class="card-thumb">{a['emoji']}</div>
          <div class="card-body">
            <div class="card-cat">{a['categorie']}</div>
            <h3>{a['titre']}</h3>
            <p>{a['extrait']}</p>
            <a href="#" class="card-link">Lire la suite →</a>
          </div>
        </article>"""

    trending = "".join(
        f'<li><a href="#">{a["titre"]}</a></li>' for a in ARTICLES[:5]
    )

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Baoulé × LingX — Histoire &amp; Culture du Peuple Baoulé</title>
  <link rel="stylesheet" href="assets/style.css"/>
</head>
<body>

{nav_html("index.html")}

<!-- HERO -->
<section class="hero">
  <div class="hero-content">
    <div class="hero-eyebrow">✦ Patrimoine &amp; Linguistique ✦</div>
    <h1>Histoire &amp; Culture du<br><span>Peuple Baoulé</span></h1>
    <p>Explorez la richesse culturelle, historique et linguistique du peuple Baoulé de Côte d'Ivoire — enrichie par le moteur d'analyse <strong>LingX</strong>.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="dictionnaire.html">Dictionnaire Baoulé</a>
      <a class="btn btn-outline"  href="lingx.html">Analyser avec LingX</a>
    </div>
  </div>
</section>

<!-- CONTENU PRINCIPAL -->
<div class="page-grid">
  <main>
    <h2 class="section-title" id="histoire">À la Une</h2>
    <div class="articles-grid">
      {cards_html}
    </div>
  </main>

  <aside class="sidebar">
    <div class="sidebar-box">
      <h4>Tendances</h4>
      <ul>{trending}</ul>
    </div>

    <div class="sidebar-box">
      <h4>⚡ LingX Quick</h4>
      <p style="font-size:.85rem;margin-bottom:1rem;color:#666">
        Analysez un mot ou une phrase en baoulé instantanément.
      </p>
      <input id="quick-input" type="text" placeholder="Entrez un mot baoulé…"
             style="width:100%;padding:.6rem;border:2px solid #e0d0c8;border-radius:4px;font-size:.9rem;margin-bottom:.6rem;outline:none"/>
      <button class="btn btn-primary" style="width:100%;font-size:.82rem"
              onclick="document.getElementById('quick-result').textContent=
                       'Tokens: '+document.getElementById('quick-input').value.toLowerCase().split(/\\s+/).filter(t=>t).length">
        Analyser
      </button>
      <p id="quick-result" style="margin-top:.6rem;font-size:.85rem;color:var(--primary);font-weight:700"></p>
      <a href="lingx.html" style="font-size:.8rem;color:var(--secondary)">→ Analyse complète</a>
    </div>

    <div class="sidebar-box">
      <h4>Mots du Jour</h4>
      <ul>
        <li><strong>Akwaba</strong> — Bienvenue</li>
        <li><strong>Nyamien</strong> — Dieu suprême</li>
        <li><strong>Tano</strong> — Esprit du fleuve</li>
        <li><strong>Sran</strong> — Être humain</li>
        <li><strong>Gnalè</strong> — La vérité</li>
      </ul>
      <a href="dictionnaire.html" class="card-link" style="display:block;margin-top:.8rem">
        Voir tout le dictionnaire →
      </a>
    </div>
  </aside>
</div>

{footer_html()}

<script src="assets/main.js"></script>
</body>
</html>
"""


# ─────────────────────────────────────────────
# PAGE : dictionnaire.html
# ─────────────────────────────────────────────
def build_dictionnaire():
    categories = sorted(set(d["categorie"] for d in DICTIONNAIRE))
    filter_btns = '<button class="filter-btn active" data-cat="all">Tout</button>'
    filter_btns += "".join(
        f'<button class="filter-btn" data-cat="{c}">{c}</button>'
        for c in categories
    )
    rows = ""
    for d in DICTIONNAIRE:
        rows += f"""
        <tr class="dict-row" data-cat="{d['categorie']}">
          <td class="baoule-word">{d['baoule']}</td>
          <td>{d['francais']}</td>
          <td><span class="badge">{d['categorie']}</span></td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Dictionnaire Baoulé × LingX</title>
  <link rel="stylesheet" href="assets/style.css"/>
</head>
<body>

{nav_html("dictionnaire.html")}

<section class="hero" style="padding:3rem 1.5rem 2.5rem">
  <div class="hero-content">
    <div class="hero-eyebrow">◈ LingX Lexique</div>
    <h1>Dictionnaire <span>Baoulé–Français</span></h1>
    <p>Recherchez, filtrez et explorez le vocabulaire baoulé enrichi par LingX.</p>
  </div>
</section>

<div class="container" style="padding-top:2rem;padding-bottom:3rem">
  <div class="search-bar">
    <input id="dict-search" type="text" placeholder="🔍  Rechercher un mot baoulé ou français…"/>
    {filter_btns}
  </div>
  <div style="background:white;border-radius:6px;box-shadow:var(--shadow);overflow:hidden">
    <table class="dict-table">
      <thead>
        <tr>
          <th>Baoulé</th>
          <th>Français</th>
          <th>Catégorie</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
  <p style="margin-top:1.2rem;font-size:.82rem;color:#888">
    {len(DICTIONNAIRE)} entrées — utilisez <a href="lingx.html" style="color:var(--secondary)">LingX</a> pour analyser un texte complet en baoulé.
  </p>
</div>

{footer_html()}

<script src="assets/main.js"></script>
</body>
</html>
"""


# ─────────────────────────────────────────────
# PAGE : lingx.html
# ─────────────────────────────────────────────
def build_lingx():
    corpus_items_html = ""
    for doc in CORPUS_LINGX:
        corpus_items_html += f"""
        <div class="corpus-item" data-texte="{doc['texte'].replace('"', '&quot;')}">
          <h4>{doc['titre']}</h4>
          <p>{doc['texte'][:100]}…</p>
        </div>"""

    total_tokens = sum(len(d["texte"].split()) for d in CORPUS_LINGX)
    total_types  = len(set(
        w.lower() for d in CORPUS_LINGX for w in d["texte"].split()
    ))

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>LingX — Analyse Linguistique Baoulé</title>
  <link rel="stylesheet" href="assets/style.css"/>
</head>
<body>

{nav_html("lingx.html")}

<section class="lingx-hero">
  <div class="hero-eyebrow" style="background:var(--secondary);color:var(--dark);display:inline-block;padding:.3rem 1rem;border-radius:20px;font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:1rem">
    ⚡ Moteur NLP
  </div>
  <h1>Ling<span>X</span> — Analyse Linguistique</h1>
  <p>Tokenisation, richesse lexicale (TTR), lisibilité Flesch-Kincaid, TF-IDF et extraction de mots-clés — appliqués au patrimoine baoulé.</p>
</section>

<!-- STATS GLOBALES -->
<div class="lingx-grid">
  <div class="stat-card">
    <h3>Documents corpus</h3>
    <div class="stat-val">{len(CORPUS_LINGX)}</div>
    <p>Textes baoulé indexés</p>
  </div>
  <div class="stat-card">
    <h3>Tokens totaux</h3>
    <div class="stat-val">{total_tokens}</div>
    <p>Mots dans le corpus</p>
  </div>
  <div class="stat-card">
    <h3>Types uniques</h3>
    <div class="stat-val">{total_types}</div>
    <p>Vocabulaire distinct</p>
  </div>
  <div class="stat-card">
    <h3>Entrées dico</h3>
    <div class="stat-val">{len(DICTIONNAIRE)}</div>
    <p>Mots Baoulé–Français</p>
  </div>
</div>

<!-- ANALYSEUR -->
<div class="lingx-analyser">
  <h2 class="section-title">🔬 Analyser un Texte</h2>
  <div class="analyser-box">
    <p style="font-size:.88rem;color:#666;margin-bottom:.8rem">
      Collez un texte ci-dessous <strong>ou cliquez sur un document du corpus</strong> pour l'analyser automatiquement.
    </p>
    <textarea id="lingx-input" placeholder="Entrez votre texte en français ou en baoulé ici…"></textarea>
    <div class="analyser-actions">
      <button id="btn-analyse" class="btn btn-primary">⚡ Analyser</button>
      <button id="btn-clear"   class="btn btn-outline" style="color:var(--primary);border-color:var(--primary)">✕ Effacer</button>
    </div>
    <div id="lingx-results"></div>
  </div>

  <!-- CORPUS -->
  <h2 class="section-title" style="margin-top:2.5rem">📚 Corpus Baoulé</h2>
  <p style="font-size:.88rem;color:#666;margin-bottom:1rem">Cliquez sur un document pour le charger dans l'analyseur.</p>
  {corpus_items_html}
</div>

{footer_html()}

<script src="assets/main.js"></script>
<script src="assets/lingx.js"></script>
</body>
</html>
"""


# ─────────────────────────────────────────────
# NOUVELLES PAGES
# ─────────────────────────────────────────────
def build_histoire():
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Histoire du Peuple Baoulé</title>
  <link rel="stylesheet" href="assets/style.css"/>
</head>
<body>
{nav_html("histoire.html")}
<section class="hero" style="padding:3rem 1.5rem 2rem">
  <div class="hero-content">
    <h1>Histoire du <span>Peuple Baoulé</span></h1>
    <p>De la migration légendaire aux royaumes modernes</p>
  </div>
</section>
<div class="container" style="padding:3rem 1.5rem">
  <section id="origines" style="margin-bottom:3rem">
    <h2 class="section-title">📜 Les Origines</h2>
    <p>Le peuple Baoulé est issu du grand groupe Akan d'Afrique de l'Ouest. Au XVIIIe siècle, suite à des conflits de succession au sein du royaume Ashanti (actuel Ghana), une partie de la population décide de migrer vers l'ouest.</p>
    <p>Cette migration, menée par la Reine Abla Pokou, marque la naissance du peuple Baoulé en Côte d'Ivoire. Le nom "Baoulé" signifie "l'enfant est mort" en référence au sacrifice légendaire.</p>
  </section>
  <section id="reine" style="margin-bottom:3rem">
    <h2 class="section-title">👑 La Reine Abla Pokou</h2>
    <p>Abla Pokou était une princesse du royaume Ashanti. Face aux persécutions, elle organise l'exode de son peuple vers l'ouest. Arrivée au fleuve Comoé en crue, elle sacrifie son fils unique pour permettre la traversée miraculeuse.</p>
    <p>Ce sacrifice fonde l'identité baoulé et fait d'Abla Pokou une figure mythique, symbole de courage et de dévouement maternel envers son peuple.</p>
  </section>
  <section id="migration" style="margin-bottom:3rem">
    <h2 class="section-title">🗺️ La Grande Migration</h2>
    <p>La migration s'est déroulée vers 1730-1760. Le peuple Baoulé traverse le fleuve Comoé et s'installe dans la région centrale de l'actuelle Côte d'Ivoire, entre Bouaké et Yamoussoukro.</p>
    <p>Ils établissent plusieurs royaumes et chefferies, maintenant leur organisation sociale Akan tout en s'adaptant à leur nouvel environnement.</p>
  </section>
  <section id="chronologie">
    <h2 class="section-title">📅 Chronologie</h2>
    <ul style="line-height:2">
      <li><strong>~1730-1760</strong> : Migration depuis le royaume Ashanti</li>
      <li><strong>XVIIIe siècle</strong> : Installation en Côte d'Ivoire centrale</li>
      <li><strong>XIXe siècle</strong> : Consolidation des royaumes baoulé</li>
      <li><strong>1893-1911</strong> : Résistance contre la colonisation française</li>
      <li><strong>1960</strong> : Indépendance de la Côte d'Ivoire</li>
      <li><strong>Aujourd'hui</strong> : Plus de 4 millions de Baoulé</li>
    </ul>
  </section>
</div>
{footer_html()}
<script src="assets/main.js"></script>
</body>
</html>
"""

def build_culture():
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Culture Baoulé</title>
  <link rel="stylesheet" href="assets/style.css"/>
</head>
<body>
{nav_html("culture.html")}
<section class="hero" style="padding:3rem 1.5rem 2rem">
  <div class="hero-content">
    <h1>Culture <span>Baoulé</span></h1>
    <p>Art, langue, musique et traditions ancestrales</p>
  </div>
</section>
<div class="container" style="padding:3rem 1.5rem">
  <section id="langue" style="margin-bottom:3rem">
    <h2 class="section-title">🗣️ Langue Baoulé</h2>
    <p>Le baoulé est une langue tonale de la famille Akan. Elle utilise des tons hauts et bas qui changent le sens des mots. Parlée par plus de 4 millions de personnes, c'est l'une des principales langues de Côte d'Ivoire.</p>
    <p>La langue possède une riche tradition orale avec proverbes, contes et chants transmis de génération en génération.</p>
  </section>
  <section id="art" style="margin-bottom:3rem">
    <h2 class="section-title">🎭 Art & Masques</h2>
    <p>Les masques baoulé sont mondialement reconnus pour leur finesse et leur beauté. Sculptés dans le bois, ils représentent des visages humains idéalisés avec des traits délicats.</p>
    <p><strong>Types de masques :</strong></p>
    <ul>
      <li><strong>Goli</strong> : Masque circulaire utilisé lors des funérailles</li>
      <li><strong>Mblo</strong> : Portrait masque représentant une personne réelle</li>
      <li><strong>Bonu Amuen</strong> : Masque de buffle pour les cérémonies</li>
    </ul>
  </section>
  <section id="musique" style="margin-bottom:3rem">
    <h2 class="section-title">🥁 Musique & Danse</h2>
    <p>La musique baoulé utilise des instruments traditionnels comme le balafon, les tambours parlants et les hochets. Chaque rythme a une signification précise et peut transmettre des messages.</p>
    <p>Les danses accompagnent toutes les cérémonies importantes : naissances, mariages, funérailles et fêtes des récoltes.</p>
  </section>
  <section id="fetes">
    <h2 class="section-title">🎉 Fêtes & Rituels</h2>
    <p><strong>Principales célébrations :</strong></p>
    <ul>
      <li><strong>Dipri</strong> : Fête de purification et de renouveau</li>
      <li><strong>Fête des ignames</strong> : Célébration des récoltes</li>
      <li><strong>Cérémonies funéraires</strong> : Hommage aux ancêtres</li>
      <li><strong>Initiations</strong> : Passage à l'âge adulte</li>
    </ul>
  </section>
</div>
{footer_html()}
<script src="assets/main.js"></script>
</body>
</html>
"""

def build_societe():
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Société Baoulé</title>
  <link rel="stylesheet" href="assets/style.css"/>
</head>
<body>
{nav_html("societe.html")}
<section class="hero" style="padding:3rem 1.5rem 2rem">
  <div class="hero-content">
    <h1>Société <span>Baoulé</span></h1>
    <p>Organisation sociale, clans et vie quotidienne</p>
  </div>
</section>
<div class="container" style="padding:3rem 1.5rem">
  <section id="organisation" style="margin-bottom:3rem">
    <h2 class="section-title">🏘️ Organisation Sociale</h2>
    <p>La société baoulé est organisée de manière hiérarchique avec le chef de village au sommet. Le conseil des anciens joue un rôle consultatif important dans les décisions communautaires.</p>
    <p>Le village (blô) est l'unité de base, regroupant plusieurs familles étendues autour de la case du chef.</p>
  </section>
  <section id="clans" style="margin-bottom:3rem">
    <h2 class="section-title">👥 Les Clans (Lo)</h2>
    <p>Le système de clans matrilinéaires (lo) structure la société baoulé. L'appartenance au clan se transmet par la mère. Chaque clan a son totem animal et ses interdits alimentaires.</p>
    <p><strong>Principaux clans :</strong> Nananfouè, Aïtou, Faafouè, Saafouè, Warèbo, etc.</p>
  </section>
  <section id="vie" style="margin-bottom:3rem">
    <h2 class="section-title">🌾 Vie Quotidienne</h2>
    <p>L'agriculture est l'activité principale : igname, manioc, plantain, cacao et café. Les femmes s'occupent des cultures vivrières et du commerce, les hommes des cultures de rente.</p>
    <p>L'artisanat (sculpture, tissage, poterie) occupe aussi une place importante dans l'économie locale.</p>
  </section>
  <section id="education">
    <h2 class="section-title">📚 Éducation</h2>
    <p>L'éducation traditionnelle se fait par transmission orale. Les enfants apprennent les valeurs, l'histoire et les savoir-faire auprès des anciens.</p>
    <p>Aujourd'hui, l'éducation moderne coexiste avec les enseignements traditionnels, préservant ainsi le patrimoine culturel.</p>
  </section>
</div>
{footer_html()}
<script src="assets/main.js"></script>
</body>
</html>
"""

def build_territoire():
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>Territoire Baoulé</title>
  <link rel="stylesheet" href="assets/style.css"/>
</head>
<body>
{nav_html("territoire.html")}
<section class="hero" style="padding:3rem 1.5rem 2rem">
  <div class="hero-content">
    <h1>Territoire <span>Baoulé</span></h1>
    <p>Géographie, villages et ressources naturelles</p>
  </div>
</section>
<div class="container" style="padding:3rem 1.5rem">
  <section id="geo" style="margin-bottom:3rem">
    <h2 class="section-title">🗺️ Géographie</h2>
    <p>Le pays Baoulé occupe le centre de la Côte d'Ivoire, dans une zone de forêt dense et de savane. Il s'étend principalement dans les régions du Bélier, du Gbêkê, de l'Iffou et du N'Zi.</p>
    <p><strong>Villes principales :</strong> Bouaké, Yamoussoukro (capitale politique), Dimbokro, Toumodi, Béoumi.</p>
  </section>
  <section id="villages" style="margin-bottom:3rem">
    <h2 class="section-title">🏡 Villages</h2>
    <p>Les villages baoulé sont organisés autour de la case du chef. Les habitations traditionnelles sont en terre battue avec des toits de chaume ou de tôle.</p>
    <p>Chaque village possède une place centrale pour les assemblées et les cérémonies, ainsi qu'un bois sacré où se déroulent les rituels.</p>
  </section>
  <section id="ressources">
    <h2 class="section-title">🌿 Ressources</h2>
    <p><strong>Agriculture :</strong> Igname, manioc, plantain, maïs, cacao, café, anacarde</p>
    <p><strong>Forêt :</strong> Bois précieux, plantes médicinales, gibier</p>
    <p><strong>Artisanat :</strong> Sculpture sur bois, tissage, poterie, vannerie</p>
    <p>Le territoire baoulé est riche en ressources naturelles qui soutiennent l'économie locale et nationale.</p>
  </section>
</div>
{footer_html()}
<script src="assets/main.js"></script>
</body>
</html>
"""

# ─────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────
def main():
    print("\nLingX x Baoule - Generation du site\n" + "-"*45)

    # Dossiers
    for d in [ROOT / "assets", ROOT / "data"]:
        mkdir(d)

    # CSS & JS
    write(ROOT / "assets" / "style.css", CSS)
    write(ROOT / "assets" / "main.js",   JS_MAIN)
    write(ROOT / "assets" / "lingx.js",  JS_LINGX)

    # Data JSON
    write(ROOT / "data" / "dictionnaire.json", json.dumps(DICTIONNAIRE, ensure_ascii=False, indent=2))
    write(ROOT / "data" / "corpus.json",       json.dumps(CORPUS_LINGX,  ensure_ascii=False, indent=2))

    # Pages HTML
    write(ROOT / "index.html",        build_index())
    write(ROOT / "dictionnaire.html", build_dictionnaire())
    write(ROOT / "lingx.html",        build_lingx())
    write(ROOT / "histoire.html",     build_histoire())
    write(ROOT / "culture.html",      build_culture())
    write(ROOT / "societe.html",      build_societe())
    write(ROOT / "territoire.html",   build_territoire())

    print("\n" + "-"*45)
    print("Site genere dans le dossier :", ROOT.resolve())
    print("\nStructure :")
    for f in sorted(ROOT.rglob("*")):
        if f.is_file():
            size = f.stat().st_size
            print(f"    {str(f.relative_to(ROOT)):40s} {size:>6} octets")

    print("\nPour lancer localement :")
    print(f"    cd {ROOT}")
    print("    python -m http.server 8000")
    print("    -> http://localhost:8000\n")


if __name__ == "__main__":
    main()

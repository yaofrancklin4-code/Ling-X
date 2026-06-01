#  Guide — Reproduire baoule.ci avec Claude (VS Code)

## Ce qu'il faut extraire et comment l'utiliser

---

## ️ Les 3 scripts à exécuter dans l'ordre

```bash
pip install requests beautifulsoup4

# 1. Contenu (texte, structure, menu)
python scrape_baoule.py

# 2. Design (CSS, couleurs, polices, composants)
python extract_design.py

# 3. Images (logos, photos, illustrations)
python extract_images.py
```

---

##  Fichiers générés

| Fichier | Contenu | Usage dans Claude |
|---|---|---|
| `baoule_site.md` | Tout le texte de chaque page | Copier-coller dans le chat |
| `baoule_site.json` | Idem en JSON structuré | `@baoule_site.json` dans Claude Code |
| `design_tokens.json` | Couleurs, polices, layout | `@design_tokens.json` |
| `media_inventory.json` | Liste de toutes les images | Référence pour les assets |
| `assets/*.css` | Fichiers CSS originaux | `@assets/` dans Claude Code |
| `images/` | Toutes les images téléchargées | Dossier assets du projet |

---

##  Comment utiliser dans Claude Code (VS Code)

### Option A — Projet complet (recommandé)
Ouvre le dossier dans VS Code avec Claude Code actif, puis tape :

```
@baoule_site.json @design_tokens.json

Reproduis ce site web sous forme d'application Next.js.
Structure :
- Page d'accueil avec hero et grille d'articles
- Pages Histoire, Culture, Société, Territoire
- Navigation avec menu déroulant
- Design fidèle : couleur principale #613942, thème sombre/chaud
- Contenu en français, peuple Baoulé
```

### Option B — Page par page
```
@baoule_site.md

En te basant sur ce contenu, crée la page "Histoire" 
avec les sections : Origines, Royaume, Colonisation, Figures historiques.
Stack : React + Tailwind CSS
```

### Option C — Fonctionnalité spécifique
```
@baoule_site.json

Le site a une page "Dictionnaire Baoulé" (/dictionnaire-baoule/).
Crée un composant React avec :
- Champ de recherche
- Filtre par lettre
- Affichage mot baoulé → traduction française
```

---

##  Design tokens à mémoriser pour Claude

Copie-colle ça en début de conversation :

```
Site : baoule.ci (culture du peuple Baoulé, Côte d'Ivoire)
Thème WordPress : Jannah 2.1.4
Couleur principale : #613942 (bordeaux/brun)
Couleur méta thème : #613942
Style général : chaleureux, culturel, éditorial
Langue : Français
Sections : Histoire | Culture | Société | Territoire | Baoule+
Fonctionnalités spéciales :
  - Dictionnaire Baoulé (recherche de mots)
  - Générateur de prénom Baoulé
  - Compteur interactif en langue Baoulé
  - Contes de Tano Kan (série de récits)
  - Infographie société Baoulé
```

---

## ⚠️ Limites de la reproduction

- **Images** : les photos d'archives sont probablement sous droits → remplacer par des illustrations libres
- **Dictionnaire** : la base de données des mots n'est pas extractible facilement (requiert le dump SQL WordPress)
- **Prénoms** : même chose, logique côté serveur
- **Commentaires** : nécessite un backend (remplacer par Disqus ou système statique)

---

##  Prompt optimal pour Claude Code

```
Je veux reproduire le site baoule.ci, un site éditorial WordPress 
sur le peuple Baoulé de Côte d'Ivoire.

Voici les fichiers d'extraction :
- @baoule_site.json : contenu de toutes les pages
- @design_tokens.json : design du site original

Crée un projet Next.js 14 (App Router) avec :
1. Layout principal avec header/nav/footer fidèles au design
2. Page d'accueil avec les 10 derniers articles
3. Pages statiques pour chaque section du menu
4. Composant ArticleCard réutilisable
5. Page article individuelle avec table des matières
6. Couleur #613942, police sans-serif élégante
7. Responsive mobile first

Génère d'abord la structure des fichiers, puis implémente page par page.
```

"""
setup_dictionnaire_baoule.py
=============================
Script tout-en-un pour le projet LingX (Django).

Ce script effectue deux tâches dans l'ordre :
  TÂCHE 1 — Corrige lingx/views.py
    • Remplace dictionary_view pour qu'elle lise DictionaryEntry (les mots officiels)
    • Neutralise les HttpResponse de debug qui affichent du code dans les pages

  TÂCHE 2 — Réinitialise le dictionnaire en base de données
    • Supprime tout le contenu existant de DictionaryEntry
    • Supprime les Vocabulary sans leçon (orphelins)
    • Insère exactement les 16 mots Baoulé-Français officiels

UTILISATION :
    Placer ce fichier dans monprojet/ (dossier contenant manage.py et lingx/)
    puis exécuter :
        python setup_dictionnaire_baoule.py

COMPATIBLE : Python 3.8+, Django 3.x / 4.x / 5.x
"""

import os
import re
import sys
import shutil
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIGURATION — modifier uniquement ces deux lignes si besoin
# ══════════════════════════════════════════════════════════════════════════════

DJANGO_SETTINGS = "monprojet.settings"   # chemin Python vers settings.py
VIEWS_PATH      = Path(__file__).parent / "lingx" / "views.py"

# ══════════════════════════════════════════════════════════════════════════════
#  DICTIONNAIRE OFFICIEL — 16 mots Baoulé-Français (ne pas modifier)
# ══════════════════════════════════════════════════════════════════════════════

MOTS_OFFICIELS = [
    {"francais": "Bonjour",          "baoule": "Agni oooooo"},
    {"francais": "Comment tu vas ?", "baoule": "Orwhou ti Pka"},
    {"francais": "Et toi",           "baoule": "Or li"},
    {"francais": "Nouvelles",        "baoule": "Yai n'glèmou"},
    {"francais": "Bonsoir",          "baoule": "M'moooo"},
    {"francais": "Maman",            "baoule": "Mami"},
    {"francais": "Papa",             "baoule": "Baba"},
    {"francais": "Du riz",           "baoule": "Avié"},
    {"francais": "Manioc",           "baoule": "Agba"},
    {"francais": "Maïs",             "baoule": "Ablé"},
    {"francais": "Igname",           "baoule": "Douho"},
    {"francais": "Banane",           "baoule": "Manda"},
    {"francais": "Orange",           "baoule": "Domi"},
    {"francais": "Mangue",           "baoule": "Amango"},
    {"francais": "Papaye",           "baoule": "Oflê"},
    {"francais": "Banane douce",     "baoule": "Blorfouê manda"},
]

# ══════════════════════════════════════════════════════════════════════════════
#  NOUVELLE dictionary_view — remplace l'ancienne dans views.py
# ══════════════════════════════════════════════════════════════════════════════

NEW_DICTIONARY_VIEW = '''
def dictionary_view(request):
    """Affiche le dictionnaire Baoulé-Français (16 mots officiels uniquement)."""
    from .models import DictionaryEntry
    query     = request.GET.get('q', '').strip()
    direction = request.GET.get('direction', 'fr_to_baoule')

    entries = DictionaryEntry.objects.all()

    if query:
        if direction == 'baule_to_fr':
            entries = entries.filter(
                Q(word_baule__icontains=query) | Q(word_french__icontains=query)
            )
        else:
            entries = entries.filter(
                Q(word_french__icontains=query) | Q(word_baule__icontains=query)
            )

    entries = entries.order_by('word_baule')

    context = {
        'query':        query,
        'direction':    direction,
        'vocabularies': entries,           # nom conservé pour compatibilité template
        'total_words':  DictionaryEntry.objects.count(),
    }
    return render(request, 'dictionnaire.html', context)
'''

# ══════════════════════════════════════════════════════════════════════════════
#  TÂCHE 1 : Correction de views.py
# ══════════════════════════════════════════════════════════════════════════════

def task1_corriger_views():
    """
    Corrige lingx/views.py :
      - Remplace dictionary_view par la version qui lit DictionaryEntry
      - Neutralise les HttpResponse de debug (code brut visible en page)
    Crée une sauvegarde views.py.bak avant toute modification.
    """
    print("\n── TÂCHE 1 : Correction de lingx/views.py ──────────────────────")

    if not VIEWS_PATH.exists():
        print(f"  [ERREUR] Fichier introuvable : {VIEWS_PATH}")
        print("  → Lance ce script depuis le dossier monprojet/")
        return False

    source = VIEWS_PATH.read_text(encoding="utf-8")

    # Sauvegarde avant modification
    bak = VIEWS_PATH.with_suffix(".py.bak")
    shutil.copy2(VIEWS_PATH, bak)
    print(f"  [✓] Sauvegarde : {bak.name}")

    modified = False

    # ── Remplacement de dictionary_view ──────────────────────────────────────
    pattern_view = re.compile(
        r"(def dictionary_view\(request\):.*?)(?=\n@|\ndef |\Z)",
        re.DOTALL,
    )
    if pattern_view.search(source):
        source = pattern_view.sub(NEW_DICTIONARY_VIEW.strip(), source, count=1)
        print("  [✓] dictionary_view remplacée.")
        modified = True
    else:
        print("  [!] dictionary_view introuvable — déjà corrigée ou absente.")

    # ── Neutralisation des HttpResponse de debug ─────────────────────────────
    debug_patterns = [
        re.compile(r'HttpResponse\s*\(\s*["\']<?(pre|code|html|<!DOCTYPE)[^"\']*["\']', re.IGNORECASE),
        re.compile(r'return\s+HttpResponse\s*\(f?["\']<html[^"\']*["\']', re.IGNORECASE),
    ]
    lines   = source.splitlines(keepends=True)
    nb_debug = 0
    for i, line in enumerate(lines):
        for dp in debug_patterns:
            if dp.search(line):
                lines[i] = f"    # [FIX] réponse debug supprimée\n    # {line.lstrip()}"
                nb_debug += 1
                modified = True
                break
    source = "".join(lines)

    if nb_debug:
        print(f"  [✓] {nb_debug} réponse(s) debug neutralisée(s).")
    else:
        print("  [✓] Aucune réponse debug détectée.")

    if modified:
        VIEWS_PATH.write_text(source, encoding="utf-8")
        print("  [✓] views.py sauvegardé.")
    else:
        print("  [i] Aucune modification nécessaire.")

    return True


# ══════════════════════════════════════════════════════════════════════════════
#  TÂCHE 2 : Réinitialisation du dictionnaire en base
# ══════════════════════════════════════════════════════════════════════════════

def task2_peupler_dictionnaire():
    """
    Réinitialise la base de données :
      - Supprime toutes les DictionaryEntry existantes
      - Supprime les Vocabulary orphelins (sans leçon associée)
      - Insère les 16 mots officiels dans DictionaryEntry
    """
    print("\n── TÂCHE 2 : Réinitialisation du dictionnaire en base ──────────")

    # Initialisation Django (une seule fois)
    sys.path.insert(0, str(Path(__file__).parent))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS)

    try:
        import django
        django.setup()
    except Exception as e:
        print(f"  [ERREUR] Django ne démarre pas : {e}")
        print("  → Vérifie que DJANGO_SETTINGS pointe bien vers ton settings.py")
        return False

    from lingx.models import DictionaryEntry, Vocabulary

    # Suppression de l'ancien contenu
    nb_entries = DictionaryEntry.objects.count()
    nb_voc     = Vocabulary.objects.filter(lesson__isnull=True).count()
    DictionaryEntry.objects.all().delete()
    Vocabulary.objects.filter(lesson__isnull=True).delete()
    print(f"  [✓] {nb_entries} DictionaryEntry supprimée(s).")
    print(f"  [✓] {nb_voc} Vocabulary orphelin(s) supprimé(s).")

    # Insertion des 16 mots officiels
    created = 0
    updated = 0
    for mot in MOTS_OFFICIELS:
        entry, is_new = DictionaryEntry.objects.get_or_create(
            word_baule=mot["baoule"],
            defaults={"word_french": mot["francais"]},
        )
        if is_new:
            created += 1
            print(f"  + {mot['francais']:22s} →  {mot['baoule']}")
        else:
            entry.word_french = mot["francais"]
            entry.save()
            updated += 1
            print(f"  ~ {mot['francais']:22s} →  {mot['baoule']}  (mis à jour)")

    total = DictionaryEntry.objects.count()
    print(f"  [✓] {created} ajouté(s), {updated} mis à jour — total en base : {total} mot(s).")
    return True


# ══════════════════════════════════════════════════════════════════════════════
#  POINT D'ENTRÉE PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  setup_dictionnaire_baoule.py")
    print("  Projet LingX — Dictionnaire Baoulé-Français")
    print("=" * 60)

    ok1 = task1_corriger_views()
    ok2 = task2_peupler_dictionnaire()

    print("\n" + "=" * 60)
    if ok1 and ok2:
        print("  [✓] Toutes les tâches sont terminées avec succès.")
        print("  → Redémarre le serveur Django pour appliquer les changements.")
    else:
        print("  [!] Une ou plusieurs tâches ont échoué — lis les messages ci-dessus.")
    print("=" * 60)


if __name__ == "__main__":
    main()

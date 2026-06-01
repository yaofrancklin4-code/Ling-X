#!/usr/bin/env python
"""
Script de vérification d'installation pour le projet LingX
Vérifie que tous les éléments sont correctement configurés
"""

import os
import sys
import django
from pathlib import Path

def check_environment():
    """Vérifie l'environnement Python"""
    print("🔍 Vérification de l'environnement Python...")
    print(f"   ✓ Python: {sys.version}")
    print(f"   ✓ Chemin: {sys.executable}")

def check_django():
    """Vérifie Django"""
    print("\n🔍 Vérification de Django...")
    try:
        print(f"   ✓ Django: {django.__version__}")
    except ImportError:
        print("   ✗ Django n'est pas installé!")
        return False
    return True

def check_settings():
    """Vérifie les paramètres Django"""
    print("\n🔍 Vérification des paramètres Django...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
        django.setup()
        print("   ✓ Paramètres Django configurés")
        return True
    except Exception as e:
        print(f"   ✗ Erreur de configuration: {e}")
        return False

def check_database():
    """Vérifie la base de données"""
    print("\n🔍 Vérification de la base de données...")
    from django.db import connections
    try:
        connections.databases
        print("   ✓ Base de données configurée")
        return True
    except Exception as e:
        print(f"   ✗ Erreur base de données: {e}")
        return False

def check_apps():
    """Vérifie les applications Django"""
    print("\n🔍 Vérification des applications...")
    from django.apps import apps
    installed_apps = [app.name for app in apps.get_app_configs()]
    
    required_apps = ['lingx', 'rest_framework']
    for app in required_apps:
        if any(required_app in installed_app for required_app in [app] for installed_app in installed_apps):
            print(f"   ✓ {app} installée")
        else:
            print(f"   ✗ {app} non installée")
            return False
    return True

def check_dictionary():
    """Vérifie le dictionnaire"""
    print("\n🔍 Vérification du dictionnaire...")
    dict_path = Path('dictionnaire_baoule_cleaned.json')
    if dict_path.exists():
        print(f"   ✓ Dictionnaire trouvé ({dict_path.stat().st_size} bytes)")
        return True
    else:
        print("   ✗ Dictionnaire non trouvé")
        return False

def check_static():
    """Vérifie les fichiers statiques"""
    print("\n🔍 Vérification des fichiers statiques...")
    static_path = Path('static')
    if static_path.exists():
        print("   ✓ Dossier static existe")
        return True
    else:
        print("   ✗ Dossier static manquant")
        return False

def main():
    """Fonction principale"""
    print("=" * 50)
    print("🚀 Vérification d'Installation LingX")
    print("=" * 50)
    
    checks = [
        ("Environnement", check_environment),
        ("Django", check_django),
        ("Paramètres", check_settings),
        ("Base de données", check_database),
        ("Applications", check_apps),
        ("Dictionnaire", check_dictionary),
        ("Fichiers statiques", check_static),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func() if check_func != check_environment else (check_environment() or True)
            results.append((name, result if isinstance(result, bool) else True))
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    print(f"\n✓ Résultat: {passed}/{total} vérifications réussies")
    
    if passed == total:
        print("\n🎉 Tout est prêt! Vous pouvez lancer le serveur.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} vérification(s) échouée(s)")
        return 1

if __name__ == '__main__':
    sys.exit(main())

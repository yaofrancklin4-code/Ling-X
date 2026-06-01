#!/usr/bin/env python
"""
Script de diagnostic et nettoyage pour LingX
Utilise les configurations et signale les problèmes
"""

import os
import sys
import django
from pathlib import Path
from django.core.management import call_command

def clean_database():
    """Nettoie la base de données"""
    print("🧹 Nettoyage de la base de données...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
        django.setup()
        
        from lingx.models import (
            Category, Vocabulary, Lesson, Quiz, 
            QuizAnswer, UserProgress, Comment
        )
        
        models = [Category, Vocabulary, Lesson, Quiz, QuizAnswer, UserProgress, Comment]
        
        for model in models:
            count = model.objects.count()
            print(f"   - {model.__name__}: {count} entrées")
        
        print("\n   ⚠️  Êtes-vous sûr? Cela supprimera TOUTES les données!")
        response = input("   Tapez 'oui' pour confirmer: ")
        
        if response.lower() == 'oui':
            for model in models:
                model.objects.all().delete()
            print("   ✓ Base de données nettoyée")
        else:
            print("   ✗ Annulé")
        
        return True
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False

def backup_database():
    """Sauvegarde la base de données"""
    print("\n💾 Sauvegarde de la base de données...")
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"backups/db_backup_{timestamp}.json"
        
        Path("backups").mkdir(exist_ok=True)
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
        django.setup()
        
        call_command('dumpdata', stdout=open(backup_file, 'w'))
        print(f"   ✓ Sauvegarde créée: {backup_file}")
        return True
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False

def restore_database(backup_file):
    """Restaure la base de données"""
    print(f"\n🔄 Restauration depuis {backup_file}...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
        django.setup()
        
        call_command('loaddata', backup_file)
        print("   ✓ Base de données restaurée")
        return True
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False

def analyze_database():
    """Analyse la base de données"""
    print("\n📊 Analyse de la base de données...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
        django.setup()
        
        from django.contrib.auth.models import User
        from lingx.models import (
            Category, Vocabulary, Lesson, Quiz, UserProgress
        )
        
        stats = {
            'Utilisateurs': User.objects.count(),
            'Catégories': Category.objects.count(),
            'Vocabulaires': Vocabulary.objects.count(),
            'Leçons': Lesson.objects.count(),
            'Quiz': Quiz.objects.count(),
            'Progressions': UserProgress.objects.count(),
        }
        
        print("\n   Statistiques:")
        for name, count in stats.items():
            print(f"   • {name}: {count}")
        
        return True
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 50)
    print("🔧 Diagnostic et Nettoyage LingX")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Analyser la base de données")
        print("2. Nettoyer la base de données")
        print("3. Sauvegarder la base de données")
        print("4. Restaurer depuis une sauvegarde")
        print("5. Quitter")
        
        choice = input("\nVotre choix (1-5): ").strip()
        
        if choice == '1':
            analyze_database()
        elif choice == '2':
            clean_database()
        elif choice == '3':
            backup_database()
        elif choice == '4':
            backup_file = input("Entrez le chemin du fichier de sauvegarde: ").strip()
            restore_database(backup_file)
        elif choice == '5':
            print("Au revoir!")
            break
        else:
            print("Choix invalide!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterruption utilisateur")
        sys.exit(0)

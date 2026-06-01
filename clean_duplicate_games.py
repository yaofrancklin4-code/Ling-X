#!/usr/bin/env python
"""
Script pour nettoyer les doublons de jeux dans la base de données
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import MiniGame
from collections import defaultdict

def clean_duplicate_games():
    """Supprime les jeux en doublon"""
    print("🧹 Nettoyage des jeux en doublon...")
    
    games = MiniGame.objects.all()
    print(f"Total de jeux avant nettoyage: {games.count()}")
    
    # Grouper par titre normalisé (insensible à la casse)
    duplicates = defaultdict(list)
    for game in games:
        # Normaliser le titre: minuscules et espaces supplémentaires
        normalized_title = game.title.lower().strip()
        duplicates[normalized_title].append(game)
    
    # Identifier les doublons
    removed_count = 0
    for title, game_list in duplicates.items():
        if len(game_list) > 1:
            print(f"\n⚠️  Doublon trouvé: '{title}'")
            print(f"   {len(game_list)} exemplaires trouvés (IDs: {[g.id for g in game_list]})")
            
            # Garder le premier, supprimer les autres
            to_keep = game_list[0]
            to_remove = game_list[1:]
            
            for game in to_remove:
                print(f"   ✗ Suppression ID {game.id}")
                game.delete()
                removed_count += 1
            
            print(f"   ✓ Conservé: ID {to_keep.id}")
    
    final_count = MiniGame.objects.count()
    print(f"\n✅ Nettoyage terminé:")
    print(f"   Avant: {games.count()} jeux")
    print(f"   Supprimés: {removed_count} doublons")
    print(f"   Après: {final_count} jeux uniques")
    
    return removed_count

def list_games():
    """Liste tous les jeux disponibles"""
    print("\n📋 Liste des jeux actuels:")
    print("─" * 60)
    
    games = MiniGame.objects.filter(is_active=True).order_by('id')
    for i, game in enumerate(games, 1):
        print(f"{i}. ID:{game.id:2} | {game.title:25} | {game.difficulty:15} | {game.points_reward} pts | {game.time_limit}s")
    
    print("─" * 60)
    print(f"Total: {games.count()} jeux actifs")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🧹 NETTOYAGE DES DOUBLONS - LingX")
    print("=" * 60)
    
    # D'abord, lister les jeux
    list_games()
    
    # Demander confirmation
    print("\n⚠️  Voulez-vous supprimer les doublons?")
    response = input("Tapez 'oui' pour confirmer: ").strip().lower()
    
    if response == 'oui':
        removed = clean_duplicate_games()
        
        print("\n" + "=" * 60)
        print("✅ Nettoyage terminé!")
        print("=" * 60)
        
        # Afficher la liste après nettoyage
        list_games()
        
        return 0
    else:
        print("✗ Annulé")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterruption utilisateur")
        sys.exit(1)

"""
Configuration pour LingX
Définit les paramètres de l'application
"""

import os
from pathlib import Path

# Chemin du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuration du dictionnaire
DICTIONARY_CONFIG = {
    'file': 'dictionnaire_baoule_cleaned.json',
    'words_per_lesson': 15,
    'generate_quizzes': True,
    'quiz_questions': 5,
    'create_categories': True,
}

# Configuration des images
IMAGE_CONFIG = {
    'download': False,  # Vérifier si les images existent
    'default_placeholder': 'https://via.placeholder.com/300',
    'quality': 'high',
}

# Configuration des leçons
LESSON_CONFIG = {
    'auto_generate': True,
    'difficulty_levels': ['A1', 'A2', 'B1', 'B2', 'C1'],
    'default_level': 'A1',
}

# Configuration de gamification
GAMIFICATION_CONFIG = {
    'enable_points': True,
    'enable_achievements': True,
    'enable_leaderboard': True,
    'points_per_lesson': 100,
    'points_per_quiz': 50,
}

# Configuration des environnements
DEBUG_MODE = os.getenv('DEBUG', 'True') == 'True'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Configuration de la base de données
DB_CONFIG = {
    'engine': 'django.db.backends.sqlite3',
    'name': 'db.sqlite3',
}

# Configuration des emails
EMAIL_CONFIG = {
    'host': os.getenv('EMAIL_HOST', 'smtp.gmail.com'),
    'port': int(os.getenv('EMAIL_PORT', 587)),
    'user': os.getenv('EMAIL_USER', ''),
    'password': os.getenv('EMAIL_PASSWORD', ''),
}

# URLs de base
URLS_CONFIG = {
    'home': '/',
    'dictionary': '/dictionnaire/',
    'lessons': '/lecons/',
    'admin': '/admin/',
    'api': '/api/',
}

# Chemins des fichiers
PATHS = {
    'media': BASE_DIR / 'media',
    'static': BASE_DIR / 'static',
    'templates': BASE_DIR / 'templates',
    'logs': BASE_DIR / 'logs',
}

print("✓ Configuration chargée")

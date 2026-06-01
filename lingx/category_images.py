# Mapping des catégories vers les images
CATEGORY_IMAGE_MAP = {
    'Salutations': 'greetings',
    'Famille': 'family',
    'Nourriture': 'food',
    'Nombres': 'numbers',
    'Animaux': 'animals',
    'Histoire': 'history',
    'Culture': 'culture',
    'Société': 'society',
    'Géographie': 'geography',
    'Prénoms': 'names',
    'Contes': 'legends',
    'Couleurs': 'colors',
    'Santé': 'health',
    'Maison': 'house',
    'Nature': 'nature',
    'Climat': 'weather',
    'Travail': 'work',
    'Émotions': 'emotions',
    'Vêtements': 'clothes',
    'Corps humain': 'body',
    'Vocabulaire courant': 'vocabulary',
}

def get_category_image(category_name):
    """Retourne le nom de fichier image pour une catégorie"""
    return CATEGORY_IMAGE_MAP.get(category_name, 'vocabulary')

from django import template

register = template.Library()

CATEGORY_IMAGE_MAP = {
    'Salutations': 'greetings',
    'Famille': 'family',
    'Nourriture': 'food',
    'Nourriture et Boissons': 'food',
    'Nombres': 'numbers',
    'Parties du Corps': 'body',
    'Corps humain': 'body',
    'Animaux': 'animals',
    'Histoire': 'history',
    'Culture': 'culture',
    'Société': 'society',
    'Géographie': 'geography',
    'Prénoms': 'names',
    'Contes': 'stories',
    'Couleurs': 'colors',
    'Santé': 'health',
    'Maison': 'house',
    'Nature': 'nature',
    'Climat': 'weather',
    'Travail': 'work',
    'Émotions': 'emotions',
    'Vêtements': 'clothes',
    'Vocabulaire courant': 'vocabulary',
}

@register.filter
def category_image(category_name):
    """Retourne le nom de fichier image pour une catégorie"""
    return CATEGORY_IMAGE_MAP.get(category_name, 'vocabulary')

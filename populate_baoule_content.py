"""
Script pour importer et remplir la base de données avec le contenu Baoulé
depuis le site baoule.ci et d'autres sources
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import (
    Category, Lesson, Vocabulary, Proverb, CultureContent, 
    BaouleName, Story, DictionaryEntry, StoryVocabulary
)
from django.contrib.auth.models import User


def create_categories():
    """Créer les catégories principales"""
    categories = [
        {
            'name': 'Salutations',
            'description': 'Apprenez les salutations courantes en Baoulé',
            'icon': '👋',
            'order': 1
        },
        {
            'name': 'Famille',
            'description': 'Les termes de parenté et relations familiales',
            'icon': '👨‍👩‍👧‍👦',
            'order': 2
        },
        {
            'name': 'Nourriture',
            'description': 'Vocabulaire des aliments et de la cuisine baoulée',
            'icon': '🍲',
            'order': 3
        },
        {
            'name': 'Histoire & Origines',
            'description': 'L\'histoire riche du peuple Baoulé et ses origines',
            'icon': '📖',
            'order': 4
        },
        {
            'name': 'Culture & Traditions',
            'description': 'Découvrez les traditions et coutumes baoulées',
            'icon': '🎭',
            'order': 5
        },
        {
            'name': 'Société',
            'description': 'Organisation sociale et rôles traditionnels',
            'icon': '🏛️',
            'order': 6
        },
        {
            'name': 'Territoire & Géographie',
            'description': 'Villages et géographie du pays baoulé',
            'icon': '🗺️',
            'order': 7
        },
        {
            'name': 'Nombres & Comptage',
            'description': 'Apprendre à compter en Baoulé',
            'icon': '🔢',
            'order': 8
        },
        {
            'name': 'Prénoms Baoulés',
            'description': 'Découvrez la signification des prénoms baoulés',
            'icon': '📛',
            'order': 9
        },
        {
            'name': 'Contes & Légendes',
            'description': 'Histoires, contes et légendes du peuple baoulé',
            'icon': '🌙',
            'order': 10
        },
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'icon': cat_data['icon'],
                'order': cat_data['order']
            }
        )
        if created:
            print(f"✓ Catégorie créée: {category.name}")
        else:
            print(f"✓ Catégorie existante: {category.name}")


def create_dictionary_entries():
    """Créer les entrées du dictionnaire Baoulé"""
    dictionary = [
        # Salutations
        {
            'word_baule': 'Nàn kɔ',
            'word_french': 'Bonjour',
            'pronunciation': 'Nan ko',
            'part_of_speech': 'Expression',
            'definition': 'Salutation formelle du matin en Baoulé',
            'is_common': True,
            'usage_context': 'Matin'
        },
        {
            'word_baule': 'ɔ wɛ',
            'word_french': 'Bonsoir',
            'pronunciation': 'O wè',
            'part_of_speech': 'Expression',
            'definition': 'Salutation du soir en Baoulé',
            'is_common': True,
            'usage_context': 'Soir'
        },
        {
            'word_baule': 'M\' kɔ yɛ',
            'word_french': 'Comment allez-vous ?',
            'pronunciation': 'Mè ko yè',
            'part_of_speech': 'Expression',
            'definition': 'Question de politesse pour s\'enquérir de la santé',
            'is_common': True,
            'usage_context': 'Polite greeting'
        },
        # Famille
        {
            'word_baule': 'Mé',
            'word_french': 'Mère',
            'pronunciation': 'Mé',
            'part_of_speech': 'Nom',
            'definition': 'La mère, parent féminin',
            'is_common': True,
            'usage_context': 'Famille'
        },
        {
            'word_baule': 'Hà',
            'word_french': 'Père',
            'pronunciation': 'Ha',
            'part_of_speech': 'Nom',
            'definition': 'Le père, parent masculin',
            'is_common': True,
            'usage_context': 'Famille'
        },
        {
            'word_baule': 'Yé',
            'word_french': 'Enfant',
            'pronunciation': 'Yé',
            'part_of_speech': 'Nom',
            'definition': 'Un enfant, jeune personne',
            'is_common': True,
            'usage_context': 'Famille'
        },
        {
            'word_baule': 'Agyè',
            'word_french': 'Frère',
            'pronunciation': 'Agyè',
            'part_of_speech': 'Nom',
            'definition': 'Frère, soeur (terme générique)',
            'is_common': True,
            'usage_context': 'Famille'
        },
        # Nourriture
        {
            'word_baule': 'Aloco',
            'word_french': 'Banane plantain frite',
            'pronunciation': 'Aloco',
            'part_of_speech': 'Nom',
            'definition': 'Plat traditionnel de banane plantain frite',
            'is_common': True,
            'usage_context': 'Cuisine'
        },
        {
            'word_baule': 'Fou-fou',
            'word_french': 'Purée de plantain',
            'pronunciation': 'Fou-fou',
            'part_of_speech': 'Nom',
            'definition': 'Plat traditionnel de purée de plantain',
            'is_common': True,
            'usage_context': 'Cuisine'
        },
        {
            'word_baule': 'Attiéké',
            'word_french': 'Couscous de manioc',
            'pronunciation': 'Attiéké',
            'part_of_speech': 'Nom',
            'definition': 'Plat populaire à base de manioc râpé et fermenté',
            'is_common': True,
            'usage_context': 'Cuisine'
        },
        # Nombres
        {
            'word_baule': 'Wɔ',
            'word_french': 'Un',
            'pronunciation': 'Wô',
            'part_of_speech': 'Nombre',
            'definition': 'Le nombre 1',
            'is_common': True,
            'usage_context': 'Nombre'
        },
        {
            'word_baule': 'Ɛ',
            'word_french': 'Deux',
            'pronunciation': 'Ê',
            'part_of_speech': 'Nombre',
            'definition': 'Le nombre 2',
            'is_common': True,
            'usage_context': 'Nombre'
        },
        {
            'word_baule': 'Ata',
            'word_french': 'Trois',
            'pronunciation': 'Ata',
            'part_of_speech': 'Nombre',
            'definition': 'Le nombre 3',
            'is_common': True,
            'usage_context': 'Nombre'
        },
        {
            'word_baule': 'Anan',
            'word_french': 'Quatre',
            'pronunciation': 'Anan',
            'part_of_speech': 'Nombre',
            'definition': 'Le nombre 4',
            'is_common': True,
            'usage_context': 'Nombre'
        },
        {
            'word_baule': 'Anu',
            'word_french': 'Cinq',
            'pronunciation': 'Anu',
            'part_of_speech': 'Nombre',
            'definition': 'Le nombre 5',
            'is_common': True,
            'usage_context': 'Nombre'
        },
    ]
    
    for dict_data in dictionary:
        entry, created = DictionaryEntry.objects.get_or_create(
            word_baule=dict_data['word_baule'],
            defaults={
                'word_french': dict_data['word_french'],
                'pronunciation': dict_data['pronunciation'],
                'part_of_speech': dict_data['part_of_speech'],
                'definition': dict_data['definition'],
                'is_common': dict_data['is_common'],
                'usage_context': dict_data['usage_context']
            }
        )
        if created:
            print(f"✓ Mot du dictionnaire créé: {entry.word_baule}")


def create_proverbs():
    """Créer des proverbes et expressions Baoulées"""
    proverbs = [
        {
            'proverb_baule': 'Kofifr wa à gbéti ma fûn',
            'proverb_french': 'Un seul doigt ne peut pas ramasser une noix de coco du sol',
            'meaning': 'L\'union fait la force. On ne peut pas accomplir de grandes choses seul.',
            'category': 'Sagesse',
            'usage_context': 'Travail en équipe'
        },
        {
            'proverb_baule': 'Tia kɔ nɔ yé',
            'proverb_french': 'C\'est l\'expérience qui crée la sagesse',
            'meaning': 'La sagesse vient de l\'expérience et du temps',
            'category': 'Sagesse',
            'usage_context': 'Apprentissage'
        },
        {
            'proverb_baule': 'Mèna ka sé blifɔ à wli n\'a',
            'proverb_french': 'La mère qui donne naissance à un enfant n\'abandonne jamais',
            'meaning': 'L\'amour maternel est inconditionnel et durable',
            'category': 'Famille',
            'usage_context': 'Relations familiales'
        },
        {
            'proverb_baule': 'Nwa à gblɛ n\'à sé kɔ wɛ',
            'proverb_french': 'Un aveugle n\'a pas honte de se tromper',
            'meaning': 'On ne peut pas juger celui qui n\'a pas les informations nécessaires',
            'category': 'Sagesse',
            'usage_context': 'Jugement'
        },
        {
            'proverb_baule': 'Hɔ bɛ à kwazo dɔ',
            'proverb_french': 'Le père pourvoit toujours aux besoins de son enfant',
            'meaning': 'La responsabilité du père envers ses enfants est primordiale',
            'category': 'Famille',
            'usage_context': 'Responsabilité'
        },
    ]
    
    for proverb_data in proverbs:
        proverb, created = Proverb.objects.get_or_create(
            proverb_baule=proverb_data['proverb_baule'],
            defaults={
                'proverb_french': proverb_data['proverb_french'],
                'meaning': proverb_data['meaning'],
                'category': proverb_data['category'],
                'usage_context': proverb_data['usage_context']
            }
        )
        if created:
            print(f"✓ Proverbe créé: {proverb.proverb_baule[:40]}...")


def create_baule_names():
    """Créer des prénoms Baoulés"""
    names = [
        {
            'name_baule': 'Akissi',
            'meaning_french': 'Enfant né le jeudi',
            'gender': 'F',
            'origin': 'Correspond au jour de naissance selon le calendrier Baoulé',
            'cultural_significance': 'Prénom traditionnel lié à la cosmologie baoulée'
        },
        {
            'name_baule': 'Kou',
            'meaning_french': 'Enfant né le samedi',
            'gender': 'M',
            'origin': 'Correspond au jour de naissance selon le calendrier Baoulé',
            'cultural_significance': 'Prénom traditionnel lié à la cosmologie baoulée'
        },
        {
            'name_baule': 'Yao',
            'meaning_french': 'Enfant né le jeudi',
            'gender': 'M',
            'origin': 'Correspond au jour de naissance selon le calendrier Baoulé',
            'cultural_significance': 'Prénom traditionnel lié à la cosmologie baoulée'
        },
        {
            'name_baule': 'Abla',
            'meaning_french': 'Enfant né le lundi',
            'gender': 'F',
            'origin': 'Correspond au jour de naissance selon le calendrier Baoulé',
            'cultural_significance': 'Prénom traditionnel lié à la cosmologie baoulée'
        },
        {
            'name_baule': 'N\'da',
            'meaning_french': 'La mère',
            'gender': 'F',
            'origin': 'Terme respectueux pour une mère de famille',
            'cultural_significance': 'Marque le respect envers la maternité'
        },
        {
            'name_baule': 'Amenan',
            'meaning_french': 'Celui qui hérite du père',
            'gender': 'M',
            'origin': 'Indique une continuité familiale importante',
            'cultural_significance': 'Importance de l\'héritage et de la transmission'
        },
        {
            'name_baule': 'Affouē',
            'meaning_french': 'Celui qui contrôle les biens',
            'gender': 'M',
            'origin': 'Terme de prestige et d\'autorité',
            'cultural_significance': 'Autorité et responsabilité'
        },
        {
            'name_baule': 'Brigitte',
            'meaning_french': 'Forte et puissante',
            'gender': 'F',
            'origin': 'Version baoulée d\'un prénom occidental',
            'cultural_significance': 'Force et détermination'
        },
    ]
    
    for name_data in names:
        name, created = BaouleName.objects.get_or_create(
            name_baule=name_data['name_baule'],
            defaults={
                'meaning_french': name_data['meaning_french'],
                'gender': name_data['gender'],
                'origin': name_data['origin'],
                'cultural_significance': name_data['cultural_significance']
            }
        )
        if created:
            print(f"✓ Prénom baoulé créé: {name.name_baule}")


def create_stories():
    """Créer des histoires et contes Baoulés"""
    stories = [
        {
            'title': 'L\'araignée et le miel',
            'story_type': 'tale',
            'description': 'Un conte traditionnel sur l\'astuce et la gourmandise',
            'full_text': '''Il était une fois une araignée très maligne qui vivait sur un grand fromager. 
Chaque jour, elle voyait des abeilles entrer et sortir d\'une ruche. L\'araignée aimait beaucoup 
le miel, mais elle ne savait pas comment l\'obtenir sans se faire piquer.

Un jour, l\'araignée eut une idée. Elle se transforma en gouttelette de rosée et entra discrètement 
dans la ruche. Malheureusement, les abeilles la découvrirent et la poursuivirent.

L\'araignée courut aussi vite qu\'elle put jusqu\'à la maison du roi. Le roi, très amusé par cette 
scène, décida de récompenser l\'araignée pour sa ruse. Il donna à l\'araignée un pot de miel, 
à condition qu\'elle promette d\'utiliser sa ruse pour aider les autres, et non pour se jouer d\'eux.

Depuis ce jour, l\'araignée est devenue le symbole de la sagesse chez les Baoulés.''',
            'moral_lesson': 'La ruse est une vertu, mais elle doit être utilisée avec sagesse et pour aider, non pour tromper.',
            'difficulty': 'debutant',
            'is_featured': True
        },
        {
            'title': 'La tortue et le lièvre',
            'story_type': 'fable',
            'description': 'La célèbre fable adaptée à la culture baoulée',
            'full_text': '''La tortue et le lièvre vivaient dans la forêt africaine. Le lièvre était fier 
de sa rapidité et se moquait constamment de la tortue pour sa lenteur.

Un jour, la tortue proposa une course au lièvre. Le lièvre rit et accepta, sûr de gagner.

Au départ, le lièvre fila à toute vitesse tandis que la tortue avançait lentement mais régulièrement. 
Après quelque temps, le lièvre se sentit fatigué. Il s\'arrêta sous un baobab pour faire une sieste, 
pensant que la tortue était bien loin derrière.

Pendant ce temps, la tortue continua son chemin sans s\'arrêter. Elle dépassa le lièvre qui dormait 
et arriva la première à la ligne d\'arrivée.

Quand le lièvre se réveilla, il était trop tard. La tortue avait gagné!''',
            'moral_lesson': 'La persévérance et la constance valent mieux que la vitesse et l\'arrogance. La patience est une vertu.',
            'difficulty': 'debutant',
            'is_featured': True
        },
        {
            'title': 'L\'origine du Baoulé',
            'story_type': 'history',
            'description': 'L\'histoire de la migration du peuple baoulé',
            'full_text': '''Le peuple baoulé a une histoire riche de migrations et d\'aventures.

Selon la tradition, les Baoulés sont originaires du Ghana actuel. Au XVIIe siècle, sous le leadership 
de la reine Abla Pokou, une partie du peuple Akan a quitté ses terres pour fuir les guerres et 
l\'instabilité politique.

La reine Abla Pokou et son armée ont traversé les terres inhospitalières, affrontant la rivière Comoé 
qui semblait infranchissable. Selon la légende, la reine aurait fait un sacrifice personnel, jetant 
son fils dans le fleuve pour que les eaux se calment et permettent au peuple de traverser.

Après avoir traversé le fleuve, le peuple a continué sa route et s\'est établi dans la région centrale 
de la Côte d\'Ivoire actuelle. Le nom "Baoulé" viendrait de "Ba Oule" signifiant "fils de Oule" en référence 
à cet événement tragique.''',
            'moral_lesson': 'Les sacrifices et la détermination peuvent mener à la construction d\'une nouvelle civilisation. L\'histoire façonne l\'identité d\'un peuple.',
            'difficulty': 'intermediaire',
            'is_featured': True
        },
    ]
    
    for story_data in stories:
        story, created = Story.objects.get_or_create(
            title=story_data['title'],
            defaults={
                'story_type': story_data['story_type'],
                'description': story_data['description'],
                'full_text': story_data['full_text'],
                'moral_lesson': story_data['moral_lesson'],
                'difficulty': story_data['difficulty'],
                'is_featured': story_data['is_featured']
            }
        )
        if created:
            print(f"✓ Histoire créée: {story.title}")


def create_culture_content():
    """Créer du contenu culturel"""
    cultures = [
        {
            'title': 'Les Fêtes et Rituels Baoulés',
            'content_type': 'celebration',
            'description': 'Découvrez les principales fêtes et célébrations de la culture baoulée',
            'detailed_content': '''Les Baoulés célèbrent plusieurs fêtes tout au long de l\'année:

1. **La Fête de l\'igname** - Célébration de la nouvelle récolte d\'igname. C\'est l\'occasion de 
remercier les esprits ancestraux et de partager la nouvelle récolte avec la communauté.

2. **Les Adieux** - Cérémonie importante lors du décès d\'une personne. C\'est une occasion pour 
la famille et la communauté de rendre hommage au défunt à travers des danses, chants et discours.

3. **Les Mariages Traditionnels** - Événement social majeur où deux familles s\'unissent. Implique 
des cadeaux, des danses et des rituels de bienvenue.

4. **Le Nouvel An Baoulé** - Marqué par des festivités, des visites familiales et des rituels de 
purification pour commencer l\'année avec bénédiction.

5. **Les Fêtes Religieuses** - Célébrations liées aux cultes des ancêtres et des esprits protecteurs.''',
            'content_type': 'celebration',
            'is_featured': True,
            'order': 1
        },
        {
            'title': 'La Musique et la Danse Baoulées',
            'content_type': 'tradition',
            'description': 'Exploration de la musique et des danses traditionnelles baoulées',
            'detailed_content': '''La musique et la danse sont au cœur de la culture baoulée:

1. **Les Instruments Traditionnels**:
   - Le tam-tam (tambour traditionnel)
   - Le balafon (xylophone africain)
   - La kora (harpe africaine)
   - Le gong

2. **Les Danses Principales**:
   - **L\'Adowa** - Danse de célébration et de joie
   - **Le Zigbiti** - Danse de mariage
   - **L\'Agbadja** - Danse funéraire
   - **Le Gumbe** - Danse sociale moderne avec racines traditionelles

3. **La Musique Contemporaine**:
   Les artistes baoulés ont modernisé la musique traditionnelle, créant des styles comme 
   le zouk, le reggae ivoirien et l\'afrobeats.''',
            'is_featured': True,
            'order': 2
        },
        {
            'title': 'L\'Organisation Sociale Baoulée',
            'content_type': 'custom',
            'description': 'Comprendre la structure sociale du peuple baoulé',
            'detailed_content': '''La société baoulée traditionelle est organisée autour de plusieurs principes:

1. **Hiérarchie Familiale**:
   - Le chef de famille (patriarche) dirige le clan
   - Les anciens sont les gardiens de la sagesse
   - Les femmes jouent des rôles importants dans l\'économie familiale

2. **Les Rôles Traditionnels**:
   - **Les Chefs** - Gouvernent les villages et règlent les différends
   - **Les Griots** - Conteurs, gardiens de l\'histoire orale
   - **Les Artisans** - Sculpteurs, tisserands, potiers
   - **Les Agriculteurs** - Base de l\'économie

3. **Les Rites de Passage**:
   - L\'initiation des jeunes (rite d\'entrée à l\'âge adulte)
   - Le mariage (union de deux familles)
   - Les funérailles (culte des ancêtres)

4. **L\'Égalité des Genres**:
   Les femmes baoulées jouissent d\'une relative liberté et autonomie, 
   particulièrement en matière commerciale et économique.''',
            'is_featured': False,
            'order': 3
        },
    ]
    
    for culture_data in cultures:
        culture, created = CultureContent.objects.get_or_create(
            title=culture_data['title'],
            defaults={
                'content_type': culture_data['content_type'],
                'description': culture_data['description'],
                'detailed_content': culture_data['detailed_content'],
                'is_featured': culture_data['is_featured'],
                'order': culture_data['order']
            }
        )
        if created:
            print(f"✓ Contenu culturel créé: {culture.title}")


def create_lessons():
    """Créer des leçons pour chaque catégorie"""
    print("\n📚 Création des leçons...")
    
    # Salutations
    salutation_category = Category.objects.get(name='Salutations')
    lessons_data = [
        {
            'category': salutation_category,
            'title': 'Salutations Basiques',
            'description': 'Apprenez les salutations courantes',
            'content': 'Utilisez ces expressions pour saluer les Baoulés',
            'difficulty': 'debutant',
            'order': 1,
            'vocabularies': [
                {'word_baule': 'Nàn kɔ', 'word_french': 'Bonjour', 'pronunciation': 'Nan ko'},
                {'word_baule': 'ɔ wɛ', 'word_french': 'Bonsoir', 'pronunciation': 'O wè'},
            ]
        },
    ]
    
    for lesson_data in lessons_data:
        category = lesson_data.pop('category')
        vocabularies = lesson_data.pop('vocabularies', [])
        
        lesson, created = Lesson.objects.get_or_create(
            title=lesson_data['title'],
            category=category,
            defaults=lesson_data
        )
        
        if created:
            print(f"✓ Leçon créée: {lesson.title}")
            
            # Ajouter le vocabulaire
            for vocab_data in vocabularies:
                vocab, vocab_created = Vocabulary.objects.get_or_create(
                    lesson=lesson,
                    word_baule=vocab_data['word_baule'],
                    defaults={
                        'word_french': vocab_data['word_french'],
                        'pronunciation': vocab_data.get('pronunciation', '')
                    }
                )
                if vocab_created:
                    print(f"  ✓ Vocabulaire ajouté: {vocab.word_baule}")


def run_population():
    """Exécuter tout le script de population"""
    print("🚀 Démarrage de la population de la base de données...\n")
    
    try:
        create_categories()
        print("\n✅ Catégories créées avec succès!\n")
        
        create_dictionary_entries()
        print("\n✅ Dictionnaire enrichi!\n")
        
        create_proverbs()
        print("\n✅ Proverbes ajoutés!\n")
        
        create_baule_names()
        print("\n✅ Prénoms baoulés ajoutés!\n")
        
        create_stories()
        print("\n✅ Histoires et contes créés!\n")
        
        create_culture_content()
        print("\n✅ Contenu culturel créé!\n")
        
        create_lessons()
        print("\n✅ Leçons créées!\n")
        
        print("=" * 60)
        print("✅ BASE DE DONNÉES REMPLIE AVEC SUCCÈS!")
        print("=" * 60)
        
        # Afficher un résumé
        print(f"\n📊 Résumé:")
        print(f"   - Catégories: {Category.objects.count()}")
        print(f"   - Leçons: {Lesson.objects.count()}")
        print(f"   - Mots du dictionnaire: {DictionaryEntry.objects.count()}")
        print(f"   - Proverbes: {Proverb.objects.count()}")
        print(f"   - Prénoms baoulés: {BaouleName.objects.count()}")
        print(f"   - Histoires et contes: {Story.objects.count()}")
        print(f"   - Contenus culturels: {CultureContent.objects.count()}")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la population: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_population()

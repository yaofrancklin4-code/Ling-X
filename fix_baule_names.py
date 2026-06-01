import os
import sys
import django

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from lingx.models import BaouleName

print("Suppression des anciens prenoms...")
BaouleName.objects.all().delete()

print("Ajout des nouveaux prenoms Baoules...")

# Noms masculins
masculine_names = [
    ('Kouadio', 'Garçon né un lundi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Koffi', 'Garçon né un vendredi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Kouame', 'Garçon né un samedi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Yao', 'Garçon né un jeudi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Konan', 'Garçon né un mardi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Kouassi', 'Garçon né un dimanche', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ("N'Guessan", 'Garçon né un mercredi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Amani', 'Paix, tranquillité', 'Prénom évoquant la sérénité', 'Valeur importante dans la société baoulée'),
    ("N'Dri", 'Force, courage', 'Prénom valorisant la bravoure', 'Qualité respectée chez les Baoulé'),
    ('Assi', 'Noble ou respecté', 'Prénom de prestige', 'Marque le respect et la noblesse'),
    ('Kacou', 'Courageux, brave', 'Prénom valorisant le courage', 'Qualité guerrière traditionnelle'),
    ('Nanan', 'Chef, roi, personne importante', 'Titre de noblesse', 'Lié à la royauté Akan'),
    ('Brou', 'Protecteur ou homme fort', 'Prénom évoquant la protection', 'Force et protection de la famille'),
    ('Kanga', 'Guerrier, homme puissant', 'Prénom de guerrier', 'Tradition guerrière baoulée'),
    ('Affoué', 'Richesse ou bénédiction', 'Prénom de prospérité', 'Symbole de bénédiction divine'),
]

for name, meaning, origin, cultural in masculine_names:
    BaouleName.objects.create(
        name_baule=name,
        meaning_french=meaning,
        gender='M',
        origin=origin,
        cultural_significance=cultural,
        order=0
    )
    print(f"+ {name} (M)")

# Noms féminins
feminine_names = [
    ('Akissi', 'Fille née un dimanche', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Ahou', 'Fille née un lundi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Adjoua', 'Fille née un mardi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Amlan', 'Fille née un mercredi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Yamoussou', 'Fille née un jeudi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Afoué', 'Fille née un vendredi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Ama', 'Fille née un samedi', 'Correspond au jour de naissance selon le calendrier Baoulé', 'Prénom traditionnel lié à la cosmologie baoulée'),
    ('Aminata', 'Digne de confiance', 'Prénom valorisant la fiabilité', 'Qualité morale importante'),
    ('Akoua', 'Femme forte', 'Prénom évoquant la force féminine', 'Force et détermination'),
    ("N'Gattia", 'Femme courageuse', 'Prénom valorisant le courage féminin', 'Bravoure et résilience'),
    ('Aya', 'Fougère, symbole de résistance', 'Plante symbolique', 'Résistance et persévérance'),
    ('Assa', 'Grâce ou beauté', 'Prénom évoquant l\'élégance', 'Beauté intérieure et extérieure'),
    ("M'Bra", 'Bénédiction', 'Prénom de bénédiction divine', 'Faveur spirituelle'),
    ("N'Dah", 'Sagesse', 'Prénom valorisant la sagesse', 'Connaissance et discernement'),
    ('Blé', 'Prospérité ou abondance', 'Prénom de richesse', 'Abondance et bénédiction matérielle'),
]

for name, meaning, origin, cultural in feminine_names:
    BaouleName.objects.create(
        name_baule=name,
        meaning_french=meaning,
        gender='F',
        origin=origin,
        cultural_significance=cultural,
        order=0
    )
    print(f"+ {name} (F)")

print(f"\nTotal: {BaouleName.objects.count()} prenoms ajoutes")
print(f"Masculins: {BaouleName.objects.filter(gender='M').count()}")
print(f"Feminins: {BaouleName.objects.filter(gender='F').count()}")
print("\nCorrection terminee!")

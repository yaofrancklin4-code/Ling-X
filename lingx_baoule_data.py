"""
LingX — Base de données Baoulé
Source : baoule.ci (Alexandre Tano Kan Koffi)
Projet : LingX — Plateforme d'apprentissage du Baoulé par la gamification
"""

# ============================================================
# 📖 HISTOIRE & ORIGINES
# ============================================================

HISTOIRE = {
    "titre": "Histoire & Origines du peuple Baoulé",
    "lecons": [
        {
            "id": "hist_01",
            "titre": "L'exode depuis le royaume Ashanti",
            "contenu": (
                "Au début du XVIIIe siècle, le royaume Akan de Kumasi (actuel Ghana) "
                "fut le théâtre de profonds conflits dynastiques. La mort du roi Osei Toutou "
                "déclencha une querelle de succession entre son fils Daaku et son cousin Opokou Ware. "
                "Daaku, frère aîné de la princesse Abla Pokou, perdit la course au trône. "
                "Cette instabilité contraignit la princesse Abla Pokou à fuir clandestinement le royaume de Kumasi."
            ),
            "mots_cles": ["Kumasi", "Ashanti", "Akan", "Abla Pokou", "exode", "XVIIIe siècle"],
        },
        {
            "id": "hist_02",
            "titre": "Le sacrifice et la naissance du nom Baoulé",
            "contenu": (
                "Face au fleuve Comoé en crue, poursuivis par les soldats, la Reine Abla Pokou "
                "accomplit le sacrifice ultime : elle immola son fils unique à l'esprit du fleuve "
                "pour permettre à son peuple de traverser. Sur l'autre rive, elle s'écria 'Ba-ouli' "
                "— 'l'enfant est mort'. Cette exclamation poignante devint le nom du peuple : Baoulé."
            ),
            "mots_cles": ["Ba-ouli", "sacrifice", "Comoé", "mythe fondateur", "identité"],
        },
        {
            "id": "hist_03",
            "titre": "L'installation en Côte d'Ivoire",
            "contenu": (
                "Les Baoulé s'établirent dans la région centrale de l'actuelle Côte d'Ivoire, "
                "entre les fleuves Bandama et Comoé. Le Royaume Baoulé (Baouléman) fut fondé au XVIIIe siècle, "
                "avec Sakassou comme capitale traditionnelle. Après le décès d'Abla Pokou vers 1760, "
                "sa nièce Akoua Boni consolida le territoire, l'étendant sur environ 30 000 km²."
            ),
            "mots_cles": ["Bandama", "Comoé", "Sakassou", "Baouléman", "Akoua Boni", "30 000 km²"],
        },
        {
            "id": "hist_04",
            "titre": "Colonisation et résistance Baoulé",
            "contenu": (
                "La fin du XIXe siècle marqua l'arrivée des puissances coloniales européennes en Afrique. "
                "Le peuple Baoulé ne se soumit pas sans résistance. Des figures historiques s'illustrèrent "
                "dans la lutte contre la domination coloniale, affirmant la fierté et la résilience du peuple."
            ),
            "mots_cles": ["colonisation", "résistance", "XIXe siècle", "figures historiques"],
        },
    ],
}

# ============================================================
# 🎭 CULTURE & TRADITIONS
# ============================================================

CULTURE = {
    "titre": "Culture & Traditions Baoulé",
    "lecons": [
        {
            "id": "cult_01",
            "titre": "Les salutations — un art de vivre",
            "contenu": (
                "Les salutations chez les Baoulé ne sont pas de simples échanges de politesse. "
                "Elles sont liées aux trois moments de la journée, symbolisant la naissance (matin), "
                "la croissance (midi) et la mort (soir)."
            ),
            "tableau": [
                {
                    "moment": "Matin",
                    "visiteur": "Ahin o!",
                    "traduction_v": "Le jour s'est levé !",
                    "reponse": "Arê o!",
                    "traduction_r": "La fraîcheur est bien là !",
                },
                {
                    "moment": "Midi",
                    "visiteur": "Antih o!",
                    "traduction_v": "Le soleil est au zénith !",
                    "reponse": "Anti o!",
                    "traduction_r": "Oui, le soleil est bien sorti !",
                },
                {
                    "moment": "Soir",
                    "visiteur": "Anou o!",
                    "traduction_v": "C'est éteint !",
                    "reponse": "Awossi o!",
                    "traduction_r": "C'est l'obscurité !",
                },
            ],
            "formules_supplementaires": {
                "Bienvenue après un voyage": "Akwaba!",
                "Asseyons-nous": "Yégouaassé",
                "Il y a une place": "Biawolè",
                "Longue absence": "N'vlèh!",
            },
        },
        {
            "id": "cult_02",
            "titre": "Les proverbes (Nyanndra) — sagesse ancestrale",
            "contenu": (
                "Les proverbes, appelés 'nyanndra' en baoulé, sont des paroles d'expérience et de sagesse "
                "populaire. Un discours sans proverbe est considéré comme 'dénudé'. "
                "Ils sont principalement le domaine des anciens et des sages."
            ),
            "proverbes": [
                {
                    "baoule": "Fama wunzin bɛ, bɛ wunzin fama",
                    "francais": "La main droite lave la main gauche et vice-versa",
                    "sens": "Solidarité et entraide",
                },
                {
                    "baoule": "Njin se min i wun kɛ ɔ yo fɛ",
                    "francais": "Le sel ne se dit pas salé",
                    "sens": "Humilité — les qualités se montrent par les actes",
                },
                {
                    "baoule": "A ni sui san nun nyansue bo-man ɔ",
                    "francais": "Si tu marches avec l'éléphant, la rosée des champs ne te mouillera pas",
                    "sens": "La protection que l'on obtient en s'associant à une personne de pouvoir",
                },
                {
                    "baoule": "Be fa'a be nyinma nnyɔn nia'an towa kunngba nun",
                    "francais": "On ne prend pas les deux yeux pour regarder dans une gourde",
                    "sens": "On ne pourchasse pas deux lièvres à la fois",
                },
                {
                    "baoule": "Sɛ a kpli ndɛn ndɛn'n, ɔ sia bla'n yo klanman tra ɔ yi",
                    "francais": "Si tu te presses vite à te marier, ta belle-mère sera plus jolie que ta femme",
                    "sens": "Le regret qui découle d'un manque de patience",
                },
                {
                    "baoule": "Awlɛn tralɛ'n yɛ ɔ yo ya- ɔ, sa bo wunlɛ'n ɔ yo-man ya",
                    "francais": "C'est attraper cœur qui fait mal, voir en bas d'un problème ne fait pas mal",
                    "sens": "La patience est un chemin d'or",
                },
            ],
        },
        {
            "id": "cult_03",
            "titre": "Fêtes et Rituels",
            "contenu": (
                "Les Baoulé rythment leur existence par un riche ensemble de fêtes et de rituels. "
                "La Fête des Ignames est l'une des plus importantes — l'igname étant à la fois aliment sacré "
                "et symbole de fertilité. Des rituels marquent chaque étape de la vie : naissance, mariage, funérailles."
            ),
            "fetes_principales": [
                {
                    "nom": "Fête des Ignames",
                    "description": "Célébration de la récolte. L'igname est un aliment sacré et symbole de fertilité.",
                },
                {
                    "nom": "Rituels de naissance",
                    "description": "La naissance, surtout de jumeaux (N'Da), est entourée de croyances fortes. Un autel est dédié aux jumeaux.",
                },
                {
                    "nom": "Rituels funéraires",
                    "description": "Les funérailles sont un moment de communion communautaire intense avec musique, danses et offrandes.",
                },
            ],
        },
        {
            "id": "cult_04",
            "titre": "Artisanat Baoulé",
            "contenu": (
                "L'art Baoulé est une forme d'expression artistique riche : sculpture, tissage, masques. "
                "Les masques Baoulé sont des œuvres sculptées avec une signification spirituelle profonde. "
                "Le pagne Baoulé est tissé selon des techniques ancestrales transmises de génération en génération."
            ),
            "formes_dart": ["Sculpture sur bois", "Tissage de pagnes", "Masques cérémoniels", "Bijoux en or"],
        },
    ],
}

# ============================================================
# 🏛️ SOCIÉTÉ
# ============================================================

SOCIETE = {
    "titre": "Organisation Sociale Baoulé",
    "lecons": [
        {
            "id": "soc_01",
            "titre": "Organisation sociale",
            "contenu": (
                "La société Baoulé est organisée autour de lignages. Les anciens (sages) jouent un rôle central "
                "dans la résolution des conflits et la transmission des savoirs. "
                "Au sein du tissu social, les femmes et les anciens occupent des positions d'importance capitale."
            ),
            "roles": {
                "Le Chef (Roi)": "Autorité politique et spirituelle suprême du village ou du groupe",
                "Les Anciens": "Gardiens de la tradition, arbitres des conflits, transmetteurs du savoir",
                "Les Femmes": "Rôle central dans la vie économique, sociale et spirituelle",
                "Les Jeunes": "Transmission des traditions par l'apprentissage et l'initiation",
            },
        },
        {
            "id": "soc_02",
            "titre": "Vie quotidienne et traditions",
            "contenu": (
                "La vie quotidienne Baoulé est rythmée par l'agriculture, les échanges commerciaux "
                "et les pratiques spirituelles. L'igname, le cacao, le café, le manioc, le maïs et le riz "
                "constituent la base de leur économie et alimentation."
            ),
            "agriculture": ["Igname (sacré)", "Cacao", "Café", "Manioc", "Maïs", "Riz"],
        },
    ],
}

# ============================================================
# 🗺️ TERRITOIRE & GÉOGRAPHIE
# ============================================================

TERRITOIRE = {
    "titre": "Territoire & Géographie Baoulé",
    "description": (
        "Le peuple Baoulé est principalement établi au centre de la Côte d'Ivoire, "
        "dans des villes comme Bouaké et Yamoussoukro, s'étendant entre les fleuves Bandama et Comoé. "
        "La région connue sous le nom de 'V Baoulé' est une étendue de savanes préforestières "
        "qui pénètre dans les forêts denses sur près de deux cents kilomètres."
    ),
    "villes_emblematiques": [
        {
            "nom": "Sakassou",
            "role": "Capitale historique et spirituelle du peuple Baoulé",
        },
        {
            "nom": "Bouaké",
            "role": "Principale ville du pays Baoulé, carrefour économique",
        },
        {
            "nom": "Yamoussoukro",
            "role": "Capitale politique de la Côte d'Ivoire, ancrage Baoulé fort",
        },
        {
            "nom": "Dimbokro",
            "role": "Ville historique, symbole de résistance coloniale Baoulé",
        },
        {
            "nom": "Daoukro",
            "role": "Cœur de la région de l'Iffou, riche en histoire Baoulé",
        },
    ],
    "fleuves": ["Bandama", "Comoé"],
    "superficie_royaume": "30 000 km²",
    "population": "3 à 4 millions d'Ivoiriens d'origine Baoulé",
}

# ============================================================
# 🔢 NOMBRES & COMPTAGE
# ============================================================

NOMBRES = {
    "titre": "Compter en Baoulé",
    "lecons": [
        {
            "id": "nb_01",
            "titre": "Les chiffres de 1 à 10",
            "mots": [
                {"chiffre": 1,  "baoule": "kɔkɔ",   "phonetique": "ko-ko"},
                {"chiffre": 2,  "baoule": "nnyo",    "phonetique": "n-nyo"},
                {"chiffre": 3,  "baoule": "ngbɛ",    "phonetique": "ng-bè"},
                {"chiffre": 4,  "baoule": "nnɔn",    "phonetique": "n-non"},
                {"chiffre": 5,  "baoule": "nnum",    "phonetique": "n-noum"},
                {"chiffre": 6,  "baoule": "nsia",    "phonetique": "n-sia"},
                {"chiffre": 7,  "baoule": "nsɔn",    "phonetique": "n-son"},
                {"chiffre": 8,  "baoule": "mɔjɔ",   "phonetique": "mo-yo"},
                {"chiffre": 9,  "baoule": "ngwlan",  "phonetique": "ng-ouan"},
                {"chiffre": 10, "baoule": "blu",     "phonetique": "blou"},
            ],
        },
        {
            "id": "nb_02",
            "titre": "Les dizaines",
            "mots": [
                {"chiffre": 10,  "baoule": "blu",          "phonetique": "blou"},
                {"chiffre": 20,  "baoule": "nnyo blu",     "phonetique": "n-nyo blou"},
                {"chiffre": 30,  "baoule": "ngbɛ blu",     "phonetique": "ng-bè blou"},
                {"chiffre": 40,  "baoule": "nnɔn blu",     "phonetique": "n-non blou"},
                {"chiffre": 50,  "baoule": "nnum blu",     "phonetique": "n-noum blou"},
                {"chiffre": 100, "baoule": "awula kɔkɔ",   "phonetique": "a-oula ko-ko"},
            ],
        },
    ],
}

# ============================================================
# 📛 PRÉNOMS BAOULÉS
# ============================================================

PRENOMS = {
    "titre": "Prénoms Baoulés",
    "description": (
        "Traditionnellement, les prénoms Baoulé sont déterminés par le jour de naissance, "
        "l'ordre dans la fratrie et les circonstances de la naissance."
    ),
    "par_jour": [
        {"jour_fr": "Lundi",    "jour_baoule": "Kissié",   "masculin": "Kouassi",          "feminin": "Akissi"},
        {"jour_fr": "Mardi",    "jour_baoule": "Djolai",   "masculin": "Kouadio",          "feminin": "Adjoua"},
        {"jour_fr": "Mercredi", "jour_baoule": "Mlan",     "masculin": "Konan",            "feminin": "Amenan"},
        {"jour_fr": "Jeudi",    "jour_baoule": "Wé",       "masculin": "Kouakou",          "feminin": "Ahou"},
        {"jour_fr": "Vendredi", "jour_baoule": "Yah",      "masculin": "Yao",              "feminin": "Aya"},
        {"jour_fr": "Samedi",   "jour_baoule": "Foué",     "masculin": "Koffi",            "feminin": "Affoué"},
        {"jour_fr": "Dimanche", "jour_baoule": "Mon-nin",  "masculin": "Kouamé",           "feminin": "Amoin"},
    ],
    "par_rang": [
        {"rang": "3ème enfant de même sexe", "prenom": "N'guessan"},
        {"rang": "4ème enfant de même sexe", "prenom": "N'dri"},
        {"rang": "9ème enfant",              "prenom": "N'goran"},
        {"rang": "10ème enfant",             "prenom": "Brou"},
        {"rang": "11ème enfant",             "prenom": "Loukou"},
        {"rang": "12ème enfant",             "prenom": "N'gbin"},
        {"rang": "Enfant de sexe différent après série", "prenom": "Kindôh"},
    ],
    "par_circonstance": [
        {"circonstance": "Né lorsque la mère était hors de la maison", "prenom": "Atoumgbré"},
        {"circonstance": "Né la tête tournée vers le sol",             "prenom": "Ahoutou"},
        {"circonstance": "Jumeaux (craints et honorés)",               "prenom": "N'Da"},
        {"circonstance": "Enfant né après des jumeaux (leur guide)",   "prenom": "Amani"},
        {"circonstance": "Né dans le désespoir (conjurer le sort)",    "prenom": "N'Gonian"},
        {"circonstance": "Enfant prématuré",                           "prenom": "Atiman"},
        {"circonstance": "Albinos",                                    "prenom": "Fri"},
    ],
}

# ============================================================
# 🌙 CONTES & LÉGENDES (Les Contes de Tano Kan)
# ============================================================

CONTES = {
    "titre": "Contes & Légendes Baoulé — Les Contes de Tano Kan",
    "description": (
        "Série de contes traditionnels mettant en scène des animaux porteurs de leçons morales, "
        "dans la tradition orale Baoulé. Source : baoule.ci."
    ),
    "contes": [
        {
            "id": "conte_04",
            "titre": "La rivière qui ne répondit pas",
            "theme": "L'écoute et l'humilité face à la nature",
        },
        {
            "id": "conte_05",
            "titre": "Le chien qui ne suivit plus personne",
            "theme": "La loyauté et la trahison",
        },
        {
            "id": "conte_06",
            "titre": "Le léopard qui marcha sans bruit",
            "theme": "La prudence et la discrétion",
        },
        {
            "id": "conte_07",
            "titre": "La tortue qui arriva avant tous",
            "theme": "La persévérance et la ruse",
        },
        {
            "id": "conte_08",
            "titre": "L'oiseau qui refusa de chanter",
            "theme": "La liberté et la résistance",
        },
    ],
    "legende_fondatrice": {
        "titre": "La Légende de la Reine Abla Pokou",
        "resume": (
            "La Reine Abla Pokou, figure emblématique du XVIIIe siècle, "
            "sacrifia son fils unique pour permettre à son peuple de traverser le fleuve Comoé. "
            "Ce sacrifice est le mythe fondateur du peuple Baoulé."
        ),
    },
}

# ============================================================
# 📚 VOCABULAIRE COURANT (par thèmes)
# ============================================================

VOCABULAIRE = {
    "🎨 Couleurs": [
        {"francais": "rouge",   "baoule": "mɔnɛ"},
        {"francais": "bleu",    "baoule": "blɔblɔ"},
        {"francais": "vert",    "baoule": "gblɛgblɛ"},
        {"francais": "blanc",   "baoule": "fitɛ"},
        {"francais": "noir",    "baoule": "tuntun"},
        {"francais": "jaune",   "baoule": "ɔhun"},
    ],
    "🍽️ Nourriture et Boissons": [
        {"francais": "igname",   "baoule": "alo"},
        {"francais": "riz",      "baoule": "ble"},
        {"francais": "eau",      "baoule": "nzue"},
        {"francais": "viande",   "baoule": "wlɛ"},
        {"francais": "poisson",  "baoule": "jɛn"},
        {"francais": "banane",   "baoule": "bɔkɔ"},
        {"francais": "manioc",   "baoule": "attiɛkɛ"},
    ],
    "🫀 Parties du Corps": [
        {"francais": "tête",     "baoule": "ti"},
        {"francais": "main",     "baoule": "sa"},
        {"francais": "pied",     "baoule": "nan"},
        {"francais": "œil",      "baoule": "nyɔn"},
        {"francais": "oreille",  "baoule": "asi"},
        {"francais": "bouche",   "baoule": "nu"},
        {"francais": "nez",      "baoule": "nzɔ"},
        {"francais": "ventre",   "baoule": "ya"},
    ],
    "🏠 Maison et Habitation": [
        {"francais": "maison",   "baoule": "fie"},
        {"francais": "porte",    "baoule": "ɔnin"},
        {"francais": "fenêtre",  "baoule": "ɔnin kpɛtɛ"},
        {"francais": "lit",      "baoule": "gie"},
        {"francais": "cuisine",  "baoule": "diguɛ fie"},
        {"francais": "village",  "baoule": "kro"},
    ],
    "🌳 Nature et Environnement": [
        {"francais": "arbre",    "baoule": "aya"},
        {"francais": "soleil",   "baoule": "owia"},
        {"francais": "pluie",    "baoule": "nzue tɔ"},
        {"francais": "fleuve",   "baoule": "sran"},
        {"francais": "montagne", "baoule": "blɔ"},
        {"francais": "forêt",    "baoule": "ɛnzin"},
        {"francais": "terre",    "baoule": "sɔ"},
    ],
    "☀️ Temps et Climat": [
        {"francais": "aujourd'hui", "baoule": "siɛn"},
        {"francais": "demain",      "baoule": "kɔ"},
        {"francais": "hier",        "baoule": "kunngba"},
        {"francais": "matin",       "baoule": "ahin"},
        {"francais": "soir",        "baoule": "anou"},
        {"francais": "nuit",        "baoule": "ngua"},
        {"francais": "jour",        "baoule": "lika"},
    ],
    "👕 Vêtements et Accessoires": [
        {"francais": "pagne",        "baoule": "kita"},
        {"francais": "habit",        "baoule": "awɔ"},
        {"francais": "chapeau",      "baoule": "ti awɔ"},
        {"francais": "chaussures",   "baoule": "nan sɛ"},
        {"francais": "tissu",        "baoule": "ɔwu"},
    ],
    "💼 Travail et Profession": [
        {"francais": "agriculteur",  "baoule": "sɔ diwlɛ"},
        {"francais": "chef",         "baoule": "ɔwun"},
        {"francais": "commerçant",   "baoule": "adjanma"},
        {"francais": "pêcheur",      "baoule": "jɛn niman"},
        {"francais": "tisserand",    "baoule": "ɔwu diwlɛ"},
    ],
    "😊 Émotions et Sentiments": [
        {"francais": "joie",        "baoule": "awlɔ"},
        {"francais": "tristesse",   "baoule": "ya flɛ"},
        {"francais": "amour",       "baoule": "dɔ"},
        {"francais": "colère",      "baoule": "ɔdwuman"},
        {"francais": "peur",        "baoule": "sɔ"},
        {"francais": "paix",        "baoule": "lalɛ"},
    ],
    "⚕️ Santé et Médecine": [
        {"francais": "maladie",     "baoule": "yaflɛ"},
        {"francais": "médecin",     "baoule": "dɔkitɛ"},
        {"francais": "médicament",  "baoule": "dihɛ"},
        {"francais": "douleur",     "baoule": "ya"},
        {"francais": "guérison",    "baoule": "yaflɛ wɔ"},
    ],
    "🦁 Animaux": [
        {"francais": "lion",         "baoule": "gyata"},
        {"francais": "éléphant",     "baoule": "sui"},
        {"francais": "singe",        "baoule": "alɛ"},
        {"francais": "oiseau",       "baoule": "anoma"},
        {"francais": "serpent",      "baoule": "owɔ"},
        {"francais": "tortue",       "baoule": "kɔnkɔn"},
        {"francais": "léopard",      "baoule": "kɛtɛ"},
        {"francais": "hippopotame",  "baoule": "amoa"},
    ],
}

# ============================================================
# 🗣️ EXPRESSIONS IDIOMATIQUES
# ============================================================

EXPRESSIONS_IDIOMATIQUES = [
    {
        "baoule": "fjǎ-dí",
        "literal": "cacher-manger",
        "sens": "boutique",
    },
    {
        "baoule": "fìtá-si˛̰̂",
        "literal": "souffler-feu",
        "sens": "éventail",
    },
    {
        "baoule": "ŋ̀ɡwa˛ ́-ɲa˛ ́ma˛ ̀",
        "literal": "vie-corde",
        "sens": "longévité",
    },
    {
        "baoule": "di blà",
        "literal": "manger femme",
        "sens": "faire l'amour",
    },
    {
        "baoule": "Akwaba!",
        "literal": "Bienvenue parmi nous !",
        "sens": "Accueil chaleureux après un voyage",
    },
]

# ============================================================
# 🔤 GRAMMAIRE DE BASE
# ============================================================

GRAMMAIRE = {
    "titre": "Grammaire Baoulé — Notions de base",
    "famille_linguistique": "Langues Akan / Tano central",
    "type": "Langue à tons (tonal)",
    "ordre_des_mots": "Sujet - Verbe - Objet (SVO)",
    "regles": [
        "Les adjectifs sont toujours placés APRÈS le nom",
        "La langue est tonale : le sens change selon la hauteur de la voix",
        "Les impératifs à la 2e personne du singulier se forment sans pronom sujet",
        "La forme minimale des adjectifs est Consonne-Voyelle (CV)",
    ],
    "morphemes_grammaticaux": ["/jɛ/", "/ni/", "/kɛ/", "/nga/", "/mɛ̰/", "/ti/"],
    "note": (
        "Ces morphèmes remplissent des fonctions syntaxiques (coordonnants, complémenteurs) "
        "mais n'ont pas de sens pris isolément."
    ),
}

# ============================================================
# 🔧 FONCTION PRINCIPALE — get_context()
# ============================================================

def get_context(rubrique: str = "tout") -> dict:
    """
    Retourne le contenu Baoulé pour une rubrique donnée.

    Paramètres :
        rubrique (str) : Nom de la rubrique souhaitée.
            Valeurs possibles :
            'histoire', 'culture', 'societe', 'territoire',
            'nombres', 'prenoms', 'contes', 'vocabulaire',
            'grammaire', 'expressions', 'tout'

    Retourne :
        dict : Données structurées pour la rubrique demandée.
    """
    catalogue = {
        "histoire":    HISTOIRE,
        "culture":     CULTURE,
        "societe":     SOCIETE,
        "territoire":  TERRITOIRE,
        "nombres":     NOMBRES,
        "prenoms":     PRENOMS,
        "contes":      CONTES,
        "vocabulaire": VOCABULAIRE,
        "grammaire":   GRAMMAIRE,
        "expressions": EXPRESSIONS_IDIOMATIQUES,
        "tout": {
            "histoire":    HISTOIRE,
            "culture":     CULTURE,
            "societe":     SOCIETE,
            "territoire":  TERRITOIRE,
            "nombres":     NOMBRES,
            "prenoms":     PRENOMS,
            "contes":      CONTES,
            "vocabulaire": VOCABULAIRE,
            "grammaire":   GRAMMAIRE,
            "expressions": EXPRESSIONS_IDIOMATIQUES,
        },
    }

    rubrique = rubrique.lower().strip()
    if rubrique not in catalogue:
        rubriques_dispo = list(catalogue.keys())
        return {
            "erreur": f"Rubrique '{rubrique}' introuvable.",
            "rubriques_disponibles": rubriques_dispo,
        }

    return catalogue[rubrique]


def lister_rubriques() -> list:
    """Retourne la liste de toutes les rubriques disponibles."""
    return [
        "histoire", "culture", "societe", "territoire",
        "nombres", "prenoms", "contes", "vocabulaire",
        "grammaire", "expressions", "tout",
    ]


def rechercher_mot(mot_francais: str) -> list:
    """
    Recherche un mot français dans tout le vocabulaire Baoulé.

    Paramètres :
        mot_francais (str) : Mot en français à rechercher.

    Retourne :
        list : Liste des entrées correspondantes avec catégorie, français et baoulé.
    """
    resultats = []
    mot = mot_francais.lower().strip()
    for categorie, mots in VOCABULAIRE.items():
        for entree in mots:
            if mot in entree["francais"].lower():
                resultats.append({
                    "categorie": categorie,
                    "francais":  entree["francais"],
                    "baoule":    entree["baoule"],
                })
    return resultats if resultats else [{"message": f"Aucun résultat pour '{mot_francais}'"}]


def get_prenom_par_jour(jour: str) -> dict:
    """
    Retourne les prénoms Baoulé correspondant à un jour de la semaine.

    Paramètres :
        jour (str) : Jour en français (ex: 'lundi', 'vendredi').

    Retourne :
        dict : Prénoms masculin, féminin et jour en Baoulé.
    """
    jour = jour.lower().strip()
    for entree in PRENOMS["par_jour"]:
        if entree["jour_fr"].lower() == jour:
            return entree
    return {"message": f"Jour '{jour}' non trouvé. Essayez : lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche."}


# ============================================================
# 🧪 TEST RAPIDE (exécution directe)
# ============================================================

if __name__ == "__main__":
    import json

    print("=" * 60)
    print("  LingX — Base de données Baoulé")
    print("  Source : baoule.ci")
    print("=" * 60)

    print("\n📋 Rubriques disponibles :")
    print(lister_rubriques())

    print("\n🔍 Recherche du mot 'eau' :")
    print(json.dumps(rechercher_mot("eau"), ensure_ascii=False, indent=2))

    print("\n📛 Prénom du vendredi :")
    print(json.dumps(get_prenom_par_jour("vendredi"), ensure_ascii=False, indent=2))

    print("\n🔢 Nombres (leçon 1) :")
    lecon_nombres = get_context("nombres")
    for mot in lecon_nombres["lecons"][0]["mots"]:
        print(f"  {mot['chiffre']:>3} → {mot['baoule']:<12} ({mot['phonetique']})")

    print("\n✅ Données chargées avec succès.")

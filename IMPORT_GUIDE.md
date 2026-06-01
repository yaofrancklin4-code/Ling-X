#  Guide d'Import du Dictionnaire Baoulé

##  Prérequis

Assurez-vous que:
- L'environnement virtuel est activé
- Django est installé
- La base de données est configurée

##  Étapes d'Installation

### 1. Activer l'environnement virtuel

```bash
# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate
```

### 2. Appliquer les migrations

```bash
cd monprojet
python manage.py makemigrations
python manage.py migrate
```

### 3. Importer le dictionnaire

```bash
python import_dictionary.py
```

Cette commande va:
- ✅ Charger les 436 entrées du dictionnaire JSON
- ✅ Créer automatiquement 21 catégories thématiques
- ✅ Générer des leçons avec 15 mots maximum chacune
- ✅ Créer des quiz automatiques pour chaque leçon
- ✅ Peupler le dictionnaire complet

### 4. Créer un super utilisateur (si nécessaire)

```bash
python manage.py createsuperuser
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

##  Résultat Attendu

Après l'import, vous aurez:

- **21 catégories** organisées par thème:
  -  Salutations
  -  Famille
  - ️ Nourriture
  -  Corps Humain
  -  Nombres
  - ⏰ Temps
  -  Couleurs
  -  Animaux
  -  Nature
  -  Maison
  -  Verbes Courants
  - ⭐ Adjectifs
  -  Pronoms & Mots Outils
  -  Émotions
  -  Santé
  -  Transport
  -  Métiers
  -  Argent & Commerce
  -  Culture & Tradition
  -  Expressions Utiles
  -  Divers

- **~50-60 leçons** avec vocabulaire progressif
- **~250+ quiz** générés automatiquement
- **436 mots** dans le dictionnaire complet

##  Fonctionnalités Disponibles

### Pour les Apprenants

1. **Parcourir les catégories** - `/categories/`
2. **Suivre des leçons** - `/lesson/<id>/`
3. **Passer des quiz** - `/quiz/<lesson_id>/`
4. **Consulter le dictionnaire** - `/dictionary/`
5. **Voir sa progression** - `/dashboard/`

### Pour les Administrateurs

1. **Interface admin** - `/admin/`
2. **Gérer les catégories**
3. **Modifier les leçons**
4. **Ajouter du vocabulaire**
5. **Créer des quiz personnalisés**

##  Réimporter le Dictionnaire

Si vous voulez réimporter (⚠️ cela supprimera les données existantes):

```bash
python import_dictionary.py
```

##  Structure des Données

### Catégorie
- Nom
- Description
- Icône emoji
- Ordre d'affichage

### Leçon
- Titre
- Catégorie parente
- Difficulté (débutant/intermédiaire/avancé)
- Points à gagner
- Vocabulaire associé

### Vocabulaire
- Mot en Baoulé
- Traduction française
- Prononciation phonétique
- Exemple de phrase
- Leçon associée

### Quiz
- Question
- Type (QCM, traduction, etc.)
- Choix de réponses
- Points

##  Personnalisation

### Modifier le nombre de mots par leçon

Dans `import_dictionary.py`, ligne 145:
```python
words_per_lesson = 15  # Changez cette valeur
```

### Modifier le nombre de quiz par leçon

Dans `import_dictionary.py`, ligne 42:
```python
for i, vocab in enumerate(vocab_list[:5]):  # Changez 5
```

### Ajouter de nouvelles catégories

Dans `import_dictionary.py`, ligne 17-38, ajoutez vos catégories:
```python
categories = {
    'Votre Catégorie': ['mot1', 'mot2', ...],
    # ...
}
```

##  Dépannage

### Erreur: "No module named 'django'"
```bash
pip install django djangorestframework pillow
```

### Erreur: "Table doesn't exist"
```bash
python manage.py migrate
```

### Erreur: "File not found"
Vérifiez que `dictionnaire_baoule_cleaned.json` est dans le dossier `monprojet/`

##  Support

Pour toute question:
1. Vérifiez les logs d'erreur
2. Consultez la documentation Django
3. Ouvrez une issue sur GitHub

## ✨ Améliorations Futures

- [ ] Import incrémental (sans supprimer les données)
- [ ] Génération d'audio automatique
- [ ] Import d'images pour le vocabulaire
- [ ] Export du dictionnaire en PDF
- [ ] API REST pour accès mobile

---

**Bon apprentissage! **

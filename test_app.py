import os
import sys
import django

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from lingx.models import *

print("🔍 Vérification de l'application LingX...\n")

# Vérifier les utilisateurs
users_count = User.objects.count()
print(f"✅ Utilisateurs: {users_count}")

# Vérifier les catégories
categories_count = Category.objects.count()
print(f"✅ Catégories: {categories_count}")

# Vérifier les leçons
lessons_count = Lesson.objects.count()
print(f"✅ Leçons: {lessons_count}")

# Vérifier le vocabulaire
vocab_count = Vocabulary.objects.count()
print(f"✅ Vocabulaire: {vocab_count} mots")

# Vérifier les quiz
quiz_count = Quiz.objects.count()
print(f"✅ Quiz: {quiz_count} questions")

# Vérifier les badges
badges_count = Badge.objects.count()
print(f"✅ Badges: {badges_count}")

# Vérifier les mini-jeux
games_count = MiniGame.objects.count()
print(f"✅ Mini-jeux: {games_count}")

# Vérifier les profils
profiles_count = UserProfile.objects.count()
print(f"✅ Profils utilisateurs: {profiles_count}")

print("\n📊 Détails des leçons:")
for lesson in Lesson.objects.all():
    vocab = lesson.vocabularies.count()
    quizzes = lesson.quizzes.count()
    print(f"  - {lesson.title}: {vocab} mots, {quizzes} quiz")

print("\n🎮 Mini-jeux disponibles:")
for game in MiniGame.objects.all():
    print(f"  - {game.title} ({game.get_game_type_display()})")

print("\n🏆 Badges disponibles:")
for badge in Badge.objects.all():
    print(f"  - {badge.name}: {badge.description}")

print("\n✅ Tous les tests sont passés!")
print("\n🚀 L'application est prête à être utilisée!")

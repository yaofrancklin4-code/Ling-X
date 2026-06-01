from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='📚')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    DIFFICULTY_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='debutant')
    order = models.IntegerField(default=0)
    number = models.IntegerField(default=0, help_text="Numéro de la leçon (1-22) pour déblocage par niveau")
    points = models.IntegerField(default=10)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.title

class Vocabulary(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='vocabularies')
    word_baule = models.CharField(max_length=100)
    word_french = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=150, blank=True)
    audio_file = models.FileField(upload_to='audio/vocabulary/', blank=True, null=True)
    example_sentence = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/vocabulary/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Vocabularies"
    
    def __str__(self):
        return f"{self.word_baule} - {self.word_french}"

class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('mcq', 'QCM'),
        ('translation', 'Traduction'),
        ('listening', 'Écoute'),
        ('matching', 'Association'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES, default='mcq')
    audio_file = models.FileField(upload_to='audio/quiz/', blank=True, null=True)
    points = models.IntegerField(default=5)
    order = models.IntegerField(default=0)
    number = models.IntegerField(default=0, help_text="Numéro du test (1-22) pour déblocage par niveau")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['lesson', 'order']
    
    def __str__(self):
        return f"Quiz: {self.question[:50]}"

class QuizChoice(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.choice_text

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Apprenant'),
        ('teacher', 'Professeur'),
        ('avance', 'Avancé'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=20, blank=True, help_text="Numéro WhatsApp avec indicatif (ex: +225XXXXXXXXXX)")
    is_verified = models.BooleanField(default=False, help_text="Professeur/Expert vérifié")
    speciality = models.CharField(max_length=200, blank=True, help_text="Spécialité (pour professeurs/experts)")
    years_experience = models.IntegerField(default=0, help_text="Années d'expérience")
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    streak_days = models.IntegerField(default=0)
    last_activity = models.DateField(auto_now=True)
    is_premium = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True, help_text="Disponible pour échanger sur WhatsApp")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Profile de {self.user.username}"
    
    def add_points(self, points):
        self.total_points += points
        self.level = (self.total_points // 100) + 1
        
        # Promotion automatique en avancé si 1000+ points
        if self.total_points >= 1000 and self.role == 'student':
            self.role = 'avance'
            self.is_verified = True
        
        self.save()
    
    def get_whatsapp_link(self):
        if self.phone_number:
            # Nettoyer le numéro (enlever espaces, tirets, etc.)
            clean_number = ''.join(filter(str.isdigit, self.phone_number))
            if not clean_number.startswith('+'):
                clean_number = '+' + clean_number
            message = f"Bonjour, je vous contacte depuis LingX pour apprendre le Baoulé."
            return f"https://wa.me/{clean_number}?text={message}"
        return None

class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'lesson']
    
    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(QuizChoice, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Quiz {self.quiz.id}"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    image = models.ImageField(upload_to='badges/', blank=True, null=True)
    condition_type = models.CharField(max_length=50)
    condition_value = models.IntegerField()
    points_reward = models.IntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'badge']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

class MiniGame(models.Model):
    GAME_TYPE_CHOICES = [
        ('memory', 'Jeu de Mémoire'),
        ('word_match', 'Association de Mots'),
        ('speed_quiz', 'Quiz Rapide'),
        ('pronunciation', 'Prononciation'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='minigames')
    title = models.CharField(max_length=200)
    description = models.TextField()
    game_type = models.CharField(max_length=20, choices=GAME_TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=Lesson.DIFFICULTY_CHOICES, default='debutant')
    points_reward = models.IntegerField(default=20)
    time_limit = models.IntegerField(default=60, help_text="Temps en secondes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_scores')
    game = models.ForeignKey(MiniGame, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    time_taken = models.IntegerField(help_text="Temps en secondes")
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-score', 'time_taken']
    
    def __str__(self):
        return f"{self.user.username} - {self.game.title}: {self.score}"

class DailyChallenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_date = models.DateField(unique=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    points_reward = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Défi du {self.challenge_date}"

class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'challenge']
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"

class Leaderboard(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Quotidien'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
        ('all_time', 'Tout le temps'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    period_start = models.DateField()
    period_end = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['period', 'rank']
        unique_together = ['user', 'period', 'period_start']
    
    def __str__(self):
        return f"{self.user.username} - {self.period}: Rang {self.rank}"

class CultureContent(models.Model):
    """Contenu culturel Baoulé"""
    CONTENT_TYPE_CHOICES = [
        ('tradition', 'Tradition'),
        ('history', 'Histoire'),
        ('custom', 'Coutume'),
        ('celebration', 'Célébration'),
    ]
    
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    description = models.TextField()
    detailed_content = models.TextField()
    image = models.ImageField(upload_to='images/culture/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Culture Contents"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

class Proverb(models.Model):
    """Proverbes et expressions traditionnelles Baoulé"""
    proverb_baule = models.TextField()
    proverb_french = models.TextField()
    meaning = models.TextField(help_text="Explication du proverbe")
    usage_context = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100, blank=True, help_text="Ex: Sagesse, Famille, Travail")
    audio_file = models.FileField(upload_to='audio/proverbs/', blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.proverb_baule[:50]}..."

class UserCultureView(models.Model):
    """Suivi des contenus culturels consultés par l'utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='culture_views')
    culture_content = models.ForeignKey(CultureContent, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'culture_content']
    
    def __str__(self):
        return f"{self.user.username} - {self.culture_content.title}"


class BaouleName(models.Model):
    """Prénoms Baoulés et leurs significations"""
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('U', 'Unisexe'),
    ]
    
    name_baule = models.CharField(max_length=100, unique=True)
    meaning_french = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    origin = models.CharField(max_length=200, blank=True, help_text="Origine ou histoire du prénom")
    cultural_significance = models.TextField(blank=True, help_text="Signification culturelle")
    similar_names = models.TextField(blank=True, help_text="Prénoms similaires ou variantes")
    audio_file = models.FileField(upload_to='audio/names/', blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name_baule']
    
    def __str__(self):
        return f"{self.name_baule} - {self.meaning_french[:50]}"


class Story(models.Model):
    """Histoires, légendes et contes Baoulés"""
    STORY_TYPE_CHOICES = [
        ('legend', 'Légende'),
        ('tale', 'Conte'),
        ('history', 'Histoire'),
        ('fable', 'Fable'),
    ]
    
    title = models.CharField(max_length=250)
    story_type = models.CharField(max_length=20, choices=STORY_TYPE_CHOICES, default='tale')
    description = models.TextField()
    full_text = models.TextField()
    baule_text = models.TextField(blank=True, help_text="Texte original en Baoulé si disponible")
    moral_lesson = models.TextField(blank=True, help_text="Leçon morale ou enseignement")
    characters = models.TextField(blank=True, help_text="Personnages principaux (séparés par des virgules)")
    difficulty = models.CharField(max_length=20, choices=Lesson.DIFFICULTY_CHOICES, default='debutant')
    image = models.ImageField(upload_to='images/stories/', blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/stories/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Stories"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title


class StoryVocabulary(models.Model):
    """Vocabulaire spécifique aux histoires"""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='vocabularies')
    word_baule = models.CharField(max_length=100)
    word_french = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=150, blank=True)
    context_sentence = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Story Vocabularies"
    
    def __str__(self):
        return f"{self.word_baule} - {self.word_french}"


class UserStoryView(models.Model):
    """Suivi des histoires consultées par l'utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_views')
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'story']
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.story.title}"


class DictionaryEntry(models.Model):
    """Dictionnaire Baoulé enrichi"""
    word_baule = models.CharField(max_length=100, unique=True)
    word_french = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=150, blank=True)
    part_of_speech = models.CharField(max_length=50, blank=True, help_text="Nom, Verbe, Adjectif, etc.")
    definition = models.TextField()
    example_sentence_baule = models.TextField(blank=True)
    example_sentence_french = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='audio/dictionary/', blank=True, null=True)
    synonyms = models.TextField(blank=True, help_text="Synonymes (séparés par des virgules)")
    antonyms = models.TextField(blank=True, help_text="Antonymes (séparés par des virgules)")
    usage_context = models.CharField(max_length=200, blank=True)
    is_common = models.BooleanField(default=False)
    is_formal = models.BooleanField(default=False)
    search_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Dictionary Entries"
        ordering = ['word_baule']
        indexes = [
            models.Index(fields=['word_baule']),
            models.Index(fields=['is_common']),
        ]
    
    def __str__(self):
        return f"{self.word_baule} - {self.word_french}"


# ============ GAMIFICATION & NOTIFICATIONS ============

class UserNotification(models.Model):
    """Système de notifications pour l'utilisateur"""
    NOTIFICATION_TYPES = [
        ('achievement', '🏆 Succès'),
        ('badge', '🎖️ Badge'),
        ('milestone', '⭐ Jalon'),
        ('streak', '🔥 Série'),
        ('level_up', '⬆️ Niveau'),
        ('reward', '🎁 Récompense'),
        ('challenge', '🎯 Défi'),
        ('leaderboard', '📊 Classement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    icon = models.CharField(max_length=50, default='ℹ️')
    points_awarded = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class UserStreak(models.Model):
    """Suivi des séries de jours consécutifs d'apprentissage"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    streak_started = models.DateField(null=True, blank=True)
    total_activities = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - Série: {self.current_streak} jours"


class DailyReward(models.Model):
    """Récompenses quotidiennes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_rewards')
    reward_date = models.DateField()
    points = models.IntegerField(default=10)
    bonus_multiplier = models.FloatField(default=1.0, help_text="Multiplicateur basé sur le streak")
    is_claimed = models.BooleanField(default=False)
    claimed_at = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=200, default="Connexion quotidienne")
    
    class Meta:
        unique_together = ['user', 'reward_date']
        ordering = ['-reward_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.reward_date}"


class Achievement(models.Model):
    """Réalisations spéciales"""
    ACHIEVEMENT_CATEGORY = [
        ('learning', '📚 Apprentissage'),
        ('completion', '✅ Complétude'),
        ('consistency', '🔥 Constance'),
        ('speed', '⚡ Rapidité'),
        ('accuracy', '🎯 Précision'),
        ('social', '👥 Social'),
        ('collector', '🏺 Collecteur'),
    ]
    
    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=ACHIEVEMENT_CATEGORY)
    icon = models.CharField(max_length=50, default='⭐')
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    condition_type = models.CharField(max_length=50)
    condition_value = models.IntegerField()
    points_reward = models.IntegerField(default=100)
    rarity = models.CharField(
        max_length=10, 
        choices=[('common', 'Courant'), ('rare', 'Rare'), ('epic', 'Épique'), ('legendary', 'Légendaire')],
        default='common'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Suivi des réalisations de l'utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    times_completed = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ['user', 'achievement']
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class VocabularyReview(models.Model):
    """Suivi des révisions SRS pour chaque mot"""
    DIFFICULTY_LEVELS = [
        ('easy', '✓ Facile'),
        ('medium', '≈ Normal'),
        ('hard', '✗ Difficile'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vocabulary_reviews')
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
    difficulty_rating = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS)
    reviewed_at = models.DateTimeField(auto_now_add=True)
    review_count = models.IntegerField(default=0)
    next_review_date = models.DateField(null=True, blank=True)
    retention_score = models.FloatField(default=0.0)  # 0-100
    
    class Meta:
        ordering = ['user', '-reviewed_at']
        indexes = [
            models.Index(fields=['user', 'vocabulary']),
            models.Index(fields=['next_review_date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.vocabulary.word_baule}"

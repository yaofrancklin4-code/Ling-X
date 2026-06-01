from django.contrib import admin
from .models import (
    Category, Lesson, Vocabulary, Quiz, QuizChoice, 
    UserProfile, LessonProgress, QuizAttempt, Badge, 
    UserBadge, MiniGame, GameScore, DailyChallenge, 
    UserChallenge, Leaderboard, CultureContent, Proverb, UserCultureView,
    BaouleName, Story, StoryVocabulary, UserStoryView, DictionaryEntry
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'created_at']
    list_editable = ['order']
    search_fields = ['name']

class VocabularyInline(admin.TabularInline):
    model = Vocabulary
    extra = 1

class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'points', 'is_premium', 'order', 'created_at']
    list_filter = ['category', 'difficulty', 'is_premium']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_premium']
    inlines = [VocabularyInline, QuizInline]

@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ['word_baule', 'word_french', 'lesson', 'pronunciation', 'created_at']
    list_filter = ['lesson__category']
    search_fields = ['word_baule', 'word_french']

class QuizChoiceInline(admin.TabularInline):
    model = QuizChoice
    extra = 4

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['question', 'lesson', 'quiz_type', 'points', 'order']
    list_filter = ['quiz_type', 'lesson__category']
    search_fields = ['question']
    inlines = [QuizChoiceInline]

@admin.register(QuizChoice)
class QuizChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'quiz', 'is_correct', 'order']
    list_filter = ['is_correct']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points', 'level', 'streak_days', 'is_premium', 'created_at']
    list_filter = ['is_premium', 'level']
    search_fields = ['user__username', 'user__email']

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_completed', 'score', 'attempts', 'completed_at']
    list_filter = ['is_completed', 'lesson__category']
    search_fields = ['user__username', 'lesson__title']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'is_correct', 'points_earned', 'created_at']
    list_filter = ['is_correct', 'created_at']
    search_fields = ['user__username']

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'condition_type', 'condition_value', 'points_reward']
    list_filter = ['condition_type']
    search_fields = ['name']

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']

@admin.register(MiniGame)
class MiniGameAdmin(admin.ModelAdmin):
    list_display = ['title', 'game_type', 'difficulty', 'points_reward', 'time_limit', 'is_active']
    list_filter = ['game_type', 'difficulty', 'is_active']
    search_fields = ['title']

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'game', 'score', 'time_taken', 'points_earned', 'created_at']
    list_filter = ['game', 'created_at']
    search_fields = ['user__username']

@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'challenge_date', 'points_reward', 'is_active']
    list_filter = ['is_active', 'challenge_date']
    search_fields = ['title']

@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'is_completed', 'points_earned', 'completed_at']
    list_filter = ['is_completed', 'challenge__challenge_date']
    search_fields = ['user__username']

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'period', 'points', 'rank', 'period_start', 'period_end']
    list_filter = ['period', 'period_start']
    search_fields = ['user__username']

@admin.register(CultureContent)
class CultureContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'is_featured', 'order', 'created_at']
    list_filter = ['content_type', 'is_featured']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_featured']

@admin.register(Proverb)
class ProverbAdmin(admin.ModelAdmin):
    list_display = ['proverb_baule', 'proverb_french', 'category', 'order']
    list_filter = ['category']
    search_fields = ['proverb_baule', 'proverb_french', 'meaning']

@admin.register(UserCultureView)
class UserCultureViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'culture_content', 'viewed_at']
    list_filter = ['culture_content', 'viewed_at']
    search_fields = ['user__username', 'culture_content__title']


@admin.register(BaouleName)
class BaouléNameAdmin(admin.ModelAdmin):
    list_display = ['name_baule', 'meaning_french', 'gender', 'order', 'created_at']
    list_filter = ['gender', 'order']
    search_fields = ['name_baule', 'meaning_french']
    list_editable = ['order']


class StoryVocabularyInline(admin.TabularInline):
    model = StoryVocabulary
    extra = 2


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'story_type', 'difficulty', 'is_featured', 'order', 'created_at']
    list_filter = ['story_type', 'difficulty', 'is_featured']
    search_fields = ['title', 'description', 'full_text']
    list_editable = ['order', 'is_featured']
    inlines = [StoryVocabularyInline]


@admin.register(StoryVocabulary)
class StoryVocabularyAdmin(admin.ModelAdmin):
    list_display = ['word_baule', 'word_french', 'story', 'pronunciation']
    list_filter = ['story']
    search_fields = ['word_baule', 'word_french']


@admin.register(UserStoryView)
class UserStoryViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'story', 'is_completed', 'viewed_at', 'completed_at']
    list_filter = ['is_completed', 'story', 'viewed_at']
    search_fields = ['user__username', 'story__title']


@admin.register(DictionaryEntry)
class DictionaryEntryAdmin(admin.ModelAdmin):
    list_display = ['word_baule', 'word_french', 'part_of_speech', 'is_common', 'is_formal', 'search_count', 'created_at']
    list_filter = ['is_common', 'is_formal', 'part_of_speech', 'usage_context']
    search_fields = ['word_baule', 'word_french', 'definition']
    readonly_fields = ['search_count', 'created_at', 'updated_at']
    list_editable = ['is_common', 'is_formal']
    
    fieldsets = (
        ('Mot et Traduction', {
            'fields': ('word_baule', 'word_french', 'pronunciation')
        }),
        ('Détails Linguistiques', {
            'fields': ('part_of_speech', 'definition', 'usage_context')
        }),
        ('Exemples', {
            'fields': ('example_sentence_baule', 'example_sentence_french'),
            'classes': ('collapse',)
        }),
        ('Relations', {
            'fields': ('synonyms', 'antonyms'),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('is_common', 'is_formal', 'audio_file')
        }),
        ('Métadonnées', {
            'fields': ('search_count', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

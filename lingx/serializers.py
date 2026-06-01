from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, Lesson, Vocabulary, Quiz, QuizChoice,
    UserProfile, LessonProgress, QuizAttempt, Badge,
    UserBadge, MiniGame, GameScore, DailyChallenge,
    CultureContent, Proverb, UserCultureView,
    BaouleName, Story, StoryVocabulary, UserStoryView, DictionaryEntry
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = '__all__'

class QuizChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizChoice
        fields = ['id', 'choice_text', 'order']

class QuizSerializer(serializers.ModelSerializer):
    choices = QuizChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    vocabularies = VocabularySerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()

class LessonProgressSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    
    class Meta:
        model = LessonProgress
        fields = '__all__'

class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer(read_only=True)
    
    class Meta:
        model = QuizAttempt
        fields = '__all__'

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = '__all__'

class MiniGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniGame
        fields = '__all__'

class GameScoreSerializer(serializers.ModelSerializer):
    game = MiniGameSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = GameScore
        fields = '__all__'

class DailyChallengeSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    
    class Meta:
        model = DailyChallenge
        fields = '__all__'


# Nouveaux Sérialiseurs pour le contenu culturel enrichi

class ProverbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proverb
        fields = '__all__'


class CultureContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CultureContent
        fields = '__all__'


class UserCultureViewSerializer(serializers.ModelSerializer):
    culture_content = CultureContentSerializer(read_only=True)
    
    class Meta:
        model = UserCultureView
        fields = '__all__'


class BaouléNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaouleName
        fields = '__all__'


class StoryVocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryVocabulary
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    vocabularies = StoryVocabularySerializer(many=True, read_only=True)
    
    class Meta:
        model = Story
        fields = '__all__'


class UserStoryViewSerializer(serializers.ModelSerializer):
    story = StorySerializer(read_only=True)
    
    class Meta:
        model = UserStoryView
        fields = '__all__'


class DictionaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DictionaryEntry
        fields = '__all__'

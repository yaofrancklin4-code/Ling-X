from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'quizzes', views.QuizViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'game-scores', views.GameScoreViewSet)
router.register(r'proverbs', views.ProverbViewSet)
router.register(r'culture', views.CultureContentViewSet)
router.register(r'baule-names', views.BaouléNameViewSet)
router.register(r'stories', views.StoryViewSet)


urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Catégories et leçons
    path('categories/', views.categories_view, name='categories'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/quiz/', views.quiz_view, name='quiz'),
    
    # Tests
    path('tests/', views.tests_list, name='tests_list'),
    
    # Jeux
    path('games/', views.games_view, name='games'),
    path('game/<int:game_id>/play/', views.game_play, name='game_play'),
    path('save-game-score/', views.save_game_score, name='save_game_score'),
    
    # Contenus culturels
    path('culture/', views.culture_view, name='culture'),
    path('dictionnaire/', views.dictionary_view, name='dictionary'),
    path('submit-quiz-answer/', views.submit_quiz_answer, name='submit_quiz_answer'),
    path('submit-game-points/', views.submit_game_points, name='submit_game_points'),
    path('histoire/', views.histoire_view, name='histoire'),
    path('societe/', views.societe_view, name='societe'),
    path('territoire/', views.territoire_view, name='territoire'),
    path('stories/', views.stories_view, name='stories'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    
    # Vocabulaire
    path('vocabulary/<int:vocab_id>/', views.vocabulary_detail, name='vocabulary_detail'),
    path('review/', views.review_vocabulary, name='review_vocabulary'),
    
    path('baule-names/', views.baule_names_view, name='baule_names'),
    path('proverbs/', views.proverbs_view, name='proverbs'),
    
    # Classement et profil
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('profile/', views.profile_view, name='profile'),
    path('community/', views.community_view, name='community'),
    path('stats/', views.user_stats, name='stats'),
    
    # Gamification & Notifications
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('daily-reward/', views.daily_reward_view, name='daily_reward'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('gamification/', views.gamification_dashboard, name='gamification_dashboard'),
    
    # Google OAuth custom views (skip confirmation pages)
    path('auth/google/login/', views.google_login_direct, name='google_login_direct'),
    path('auth/google/callback/', views.google_login_callback, name='google_login_callback'),
    
    path('a-propos/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('guide/', views.guide_view, name='guide'),

    # API REST
    path('api/', include(router.urls)),
]

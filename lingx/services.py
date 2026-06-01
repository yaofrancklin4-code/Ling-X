"""
Service de gamification pour LingX
Gère les badges, achievements, streaks, notifications, etc.
"""

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
from lingx.models import (
    UserNotification, UserStreak, DailyReward, Achievement, 
    UserAchievement, UserBadge, Badge, LessonProgress, QuizAttempt
)


class GamificationService:
    """Service principal de gamification"""
    
    @staticmethod
    def award_points(user, points, reason="", source_type="quiz"):
        """Attribue des points et déclenche les notifications associées"""
        profile = user.profile
        old_level = profile.level
        old_points = profile.total_points
        
        # Ajouter les points
        profile.add_points(points)
        
        # Créer une notification
        notification_data = {
            'notification_type': 'reward',
            'title': f"🎁 +{points} points",
            'message': f"Vous avez gagné {points} points! {reason}",
            'icon': '✨',
            'points_awarded': points,
        }
        
        # Vérifier les milestones de points
        milestones = [100, 250, 500, 1000, 2500, 5000, 10000]
        if old_points < 1000 and profile.total_points >= 1000:
            notification_data.update({
                'notification_type': 'milestone',
                'title': '⭐ Jalon: 1000 points atteints!',
                'message': 'Vous êtes promu EXPERT!',
                'icon': '⭐',
            })
        
        # Vérifier les changements de niveau
        if profile.level > old_level:
            notification_data.update({
                'notification_type': 'level_up',
                'title': f'⬆️ Niveau {profile.level} atteint!',
                'message': f'Bravo! Vous êtes passé au niveau {profile.level}!',
                'icon': '🎉',
            })
        
        notification = UserNotification.objects.create(user=user, **notification_data)
        
        return notification
    
    @staticmethod
    def update_streak(user):
        """Met à jour le streak de l'utilisateur"""
        today = date.today()
        
        # Obtenir ou créer le streak
        streak, created = UserStreak.objects.get_or_create(user=user)
        
        if streak.last_activity_date is None:
            # Première activité
            streak.current_streak = 1
            streak.longest_streak = 1
            streak.streak_started = today
            streak.last_activity_date = today
            streak.total_activities = 1
        elif streak.last_activity_date == today:
            # Déjà actif aujourd'hui
            pass
        elif streak.last_activity_date == today - timedelta(days=1):
            # Continuation du streak
            streak.current_streak += 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
            streak.last_activity_date = today
            streak.total_activities += 1
            
            # Créer une notification de streak
            if streak.current_streak % 5 == 0:
                UserNotification.objects.create(
                    user=user,
                    notification_type='streak',
                    title=f'🔥 {streak.current_streak} jours de suite!',
                    message=f'Incroyable! Vous avez une série de {streak.current_streak} jours!',
                    icon='🔥',
                    points_awarded=50
                )
        else:
            # Streak brisée
            old_streak = streak.current_streak
            streak.current_streak = 1
            streak.streak_started = today
            streak.last_activity_date = today
            
            if old_streak >= 3:
                UserNotification.objects.create(
                    user=user,
                    notification_type='streak',
                    title='😢 Série interrompue',
                    message=f'Votre série de {old_streak} jours est terminée. Recommencez!',
                    icon='😢',
                )
        
        streak.save()
        return streak
    
    @staticmethod
    def claim_daily_reward(user):
        """Revendique la récompense quotidienne"""
        today = date.today()
        
        # Vérifier s'il existe déjà une récompense pour aujourd'hui
        existing_reward = DailyReward.objects.filter(user=user, reward_date=today).first()
        
        if existing_reward and existing_reward.is_claimed:
            return None, "Vous avez déjà revendiqué votre récompense aujourd'hui"
        
        # Obtenir le multiplicateur de streak
        streak = UserStreak.objects.filter(user=user).first()
        multiplier = 1.0
        if streak:
            multiplier = min(1.0 + (streak.current_streak * 0.1), 3.0)  # Max 3x
        
        # Calculer les points
        base_points = 10
        total_points = int(base_points * multiplier)
        
        # Créer ou mettre à jour la récompense
        reward, created = DailyReward.objects.get_or_create(
            user=user,
            reward_date=today,
            defaults={
                'points': base_points,
                'bonus_multiplier': multiplier,
                'is_claimed': True,
                'claimed_at': timezone.now(),
                'description': f"Bonus quotidien (Multiplicateur: {multiplier:.1f}x)"
            }
        )
        
        if not created and not reward.is_claimed:
            reward.is_claimed = True
            reward.claimed_at = timezone.now()
            reward.save()
        
        # Attribuer les points
        GamificationService.award_points(
            user, 
            total_points, 
            f"(Multiplicateur: {multiplier:.1f}x)",
            "daily_reward"
        )
        
        return reward, f"Vous avez reçu {total_points} points!"
    
    @staticmethod
    def check_and_award_badges(user):
        """Vérifie et attribue les badges si conditions sont remplies"""
        profile = user.profile
        badges_earned = []
        
        # Badge "Premier pas" - Première leçon complétée
        if LessonProgress.objects.filter(user=user, is_completed=True).count() == 1:
            try:
                badge = Badge.objects.get(condition_type='first_lesson')
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    badges_earned.append(badge)
            except Badge.DoesNotExist:
                pass
        
        # Badge "Étudiant" - 5 leçons complétées
        if LessonProgress.objects.filter(user=user, is_completed=True).count() >= 5:
            try:
                badge = Badge.objects.get(condition_type='five_lessons')
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    badges_earned.append(badge)
            except Badge.DoesNotExist:
                pass
        
        # Badge "Maître" - 10 leçons complétées
        if LessonProgress.objects.filter(user=user, is_completed=True).count() >= 10:
            try:
                badge = Badge.objects.get(condition_type='ten_lessons')
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    badges_earned.append(badge)
            except Badge.DoesNotExist:
                pass
        
        # Badge "Quiz Master" - 50 quiz complétés correctement
        if QuizAttempt.objects.filter(user=user, is_correct=True).count() >= 50:
            try:
                badge = Badge.objects.get(condition_type='quiz_master')
                user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    badges_earned.append(badge)
            except Badge.DoesNotExist:
                pass
        
        # Créer des notifications pour chaque badge
        for badge in badges_earned:
            UserNotification.objects.create(
                user=user,
                notification_type='badge',
                title=f'🎖️ Badge débloqué: {badge.name}',
                message=badge.description,
                icon=badge.icon,
                points_awarded=badge.points_reward
            )
        
        return badges_earned
    
    @staticmethod
    def check_and_award_achievements(user):
        """Vérifie et attribue les achievements"""
        achievements_earned = []
        profile = user.profile
        
        # Achievement "Débutant" - 100 points
        if profile.total_points >= 100:
            try:
                achievement = Achievement.objects.get(condition_type='beginner', condition_value=100)
                user_ach, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
                if created:
                    achievements_earned.append(achievement)
            except Achievement.DoesNotExist:
                pass
        
        # Achievement "Apprenti" - 500 points
        if profile.total_points >= 500:
            try:
                achievement = Achievement.objects.get(condition_type='learner', condition_value=500)
                user_ach, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
                if created:
                    achievements_earned.append(achievement)
            except Achievement.DoesNotExist:
                pass
        
        # Achievement "Expert" - 1000 points
        if profile.total_points >= 1000:
            try:
                achievement = Achievement.objects.get(condition_type='expert', condition_value=1000)
                user_ach, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
                if created:
                    achievements_earned.append(achievement)
            except Achievement.DoesNotExist:
                pass
        
        # Achievement "Maître" - 5000 points
        if profile.total_points >= 5000:
            try:
                achievement = Achievement.objects.get(condition_type='master', condition_value=5000)
                user_ach, created = UserAchievement.objects.get_or_create(user=user, achievement=achievement)
                if created:
                    achievements_earned.append(achievement)
            except Achievement.DoesNotExist:
                pass
        
        # Créer des notifications
        for achievement in achievements_earned:
            UserNotification.objects.create(
                user=user,
                notification_type='achievement',
                title=f'⭐ Succès débloqué: {achievement.name}',
                message=achievement.description,
                icon=achievement.icon,
                points_awarded=achievement.points_reward
            )
        
        return achievements_earned
    
    @staticmethod
    def get_user_notifications(user, limit=10, unread_only=False):
        """Récupère les notifications de l'utilisateur"""
        query = UserNotification.objects.filter(user=user)
        
        if unread_only:
            query = query.filter(is_read=False)
        
        return query[:limit]
    
    @staticmethod
    def mark_notification_as_read(notification):
        """Marque une notification comme lue"""
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return notification
    
    @staticmethod
    def get_leaderboard(period='all_time', limit=100):
        """Récupère le classement"""
        from lingx.models import Leaderboard
        
        leaderboards = Leaderboard.objects.filter(period=period).select_related('user').order_by('rank')[:limit]
        return leaderboards

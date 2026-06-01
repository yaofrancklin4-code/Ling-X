from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.db import IntegrityError


class CustomGoogleAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter pour Google OAuth qui auto-signup sans pages intermédiaires
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Appelé avant la connexion sociale
        """
        # Si l'utilisateur existe déjà par email, liez-le
        if sociallogin.is_existing:
            return
        
        try:
            # Cherchez un utilisateur avec cet email
            user = User.objects.get(email=sociallogin.account.extra_data.get('email'))
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Sauvegardez l'utilisateur - auto-créez s'il n'existe pas
        """
        user = super().save_user(request, sociallogin, form)
        
        # Auto-populate first and last name from Google
        extra_data = sociallogin.account.extra_data
        user.first_name = extra_data.get('given_name', '')
        user.last_name = extra_data.get('family_name', '')
        user.save()
        
        return user
    
    def populate_user(self, request, sociallogin, data):
        """
        Peuplez les données utilisateur depuis Google
        """
        user = super().populate_user(request, sociallogin, data)
        
        if 'given_name' in data:
            user.first_name = data.get('given_name')
        if 'family_name' in data:
            user.last_name = data.get('family_name')
        
        return user

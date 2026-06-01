from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import login

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(pre_social_login)
def link_to_local_user(sender, request, user, **kwargs):
    """
    Auto-connect user and skip confirmation pages
    """
    try:
        # Try to find existing user with same email
        existing_user = User.objects.get(email=user.email)
        # Connect the accounts
        sociallogin = kwargs.get('sociallogin')
        if sociallogin:
            sociallogin.connect(request, existing_user)
    except User.DoesNotExist:
        # New user will be auto-created by allauth with AUTO_SIGNUP
        pass


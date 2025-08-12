from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    avatar = models.ImageField(_('Avatar'), upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True)
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True)
    preferred_language = models.CharField(_('Preferred Language'), max_length=5, 
                                        choices=[('en', 'English'), ('az', 'Azerbaijani'), ('ru', 'Russian')], 
                                        default='en')
    receive_newsletter = models.BooleanField(_('Receive Newsletter'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_full_name(self):
        """Return user's full name or username if not available"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username

    def get_favorites_count(self):
        """Get count of user's favorite products"""
        return self.user.favorites.count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)

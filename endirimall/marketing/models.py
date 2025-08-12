from django.db import models
from django.utils.translation import gettext_lazy as _


class EmailSubscription(models.Model):
    """Model for email newsletter subscriptions"""
    email = models.EmailField(_('Email Address'), unique=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    subscribed_at = models.DateTimeField(_('Subscribed At'), auto_now_add=True)
    unsubscribed_at = models.DateTimeField(_('Unsubscribed At'), blank=True, null=True)

    class Meta:
        verbose_name = _('Email Subscription')
        verbose_name_plural = _('Email Subscriptions')
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

    def unsubscribe(self):
        """Mark subscription as inactive"""
        from django.utils import timezone
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()

    def resubscribe(self):
        """Mark subscription as active"""
        self.is_active = True
        self.unsubscribed_at = None
        self.save()

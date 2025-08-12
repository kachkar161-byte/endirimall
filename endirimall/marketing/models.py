"""
Marketing app models for email subscriptions and promotional content.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator


class EmailSubscription(models.Model):
    """
    Model for managing email newsletter subscriptions.
    """
    email = models.EmailField(
        _('Email'),
        max_length=254,
        unique=True,
        validators=[EmailValidator()]
    )
    is_active = models.BooleanField(_('Active'), default=True)
    subscribed_at = models.DateTimeField(_('Subscribed At'), auto_now_add=True)
    unsubscribed_at = models.DateTimeField(_('Unsubscribed At'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Email Subscription')
        verbose_name_plural = _('Email Subscriptions')
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
    
    def unsubscribe(self):
        """Mark subscription as inactive."""
        from django.utils import timezone
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()


class Newsletter(models.Model):
    """
    Model for creating and sending newsletters.
    """
    subject = models.CharField(_('Subject'), max_length=200)
    content = models.TextField(_('Content'))
    html_content = models.TextField(_('HTML Content'), blank=True)
    is_sent = models.BooleanField(_('Sent'), default=False)
    sent_at = models.DateTimeField(_('Sent At'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.subject


class PromotionalBanner(models.Model):
    """
    Model for promotional banners displayed on the site.
    """
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(_('Image'), upload_to='promotional_banners/')
    link = models.URLField(_('Link'), blank=True)
    button_text = models.CharField(_('Button Text'), max_length=50, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    start_date = models.DateTimeField(_('Start Date'), blank=True, null=True)
    end_date = models.DateTimeField(_('End Date'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Promotional Banner')
        verbose_name_plural = _('Promotional Banners')
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title
    
    def is_currently_active(self):
        """Check if banner is currently active based on dates."""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False
        
        if self.start_date and now < self.start_date:
            return False
        
        if self.end_date and now > self.end_date:
            return False
        
        return True
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
import csv
from .models import EmailSubscription


@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    """Admin configuration for EmailSubscription model"""
    list_display = ('email', 'is_active', 'subscribed_at', 'unsubscribed_at')
    list_filter = ('is_active', 'subscribed_at', 'unsubscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    list_editable = ('is_active',)
    date_hierarchy = 'subscribed_at'
    
    fieldsets = (
        (None, {
            'fields': ('email', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['export_as_csv', 'activate_subscriptions', 'deactivate_subscriptions']
    
    def export_as_csv(self, request, queryset):
        """Export selected subscriptions as CSV"""
        meta = self.model._meta
        field_names = ['email', 'is_active', 'subscribed_at', 'unsubscribed_at']
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}.csv'
        
        writer = csv.writer(response)
        writer.writerow(field_names)
        
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)
        
        return response
    export_as_csv.short_description = _('Export selected subscriptions as CSV')
    
    def activate_subscriptions(self, request, queryset):
        """Activate selected subscriptions"""
        updated = 0
        for subscription in queryset:
            if not subscription.is_active:
                subscription.resubscribe()
                updated += 1
        self.message_user(request, f'{updated} subscriptions activated.')
    activate_subscriptions.short_description = _('Activate selected subscriptions')
    
    def deactivate_subscriptions(self, request, queryset):
        """Deactivate selected subscriptions"""
        updated = 0
        for subscription in queryset:
            if subscription.is_active:
                subscription.unsubscribe()
                updated += 1
        self.message_user(request, f'{updated} subscriptions deactivated.')
    deactivate_subscriptions.short_description = _('Deactivate selected subscriptions')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-subscribed_at')
    
    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to changelist"""
        extra_context = extra_context or {}
        
        # Get statistics
        total_subscriptions = EmailSubscription.objects.count()
        active_subscriptions = EmailSubscription.objects.filter(is_active=True).count()
        inactive_subscriptions = total_subscriptions - active_subscriptions
        
        extra_context['total_subscriptions'] = total_subscriptions
        extra_context['active_subscriptions'] = active_subscriptions
        extra_context['inactive_subscriptions'] = inactive_subscriptions
        
        return super().changelist_view(request, extra_context=extra_context)

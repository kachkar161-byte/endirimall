from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Profile')
    fields = ('avatar', 'phone_number', 'date_of_birth', 'preferred_language', 'receive_newsletter')


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'favorites_count')
    list_filter = BaseUserAdmin.list_filter + ('profile__preferred_language', 'profile__receive_newsletter')
    
    def favorites_count(self, obj):
        """Display user's favorites count"""
        count = obj.favorites.count()
        return format_html('<strong>{}</strong>', count)
    favorites_count.short_description = _('Favorites')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('favorites', 'profile')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model"""
    list_display = ('user', 'preferred_language', 'receive_newsletter', 'favorites_count', 'created_at')
    list_filter = ('preferred_language', 'receive_newsletter', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'avatar_preview')
    
    fieldsets = (
        (_('User'), {
            'fields': ('user',)
        }),
        (_('Profile Information'), {
            'fields': ('avatar', 'avatar_preview', 'phone_number', 'date_of_birth')
        }),
        (_('Preferences'), {
            'fields': ('preferred_language', 'receive_newsletter')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def avatar_preview(self, obj):
        """Display avatar preview"""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px; border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url
            )
        return '-'
    avatar_preview.short_description = _('Avatar Preview')
    
    def favorites_count(self, obj):
        """Display user's favorites count"""
        count = obj.user.favorites.count()
        return format_html('<strong>{}</strong>', count)
    favorites_count.short_description = _('Favorites')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user').prefetch_related('user__favorites')


# Unregister the original User admin and register the extended one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

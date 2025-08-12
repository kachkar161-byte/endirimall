"""
Django admin configuration for endirimall project.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from deals.models import Product, Category, Store, Favorite, SliderImage, ProductView
from marketing.models import EmailSubscription, Newsletter, PromotionalBanner


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Admin configuration for Store model."""
    list_display = ['name', 'website', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'logo')
        }),
        (_('Contact Information'), {
            'fields': ('website', 'phone', 'address')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ['name', 'parent', 'is_active', 'order', 'products_count', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    def products_count(self, obj):
        """Display the count of products in this category."""
        return obj.get_products_count()
    products_count.short_description = _('Products Count')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'image', 'parent')
        }),
        (_('Status & Order'), {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    list_display = [
        'name', 'category', 'store', 'original_price', 'discounted_price', 
        'discount_percentage', 'is_active', 'is_featured', 'is_hot_deal', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_featured', 'is_hot_deal', 'category', 'store', 'created_at'
    ]
    search_fields = ['name', 'description', 'sku', 'brand', 'model']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    readonly_fields = ['discount_percentage']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'short_description')
        }),
        (_('Pricing'), {
            'fields': ('original_price', 'discounted_price', 'discount_percentage')
        }),
        (_('Images'), {
            'fields': ('main_image', 'additional_images')
        }),
        (_('Relationships'), {
            'fields': ('category', 'store')
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_featured', 'is_hot_deal')
        }),
        (_('Metadata'), {
            'fields': ('sku', 'brand', 'model')
        }),
        (_('Timing'), {
            'fields': ('expires_at',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('category', 'store')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin configuration for Favorite model."""
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user', 'product')


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    """Admin configuration for SliderImage model."""
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    ordering = ['order', 'created_at']
    
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'subtitle', 'image')
        }),
        (_('Link & Button'), {
            'fields': ('link', 'button_text')
        }),
        (_('Status & Order'), {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    """Admin configuration for ProductView model."""
    list_display = ['product', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['product__name', 'ip_address']
    ordering = ['-viewed_at']
    readonly_fields = ['viewed_at']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('product')


@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    """Admin configuration for EmailSubscription model."""
    list_display = ['email', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'subscribed_at', 'unsubscribed_at']
    search_fields = ['email']
    ordering = ['-subscribed_at']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        """Activate selected subscriptions."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} abunəlik aktivləşdirildi')
    activate_subscriptions.short_description = _('Seçilmiş abunəlikləri aktivləşdir')
    
    def deactivate_subscriptions(self, request, queryset):
        """Deactivate selected subscriptions."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} abunəlik deaktivləşdirildi')
    deactivate_subscriptions.short_description = _('Seçilmiş abunəlikləri deaktivləşdir')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin configuration for Newsletter model."""
    list_display = ['subject', 'is_sent', 'sent_at', 'created_at']
    list_filter = ['is_sent', 'created_at', 'sent_at']
    search_fields = ['subject', 'content']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'sent_at']
    
    fieldsets = (
        (_('Content'), {
            'fields': ('subject', 'content', 'html_content')
        }),
        (_('Status'), {
            'fields': ('is_sent', 'sent_at')
        }),
    )


@admin.register(PromotionalBanner)
class PromotionalBannerAdmin(admin.ModelAdmin):
    """Admin configuration for PromotionalBanner model."""
    list_display = ['title', 'order', 'is_active', 'start_date', 'end_date', 'created_at']
    list_filter = ['is_active', 'created_at', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    ordering = ['order', 'created_at']
    
    fieldsets = (
        (_('Content'), {
            'fields': ('title', 'description', 'image')
        }),
        (_('Link & Button'), {
            'fields': ('link', 'button_text')
        }),
        (_('Status & Order'), {
            'fields': ('is_active', 'order')
        }),
        (_('Timing'), {
            'fields': ('start_date', 'end_date')
        }),
    )


# Customize admin site
admin.site.site_header = _('Endirimall Admin')
admin.site.site_title = _('Endirimall Admin Portal')
admin.site.index_title = _('Endirimall İdarəetmə Paneli')
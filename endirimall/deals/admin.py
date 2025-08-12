from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Store, Category, Product, SliderImage, Favorite


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Admin configuration for Store model"""
    list_display = ('name', 'website_url', 'is_active', 'products_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'logo', 'website_url')
        }),
        (_('Content'), {
            'fields': ('description',)
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def products_count(self, obj):
        """Display number of products for this store"""
        count = obj.products.count()
        return format_html('<strong>{}</strong>', count)
    products_count.short_description = _('Products')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model"""
    list_display = ('name', 'icon_display', 'is_active', 'products_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'icon')
        }),
        (_('Content'), {
            'fields': ('description',)
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def icon_display(self, obj):
        """Display Bootstrap icon"""
        if obj.icon:
            return format_html('<i class="bi bi-{}"></i> {}', obj.icon, obj.icon)
        return '-'
    icon_display.short_description = _('Icon')
    
    def products_count(self, obj):
        """Display number of products in this category"""
        count = obj.products.count()
        return format_html('<strong>{}</strong>', count)
    products_count.short_description = _('Products')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model"""
    list_display = (
        'title', 'store', 'category', 'discounted_price', 'discount_percentage', 
        'is_featured', 'is_active', 'created_at'
    )
    list_filter = (
        'is_active', 'is_featured', 'store', 'category', 'created_at',
        ('valid_until', admin.DateFieldListFilter)
    )
    search_fields = ('title', 'description', 'store__name', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'discount_percentage', 'savings_display')
    list_editable = ('is_featured', 'is_active')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'store', 'category')
        }),
        (_('Content'), {
            'fields': ('description',)
        }),
        (_('Pricing'), {
            'fields': ('original_price', 'discounted_price', 'discount_percentage', 'savings_display'),
            'description': _('Discount percentage is calculated automatically.')
        }),
        (_('Deal Information'), {
            'fields': ('deal_url', 'valid_until')
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_featured')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def savings_display(self, obj):
        """Display savings amount"""
        savings = obj.get_savings()
        return format_html('<span style="color: green; font-weight: bold;">${}</span>', savings)
    savings_display.short_description = _('Savings')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('store', 'category')
    
    actions = ['make_featured', 'remove_featured', 'activate_products', 'deactivate_products']
    
    def make_featured(self, request, queryset):
        """Mark selected products as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products marked as featured.')
    make_featured.short_description = _('Mark selected products as featured')
    
    def remove_featured(self, request, queryset):
        """Remove featured status from selected products"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} products removed from featured.')
    remove_featured.short_description = _('Remove featured status')
    
    def activate_products(self, request, queryset):
        """Activate selected products"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products activated.')
    activate_products.short_description = _('Activate selected products')
    
    def deactivate_products(self, request, queryset):
        """Deactivate selected products"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products deactivated.')
    deactivate_products.short_description = _('Deactivate selected products')


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    """Admin configuration for SliderImage model"""
    list_display = ('title', 'image_preview', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'alt_text')
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'image_preview')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'image_preview', 'alt_text')
        }),
        (_('Settings'), {
            'fields': ('link_url', 'order', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        """Display image preview"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 100px; object-fit: cover;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = _('Preview')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin configuration for Favorite model"""
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at', 'product__category', 'product__store')
    search_fields = ('user__username', 'user__email', 'product__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'product', 'product__store', 'product__category')


# Customize admin site
admin.site.site_header = _('Endirimall Administration')
admin.site.site_title = _('Endirimall Admin')
admin.site.index_title = _('Welcome to Endirimall Administration')

# Add custom CSS for admin
class AdminMediaMixin:
    """Mixin to add custom CSS to admin"""
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Apply custom styling to all admin classes
for model_admin in [StoreAdmin, CategoryAdmin, ProductAdmin, SliderImageAdmin, FavoriteAdmin]:
    model_admin.__bases__ = (AdminMediaMixin,) + model_admin.__bases__
